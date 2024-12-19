import json
from langchain.prompts import PromptTemplate


def prompt_template_from_json(prompt_name: str):
    with open(f"prompts/{prompt_name}.json", "r") as f:
        story_prompt_dict = json.load(f)

    # Recreate the PromptTemplate object
    story_prompt_template = PromptTemplate(
        input_variables=story_prompt_dict["input_variables"],
        template=story_prompt_dict["template"],
    )

    return story_prompt_template


def parse_json_choice_prompt(json_string: str):
    # Parse the JSON string
    print("JSON string", json_string)
    parsed_data = json.loads(json_string)
    print("Parsed data", parsed_data)

    # Access the choices

    choices = parsed_data["choices"]

    string_choices = list()
    for choice in choices:
        string_choices.append(choice["text"])

    return string_choices
