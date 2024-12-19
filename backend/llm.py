import google.generativeai as genai
import database as db
from json_prompts import prompt_template_from_json, parse_json_choice_prompt


# Read the Google API key from a file
def read_google_api_key(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read().strip()


GOOGLE_API_KEY = read_google_api_key("google_api_key.txt")


async def configure_llm(system_instructions: str):
    """
    Configure and initialize the Gemini LLM model.

    Args:
        system_instructions (str, optional): System instructions for the model.

    Returns:
        GenerativeModel: Configured Gemini model instance.
    """

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(
        model_name="models/gemini-1.5-flash", system_instruction=system_instructions
    )
    return model


async def story_from_themes(theme: str, user_id: int, story_id: int) -> list:
    """
    Generate a story from a prompt using the Gemini 1.5 Flash model.
    """
    # Load prompts
    system_prompt_template = prompt_template_from_json("danish_story_writer")
    story_prompt_template = prompt_template_from_json("initial_story_prompt")

    # Get system instructions and format story prompt
    system_instructions = system_prompt_template.template
    story_prompt = story_prompt_template.format(theme=theme)

    # Start chat
    model = await configure_llm(system_instructions=system_instructions)
    gemini_chat = model.start_chat()
    response = gemini_chat.send_message(story_prompt)

    # Save to database
    db.insert_chat_history(user_id, story_id, "user", story_prompt)
    db.insert_chat_history(user_id, story_id, "model", response.text)

    return [story_prompt, response.text]


async def continue_story(prompt: str, user_id: int, story_id: int) -> list:
    """
    Continue an existing chat conversation with the LLM.
    """
    # Load prompts
    system_prompt_template = prompt_template_from_json("danish_story_writer")
    system_instructions = system_prompt_template.template

    # Get chat history
    chat_history = db.get_formatted_chat_history(user_id, story_id)

    # Get next response
    prompt_and_response = await chat_with_llm(prompt, system_instructions, chat_history)

    # Save chat history
    db.insert_chat_history(user_id, story_id, "user", prompt)
    db.insert_chat_history(user_id, story_id, "model", prompt_and_response[1])

    return prompt_and_response


async def chat_with_llm(
    prompt: str,
    system_instructions: str,
    chat_history: list = None,
) -> str:
    """
    Chat with the LLM.
    """

    model = await configure_llm(system_instructions=system_instructions)
    if chat_history:
        formatted_history = chat_history
        gemini_chat = model.start_chat(history=formatted_history)
    else:
        gemini_chat = model.start_chat()

    response = gemini_chat.send_message(prompt)

    return [prompt, response.text]


async def get_three_options(user_id: int, story_id: int) -> str:
    """
    Get three options for the story.
    """

    # Load prompts
    system_prompt_template = prompt_template_from_json("danish_story_writer")
    three_options_prompt_template = prompt_template_from_json("three_options")
    system_instructions = system_prompt_template.template
    three_options_prompt = three_options_prompt_template.format()

    # Get chat history
    chat_history = db.get_formatted_chat_history(user_id, story_id)

    # Generate three options
    prompt_and_response = await chat_with_llm(
        three_options_prompt, system_instructions, chat_history
    )

    # Save chat history
    db.insert_chat_history(user_id, story_id, "user", three_options_prompt)
    db.insert_chat_history(user_id, story_id, "model", prompt_and_response[1])
    choice_list = parse_json_choice_prompt(prompt_and_response[1])
    print("Choice list", choice_list)
    return choice_list
