"""
Environment observation: capture screen, extract text and UI elements.
Core perception module.
"""

from ..perception.vision import capture_screen
from ..perception.ocr_reader import read_screen_text
from ..perception.ui_map import extract_ui_elements
from .logger import logger


def observe():
    """
    Observe current environment state.
    
    Returns:
        Dict with image_path, text (OCR), and elements (UI)
    """
    
    logger.debug("Capturing screen...")
    image_path = capture_screen()
    logger.debug(f"Screen captured: {image_path}")

    logger.debug("Reading screen text with OCR...")
    screen_text = read_screen_text(image_path)
    logger.debug(f"OCR extracted {len(screen_text)} characters")

    logger.debug("Extracting UI elements...")
    ui_elements = extract_ui_elements(image_path)
    logger.debug(f"Found {len(ui_elements)} UI elements")

    return {
        "image": image_path,
        "text": screen_text,
        "elements": ui_elements
    }