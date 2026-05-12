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
        max_tokens=1024
    )

    text = response.choices[0].message.content.strip()

    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(text)