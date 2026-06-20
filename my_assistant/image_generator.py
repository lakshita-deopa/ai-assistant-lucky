import torch
from diffusers import StableDiffusionPipeline
import base64
from io import BytesIO

class ImageGenerator:
    def __init__(self):
        self.pipe = None

    def load_model(self):
        if self.pipe is None:
            print("Loading image model from local folder...")
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "./sd_model",
                torch_dtype=torch.float16,
                safety_checker=None
            )
            self.pipe = self.pipe.to("cuda")
            self.pipe.enable_attention_slicing()
            print("Image model loaded!")

    def generate(self, prompt: str) -> str:
        self.load_model()
        print(f"Generating image for: {prompt}")
        image = self.pipe(
            prompt,
            num_inference_steps=35,
            height=512,
            width=512
        ).images[0]
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return img_str