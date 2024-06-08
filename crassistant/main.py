""" This module contains the main functions of the program """

import os
import dataclasses
import tkinter as tk
import cv2
import numpy as np
import pyautogui
import skimage
from PIL import Image, ImageTk


@dataclasses.dataclass
class Slot:
    """This class represents a slot in the game"""

    index: int = None
    screenshot: str = None
    card_image: str = None
    card_name: str = None
    similarity: float = 0.0


def take_screenshot(the_slots) -> list:
    """Take a screenshot of the screen and display it"""

    cards_region = (750, 90, 480, 75)

    # Take a screenshot of the screen
    screenshot = pyautogui.screenshot(region=cards_region)

    # Convert the screenshot to a numpy array
    screenshot = np.array(screenshot)

    # Convert the screenshot to BGR
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Cut the screenshot horizontally in 8 equal parts
    screenshots = np.hsplit(screenshot, 8)

    # Assign each screenshot to a slot
    for j in range(8):

        path = os.path.join(
            os.getcwd(), "crassistant", "img", "screenshots", f"screenshot{j}.png"
        )

        # Save the screenshot in the screenshots directory
        cv2.imwrite(path, screenshots[j])

        the_slots[j].screenshot = path

    return the_slots


# Function to resize all the images in the img/cards directory to 75x60
# and save them in the img/resized directory
def resize_images(width, height) -> None:
    """Resize all the images in the img/cards directory"""

    path = os.path.join(os.getcwd(), "crassistant", "img", "cards")
    resized_path = os.path.join(os.getcwd(), "crassistant", "img", "resized")

    # If the directory img/resized is not empty, do nothing
    if os.listdir(resized_path):
        return

    # Get the list of images in the img/cards directory
    images = os.listdir(path)

    for image in images:

        # Read the image
        image_file = cv2.imread(os.path.join(path, image))

        # Resize the image
        size = (width, height)
        resized_image = cv2.resize(image_file, size, interpolation=cv2.INTER_AREA)

        # Save the resized image
        cv2.imwrite(os.path.join(resized_path, image), resized_image)


# Function to find out which images from the img diretory is the most close to the screenshot
def find_closest_image(the_slot, unknown_image_path, unknown_image) -> Slot:
    """Find the image that is the most close to the screenshot of the slot"""

    # Get the screenshot of the slot
    screenshot = cv2.imread(the_slot.screenshot)

    # Get the similarity between the screenshot and the unknown image
    similarity = skimage.metrics.structural_similarity(
        unknown_image, screenshot, win_size=7, channel_axis=2
    )

    # If the similarity is high, the slot is empty
    if similarity > 0.75:
        the_slot.card_image = unknown_image_path
        the_slot.card_name = "unknown"
        the_slot.similarity = similarity
        return the_slot

    max_ssim = -1
    most_similar_image = None
    image_path_chosen = None

    path = os.path.join(os.getcwd(), "crassistant", "img", "resized")

    # Get the list of images in the img/cards directory
    images = os.listdir(path)

    for image in images:

        image_path = os.path.join(path, image)

        # Read the image
        image_file = cv2.imread(image_path)

        similarity = skimage.metrics.structural_similarity(
            image_file, screenshot, win_size=7, channel_axis=2
        )

        if similarity > max_ssim:
            max_ssim = similarity
            most_similar_image = image
            image_path_chosen = image_path

    the_slot.card_image = image_path_chosen
    the_slot.card_name = most_similar_image.split(".")[0]
    the_slot.similarity = max_ssim

    return the_slot


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

    slots = take_screenshot(slots)
    unknown_from_there = False
    for i in range(8):

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

    root.after(
        1000,
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
