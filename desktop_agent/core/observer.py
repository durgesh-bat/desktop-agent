from ..perception.vision import capture_screen
from ..perception.ocr_reader import read_screen_text
from ..perception.ui_map import extract_ui_elements


def observe():

    image_path = capture_screen()

    screen_text = read_screen_text(image_path)

    ui_elements = extract_ui_elements(image_path)

    return {
        "image": image_path,
        "text": screen_text,
        "elements": ui_elements
    }