"""This module contains the Slot class which represents a slot in the game."""

from pydantic import BaseModel


class Slot(BaseModel):
    """This class represents a slot in the game"""

    index: int = None
    previous_screenshot: str = None
    current_screenshot: str = None
    similarity: float = 0.0
    iterations_since_last_change: int = 0
