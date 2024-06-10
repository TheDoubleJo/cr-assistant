""" This module contains the main functions of the program """

import os
import tkinter as tk
from PIL import Image, ImageTk
from crassistant.models.slot import Slot
from crassistant.models.cards_in_hand import CardsInHand
from crassistant.image_utils import take_screenshot, is_unknown, calculate_similarity


def new_game(slots, cards_in_hand) -> tuple:
    """Initialize a new game"""

    for slot in slots:
        slot.previous_screenshot = slot.current_screenshot
        slot.similarity = 1
        slot.iterations_since_last_change = 100

    # Initialize the 4 cards in hand
    cards_in_hand.card1 = slots[0]
    cards_in_hand.card2 = slots[1]
    cards_in_hand.card3 = slots[2]
    cards_in_hand.card4 = slots[3]
    cards_in_hand.last_4_cards_played.queue.clear()

    return slots, cards_in_hand


def cards_in_hand_algo(cards_in_hand, slots, slot_changed) -> CardsInHand:
    """This function returns the 4 cards currently in hand"""

    if cards_in_hand.last_4_cards_played.full():
        new_card_in_hand = cards_in_hand.last_4_cards_played.get()
    else:
        new_card_in_hand = 4 + cards_in_hand.last_4_cards_played.qsize()

    cards_in_hand.last_4_cards_played.put(slot_changed.index)

    if slot_changed.index == cards_in_hand.card1.index:
        cards_in_hand.card1 = slots[new_card_in_hand]
    elif slot_changed.index == cards_in_hand.card2.index:
        cards_in_hand.card2 = slots[new_card_in_hand]
    elif slot_changed.index == cards_in_hand.card3.index:
        cards_in_hand.card3 = slots[new_card_in_hand]
    elif slot_changed.index == cards_in_hand.card4.index:
        cards_in_hand.card4 = slots[new_card_in_hand]

    return cards_in_hand


def update(
    root,
    slots,
    cards_in_hand,
    previous_screenshot_labels,
    current_screenshot_labels,
    similirity_vars,
    cards_in_hand_labels,
    slot_number_vars,
    unknown_image_path,
    game_in_progress,
):
    """Update the GUI"""

    slots = take_screenshot(slots)
    slots_changed = []
    for i in range(8):

        slot = slots[i]

        # Unknown detection
        if i == 0 and not game_in_progress and is_unknown(slot, unknown_image_path):
            print("New game detected !")
            # Initialize a new game
            slots, cards_in_hand = new_game(slots, cards_in_hand)
            game_in_progress = True

        if not game_in_progress:
            break

        # Screenshots comparison
        slot.similarity = calculate_similarity(
            slot.previous_screenshot, slot.current_screenshot
        )

        # Change detection
        if slot.similarity < 0.3 and slot.iterations_since_last_change > 5:
            slot.iterations_since_last_change = 0
            print(f"Change detected in slot {slot.index}")
            cards_in_hand = cards_in_hand_algo(cards_in_hand, slots, slot)
            slots_changed.append(slot.index)
        else:
            slot.iterations_since_last_change += 1

        # GUI update
        previous_screenshot_labels[i].configure(
            image=current_screenshot_labels[i].image
        )
        previous_screenshot_labels[i].image = current_screenshot_labels[i].image

        current_screenshot = Image.open(slot.current_screenshot)
        current_screenshot_image = ImageTk.PhotoImage(current_screenshot)
        current_screenshot_labels[i].configure(image=current_screenshot_image)
        current_screenshot_labels[i].image = current_screenshot_image

        similirity_vars[i].set(f"{slot.similarity:0.3f}")

    if len(slots_changed) > 3:
        print("Game over !")
        game_in_progress = False

    if game_in_progress:

        cards_in_hand_image1 = Image.open(cards_in_hand.card1.previous_screenshot)
        cards_in_hand_image_tk1 = ImageTk.PhotoImage(cards_in_hand_image1)
        cards_in_hand_labels[0].configure(image=cards_in_hand_image_tk1)
        cards_in_hand_labels[0].image = cards_in_hand_image_tk1

        slot_number_vars[0].set(f"{cards_in_hand.card1.index}")

        cards_in_hand_image2 = Image.open(cards_in_hand.card2.previous_screenshot)
        cards_in_hand_image_tk2 = ImageTk.PhotoImage(cards_in_hand_image2)
        cards_in_hand_labels[1].configure(image=cards_in_hand_image_tk2)
        cards_in_hand_labels[1].image = cards_in_hand_image_tk2

        slot_number_vars[1].set(f"{cards_in_hand.card2.index}")

        cards_in_hand_image3 = Image.open(cards_in_hand.card3.previous_screenshot)
        cards_in_hand_image_tk3 = ImageTk.PhotoImage(cards_in_hand_image3)
        cards_in_hand_labels[2].configure(image=cards_in_hand_image_tk3)
        cards_in_hand_labels[2].image = cards_in_hand_image_tk3

        slot_number_vars[2].set(f"{cards_in_hand.card3.index}")

        cards_in_hand_image4 = Image.open(cards_in_hand.card4.previous_screenshot)
        cards_in_hand_image_tk4 = ImageTk.PhotoImage(cards_in_hand_image4)
        cards_in_hand_labels[3].configure(image=cards_in_hand_image_tk4)
        cards_in_hand_labels[3].image = cards_in_hand_image_tk4

        slot_number_vars[3].set(f"{cards_in_hand.card4.index}")

    root.after(
        1000,
        update,
        root,
        slots,
        cards_in_hand,
        previous_screenshot_labels,
        current_screenshot_labels,
        similirity_vars,
        cards_in_hand_labels,
        slot_number_vars,
        unknown_image_path,
        game_in_progress,
    )


