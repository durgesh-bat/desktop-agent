import time

from window_manager import (
    get_active_window,
    focus_window
)


print("Before:")
print(get_active_window())


print("Switching to Chrome...")

focus_window("Chrome")

time.sleep(2)


print("After:")
print(get_active_window())