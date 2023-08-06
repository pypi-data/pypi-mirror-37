# -*- coding: utf-8 -*-
########################################################################################################################
#    File: cache.py
#  Author: Dan Huckson, https://github.com/unodan
#    Date: 2018-10-29
########################################################################################################################
from os import path
from json import dump, load
from logging import info, error


class URICache:
    def __init__(self, data=None, **kwargs):
        if isinstance(data, dict):
            self.data = data
        elif isinstance(data, str) and path.isfile(data):
            self.data = self.load(data)
        else:
            self.data = kwargs.get('data', {})

    @staticmethod
    def sanitize(uri=''):
        """
        Sanitize the uri.

        The sanitize method returns a sanitized version of the string passed to it.

        Parameters
        ----------
        uri: str
            The uri location string.

        Returns
        -------
        str
            Returns a sanitized uri string.
        """
        if uri:
            uri = uri.replace('\\', '/')

        return uri

    def set(self, data=None, uri=None):
        """
        Set cache member.

        The set method sets a cache member specified by the uri parameter with the data from the data parameter.

        Parameters
        ----------
        data : scalar variable
            The data to store.
        uri: str
            The cache location (target) where the data is to be stored.

        Returns
        -------
        Nothing
        """

        def deep_iterate(value, _uri):
            _uri = self.sanitize(_uri)

            def parse(segment, location):
                parts = location.split('/', 1)
                target = parts[0]

                if len(parts) > 1:
                    if target not in segment:
                        segment[target] = {}

                    parse(segment[target], parts[1])
                else:
                    segment[target] = value

            if _uri and '/' in _uri:
                parse(self.data, _uri)
            elif _uri is None or _uri == '.':
                self.data = value
            else:
                self.data = {**self.data, **{_uri: value}}

        if isinstance(data, dict):
            def iterate(member, location=None):
                for key, item in member.items():
                    if isinstance(item, dict):
                        iterate(item, key)
                    else:
                        deep_iterate(item, location + '/' + key)
            iterate(data, uri)
        else:
            deep_iterate(data, uri)

    def get(self, uri=None, default=None):
        """
        Get cache member.

        The get method gets the data located at the specified uri if it exists.
        If the uri (target) is not in the cache and the default parameter is set,
        then the default value will be returned.

        Parameters
        ----------
        uri: str
            The cache location (target) where the data is to be stored.
        default :
            The default value to return if the target can't be found.

        Returns
        -------
            Returns the data if found in the cache, if target is not in the cache and default parameter is set
            then the default is returned else None is returned.
        """

        uri = self.sanitize(uri)

        def parse(segment, location):
            parts = location.split('/', 1)
            target = parts[0]

            if len(parts) > 1:
                if target not in segment:
                    return default
                else:
                    return parse(segment[target], parts[1])

            elif target in segment:
                return segment[target]

            return default

        if uri and '/' in uri:
            return parse(self.data, uri)
        elif uri == '.' or uri is None:
            return self.data
        else:
            data = None
            if self.data:
                data = self.data.get(uri, default)

            if not data:
                data = default

            return data

    def load(self, file):
        """
        Load data from disk.

        The load method initializes the cache data from the given file path if the file exists.

        Parameters
        ----------
        file : str
            Path to the data file on disk.

        Returns
        -------
        dict
            If the file exists return the data in the file else return False.
        """
        try:
            with open(file, 'r') as f:
                self.data = load(f)
                info('json_read:Filename="' + file + '":Success')
                return self.data

        except OSError as e:
            error('json_read:Filename="' + file + '":' + e.strerror + ":Failed")
            return False

    def save(self, file):
        """
        Save data to disk.

        The save method saves the cache data to the given file path,
        previous contents of the file are over writen.


        Parameters
        ----------
        file : str
            File path were to write the file to disk.

        Returns
        -------
        bool
            If an error occurred return True else False.
        """

        try:
            with open(file, 'w') as f:
                dump(self.data, f, indent=4)

                info('json_write:Filename="' + file + '":Success')
                return False

        except OSError as e:
            error('json_write:Filename="' + file + '"' + e.strerror)
            return True

    def remove(self, uri):
        """
        Remove cache member.

        The remove method removes a cache member specified by the uri parameter from the cache.

        Parameters
        ----------
        uri: str
            The cache location (target) that is to be removed.

        Returns
        -------
        Nothing
        """

        uri = self.sanitize(uri)

        def parse(segment, location):
            parts = location.split('/', 1)
            target = parts[0]

            if len(parts) > 1:
                return parse(segment[target], parts[1])
            elif target in segment:
                del segment[target]

        if uri and '/' in uri:
            return parse(self.data, uri)

    def update(self, update_data, target=''):
        """
        Update cache member.

        The Update method updates the cache location specified by the uri parameter,
        with the data in update_data parameter.

        Parameters
        ----------
        target: str
            The cache location (uri) that is to be updated.
        update_data:
            The data to update the cache with.

        Returns
        -------
        Nothing
        """
        def updater(data, uri):
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        updater(value, uri + '/' + key)
                    else:
                        self.set(value, uri + '/' + key)
            else:
                self.set(data, uri)

        if not isinstance(self.get(target, True), dict):
            self.remove(target)
            parts = target.rsplit('/', 1)
            updater({parts[1]: update_data}, parts[0])
        else:
            updater(update_data, target)
