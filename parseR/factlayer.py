"""Representation of a fact layer
"""

class FactLayer(object):
  """A class for a fact layer in a level of the planning graph. It
  contains not only a list of facts, but also the mutexes among them.

  Attributes:
      actions (:obj:`set`): The facts in this layer as a list of :obj:`string` 
      mutex_actions (:obj:`set`): The mutex between the facts, represented as a set of tuples (:obj:`string`, :obj:`string`) 


  """


  def __init__(self, facts = set()):
    """
    Constructor
    """
    self.facts = facts.copy() 	      # list of all the facts in the layer
    self.mutex_facts = set()   # set of pairs of facts that are mutex in the layer

  def addFact(self, fact):
    """Add a fact to the layer 

    Args: 
        act (:obj:`string`): The fact to add 
    """

    self.facts.add(fact)
    
  def removeFact(self, fact):
    """Remove a fact from the layer 
 
    Args: 
        act (:class:`task.Operator`): The fact to remove
    """

    self.facts.remove(fact)
    
  def getFacts(self):
    """Get the facts in this layer

    
    Returns:
        A set of :class:`task.Operator`
    """

    return self.facts    
  
  def addMutexProp(self, fact1, fact2):
    """ Add a mutex between fact1 and fact2

    Args:
        fact1 (:class:`task.Operator`)
        fact2 (:class:`task.Operator`)
    """

    
    self.mutex_facts.add((fact1,fact2))
    self.mutex_facts.add((fact2,fact1))
  
  def isMutex(self, fact1, fact2):
    """
    Args:
        fact1 (:class:`task.Operator`)
        fact2 (:class:`task.Operator`)
    
    Returns: 
        bool: True if the facts fact1 and fact2 are mutex in this fact layer, False otherwise
     """

    return (fact1,fact2) in self.mutex_facts  
  
  def getMutexFacts(self):
    """Get the set of mutexes 

    Returns:
        The mutexes as a set of pairs (:class:`task.Operator`, :class:`task.Operator`)
    """
    return self.mutex_facts  
  
  def applicable(self, op):
    """Check if a given action can be applied from this layer, i.e., if
    all facts that are preconditions of the action exist in this layer
  
    Args:
        op (:class:`task.Operator`): The action to check
    
    Returns:
        bool: True if all facts that are preconditions of the action exist in this layer (i.e. the action can be applied)

    """
    for f in op.preconditions:
      if f not in self.facts:
        return False
    return True
    #return set(op.preconditions) <= self.facts

  def __eq__(self, other):
    return (isinstance(other, self.__class__)
      and self.__dict__ == other.__dict__)

  def __ne__(self, other):
    return not self.__eq__(other)
  def __str__(self):
    str = "\t\tfacts < "+ " ".join(self.facts)+">\n"\
          "\t\tmutex < "+ " ".join([a.__repr__()+"-"+b.__repr__() for (a,b) in self.mutex_facts])+">"
    return str
      
