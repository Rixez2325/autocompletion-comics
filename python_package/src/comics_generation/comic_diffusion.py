import json
import os
from diffusers import DiffusionPipeline
from PIL.Image import Image
from helpers.aws_helper import load_json_from_s3, save_images_to_s3
from helpers.path_helper import GENERATED_PANELS_DIR, GENERATED_PROMPS_DIR
from typing import Dict, List

COMIC_DIFFUSION_REPOSITORY = "assets/Comic-Diffusion"
ARTSTYLE = ", pepelarraz artstyle"


def diffusion_demo():
    pipeline = init_pipeline(COMIC_DIFFUSION_REPOSITORY)
    prompt_1 = "Superman hovering above Gotham skyline, Batman standing on rooftop, both exchanging intense glances"
    prompt_2 = "Batman throwing a batarang at Superman, while Superman deflects it with his heat vision, sending the batarang back at Batman"
    prompt_3 = "Batman and Superman standing face to face, with Batman holding a piece of kryptonite and Superman weakened on the ground"
    prompt_4 = "Batman and Superman shaking hands in front of the Justice League headquarters, with other superheroes in the background, ready to fight any impending threat"

    images = []
    images.append(generate_image(pipeline, prompt_1))
    images.append(generate_image(pipeline, prompt_2))
    images.append(generate_image(pipeline, prompt_3))
    images.append(generate_image(pipeline, prompt_4))
    save_images_local(images)


def generate_images():
    pipeline = init_pipeline(COMIC_DIFFUSION_REPOSITORY)
    prompts = get_prompts_from_s3()
    # images = [generate_image(pipeline, prompt) for prompt in prompts]
    # save_images_to_s3(images, GENERATED_PANELS_DIR)


def generate_image(pipeline: DiffusionPipeline, prompt) -> Image:
    kwargs = format_prompt(
        prompt,
        num_inference_steps=1,
        guidance_scale=1,
    )
    output = pipeline(**kwargs)

    return output.images[0]


def format_prompt(
    prompt,
    width: int = 368 * 2,
    height: int = 544 * 2,
    num_images_per_prompt: int = 1,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
) -> Dict:
    return {
        "prompt": prompt + ARTSTYLE,
        "height": height,
        "width": width,
        "num_inference_steps": num_inference_steps,  # More denoising steps usually lead to a higher quality image
        "negative_prompt": "cloning, clones, same face",
        "num_images_per_prompt": num_images_per_prompt,
        # "generator": ,   # torch.generator("cuda") tu use for GPU
        # "output_type": , # can be PIL.Image or np.array
        "guidance_scale": guidance_scale,  # Higher guidance scale encourages to generate images that are closely linked to the text prompt
    }


def save_images_local(images: list[Image]):
    for i, image in enumerate(images):
        with open(f"{GENERATED_PANELS_DIR}/image_{i}.png", "w") as f:
            image.save(f, format="PNG")


def init_pipeline(pretrained_model_name_or_path=COMIC_DIFFUSION_REPOSITORY):
    return DiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        safety_checker=None,
        local_files_only=True,
    )


def get_prompts_from_s3() -> List:
    prompts_files = load_json_from_s3(GENERATED_PROMPS_DIR)
    return [file["prompt"] for file in prompts_files]
