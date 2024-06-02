""" This module contains the main functions of the program """

import cv2
import numpy as np
import pyautogui


def search_image(image_path: str):
    """Search for an image in the screen"""

    # Take a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

    # Load the image
    image = cv2.imread(image_path)

    # Search the image
    result = cv2.matchTemplate(screenshot, image, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    print(min_loc, max_loc)
    print(min_val, max_val)

    # Return the coordinates of the image
    return max_loc


search_image("img/truc.png")
