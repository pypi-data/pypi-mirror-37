#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections


class Storage(object):
    """
    A Storage object wraps a dictionary.
    In addition to `obj['foo']`, `obj.foo` can also be used for accessing
    values.

    Wraps the dictionary instead of extending it so that the number of names
    that can conflict with keys in the dict is kept minimal.

        >>> o = Storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> 'a' in o
        True
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'

        Based on Storage in web.py (public domain)
    """
    __internal_vars = ('_dict', '_normalize', '_denormalize')

    def __init__(self, dict_=None, default_factory=None, normalize=None,
                 denormalize=None, case_insensitive=False, **kwargs):
        '''
        dict_: Dict to use as backend for Storage object, normalize will not
               be called for existing items.
        case_insensitive: All given keys will be converted to lower case before
                          trying to set/access the dict. If a populated dict_
                          is given it must already have all keys in lower case.
        default_factory: if dict_ is None and default_factory is set then a
                         defaultdict will be used with the specified
                         default_factory.
        normalize: function that normalizes keys, case_insensitive for example
                   is implemented as a normalizer that lower cases each key.
        denormalize: function that is called on each key before it is returned
                     to the caller(iteritems and __iter__).

        '''
        if dict_ is not None:
            self._dict = dict_
        elif default_factory:
            self._dict = collections.defaultdict(default_factory, **kwargs)
        else:
            self._dict = dict(**kwargs)
        if normalize and case_insensitive:
            self._normalize = lambda key: normalize(key.lower())
        elif case_insensitive:
            self._normalize = lambda key: key.lower()
        elif normalize:
            self._normalize = normalize
        else:
            self._normalize = lambda key: key  # Do nothing
        if denormalize:
            self._denormalize = denormalize
        else:
            self._denormalize = lambda key: key  # Do nothing
        for key, value in kwargs.items():
            self[key] = value

    def get_dict(self):
        ''' Get the contained dict.
            all keys will be in their normalized form.
        '''
        return self._dict

    def iteritems(self):
        ''' Iterate over all (key, value) pairs.
        All keys will be denormalized.
        '''
        for key, value in self._dict.items():
            yield self._denormalize(key), value

    def __getattr__(self, key):
        try:
            # prevent recursion (triggered by pickle.load()
            if key in Storage.__internal_vars:
                raise AttributeError('No such attribute: ' + repr(key))
            key = self._normalize(key)
            return self[key]
        except KeyError as err:
            raise AttributeError(err)

    def __setattr__(self, key, value):
        # prevent recursion (triggered by pickle.load()
        if key in Storage.__internal_vars:
            object.__setattr__(self, key, value)
        else:
            key = self._normalize(key)
            self[key] = value

    def __delattr__(self, key):
        try:
            key = self._normalize(key)
            del self[key]
        except KeyError as err:
            raise AttributeError(err)

    # For container methods pass-through to the underlying dict.
    def __getitem__(self, key):
        key = self._normalize(key)
        return self._dict[key]

    def __setitem__(self, key, value):
        key = self._normalize(key)
        self._dict[key] = value

    def __delitem__(self, key):
        key = self._normalize(key)
        del self._dict[key]

    def __contains__(self, key):
        key = self._normalize(key)
        return key in self._dict

    def __iter__(self):
        for key in self._dict:
            yield self._denormalize(key)

    def __len__(self):
        return self._dict.__len__()

    def __eq__(self, other):
        return isinstance(other, Storage) and self._dict == other._dict

    __hash__ = None

    def __repr__(self):
        items = []
        if isinstance(self._dict, collections.defaultdict):
            items.append('default_factory={0}'.format(
                self._dict.default_factory))
        items.extend('{0}={1}'.format(self._denormalize(i[0]), repr(i[1]))
                     for i in sorted(self._dict.items()))
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(items))
