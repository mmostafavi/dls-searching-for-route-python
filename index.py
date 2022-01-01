import enum

state_names = ["left_side", "boat", "right_side"]

class State:
  def __init__(self) -> None:
    self.left_side = ["P", "T", "F", "M", "B", "B", "G", "G"]
    self.boat = []
    self.right_side = []
  
  def __getitem__(self, key):
    return getattr(self, key)

  
  def copy(self):
    copiedState = State()
    copiedState.left_side = self.left_side.copy()
    copiedState.right_side = self.right_side.copy()
    copiedState.boat = self.boat.copy()
    return copiedState

class Directions(enum.Enum):
  LeftToRight = 1
  RightToLeft = 2

class Move:
  moveDirection = None
  passengers = []

  def __init__():
    pass

  def setPassengers(self, passengers):
    self.passengers = passengers
  
  def setDirection(self, direction):
    self.direction = direction

class Node:
  parentNode = None
  children = []
  stateId = None
  state = None
  move = None
  

  def __init__(self):
    self.state = State()

  def childOf(self, node):
    self.parentNode = node
  
  def createChild(self):
    newNode = Node()
    newNode.childOf(self)
    return newNode

  def setMove(self, move):
    self.move = move

  def setState(self, state):
    self.state = state
    self.stateId = calculateStateId(state)

  def getParentNode(self):
    return self.parentNode
  



state_names = ["left_side", "boat", "right_side"]

state = State()

def isGoal(state):
  if state.left_side == [] and state.boat == []: return True
  return False


def isValid(state):
  # check if number of people on boat is less that 3
  if len(state.boat) > 2 : return False

  # check if the P is with T if T is not alone
  for name in state_names :
    if "T" in state[name] and "P" not in state[name]: 
      if len(state[name]) > 1:
        return False

  # check if M or P or F is in boat if it's moving
  if len(state.boat) > 0:
    if "P" not in state.boat and "M" not in state.boat and "F" not in state.boat: return False

  for name in state_names:
    # check if boys are with mother in absence of father
    if "B" in state[name] and "M" in state[name] and "F" not in state[name]: return False

    #check if girls are with father in absence of mother
    if "G" in state[name] and "F" in state[name] and "M" not in state[name]: return False

  return True


# calculate a state ID for each State to prevent infinite loop
# during calculations
def calculateStateId(state):
  weights = {
    "G": 1,
    "B": 10,
    "P": 100,
    "M": 1000,
    "F": 10000,
    "T": 100000,
  }

  result = 0

  for name in state_names:
    for member in state[name]:
      # perform the calculation just for cases where all members
      # are in left or right side of river
      if name == "boat" and state[name] > 1: raise Exception("Invalid State")

      if name == "left_side":
        result += weights[member]
      else:
        result -= weights[member]
  
  return result

if __name__ == "__main__":
  pass  
