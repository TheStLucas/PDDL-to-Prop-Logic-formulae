# -*- coding: utf-8 -*-
# This file is part of pyperplan.
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

"""Classes that are used to represent a planning problem. 

A planning problem is basically an instance of the Task class.

Note: 
    A task object can be created from a PDDL file using the parser.

Example::

    from tools import parse_pddl
    task = parse_pddl('testbed/domain-blocks.pddl', 'testbed/blocks.pddl')
    print("Planning problem parsed ")
    print(task)

"""


class Operator:
    """This class represents an operator (action). 

    Attributes:

        preconditions (:obj:`frozenset`): Represent the facts that have to be true before the operator can be applied.
        add_effects (:obj:`frozenset`): The facts that the operator makes true.  
        delete_effects (:obj:`frozenset`): The facts that the operator makes false.

    """
    def __init__(self, name, preconditions, add_effects, del_effects):
        self.name = name
        self.preconditions = set(preconditions)
        self.add_effects = set(add_effects)
        self.del_effects = set(del_effects)

    def set_precondition(self, precond=set()):
        """Set the preconditions        
        """
        
        self.preconditions.update(precond)
    def set_add_effects(self, add_facts=set()):
        """Set the add effects    

        Set the facts that are added by this operator
        """
        self.add_effects.update(add_facts)
        
    def set_del_effects(self, del_facts=set()):
        """Set the delete effects

        Set the facts that are removed by this operator
        """
        self.del_effects.update(del_facts)

    def clear_precondition(self, precond=set()):
        """Clear the preconditions        
        """
        
        self.preconditions = frozenset(precond)
    def clear_add_effects(self, add_facts=set()):
        """Clear the add effects    

        Clear the facts that are added by this operator
        """
        self.add_effects = frozenset(add_facts)
        
    def clear_del_effects(self, del_facts=set()):
        """Clear the delete effects

        Clear the facts that are removed by this operator
        """
        self.del_effects = frozenset(del_facts)

    def applicable(self, state: set) -> bool:
        """Check if the operator can be applied to a given state
        
        Operators are applicable when their set of preconditions is a subset
        of the facts that are true in "state".
        
        Args:
            state: The state from which to check if the operator is applicable

        Returns: 
            True if the operator's preconditions is a subset of the state, False otherwise
        """
        return self.preconditions <= state

    def apply(self, state: set ) -> set:
        """Apply operator to a given state
        
        Applying an operator implies removing the facts that are made
        false the operator from the set of true facts in state and
        adding the facts made true.

        Note that therefore it is possible to have operands that make a
        fact both false and true. This results in the fact being true
        at the end.

        Args: 
            state (set) : The state from which the operator should be applied to

        Returns:
            A new state (set of facts) after the application ofthe operator

        """
        assert self.applicable(state)
        assert type(state) in (frozenset, set)
        return (state - self.del_effects) | self.add_effects

    def __str__(self):
        s = '%s\n' % self.name
        for group, facts in [('PRE', self.preconditions),
                             ('ADD', self.add_effects),
                             ('DEL', self.del_effects)]:
            for fact in facts:
                s += '  %s: %s\n' % (group, fact)
        return s

    def __repr__(self):
        return '<Op %s>' % self.name


class Task:
    """
    A planning task

    Atrributes:
        name (:obj:`string`): The task's name
        facts (:obj:`set`): A set of all the fact names that are valid in the domain
        initial_state (:obj:`set`): A set of fact names that are true at the beginning
        goals (:obj:`set`): A set of fact names that must be true to solve the problem
        operators(:obj:`set`): A set of :class:`task.Operator` representing the valid actions in the problem

    """
    def __init__(self, name, facts, initial_state, goals, operators):
        """Constructor
        Args:
        """
        self.name = name
        self.facts = facts
        self.initial_state = initial_state
        self.goals = goals
        self.operators = operators

    def goal_reached(self, state: set) -> bool:
        """Check if the goal has been reached at a given state

        The goal has been reached if all facts that are true in "goals"
        are true in "state".

        Args:
            state: The state that is being checked

        Returns:
            True if all the goals are reached, False otherwise
        """
        return self.goals <= state

    def get_successor_states(self, state: set) -> list:
        """Get the successor states from a given state

        The successor states result from the application of all the
        applicable operators to a given state

        Args: 
            state: The state from which to generate the successors


        Returns: 
            A list with (op, new_state) pairs where "op" is the applicable operator (instance of task.Operator) and "new_state" the state that results when "op" is applied in state "state".

        """
        return [(op, op.apply(state)) for op in self.operators
                if op.applicable(state)]

    def copy(self):
        """Get a deep copy of the task 
        
        Returns:
            A copy of this task object
        """
        import copy
        return copy.deepcopy(self)

    
    def __str__(self):
        s = 'Task {0}\n  Vars:  {1}\n  Init:  {2}\n  Goals: {3}\n  Ops:   {4}'
        return s.format(self.name, ', '.join(self.facts),
                             self.initial_state, self.goals,
                             '\n'.join(map(repr, self.operators)))

    def __repr__(self):
        string = '<Task {0}, vars: {1}, operators: {2}>'
        return string.format(self.name, len(self.facts), len(self.operators))
