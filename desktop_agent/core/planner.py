"""
Action planning: use LLM to decide next action based on task and observation.
"""

from ..llm.agent import get_actions
from .state import state
from .logger import logger


def plan(task, observation):
    """
    Plan next action using LLM.
    
    Args:
        task: High-level task description
        observation: Current screen observation
        
    Returns:
        Action dict (single action)
    """
    
    logger.debug("Creating planning prompt...")
    
    prompt = f"""
Task:
{task}

Current visible screen text:

{observation["text"][:500]}

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
  "action": "type",
  "text": "search query"
}}
"""

    logger.info("Calling LLM for action planning...")
    
    try:
        result = get_actions(prompt)
        
        if isinstance(result, dict) and "actions" in result:
            action = result["actions"][0]
        else:
            action = result
        
        logger.info(f"LLM returned action: {action.get('action', 'unknown')}")
        return action
        
    except Exception as e:
        logger.error(f"Planning failed: {e}", exc_info=True)
        # Return safe fallback action
        return {"action": "wait", "seconds": 2}