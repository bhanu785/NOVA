from ollama import chat
from ollama import ChatResponse
from tools import create_tool

# processes user command with ollama qwen3:8b model and returns tool calls
def llm_process(command: str) -> list:
    # all tools and descriptions from tools.py
    tool = [
        create_tool(
            "open_app",
            "Opens a Mac application",
            {

            "app": {

                "type": "string",

                "description": "The application to open (MUST BE A VALID MAC APPLICATION NAME)."

            }

            },
            ["app"]
        ),
        create_tool(
            "close_app",
            "Closes a Mac application",
            {

            "app": {

                "type": "string",

                "description": "The application to close (MUST BE A VALID MAC APPLICATION NAME)."

            }

            },
            ["app"]
        ),
        # create_tool(
        #     "search_browser",
        #     "Searches the browser based on user query",
        #     {

        #     "query": {

        #         "type": "string",

        #         "description": "URL that should be searched up"

        #     }

        #     },
        #     ["query"]
        # ),
        create_tool(
            "speak",
            "speaks text using Piper TTS",
            {

            "text": {

                "type": "string",

                "description": "What should be said by the LLM"

            }

            },
            ["text"]
        ),
        create_tool(
            "type",
            "types text",
            {

            "text": {

                "type": "string",

                "description": "What text should be typed"

            },
            "duration": {
                "type": "float",
                "description": "How long the duration between characters should be"
            }

            },
            ["text"]
        ),
        create_tool(
            "use_shortcut",
            "performs a MacOS hotkey shortcut",
            {

            "args": {

                "type": "list",

                "description": "The keys required to perform a MAC shortcut IN ORDER"

            }

            },
            ["args"]
        ),
        # create_tool(
        #     "get_all_window_info",
        #     "gets information about every open window and application on the system",
        #     {}
        # ),
        # create_tool(
        #     "focus_app",
        #     "Brings an app into focus based on its name, and if the window is a browser, its url (USE ONLY INFORMATION FROM get_all_window_info)",
        #     {

        #     "app_name": {

        #         "type": "string",

        #         "description": "The app that the user wants to bring to focus"

        #     },
        #     "url": {
        #         "type": "string",

        #         "description": "The URL of the tab the specific browser window has open (USE ONLY INFORMATION FROM get_all_window_info)"
        #     }

        #     },
        #     ["app_name"]
        # ),
        create_tool(
            "control_volume",
            "Can change the volume of the system",
            {

            "desired_volume": {

                "type": "string",

                "description": "The desired volume the user wants the system to be at"

            }

            },
            ["desired_volume"]
        ),
        create_tool(
            "make_file",
            "makes custom file",
            {

            "name": {

                "type": "string",

                "description": "name of the file"

            },

            "contents": {
                "type": "string",

                "description": "the contents of the file"
            }

            },
            ["name", "contents"]
        )

    ]
    
    messages =  [{
            "role": "system",
            "content": """

            You are NOVA, an AI assistant for macOS.

            Use the available tools to complete the user's request(Call him SIR ALL THE TIME).

            Call only the tools that are necessary (USE THE SPEAK TOOL FOR ALL REQUESTS, you're an AI agent).

            Never invent tool arguments.

            Choose the correct tool(s) as QUICKLY AS POSSIBLE.

            If information is missing, use another tool or ask the user.

            If the user only wants information, use the speak tool.

            Respond only with tool calls.


            """
    },
    {
        "role": "user",
        "content": command
    }]

    response: ChatResponse = chat(
    model="qwen3:8b", 
    messages=messages,
    tools=tool,
    think=False
    )

    return response.message.tool_calls