def main():
    """Main function"""

    # Initialize the 8 slots
    slots = []
    for i in range(8):
        slots.append(Slot(i, None, None, None))

    # Initialize the 4 cards in hand
    cards_in_hand = CardsInHand(
        card1=slots[0], card2=slots[1], card3=slots[2], card4=slots[3]
    )

    # Get the unknown image in the img/misc directory
    unknown_image_path = os.path.join(
        os.getcwd(), "crassistant", "img", "misc", "unknown.png"
    )

    # create root window
    root = tk.Tk()

    # root window title and dimension
    root.title("CR assistant")
    # Set geometry (widthxheight)
    root.geometry("600x300")

    previous_screenshot_labels = []
    current_screenshot_labels = []
    similirity_vars = []
    cards_in_hand_labels = []
    slot_number_vars = []

    screenshot = Image.open(unknown_image_path)
    screenshot_image = ImageTk.PhotoImage(screenshot)

    # Set a grid with 1 row and 8 columns
    for column in range(8):

        previous_screenshot_label = tk.Label(
            root,
            image=screenshot_image,
        )

        previous_screenshot_label.grid(row=0, column=column)
        previous_screenshot_label.image = screenshot_image
        previous_screenshot_labels.append(previous_screenshot_label)

        current_screenshot_label = tk.Label(
            root,
            image=screenshot_image,
        )

        current_screenshot_label.grid(row=1, column=column)
        current_screenshot_label.image = screenshot_image
        current_screenshot_labels.append(current_screenshot_label)

        similirity_var = tk.StringVar()
        similirity_vars.append(similirity_var)

        tk.Label(
            root,
            textvariable=similirity_var,
        ).grid(row=2, column=column)

    for column in range(4):

        cards_in_hand_label = tk.Label(
            root,
            image=screenshot_image,
        )

        cards_in_hand_label.grid(row=3, column=column)
        cards_in_hand_label.image = screenshot_image
        cards_in_hand_labels.append(cards_in_hand_label)

        slot_number_var = tk.StringVar()
        slot_number_vars.append(slot_number_var)

        tk.Label(
            root,
            textvariable=slot_number_var,
        ).grid(row=4, column=column)

    update(
        root,
        slots,
        cards_in_hand,
        previous_screenshot_labels,
        current_screenshot_labels,
        similirity_vars,
        cards_in_hand_labels,
        slot_number_vars,
        unknown_image_path,
        False,
    )

    root.mainloop()


if __name__ == "__main__":
    main()
