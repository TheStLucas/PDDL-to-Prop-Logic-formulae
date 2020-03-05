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
from __future__ import print_function

import sys
import os
import re
import logging
import time
import grounding
import tools
from a_star import  astar_search 
from heuristic_blind import BlindHeuristic
from tools  import parse_pddl


if __name__ == '__main__':
    # Commandline parsing
    domain = sys.argv[1]
    problem = sys.argv[2]

    loglevel = 'info'
    logging.basicConfig(level=getattr(logging, loglevel.upper()),
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    stream=sys.stdout)
    search_start_time = time.clock()
    solution = None
    task = parse_pddl(domain, problem)
    heuristic = BlindHeuristic(task)
    solution = astar_search(task, heuristic)


    logging.info('Search end: {0}'.format(task.name))


    
    logging.info('Wall-clock search time: {0:.2}'.format(time.clock() -
                                                         search_start_time))
    

    if solution is None:
        logging.warning('No solution could be found')
    else:
        logging.info('Solution found: Plan length=%s' % len(solution))
        for op in solution:
            print(op.name)
