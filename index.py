import enum
import time

state_names = ["left_side", "boat", "right_side"]

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

# check if the passed state is the final Goal
def isGoal(state):
  if state.left_side == [] and state.boat == []: return True
  return False

# checks if the passed state is a valid State
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

class State:
  left_side = None
  boat = None
  right_side = None
  boat_position = None

  def __init__(self) -> None:
    self.left_side = ["P", "T", "F", "M", "B", "B", "G", "G"]
    self.boat = []
    self.right_side = []
    self.boat_position = BoatPosition.Left
  
  def __getitem__(self, key):
    return getattr(self, key)

  
  def copy(self):
    copiedState = State()
    copiedState.left_side = self.left_side.copy()
    copiedState.right_side = self.right_side.copy()
    copiedState.boat = self.boat.copy()
    copiedState.boat_position = self.boat_position
    return copiedState

class Directions(enum.Enum):
  LeftToRight = 1
  RightToLeft = 2

class BoatPosition(enum.Enum):
  Left = 1
  Right = 2

class Move:
  moveDirection = None
  passengers = None

  def __init__(self):
    self.passengers = []
    pass

  def setPassengers(self, passengers):
    self.passengers = passengers
  
  def setDirection(self, direction):
    self.moveDirection = direction

class StateId:
  stateId = None
  move = None

  def __init__(self, stateId, move):
    self.stateId = stateId
    self.move = move.moveDirection

class Node:
  parentNode = None
  children = None
  previousStateIds = None
  stateId = None
  state = None
  move = None
  isProcessed = None

  
  def __init__(self):
    self.isProcessed = False
    self.children = []
    self.previousStateIds = []
    self.state = State()
    self.stateId = StateId(111122, Move())

  def childOf(self, node):
    self.parentNode = node
  
  def createChild(self, state, move):
    newNode = Node()
    newNode.childOf(self)
    newNode.setMove(move)
    newNode.setState(state)
    self.children.append(newNode)
    newPreviousStateIds = self.previousStateIds.copy()
    newPreviousStateIds.append(self.stateId)
    newNode.setPreviousStateIds(newPreviousStateIds)
    return newNode

  def setMove(self, move):
    self.move = move

  def setPreviousStateIds(self, stateIds):
    self.previousStateIds = stateIds

  def setState(self, state):
    self.state = state
    stateId = calculateStateId(self.state)
    self.stateId = StateId(stateId, self.move)

  def getParentNode(self):
    return self.parentNode
  
  def generateChildren(self):
    # for left to right move
    if self.state.boat_position == BoatPosition.Left:
      # possible moves with one person in the boat
      for member in self.state.left_side:
        copiedState = self.state.copy()
        copiedState.left_side.remove(member)
        copiedState.boat.append(member)
        membersOnBoatValidityCheck = isValid(copiedState)

        if membersOnBoatValidityCheck :
          copiedState.boat = []
          copiedState.right_side.append(member)
          copiedState.boat_position = BoatPosition.Right
          membersMovedToOtherSideValidityCheck = isValid(copiedState)

          if membersMovedToOtherSideValidityCheck :
            copiedStateId = calculateStateId(copiedState)
            newMove = Move()
            newMove.setDirection(Directions.LeftToRight)
            newMove.setPassengers([member])
            isLoop = False
            for id in self.previousStateIds:
              if id.stateId == copiedStateId and id.move == newMove.moveDirection:
                isLoop = True
                break
            
            if not isLoop:
              self.createChild(copiedState, newMove)
            

      # possible moves with two person on the boat
      for i in range(len(self.state.left_side)):
        for j in range(i + 1, len(self.state.left_side)):
          copiedState = self.state.copy()
          copiedState.boat.append(self.state.left_side[i])
          copiedState.boat.append(self.state.left_side[j])
          copiedState.left_side.pop(j)
          copiedState.left_side.pop(i)
          membersOnBoatValidityCheck = isValid(copiedState)

          if membersOnBoatValidityCheck :

            copiedState.boat = []
            copiedState.right_side.append(self.state.left_side[j])
            copiedState.right_side.append(self.state.left_side[i])
            
            copiedState.boat_position = BoatPosition.Right
            membersMovedToOtherSideValidityCheck = isValid(copiedState)

            if membersMovedToOtherSideValidityCheck :
              copiedStateId = calculateStateId(copiedState)
              newMove = Move()
              newMove.setDirection(Directions.LeftToRight)
              newMove.setPassengers([self.state.left_side[j], self.state.left_side[i]])
              isLoop = False
              for id in self.previousStateIds:
                if id.stateId == copiedStateId and id.move == newMove.moveDirection:
                  isLoop = True
                  break
              
              if not isLoop:
                self.createChild(copiedState, newMove)      
              
    # for Right to left move
    else:
      # possible moves with one person in the boat
      for member in self.state.right_side:
        copiedState = self.state.copy()
        copiedState.right_side.remove(member)
        copiedState.boat.append(member)
        membersOnBoatValidityCheck = isValid(copiedState)

        if membersOnBoatValidityCheck :
          copiedState.boat = []
          copiedState.left_side.append(member)
          copiedState.boat_position = BoatPosition.Left
          membersMovedToOtherSideValidityCheck = isValid(copiedState)

          if membersMovedToOtherSideValidityCheck :
            copiedStateId = calculateStateId(copiedState)
            newMove = Move()
            newMove.setDirection(Directions.RightToLeft)
            newMove.setPassengers([member])
            isLoop = False
            for id in self.previousStateIds:
              if id.stateId == copiedStateId and id.move == newMove.moveDirection:
                isLoop = True
                break
            
            if not isLoop:
              self.createChild(copiedState, newMove)

      # possible moves with two person on the boat
      for i in range(len(self.state.right_side)):
        for j in range(i + 1, len(self.state.right_side)):
          copiedState = self.state.copy()
          copiedState.boat.append(self.state.right_side[i])
          copiedState.boat.append(self.state.right_side[j])
          copiedState.right_side.pop(j)
          copiedState.right_side.pop(i)
          membersOnBoatValidityCheck = isValid(copiedState)

          if membersOnBoatValidityCheck :

            copiedState.boat = []
            copiedState.left_side.append(self.state.right_side[j])
            copiedState.left_side.append(self.state.right_side[i])
            
            copiedState.boat_position = BoatPosition.Left
            membersMovedToOtherSideValidityCheck = isValid(copiedState)

            if membersMovedToOtherSideValidityCheck :
              copiedStateId = calculateStateId(copiedState)
              newMove = Move()
              newMove.setDirection(Directions.RightToLeft)
              newMove.setPassengers([self.state.right_side[j], self.state.right_side[i]])
              isLoop = False
              for id in self.previousStateIds:
                if id.stateId == copiedStateId and id.move == newMove.moveDirection:
                  isLoop = True
                  break
              
              if not isLoop:
                self.createChild(copiedState, newMove)

