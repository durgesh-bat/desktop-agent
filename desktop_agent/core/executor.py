"""
Action execution: run planned actions safely with focus management and error handling.
"""

from ..actions.actions import (
    open_app,
    open_website,
    type_text,
    press_key,
    wait,
    click
)
import time

from ..actions.window_manager import (
    focus_window,
    get_active_window
)

from .state import state
from ..perception.click_text import click_text
from .logger import logger, log_action, log_result


ALLOWED_ACTIONS = [
    "open_app",
    "open_website",
    "type",
    "press",
    "wait",
    "click",
    "done",
    "click_text"
]

ACTION_COOLDOWN = 0.5  # seconds between actions


def execute_actions(actions, current_image=None):
    """
    Execute list of actions safely.
    
    Args:
        actions: List of action dicts
        current_image: Current screenshot path for click_text
    """
    
    if not actions:
        logger.warning("No actions to execute")
        return
    
    logger.info(f"Executing {len(actions)} action(s)")
    
    for i, item in enumerate(actions):
        action = item.get("action")
        
        if not action:
            logger.warning(f"Action {i} has no 'action' key")
            continue
        
        if action not in ALLOWED_ACTIONS:
            logger.error(f"Action blocked: {action} not in allowed list")
            continue
        
        logger.debug(f"Executing action {i+1}: {action}")
        
        try:
            if action == "open_app":
                _exec_open_app(item)
                
            elif action == "open_website":
                _exec_open_website(item)
                
            elif action == "type":
                _exec_type(item)
                
            elif action == "press":
                _exec_press(item)
                
            elif action == "wait":
                _exec_wait(item)
                
            elif action == "click":
                _exec_click(item)
                
            elif action == "done":
                logger.info("Task marked as done")
                
            elif action == "click_text":
                _exec_click_text(item, current_image)
        
        except Exception as e:
            logger.error(f"Error executing {action}: {e}", exc_info=True)
            continue
        
        # Cooldown between actions
        time.sleep(ACTION_COOLDOWN)


def _exec_open_app(item):
    """Execute open_app action."""
    app_name = item.get("app")
    if not app_name:
        logger.warning("open_app missing 'app' parameter")
        return
    
    log_action("open_app", app_name)
    open_app(app_name)
    
    if app_name.lower() == "chrome":
        state["chrome_opened"] = True
        logger.info("Chrome opened, setting state flag")


def _exec_open_website(item):
    """Execute open_website action."""
    url = item.get("url")
    if not url:
        logger.warning("open_website missing 'url' parameter")
        return
    
    log_action("open_website", url[:50])
    open_website(url)


def _exec_type(item):
    """Execute type action with Chrome focus management."""
    text = item.get("text")
    if not text:
        logger.warning("type action missing 'text' parameter")
        return
    
    # Try to focus Chrome
    logger.debug("Attempting to focus Chrome...")
    focused = focus_window("Chrome")
    
    if not focused:
        logger.warning("Could not focus Chrome, trying alternative focus method")
        # Fallback: try with shorter name
        focused = focus_window("chrome")
    
    if not focused:
        logger.error("Failed to focus Chrome window")
        log_result(False, "Chrome window not found")
        return
    
    # Verify Chrome is active
    time.sleep(0.5)
    active = get_active_window()
    logger.debug(f"Active window after focus: {active}")
    
    if not active or "chrome" not in active.lower():
        logger.warning(f"Chrome not active, current window: {active}")
        log_result(False, "Chrome window not active after focus attempt")
        return
    
    # Now type
    logger.info(f"Typing into Chrome: {text[:30]}...")
    log_action("type", text[:50])
    type_text(text)
    log_result(True, f"Typed {len(text)} characters")


def _exec_press(item):
    """Execute press_key action."""
    key = item.get("key")
    if not key:
        logger.warning("press action missing 'key' parameter")
        return
    
    log_action("press", key)
    press_key(key)
    log_result(True, f"Pressed key: {key}")


def _exec_wait(item):
    """Execute wait action."""
    seconds = item.get("seconds", 1)
    
    if not isinstance(seconds, (int, float)):
        logger.warning(f"wait action has invalid seconds: {seconds}")
        return
    
    logger.debug(f"Waiting {seconds} seconds")
    log_action("wait", f"{seconds}s")
    wait(seconds)
    log_result(True, f"Waited {seconds}s")


def _exec_click(item):
    """Execute click action."""
    x = item.get("x")
    y = item.get("y")
    
    if x is None or y is None:
        logger.warning(f"click action has invalid coordinates: ({x}, {y})")
        return
    
    log_action("click", f"({x}, {y})")
    click(x, y)
    log_result(True, f"Clicked at ({x}, {y})")


def _exec_click_text(item, current_image):
    """Execute click_text action."""
    text = item.get("text")
    if not text:
        logger.warning("click_text action missing 'text' parameter")
        return
    
    if not current_image:
        logger.warning("click_text requires current_image but none provided")
        return
    
    log_action("click_text", text[:30])
    logger.info(f"Searching for text on screen: {text}")
    
    success = click_text(current_image, text)
    
    if success:
        log_result(True, f"Clicked text: {text}")
    else:
        log_result(False, f"Text not found: {text}")
