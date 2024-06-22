"""This module contains the CardsInHand class which represents the 4 cards currently in hand."""

import queue
from pydantic import BaseModel
from crassistant.models.slot import Slot


class CardsInHand(BaseModel):
    """This class represents the 4 cards currently in hand."""

    card1: Slot = None
    card2: Slot = None
    card3: Slot = None
    card4: Slot = None

    last_4_cards_played: queue.Queue = queue.Queue(maxsize=4)
