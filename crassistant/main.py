""" This module contains the main functions of the program """

import os
import tkinter as tk
from time import perf_counter as pc

# from multiprocessing import Pool
import cv2
from PIL import Image, ImageTk
import skimage
from crassistant.slot import Slot
from crassistant.image_utils import take_screenshot


# def update_slot(slot):
#     slot = take_screenshot(slot)
#     current_screenshot = Image.open(slot.current_screenshot)
#     current_screenshot_image = ImageTk.PhotoImage(current_screenshot)
#     return slot, current_screenshot_image


def update(
    root,
    slots,
    previous_screenshot_labels,
    current_screenshot_labels,
    similirity_vars,
):
    """Update the GUI"""

    # Start a timer
    t0 = pc()

    slots = take_screenshot(slots)

    for i in range(8):

        slot = slots[i]

        previous_screenshot_labels[i].configure(
            image=current_screenshot_labels[i].image
        )
        previous_screenshot_labels[i].image = current_screenshot_labels[i].image

        current_screenshot = Image.open(slot.current_screenshot)
        current_screenshot_image = ImageTk.PhotoImage(current_screenshot)
        current_screenshot_labels[i].configure(image=current_screenshot_image)
        current_screenshot_labels[i].image = current_screenshot_image

        previous_screenshot_cv2 = cv2.imread(slot.previous_screenshot)
        current_screenshot_cv2 = cv2.imread(slot.current_screenshot)

        similarity = skimage.metrics.structural_similarity(
            previous_screenshot_cv2,
            current_screenshot_cv2,
            win_size=7,
            channel_axis=2,
        )

        slot.similarity = similarity

        similirity_vars[i].set(f"{slot.similarity:0.3f}")

    print(f"{pc() - t0:0.3f}")

    root.after(
        1000,
        update,
        root,
        slots,
        previous_screenshot_labels,
        current_screenshot_labels,
        similirity_vars,
    )


def main():
    """Main function"""

    # Initialize the 8 slots
    slots = []
    for i in range(8):
        slots.append(Slot(i, None, None, None))

    # Get the unknown image in the img/misc directory
    unknown_image_path = os.path.join(
        os.getcwd(), "crassistant", "img", "misc", "unknown.png"
    )

    # create root window
    root = tk.Tk()

    # root window title and dimension
    root.title("CR assistant")
    # Set geometry (widthxheight)
    root.geometry("600x200")

    previous_screenshot_labels = []
    current_screenshot_labels = []
    similirity_vars = []
    # Set a grid with 1 row and 8 columns
    for column in range(8):

        screenshot = Image.open(unknown_image_path)
        screenshot_image = ImageTk.PhotoImage(screenshot)

        previous_screenshot_label = tk.Label(
            root,
            image=screenshot_image,
        )

        previous_screenshot_label.grid(row=0, column=column)
        previous_screenshot_label.image = screenshot_image
        previous_screenshot_labels.append(previous_screenshot_label)

        card = Image.open(unknown_image_path)
        card_image = ImageTk.PhotoImage(card)

        current_screenshot_label = tk.Label(
            root,
            image=card_image,
        )

        current_screenshot_label.grid(row=1, column=column)
        current_screenshot_label.image = card_image
        current_screenshot_labels.append(current_screenshot_label)

        similirity_var = tk.StringVar()
        similirity_vars.append(similirity_var)

        tk.Label(
            root,
            textvariable=similirity_var,
        ).grid(row=3, column=column)

    update(
        root,
        slots,
        previous_screenshot_labels,
        current_screenshot_labels,
        similirity_vars,
    )

    root.mainloop()


main()
