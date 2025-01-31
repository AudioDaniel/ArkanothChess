from event import subscribe
from event import post_event


# Controls the game loop and turn order
class TurnManager():

    def __init__(self):
        # Represents the current player turn (True for green player and False for red)
        current_player : bool = True
        pass

    def start_turn(self):
        post_event("turn_start", self)
        pass
