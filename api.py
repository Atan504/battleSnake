"""
Welcome to the API Documentation!

You probably want to get started with `API` methods, and have a look at `Result`.
"""

from __future__ import annotations

from enum import Enum
from typing import List, Tuple


class PlayerState:
    position: List[Tuple[int, int]]
    """A list of snake nodes, where the first one is the player's tail, last is head."""

    health: int
    """The current health of the snake."""

    length: int
    """The current length of the snake."""

    head: Tuple[int, int]
    """The location of the head of the snake."""

    body: List[Tuple[int, int]]
    """The location list of everything but the head of the snake."""


class Result(Enum):
    """
    An enum representing result of API methods.
    See each method for a list of possible results.
    If a method was successful, it always returns `OK`.
    """

    OK = 0
    INVALID_DIRECTION = 1

    def __bool__(self):
        return self == Result.OK


class API:
    """
    test
    The main access point for your bot. Access this using `self.context` inside your `run` method.

    Each action method returns `Result`, which is `Result.OK` if it succeeded, or another value explaining why it failed.
    """

    def set_direction(self, direction: str):
        """
        sets the direction of your snake's next move,
        "U" to move Up
        "D" to move Down
        "L" to move Left
        "R" to move Right
        """
        raise NotImplementedError("Not Implemented!")

    def get_myself(self) -> PlayerState:
        """
        returns your own player state
        """
        raise NotImplementedError("Not Implemented!")

    def get_apples(self) -> List[Tuple[int, int]]:
        """
        returns a list of the coordinates (x,y) where apples are located.
        """
        raise NotImplementedError("Not Implemented!")

    def get_game_size(self) -> Tuple[int, int]:
        """
        returns the width,height of the game map.
        """
        raise NotImplementedError("Not Implemented!")

    def get_occupied_tiles(self) -> List[Tuple[int, int]]:
        "returns a list of tiles occupied by snakes, as coordinates (x,y)"
        raise NotImplementedError("Not Implemented!")

    def in_bounds(self, coord: Tuple[int, int]) -> bool:
        """returns true if coord (a coordinate (x,y)) is in the bounds of the game map"""
        raise NotImplementedError("Not Implemented!")

    def get_active_players(self) -> List[PlayerState]:
        """returns a list of all active players"""
        raise NotImplementedError("Not Implemented!")

    def get_position(self, player: PlayerState) -> List[Tuple[int, int]]:
        """
        returns a list of the tiles player is occupying as coords (x,y)
        the tail is at the first position (position[0]), head is at the last position (position[-1])
        """
        raise NotImplementedError("Not Implemented!")

    def get_length(self, player: PlayerState) -> int:
        """
        returns the length of the snake
        """
        raise NotImplementedError("Not Implemented!")

    def get_health(self, player: PlayerState) -> int:
        """
        returns the health of the snake, when this value gets to 0, the snake will be eliminated
        """
        raise NotImplementedError("Not Implemented!")

    def get_has_eaten_last_step(self, player: PlayerState) -> int:
        """
        0 if the snake has not eaten last step, 1 if it had.
        in the first step, has_eaten is set to 2, as the snake needs to strech out from its initial state.
        """
        raise NotImplementedError("Not Implemented!")

    ### GENERAL METHODS ###

    def log_info(self, text: str):
        """
        Prints the text to the console as an info message.

        **Warning:** Writing to log every time the `run` method is called might slow down the game.
        """
        raise NotImplementedError("Log")

    def log_warning(self, text: str):
        """
        Prints the text to the console as a warning.

        **Warning:** Writing to log every time the `run` method is called might slow down the game.
        """
        raise NotImplementedError("Log")

    def log_error(self, text: str):
        """
        Prints the text to the console as an error.

        **Warning:** Writing to log every time the `run` method is called might slow down the game.
        """
        raise NotImplementedError("Log")


class CodeBattlesBot:
    """
    Base class for writing your bots.

    **Important:** Your bot must subclass this directly, and be called MyBot!

    **Important:** Your bot must not have a custom __init__ method. Use `setup` for any setup code you may have.

    **Example:**

    ```python
    class MyBot(CodeBattlesBot):
        def setup(self):
            self.first_move = "L"
        def run(self):
            self.context.set_direction(self.first_move)
    ```
    """

    context: API

    def __init__(self, context: API):
        """Do not override this function."""

        self.context = context
        self.setup()

    def setup(self) -> None:
        """
        This optional method will be called upon construction.

        If you need to define any instance variables like in a constructor, do it here.
        """

        pass

    def run(self) -> None:
        """
        This method will be called once every game step.

        Interact with the game using `self.context`.
        """

        pass


Context = API
Exceptions = Result
