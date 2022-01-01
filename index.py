class State:
  def __init__(self) -> None:
    self.left_side = ["P", "T", "F", "M", "B", "B", "G", "G"],
    self.boat = [],
    self.right_side = []
  
  def copy(self):
    copiedState = State()
    copiedState.left_side = self.left_side.copy()
    copiedState.right_side = self.right_side.copy()
    copiedState.boat = self.boat.copy()
    return copiedState


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


  
def __main__():
  pass
  