# finding the right sequence
def findTheSequence(node):
  
  if isGoal(node.state):
    return node

  if not node.isProcessed:
    node.generateChildren()
    node.isProcessed = True
  
  result = None
  for child in node.children:
    result = findTheSequence(child)
    if isinstance(result, Node): break
    
  return result

def show(node):
  nodes_array_sorted = []
  while node.getParentNode() != None:
    nodes_array_sorted.insert(0, node)
    node = node.getParentNode()
  
  for (index, item) in enumerate(nodes_array_sorted):
    print("Move number #", index, ": ")
    print("In this move ",item.move.passengers, " went from ", end='')
    if item.move.moveDirection == Directions.RightToLeft:
      print("Right to Left")
    else:
      print("Left to Right")
    
    print()
    print("Left side of River")
    print("-----------------------")
    print(item.state.left_side)
    print("-----------------------")
    print("right side of River")
    print("-----------------------")
    print(item.state.right_side)
    print("-----------------------")
    print()
    print()
    print("-------------------------------------------------------------------")

def pathShow(node, waiting_time):
  nodes_array_sorted = []
  while node.getParentNode() != None:
    nodes_array_sorted.insert(0, node)
    node = node.getParentNode()
  
  for (index, item) in enumerate(nodes_array_sorted):
    print("Move number #", index, ": ")
    print("In this move ",item.move.passengers, " went from ", end='')
    if item.move.moveDirection == Directions.RightToLeft:
      print("Right to Left")
    else:
      print("Left to Right")
    
    print()
    print("Left side of River")
    print("-----------------------")
    print(item.state.left_side)
    print("-----------------------")
    print("right side of River")
    print("-----------------------")
    print(item.state.right_side)
    print("-----------------------")
    print()
    print()
    print("-------------------------------------------------------------------")
    time.sleep(waiting_time)

if __name__ == "__main__":
  firstNode = Node()
  firstNode.generateChildren()
  sequence = findTheSequence(firstNode)
  pathShow(sequence, 1)
  
