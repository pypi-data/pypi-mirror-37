#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import
import argparse
import pkg_resources
import logging
import sys

import aadbook.config
from .contacts import Contacts

log = logging.getLogger(__name__)

CONFIG_FILE = '~/.aadbookrc'


def do_config_template(config, args):
    print(aadbook.config.TEMPLATE)


def do_authenticate(config, args):
    auth = config.auth

    auth.authenticate(ignore_refresh_token=True)
    print('Authentication succeeded')


def do_reload(config, args):
    contacts = Contacts(config)
    contacts.reload()


def do_query(config, args):
    contacts = Contacts(config)
    contacts.query(args.query)


def _build_parser():
    """
    Return a command-line arguments parser.
    """
    parser = argparse.ArgumentParser(description='Search you Azure AD contacts from mutt or the command-line.')
    parser.add_argument('-c', '--config', help='Specify alternative configuration file.', metavar="FILE")
    parser.add_argument('-v', '--verbose', dest="log_level", action='store_const',
                        const=logging.INFO, help='Be verbose about what is going on (stderr).')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%%(prog)s %s' % pkg_resources.get_distribution("aadbook").version,
                        help="Print version and exit")
    parser.add_argument('-d', '--debug', dest="log_level", action='store_const',
                        const=logging.DEBUG, help='Output debug info (stderr).')
    parser.set_defaults(config=CONFIG_FILE, log_level=logging.ERROR)

    subparsers = parser.add_subparsers()

    parser_config_template = subparsers.add_parser('config-template',
                                                   description='Prints a template for .aadbookrc to stdout')
    parser_config_template.set_defaults(func=do_config_template)

    parser_reload = subparsers.add_parser('authenticate',
                                          description='Azure AD authentication.')
    parser_reload.set_defaults(func=do_authenticate)

    parser_reload = subparsers.add_parser('reload',
                                          description='Force reload of the cache.')
    parser_reload.set_defaults(func=do_reload)

    parser_query = subparsers.add_parser('query',
                                         description='Search contacts using query (regex).')
    parser_query.add_argument('query', help='regex to search for.', metavar='QUERY')
    parser_query.set_defaults(func=do_query)

    return parser


def _main():
    parser = _build_parser()

    args = [arg.decode(aadbook.config.ENCODING) for arg in sys.argv[1:]]
    args = parser.parse_args(args)

    logging.basicConfig(level=args.log_level)

    try:
        if args.func == do_config_template:
            config = None
        else:
            config = aadbook.config.read_config(args.config)
        args.func(config, args)
    except aadbook.config.ConfigError as err:
        sys.exit(u'Configuration error: ' + unicode(err))


if __name__ == '__main__':
    _main()
