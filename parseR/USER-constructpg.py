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

import sys
import os
import logging
import time
from planning_graph import PlanningGraph
from tools  import parse_pddl
        
def construct_planning_graph(task):
    pg = PlanningGraph(task)
    # your code here
    # you should generate all the necessary levels

    return pg
        
if __name__ == '__main__':
    # Commandline parsing
    domain = sys.argv[1]
    problem = sys.argv[2]

    log_levels = ['debug', 'info', 'warning', 'error']

    loglevel = 'info'
    logging.basicConfig(level=getattr(logging, loglevel.upper()),
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    stream=sys.stdout)

    task = parse_pddl(domain, problem)
    logging.info('Constructing planning graph: {0}'.format(task.name))
    pg = construct_planning_graph(task)
    
    logging.info("Finished planning graph construction with %d levels"% len(pg.levels))
