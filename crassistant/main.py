""" This module contains the main functions of the program """

import os
import tkinter as tk
from time import perf_counter as pc
from PIL import Image, ImageTk
import cv2
from crassistant.slot import Slot
from crassistant.image_utils import take_screenshot, resize_images, find_closest_image


def update(
    root,
    slots,
    unknown_image_path,
    unknown_image,
    screenshot_image_labels,
    card_image_labels,
    card_vars,
    similirity_vars,
):
    """Update the GUI"""

    # Start a timer
    t0 = pc()

    slots = take_screenshot(slots)

    t_screenshot = pc() - t0
    print(f"  {t_screenshot:0.3f}")

    unknown_from_there = False
    for i in range(8):

        t1 = pc()

        slot = slots[i]

        if unknown_from_there:
            slot.card_name = "unknown"
            slot.card_image = unknown_image_path
            continue

        slot = find_closest_image(slot, unknown_image_path, unknown_image)

        if slot.card_name == "unknown":
            unknown_from_there = True

        screenshot = Image.open(slot.screenshot)
        screenshot_image = ImageTk.PhotoImage(screenshot)
        screenshot_image_labels[i].configure(image=screenshot_image)
        screenshot_image_labels[i].image = screenshot_image

        card = Image.open(slot.card_image)
        card_image = ImageTk.PhotoImage(card)
        card_image_labels[i].configure(image=card_image)
        card_image_labels[i].image = card_image

        card_vars[i].set(slot.card_name)

        similirity_vars[i].set(f"{slot.similarity:0.3f}")

        t_card = pc() - t1
        print(f"  card {i}:{t_card:0.3f}")

    print(f"{pc() - t0:0.3f}")

    root.after(
        3000,
        update,
        root,
        slots,
        unknown_image_path,
        unknown_image,
        screenshot_image_labels,
        card_image_labels,
        card_vars,
        similirity_vars,
    )


def main():
    """Main function"""

    # Initialize the 8 slots
    slots = []
    for i in range(8):
        slots.append(Slot(i, None, None, None))

    resize_images(60, 75)

    # Get the unknown image in the img/misc directory
    unknown_image_path = os.path.join(
        os.getcwd(), "crassistant", "img", "misc", "unknown.png"
    )

    unknown_image = cv2.imread(unknown_image_path)

    # create root window
    root = tk.Tk()

    # root window title and dimension
    root.title("CR assistant")
    # Set geometry (widthxheight)
    root.geometry("600x200")

    screenshot_image_labels = []
    card_image_labels = []
    card_vars = []
    similirity_vars = []
    # Set a grid with 1 row and 8 columns
    for column in range(8):

        screenshot = Image.open(unknown_image_path)
        screenshot_image = ImageTk.PhotoImage(screenshot)

        screenshot_label = tk.Label(
            root,
            image=screenshot_image,
        )

        screenshot_label.grid(row=0, column=column)
        screenshot_label.image = screenshot_image
        screenshot_image_labels.append(screenshot_label)

        card = Image.open(unknown_image_path)
        card_image = ImageTk.PhotoImage(card)

        card_label = tk.Label(
            root,
            image=card_image,
        )

        card_label.grid(row=1, column=column)
        card_label.image = card_image
        card_image_labels.append(card_label)

        card_name_var = tk.StringVar()
        card_vars.append(card_name_var)

        tk.Label(root, textvariable=card_name_var).grid(row=2, column=column)

        similirity_var = tk.StringVar()
        similirity_vars.append(similirity_var)

        tk.Label(
            root,
            textvariable=similirity_var,
        ).grid(row=3, column=column)

    update(
        root,
        slots,
        unknown_image_path,
        unknown_image,
        screenshot_image_labels,
        card_image_labels,
        card_vars,
        similirity_vars,
    )

    root.mainloop()


main()
