import sys
import os

from desktop_agent.perception.vision import capture_screen
from desktop_agent.perception.click_text import click_text


path = capture_screen()

click_text(path, "Google")