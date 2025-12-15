import torch
from diffusers import StableDiffusionPipeline

# Load the pre-trained Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(model_id)
pipe = pipe.to(device)

# Function to generate an image from a prompt
def generate_image(prompt, output_path):
    with torch.no_grad():
        image = pipe(prompt).images[0]
        image.save(output_path)

# Example usage
if __name__ == "__main__":
    prompt = "A fantasy landscape with mountains and a river"
    output_path = "output_image.png"
    generate_image(prompt, output_path)
    print(f"Image saved to {output_path}")