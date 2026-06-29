from ollama import chat
from ollama import ChatResponse

TOOLS = ["open_app", "close_app", "search_browser"]

def llm_process(command):
    schema = {
        "type": "object",
        "properties": {
            "app": {
                "type": "string"
            },
            "action": {
                "type": "string"
            },
            "speech": {
                "type": "string"
            }
        },
        "required": ["app", "action", "speech"]
    }

    response: ChatResponse = chat(model="gemma3", messages=[
        {
            "role": "system",
            "content": """

    You are an AI that extracts application names.

    Return ONLY a JSON object.

    In the JSON object, make sure to return what the user is trying to do with the application (open or close)

    You are also an AI Agent, so you have to say something like 'opening spotify' or whatever the application is make sure to include it in the JSON object

    Examples:

    {
    "app": "Google Chrome",
    "action": "close",
    "speech": "Closing Google Chrome"
    }
    {
    "app: "Spotify",
    "action": "open",
    "speech": "Opening spotify"
    }

    If no application is mentioned:

    {
    "app": null,
    "action": null,
    "speech:" "No application found"
    }


    """
        },
        {
            "role": "user",
            "content": command
        }
    ],
    format=schema
    )
    return response.message.content