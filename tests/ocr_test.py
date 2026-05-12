import sys
import os

from desktop_agent.perception.vision import capture_screen
from desktop_agent.perception.ocr_reader import read_screen_text


path = capture_screen()

text = read_screen_text(path)

print(text)