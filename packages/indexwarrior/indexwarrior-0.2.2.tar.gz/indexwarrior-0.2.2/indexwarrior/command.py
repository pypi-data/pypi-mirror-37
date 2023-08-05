#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#     David Pose Fernández <dpose@bitergia.com>
#

import argparse

from indexwarrior.errors import ParserException

DESC_MSG = """"Life among ES indexes is tough so am I"""
DEFAULT_ES_TIMEOUT = 30


class IndexWarriorParser:

    @staticmethod
    def parse(*args):
        """Parse arguments from the command line."""

        parser = argparse.ArgumentParser(description=DESC_MSG)

        parser.add_argument('--es_timeout', type=int, dest='es_timeout', default=DEFAULT_ES_TIMEOUT,
                            help='ES timeout. Set a custom timeout if needed. By default this value is set to 30 sec')

        parser.add_argument(dest='es_host',
                            help='ES host. When it does not start by http(s):// the tool understands you are using a shorcut stored at ~/.indexwarrior')

        subparsers = parser.add_subparsers(dest='subparser_name')

        ## index subcommands start here
        parser_index = subparsers.add_parser('index', help='index operations')
        index_subparser = parser_index.add_subparsers(dest='command')

        parser_show = index_subparser.add_parser('show', help='show indexes')
        parser_show.add_argument('--less', dest='less', action='store_true',
                                 help='displays less information, useful for slow ES instances')

        parser_compare = index_subparser.add_parser('compare', help='compare two indexes')
        parser_compare.add_argument(dest='index_a', help='first index to be compared')
        parser_compare.add_argument(dest='index_b', help='index to be compared with')
        parser_compare.add_argument('--buckets', required=False, default='10',
                                    help='buckets (origins) to be returned')

        parser_drop = index_subparser.add_parser('drop',
                                                 help='remove all indexes older than an expiration date (date field for expiration date = metadata__timestamp)')
        parser_drop.add_argument(dest='date', help='expiration date in format 2017-04-05T07:41:44.993Z')
        parser_drop.add_argument('--term', dest='term', required=False,
                                 help='match term with index name')

        parser_delete = index_subparser.add_parser('delete', help='delete index (or items from a particular index)')
        parser_delete.add_argument(dest='index', help='index name')
        parser_delete.add_argument('--origin', help='origin of the docs to be removed')
        parser_delete.add_argument('--older_than', help='data older than this date will be removed')
        parser_delete.add_argument('--date_field', default='grimoire_creation_date',
                                   help='date field used to filter data (by default grimoire_creation_date)')

        # alias subcommands start here
        parser_alias = subparsers.add_parser('alias', help='aliases operations')
        alias_subparser = parser_alias.add_subparsers(dest='command')

        parser_add = alias_subparser.add_parser('add', help='add alias')
        parser_add.add_argument(dest='alias_name', help='name of the alias')
        parser_add.add_argument(dest='index_names', nargs='+', help='list of index names (e.g. index_a index_b)')

        parser_add = alias_subparser.add_parser('delete', help='delete alias')
        parser_add.add_argument(dest='alias_name', help='name of the alias')
        parser_add.add_argument(dest='index_names', nargs='+', help='list of index names (e.g. index_a index_b)')

        parser_show = alias_subparser.add_parser('show', help='show aliases')
        parser_show.add_argument('--filters', dest='show_filters', action='store_true',
                                 help='show aliases and their filters')

        parser_switch = alias_subparser.add_parser('switch', help='move aliases from one index to another')
        parser_switch.add_argument('-o', '--old-index', dest='old_index', required=True,
                                   help='index to be switched')
        parser_switch.add_argument('-n', '--new-index', dest='new_index', required=True,
                                   help='new index to be linked')

        parser_autoupdate = alias_subparser.add_parser('autoupdate',
                                                       help='update alias automaticaly if fresher & bigger index is found')
        parser_autoupdate.add_argument(dest='alias_names', nargs='+', help='list of alias names to be updated')

        try:
            return parser.parse_args(args)
        except SystemExit:
            raise ParserException