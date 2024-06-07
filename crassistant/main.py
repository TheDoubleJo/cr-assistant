""" This module contains the main functions of the program """

import os
import cv2
import numpy as np
import pyautogui

# from skimage.metrics import structural_similarity as ssim
import skimage


class Slot:
    """This class represents a slot in the game"""

    index = None
    screenshot = None
    cardImage = None
    cardName = None

    def __init__(
        self,
        an_index,
    ):
        self.index = an_index


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
        the_slots[j].screenshot = screenshots[j]

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
def find_closest_image(the_slot, unknown_image) -> Slot:
    """Find the image that is the most close to the screenshot of the slot"""

    # Get the screenshot of the slot
    screenshot = the_slot.screenshot

    # Get the similarity between the screenshot and the unknown image
    similarity = skimage.metrics.structural_similarity(
        unknown_image, screenshot, win_size=7, channel_axis=2
    )

    # If the similarity is high, the slot is empty
    if similarity > 0.75:
        the_slot.screenshot = screenshot
        the_slot.cardImage = unknown_image
        the_slot.cardName = "unknown"
        return the_slot

    max_ssim = -1
    most_similar_image = None
    image_file_chosen = None

    path = os.path.join(os.getcwd(), "crassistant", "img", "resized")

    # Get the list of images in the img/cards directory
    images = os.listdir(path)

    for image in images:

        # Read the image
        image_file = cv2.imread(os.path.join(path, image))

        similarity = skimage.metrics.structural_similarity(
            image_file, screenshot, win_size=7, channel_axis=2
        )

        if similarity > max_ssim:
            max_ssim = similarity
            most_similar_image = image
            image_file_chosen = image_file

    the_slot.cardImage = image_file_chosen
    the_slot.screenshot = screenshot
    the_slot.cardName = most_similar_image.split(".")[0]

    print(f"{the_slot.cardName} : {max_ssim}")

    return the_slot


def main():
    """Main function of the program"""

    # Initialize the 8 slots
    slots = []
    for i in range(8):
        slots.append(Slot(i))

    take_screenshot(slots)

    resize_images(slots[0].screenshot.shape[1], slots[0].screenshot.shape[0])

    # Get the unknown image in the img/misc directory
    unknown_image = cv2.imread(
        os.path.join(os.getcwd(), "crassistant", "img", "misc", "unknown.png")
    )

    unknown_from_there = False

    for slot in slots:

        if unknown_from_there:
            slot.cardName = "unknown"
            slot.cardImage = unknown_image
            continue

        slot = find_closest_image(slot, unknown_image)

        if slot.cardName == "unknown":
            unknown_from_there = True

    for slot in slots:
        print(slot.cardName)
        cv2.imshow("screenshot", slot.screenshot)
        cv2.imshow("card", slot.cardImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


main()
