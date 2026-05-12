import sys
import os

from desktop_agent.perception.vision import capture_screen

path = capture_screen()

print("Saved:", path)