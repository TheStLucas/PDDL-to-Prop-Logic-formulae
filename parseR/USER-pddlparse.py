#! /usr/bin/env python3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#
import logging
import sys
from tools import parse_pddl

if __name__ == '__main__':
    # Commandline parsing
    domain = sys.argv[1]
    problem = sys.argv[2]

    # logging tool provided
    # use any of the following levels to increase verbosity
    # possible log_levels = ['debug', 'info', 'warning', 'error']

    loglevel = 'info'
    logging.basicConfig(level=getattr(logging, loglevel.upper()),
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        stream=sys.stdout)


    task = parse_pddl(domain, problem)
    logging.info('Parsed planning problem: {0}'.format(task.name))
    print(task)

