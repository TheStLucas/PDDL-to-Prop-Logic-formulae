"""Representation of an action layer
"""

class ActionLayer(object):
  """A class for an action layer in a level of the planning graph.  It contains not only a list of actions, but also the mutexes among them.

  Attributes:
      actions (:obj:`set`): The actions in this layer as a set of :class:`task.Operator` 
      mutex_actions (:obj:`set`): The mutex actions, represented as a set of tuples (:class:`task.Operator`, :class:`task.Operator`) 
      actions_for_prop (:obj:`dict`): A map between facts and the set of :class:`task.Operator` s that have them in the add_effects

  """


  def __init__(self):
    """
    Constructor
    """
    self.actions = set()       # list of all the actions in the layer
    self.mutex_actions = set() # list of pairs of action that are mutex in the layer
    self.actions_for_prop = dict()

  def _update_actions_for_prop(self):
    self.actions_for_prop = dict()
    for act in self.actions:
      for p in act.add_effects:
        if p not in self.actions_for_prop:
          self.actions_for_prop[p] = list()
          self.actions_for_prop[p].add(act)

  def addAction(self, act):
    """Add an action to the layer 

    Args: 
        act (:class:`task.Operator`): The action to add 
    """
    self.actions.add(act)
    for p in act.add_effects:
        if p not in self.actions_for_prop:
          self.actions_for_prop[p] = set()
          self.actions_for_prop[p].add(act)

    
    
  def removeActions(self, act):
    """Remove an action from the layer 
 
    Args: 
        act (:class:`task.Operator`): The action to remove
    """

    self.actions.erase(act)
    self._update_actions_for_prop()
    
  def getActions(self):
    """Get the actions in this layer

    
    Returns:
        A set of :class:`task.Operator`
    """
    return self.actions
  
  def getMutexActions(self):
    """Get the set of mutexes 

    Returns:
        The mutexes as a set of pairs (:class:`task.Operator`, :class:`task.Operator`)
    """
    return self.mutex_actions
    
  def addMutexActions(self, action1, action2):
    """ Add a mutex between action1 and action2

    Args:
        action1 (:class:`task.Operator`)
        action2 (:class:`task.Operator`)
    """
    self.mutex_actions.add((action1,action2))
    self.mutex_actions.add((action2,action1))
  
  
  def isMutex(self, action1, action2):
    """
    Args:
        action1 (:class:`task.Operator`)
        action2 (:class:`task.Operator`)
    
    Returns: 
        bool: True if the actions action1 action2 are mutex in this action layer, False otherwise
     """
    return (action1,action2) in self.mutex_actions
  
  def effectExists(self, fact):
    """Check if there is an action in this layer that adds a given fact
    
    Args:
        fact: The fact to check inside the add_effects of the actions in this layer
    
    Returns:
        bool: True if at least one of the actions in this layer has the fact/proposition `fact` in its add list
    """
    for act in self.actions:
      if fact in act.add_effects:
        return True
    return False
  
  def getActionsForCondition(self, fact):
    """ Get all the actions in this layer that have the fact in its add list
    
    Args:
        fact: The fact to check
    
    Returns:
        set: A set of :class:`task.Operator` that have fact in their :attr:`task.Operator.add_effects`
    """
    if fact not in self.actions_for_prop:
      return set()
    else:
      return self.actions_for_prop[fact]

    
  def __str__(self):
    str = "\t\tactions < "+" ".join([act.__repr__() for act in self.actions])+ ">\n"\
          "\t\tmutex < "+ "  ".join([a.__repr__()+"-"+b.__repr__() for (a,b) in self.mutex_actions])+ ">"
    return str

  def __eq__(self, other): return (isinstance(other, self.__class__)
    and self.__dict__ == other.__dict__)

  def __ne__(self, other): return not self.__eq__(other)
