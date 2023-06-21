import openai
import os
from dotenv import load_dotenv
from textwrap import dedent

GPT_MODEL = "gpt-3.5-turbo"

load_dotenv("./api_key.env")
openai.api_key = os.getenv("OPENAI_API_KEY")


def ask_gpt(
    nb_panels_to_generate: int,
    previous_panels_description: list[dict],
) -> list[dict]:
    messages = set_message(nb_panels_to_generate, previous_panels_description)
    response = openai.ChatCompletion.create(model=GPT_MODEL, messages=messages)
    new_prompts = extract_panels_prompts(response)
    return new_prompts


def extract_panels_prompts(response: dict) -> list[dict]:
    prompts_str = response["choices"][0]["message"]["content"]
    prompts_list = split_prompts_str(prompts_str)
    return prompts_list


def split_prompts_str(prompts_str: str) -> list[dict]:
    prompts = prompts_str.split("\n\n")
    result = []
    for prompt in prompts:
        tmp = prompt.split("\n")[1:]
        dict = {}
        dict["prompt"] = f"{tmp[0].split(':')[1]} {tmp[1].split(':')[1]}"
        dict["text"] = tmp[2].split(":")[1]
        result.append(dict)

    return result


def format_panels_description(previous_panels_description: list[dict]):
    result = ""

    for i, panel in enumerate(previous_panels_description):
        result += dedent(
            f"""
            panel {i+1}:
            characters: {', '.join(panel['characters'])}
            visual_context: {panel["visual_context"]}
            text: {', '.join(panel["text"])}"""
        )

    return result


def set_message(
    nb_panels_to_generate: int,
    previous_panels_description: list[dict],
):
    return [
        {
            "role": "system",
            "content": dedent(
                """
                    You are a comics writer, 
                    when you write a panel you have to describe it as following: 
                    give principals characters, the action performed, and visual context. 
                    A panel need to be a single sentences.
                    exemple: batman talking to spiderman on a roof, nightsky, city in background"""
            ),
        },
        {
            "role": "user",
            "content": dedent(
                f"""
                    Here are a description of a comics page, panels by panels:
                    {format_panels_description(previous_panels_description)}
                    Write {nb_panels_to_generate} panels that follow this story."""
            ),
        },
    ]


def demo():
    demo_description = [
        {
            "characters": ["batman", "superman"],
            "visual_context": "on a rooof, city in background, nightsky",
            "text": ["I'm the boss", "No I am !"],
        },
        {
            "characters": ["batman", "superman"],
            "visual_context": "on the streets",
            "text": ["You dead bro"],
        },
    ]

    prompt_str_demo = "Panel 3:\ncharacters: batman, superman, the Joker\nvisual_context: in an alley, dimly lit by a street lamp\ntext: We have a common enemy, Joker. Let's take him down.\n\nPanel 4:\ncharacters: batman, superman, the Joker\nvisual_context: Mid-battle in a cluttered warehouse\ntext: We won't let you hurt anyone else, Joker.\n\nPanel 5:\ncharacters: batman, superman, the Joker\nvisual_context: In the aftermath of the battle, with the Joker lying defeated\ntext: We make a good team, Superman.\n\nPanel 6:\ncharacters: batman, superman\nvisual_context: back on the roof where they started, watching the sunrise over the city\ntext: Maybe next time we can avoid the Joker's traps."

    generated_prompts = ask_gpt(4, demo_description)

    print(generated_prompts)
