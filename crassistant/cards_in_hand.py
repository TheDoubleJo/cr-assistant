"""This module contains the CardsInHand class which represents the 4 cards currently in hand."""

import dataclasses
import queue
from crassistant.slot import Slot


@dataclasses.dataclass
class CardsInHand:
    """This class represents the 4 cards currently in hand."""

    card1: Slot = None
    card2: Slot = None
    card3: Slot = None
    card4: Slot = None

    last_4_cards_played: queue.Queue = queue.Queue(maxsize=4)
