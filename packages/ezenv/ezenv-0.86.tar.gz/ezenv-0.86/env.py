#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    env.py

    Simplified access to environment variables in Python.

    @copyright: 2018 by Mike Miller
    @license: LGPL

'''
import sys, os
try:
    from collections.abc import MutableMapping
except ImportError:
    from collections import MutableMapping  # Py2

__version__ = '0.86'

if os.name == 'nt':
    _sensitive_default = False
else:
    _sensitive_default = True


class Entry(str):
    ''' Represents an entry in the environment.

        Contains the functionality of strings plus a number of convenience
        properties for type conversion.
    '''
    def __new__(cls, name, value):
        return str.__new__(cls, value)  # Py2/3

    def __init__(self, name, value):
        self.name = name
        self.value = value

    @property
    def truthy(self):
        ''' Recognize a Boolean-like string value as a Boolean.
            Note: the rules are a bit different than string "truthiness."

            '0'             --> False
            '1'             --> True
            ('no', 'false') --> False  # case-insensitive
            ('yes', 'true') --> True   # case-insensitive
        '''
        lower = self.lower()
        if lower.isdigit():
            return bool(int(lower))
        elif lower in ('yes', 'true'):
            return True
        elif lower in ('no', 'false'):
            return False
        elif self == '':
            return False
        else:
            return None
    bool = truthy  # deprecated

    @property
    def float(self):
        ''' Return a float. '''
        return float(self)

    @property
    def int(self):
        ''' Return an intsky. '''
        return int(self)

    @property
    def list(self, sep=os.pathsep):
        ''' Split a path string (defaults to os.pathsep) and return list.

            Use str.split instead when a custom delimiter is needed.
        '''
        return self.split(sep)

    @property
    def path(self):
        ''' Return a path string as a Path object. '''
        from pathlib import Path
        return Path(self)

    @property
    def path_list(self, sep=os.pathsep):
        ''' Return list of Path objects. '''
        from pathlib import Path
        return [ Path(pathstr) for pathstr in self.split(sep) ]

    @property
    def from_json(self):
        ''' Parse a JSON string. '''
        from json import loads
        return loads(self)

    def __repr__(self):
        if self.value:
            return "Entry('%s', '%s')" % (self.name, self.value)
        else:
            return ''


class Environment(MutableMapping):
    ''' A mapping object that presents a simplified view of the OS Environment.

        blankify takes precedence over noneify.
    '''
    _Entry_class = Entry    # save for Python2 compatibility :-/

    def __init__(self, environ=os.environ,
                       sensitive=_sensitive_default,
                       blankify=False,
                       noneify=True,
                       writable=False,
                ):
        # setobj - prevents infinite recursion due to custom setattr
        # https://stackoverflow.com/a/16237698/450917
        setobj = object.__setattr__
        setobj(self, '_blankify', blankify)
        setobj(self, '_noneify', noneify),
        setobj(self, '_original_env', environ),
        setobj(self, '_sensitive', sensitive),
        setobj(self, '_writable', writable),

        if sensitive:
            setobj(self, '_envars', environ)
        else:
            # TODO: cache these instead, will affect .prefix
            setobj(self, '_envars', { name.lower(): value
                                      for name, value in environ.items() })

    def __contains__(self, name):
        return name in self._envars

    def __getattr__(self, name):
        ''' Customize attribute access, allow direct access to variables. '''

        # need an loophole for configuring a new instance
        if name == 'Environment':
            return Environment
        elif name == 'Entry':
            return Entry or self._Entry_class  # Py2

        if not self._sensitive:
            name = name.lower()

        try:
            #~ return Entry(name, self._envars[name])
            return self._Entry_class(name, self._envars[name])  # Py2 compat
        except KeyError as err:
            if self._blankify:
                return self._envars.setdefault(name, Entry('', ''))
            elif self._noneify:
                return None
            else:
                raise AttributeError(name)

    def __setattr__(self, name, value):
        if self._writable:
            self._envars[name] = value

            if self._original_env is os.environ:  # push to environment
                os.environ[name] = value
        else:
            raise AttributeError('Environment is read-only.')

    def __delattr__(self, name):
        del self._envars[name]

    # MutableMapping needs these implemented, defers to internal dict
    def __len__(self):                  return len(self._envars)
    def __delitem__(self, key):         del self._envars[key]
    def __getitem__(self, key):         return self._envars[key]
    def __setitem__(self, key, item):   self.data[key] = item
    def __iter__(self):                 return iter(self._envars)

    def __repr__(self):
        entry_list = ', '.join([ ('%s=%r' % (k, v)) for k, v in self.items() ])
        return '%s(%s)' % (self.__class__.__name__, entry_list)

    def prefix(self, prefix, lowercase=True):
        ''' Returns a dictionary of keys with the same prefix.
            Compat with kr/env, lowercased.

            > xdg = env.prefix('XDG_')

            > for key, value in xdg.items():
                 print('%-20s' % key, value[:6], '…')
            config_dirs      /etc/x…
            current_desktop  MATE
            data_dirs        /usr/s…
            …
        '''
        env_subset = {}
        for key in self._envars.keys():
            if key.startswith(prefix):
                new_key = key[len(prefix):]  # cut front
                new_key = new_key.lower() if lowercase else new_key
                env_subset[new_key] = str(self._envars[key]) # str strips Entry

        return Environment(environ=env_subset,
                           sensitive=self._sensitive,
                           blankify=self._blankify,
                           noneify=self._noneify,
                           writable=self._writable,
                          )

    def map(self, **kwargs):
        ''' Change a name on the fly.  Compat with kr/env. '''
        return { key: str(self._envars[kwargs[key]])  # str strips Entry
                 for key in kwargs }


if __name__ == '__main__':

    __doc__ += '''  # keep tests close

        Default::

            >>> env = Environment(testenv, writable=True)

            >>> env.USER                                # repr
            Entry('USER', 'fred')

            >>> env.USER.title()                        # str ops available
            'Fred'

            >>> env.user                                # missing --> None

            >>> print(f'term: {env.TERM}')              # interpolation
            term: xterm-256color

            >>> 'NOPE' in env                           # check existence
            False

            >>> 'EMPTY' in env                          # check existence
            True

            >>> bool(env.EMPTY)                         # check if empty: False
            False

            >>> env['PI']                               # getitem syntax
            '3.14'

            >>> env.PI.float                            # type conversion
            3.14

            >>> env.STATUS.int
            5150

            >>> env.QT_ACCESSIBILITY.truthy             # 0/1/yes/no/true/false
            True

            >>> sorted(env.JSON_DATA.from_json.keys())  # compat < 3.6
            ['one', 'three', 'two']

            >>> env.XDG_DATA_DIRS.list
            ['/usr/local/share', '/usr/share']

            # using isinstance to avoid Platform errs:
            >>> from pathlib import Path
            >>> isinstance(env.SSH_AUTH_SOCK.path, Path)
            True

            >>> all(map(lambda p: isinstance(p, Path), env.XDG_DATA_DIRS.path_list))
            True

        KR/env compatibility::

            >>> sorted(env.prefix('XDG_', False).keys())
            ['DATA_DIRS', 'SESSION_ID', 'SESSION_TYPE']

            >>> env.map(username='USER')
            {'username': 'fred'}

        Writing possible when writable is set to True (see above),
        though not typically useful::

            >>> env.READY
            Entry('READY', 'no')

            >>> env.READY = 'yes'

            >>> env.READY
            Entry('READY', 'yes')

        Unicode::

            >>> env.MÖTLEY = 'Crüe'
            >>> env.MÖTLEY
            Entry('MÖTLEY', 'Crüe')

        Noneify False::

            >>> env = Environment(testenv, noneify=False)
            >>> env.USERZ                               # missing, kaboom!
            Traceback (most recent call last):
            AttributeError: USERZ

        Blankify True::

            >>> env = Environment(testenv, blankify=True)
            >>> env.USERZ                               # missing --> blank
            <BLANKLINE>

        Sensitive False::

            >>> env = Environment(testenv, sensitive=False)
            >>> str(env.USER)                           # interactive repr
            'fred'
            >>> str(env.user)                           # interactive repr
            'fred'

        Errors::

            >>> env.XDG_DATA_DIRZ.list               # TODO: figure out
            Traceback (most recent call last):
            AttributeError: 'NoneType' object has no attribute 'list'

    '''
    import doctest

    testenv = dict(
        EMPTY='',
        JSON_DATA='{"one":1, "two":2, "three":3}',
        PI='3.14',
        READY='no',
        STATUS='5150',
        QT_ACCESSIBILITY='1',
        SSH_AUTH_SOCK='/run/user/1000/keyring/ssh',
        TERM='xterm-256color',
        USER='fred',
        XDG_DATA_DIRS='/usr/local/share:/usr/share',
        XDG_SESSION_ID='c1',
        XDG_SESSION_TYPE='x11',
    )

    # testmod returns (failure_count, test_count):
    sys.exit(
        doctest.testmod(verbose=(True if '-v' in sys.argv else False))[0]
    )

else:
    # save original module for later, just in case it's needed.
    Environment._module = sys.modules[__name__]

    # Wrap module with instance for direct access
    sys.modules[__name__] = Environment()
