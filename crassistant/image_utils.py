"""This module contains functions to take a screenshot, resize image, find the most similar image"""

import os
import shutil
import cv2
import numpy as np
import pyautogui
import skimage


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

        current_screenshot_path = os.path.join(
            os.getcwd(),
            "crassistant",
            "img",
            "screenshots",
            f"current_screenshot_{j}.png",
        )

        previous_screenshot_path = os.path.join(
            os.getcwd(),
            "crassistant",
            "img",
            "screenshots",
            f"previous_screenshot_{j}.png",
        )

        # Rename the current screenshot file to previous screenshot file
        if os.path.exists(current_screenshot_path):
            shutil.move(current_screenshot_path, previous_screenshot_path)

        # Save the screenshot in the screenshots directory
        cv2.imwrite(current_screenshot_path, screenshots[j])

        the_slots[j].previous_screenshot = previous_screenshot_path
        the_slots[j].current_screenshot = current_screenshot_path

    return the_slots


def calculate_similarity(image1_path, image2_path) -> float:
    """Calculate the similarity between two images"""

    # Load the images
    image1 = cv2.imread(image1_path)
    image2 = cv2.imread(image2_path)

    # Convert the images to grayscale
    # image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    # image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # Calculate the structural similarity index
    coef = skimage.metrics.structural_similarity(
        image1, image2, win_size=7, channel_axis=2
    )

    return coef


# Function the check if the provided image is similar to the 'unknown' image
def is_unknown(slot, unknown_image_path) -> bool:
    """Check if the provided image is similar to the 'unknown' image"""

    similarity = calculate_similarity(slot.current_screenshot, unknown_image_path)

    return similarity > 0.7
