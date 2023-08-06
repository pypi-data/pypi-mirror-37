#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import logging
import os
import time
import pickle
import re
import sys


import requests
from collections import namedtuple

log = logging.getLogger(__name__)

Contact = namedtuple('Contact', 'name mail'.split())

CACHE_FORMAT_VERSION = '1.0'
MAX_USERS_PER_PAGE = 999


class Cache(object):
    def __init__(self, config):
        self._config = config
        self.contacts = self._load_contacts()

    def _load_contacts(self):
        cache = None

        # if cache newer than cache_expiry_hours
        if (os.path.exists(self._config.cache_filename) and
            ((time.time() - os.path.getmtime(self._config.cache_filename)) <
             (int(self._config.cache_expiry_hours) * 60 * 60))):
            try:
                log.debug('Loading cache: ' + self._config.cache_filename)
                cache = pickle.load(open(self._config.cache_filename, 'rb'))
                if cache.get('aadbook_cache') != CACHE_FORMAT_VERSION:
                    log.info('Detected old cache format')
                    cache = None  # Old cache format
            except StandardError, err:
                log.info('Failed to read the cache file: %s', err)
                raise
        if cache:
            return cache.get('contacts')

    def update(self, contacts):
        self.contacts = contacts
        self.save()

    def save(self):
        """Pickle the addressbook and a timestamp

        """
        if self.contacts:  # never write a empty addressbook
            cache = {'contacts': self.contacts,
                     'aadbook_cache': CACHE_FORMAT_VERSION}
            pickle.dump(cache, open(self._config.cache_filename, 'wb'))


class Contacts(object):
    def __init__(self, config):
        self._config = config
        self._auth = config.auth
        self.cache = Cache(config)

    def reload(self):
        all_users = []
        for users in self._fetch_users():
            sys.stdout.write('.')
            sys.stdout.flush()
            all_users.extend(users)

        self.cache.update(all_users)

    def _fetch_users(self):
        session = requests.Session()
        session.headers.update({
            'Authorization': "Bearer " + self._auth.creds['accessToken']
        })
        response = session.get(self._users_url).json()
        [users, next] = self._parse_users_response(response)
        yield users
        while next:
            response = session.get(next).json()
            [users, next] = self._parse_users_response(response)
            yield users

    @property
    def _users_url(self):
        return ('https://graph.microsoft.com/v1.0/users?$top=%s'
                % MAX_USERS_PER_PAGE)

    def _parse_users_response(self, response):
        def parse_contact(account):
            return Contact(account['displayName'], account['mail'])

        if 'value' not in response:
            raise ContactsParseError("Failed to parse contacts\n%s" % response)

        users = map(parse_contact, response['value'])
        next = (response['@odata.nextLink']
                if '@odata.nextLink' in response else None)
        return [users, next]

    def query(self, query):
        if not self.cache.contacts:
            self.reload()

        matching_contacts = sorted(self.__query_contacts(query),
                                   key=lambda c: c.name)
        # mutt's query_command expects the first line to be a message,
        # which it discards.
        print "\n",
        for contact in matching_contacts:
            name = contact.name
            mail = contact.mail
            print (u'\t'.join((mail, name))).encode(self._config.encoding,
                                                    errors='replace')

    def __query_contacts(self, query):
        match = re.compile(query.replace(' ', '.*'), re.I).search
        for contact in self.cache.contacts:
            if contact.mail:
                if any(itertools.imap(match,
                                      [contact.name, contact.mail])):
                    yield contact


class ContactsParseError(StandardError):
    pass
