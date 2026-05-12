from ..llm.agent import get_actions
from .state import state
from .logger import logger


def plan(task, observation):

    prompt = f"""
Task:
{task}

Current visible screen text:

{observation["text"]}

Current state:

{state}

Rules:
- If Chrome already opened, do NOT open it again.
- If search results visible, return done.
- Avoid repeating actions.
- Return ONLY ONE action.
- Return ONLY valid JSON.

JSON format:

{{
  "actions":[]
}}
"""

    result = get_actions(prompt)

    return result["actions"][0]