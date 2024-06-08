"""This module contains the Slot class which represents a slot in the game."""

import dataclasses


@dataclasses.dataclass
class Slot:
    """This class represents a slot in the game"""

    index: int = None
    screenshot: str = None
    card_image: str = None
    card_name: str = None
    similarity: float = 0.0
