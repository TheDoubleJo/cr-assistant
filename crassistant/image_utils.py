"""This module contains functions to take a screenshot, resize image, find the most similar image"""

import os
import shutil
import cv2
import numpy as np
import pyautogui


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
