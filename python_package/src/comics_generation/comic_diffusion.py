from diffusers import DiffusionPipeline
from PIL.Image import Image

COMIC_DIFFUSION_REPOSITORY = "assets/Comic-Diffusion"
GENERATED_IMAGE_DIR = "datasets/generated_panels"
ARTSTYLE = ", pepelarraz artstyle"


def generate_images(pipeline: DiffusionPipeline, prompt: str) -> list[Image]:
    kwargs = format_prompt(prompt, num_inference_steps=1, guidance_scale=1)
    output = pipeline(**kwargs)

    return output.images


def format_prompt(
    prompt: str,
    num_images_per_prompt: int = 1,
    num_inference_steps: int = 50,
    guidance_scale: float = 7.5,
) -> dict:
    return {
        "prompt": prompt + ARTSTYLE,
        # "height": ,
        # "width": ,
        "num_inference_steps": num_inference_steps,  # More denoising steps usually lead to a higher quality image
        # "negative_prompt": ,
        "num_images_per_prompt": num_images_per_prompt,
        # "generator": ,   # torch.generator("cuda") tu use for GPU
        # "output_type": , # can be PIL.Image or np.array
        # "return_dict": True,  # boolean, to test
        "guidance_scale": guidance_scale,  # Higher guidance scale encourages to generate images that are closely linked to the text prompt
    }


def save_images(images: list[Image]):
    for i, image in enumerate(images):
        with open(f"{GENERATED_IMAGE_DIR}/image_{i}.jpeg", "w") as f:
            image.save(f, format="JPEG")


def init_pipeline(pretrained_model_name_or_path: str = COMIC_DIFFUSION_REPOSITORY):
    return DiffusionPipeline.from_pretrained(
        pretrained_model_name_or_path=pretrained_model_name_or_path,
        safety_checker=None,
        local_files_only=True,
    )


pipeline = init_pipeline(COMIC_DIFFUSION_REPOSITORY)
prompt = "batman on a roof, nightsky, city in background"
images = generate_images(pipeline, prompt)
save_images(images)
