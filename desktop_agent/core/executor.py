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
from .logger import logger, log_section, log_action, log_result


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


def execute_actions(actions, current_image=None):

    for item in actions:

        action = item.get("action")

        if action not in ALLOWED_ACTIONS:

            print(f"Blocked action: {action}")

            continue


        print(f"Executing: {action}")


        if action == "open_app":

            open_app(item["app"])

            if item["app"] == "chrome":

                state["chrome_opened"] = True


        elif action == "open_website":

            open_website(item["url"])


        elif action == "type":

            focused = focus_window("Chrome")

            if not focused:

                print("Could not focus Chrome")

                continue


            time.sleep(1)


            active = get_active_window()

            if not active or "Chrome" not in active:

                print("Chrome not active")

                continue


            print("Typing into Chrome")

            type_text(item["text"])

        elif action == "press":

            press_key(item["key"])


        elif action == "wait":

            wait(item["seconds"])


        elif action == "click":

            click(item["x"], item["y"])


        elif action == "done":

            print("Task completed")


        elif action == "click_text":

            success = click_text(
                current_image,
                item["text"]
            )

            print("Click success:", success)