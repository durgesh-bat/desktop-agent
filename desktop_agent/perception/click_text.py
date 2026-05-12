import time

from .text_locator import find_text_position
from ..actions.actions import click
from ..core.logger import logger, log_action, log_result


def click_text(image_path, text):

    print(f"Searching for text: {text}")

    pos = find_text_position(
        image_path,
        text
    )

    if not pos:

        print(f"Text not found: {text}")

        return False


    x, y = pos

    print(f"Clicking '{text}' at ({x}, {y})")

    click(x, y)

    time.sleep(1)

    return True