import pyautogui
import subprocess
import time
import webbrowser
from .app_map import APP_MAP
from ..core.logger import logger, log_action, log_result

def open_app(app_name):

    app_name = app_name.lower()

    command = APP_MAP.get(app_name)

    if not command:
        logger.warning(f"Unknown app: {app_name}")
        return

    try:
        logger.info(f"Opening app: {app_name}")
        subprocess.Popen(command, shell=True)

        # Wait for app to fully open
        time.sleep(3)

        log_result(True, f"Opened: {app_name}")

    except Exception as e:
        logger.error(f"Error opening {app_name}: {e}", exc_info=True)
        log_result(False, f"Failed to open {app_name}")


def open_website(url):
    try:
        logger.info(f"Opening website: {url}")
        webbrowser.open(url)
        log_result(True, f"Website opened: {url}")
    except Exception as e:
        logger.error(f"Error opening website {url}: {e}", exc_info=True)
        log_result(False, f"Failed to open website {url}")


def type_text(text):
    try:
        logger.debug(f"Typing text: {text[:50]}...")
        pyautogui.write(text, interval=0.03)
        log_result(True, f"Typed {len(text)} characters")
    except Exception as e:
        logger.error(f"Error typing text: {e}", exc_info=True)
        log_result(False, "Failed to type text")


def press_key(key):
    try:
        logger.debug(f"Pressing key: {key}")
        pyautogui.press(key)
        log_result(True, f"Pressed key: {key}")
    except Exception as e:
        logger.error(f"Error pressing key {key}: {e}", exc_info=True)
        log_result(False, f"Failed to press key {key}")


def wait(seconds):
    logger.debug(f"Waiting {seconds} seconds")
    time.sleep(seconds)

def click(x, y):
    try:
        logger.debug(f"Clicking at coordinates: ({x}, {y})")
        pyautogui.click(x, y)
        log_result(True, f"Clicked at ({x}, {y})")
    except Exception as e:
        logger.error(f"Error clicking at ({x}, {y}): {e}", exc_info=True)
        log_result(False, f"Failed to click at ({x}, {y})")