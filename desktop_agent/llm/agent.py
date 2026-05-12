import json

from openai import OpenAI

from .config import NVIDIA_API_KEY
from ..core.logger import logger, log_action


client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=NVIDIA_API_KEY
)


SYSTEM_PROMPT = """
You are a desktop automation AI.

Return ONLY valid JSON.

Never return markdown.
Never explain anything.

Available actions:
- open_app
- open_website
- type
- press
- wait
- click
- click_text
- done

JSON format:

{
  "actions": []
}

Examples:

{
  "actions":[
    {
      "action":"open_app",
      "app":"chrome"
    }
  ]
}

{
  "actions":[
    {
      "action":"click_text",
      "text":"Search chats"
    }
  ]
}
"""


def get_actions(user_input):
    """
    Call LLM to get next action(s).
    
    Args:
        user_input: Task description and context
        
    Returns:
        Dict with 'actions' key containing list of actions
    """
    
    logger.debug("Calling NVIDIA Qwen LLM for action planning...")
    
    try:
        response = client.chat.completions.create(
            model="qwen/qwen3-coder-480b-a35b-instruct",
            messages=[
                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },
                {
                    "role":"user",
                    "content":user_input
                }
            ],
            temperature=0.2,
            top_p=0.8,
            max_tokens=1024,
            timeout=30
        )

        text = response.choices[0].message.content.strip()
        logger.debug(f"LLM raw response: {text[:100]}...")

        # Clean up response
        text = (
            text
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        logger.debug(f"Cleaned response: {text[:100]}...")
        
        # Parse JSON
        result = json.loads(text)
        
        logger.info(f"LLM returned {len(result.get('actions', []))} action(s)")
        
        if result.get("actions"):
            first_action = result["actions"][0]
            logger.info(f"First action: {first_action.get('action', 'unknown')}")
        
        return result
    
    except json.JSONDecodeError as e:
        logger.error(f"LLM returned invalid JSON: {e}")
        logger.error(f"Response was: {text}")
        # Return safe fallback
        return {"actions": [{"action": "wait", "seconds": 2}]}
    
    except Exception as e:
        logger.error(f"LLM API error: {e}", exc_info=True)
        # Return safe fallback
        return {"actions": [{"action": "wait", "seconds": 2}]}