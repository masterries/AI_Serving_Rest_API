import torch
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
from models.model_interface import ModelInterface
from utils.config import settings
import logging
import os

logger = logging.getLogger(__name__)

class BLIPBase(ModelInterface):
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = "Salesforce/blip-image-captioning-base"
        
        # Check if the model is already downloaded
        if not os.path.exists(settings.BLIP_MODEL_PATH):
            logger.info(f"BLIP model not found at {settings.BLIP_MODEL_PATH}. Downloading...")
            self.download_model()
        
        logger.info(f"Loading BLIP model from {settings.BLIP_MODEL_PATH}")
        self.processor = BlipProcessor.from_pretrained(settings.BLIP_MODEL_PATH)
        self.model = BlipForConditionalGeneration.from_pretrained(settings.BLIP_MODEL_PATH).to(self.device)
        logger.info("BLIP model loaded successfully")

    def download_model(self):
        try:
            # This will download and cache the model
            processor = BlipProcessor.from_pretrained(self.model_name)
            model = BlipForConditionalGeneration.from_pretrained(self.model_name)
            
            # Save the model to the specified path
            os.makedirs(settings.BLIP_MODEL_PATH, exist_ok=True)
            processor.save_pretrained(settings.BLIP_MODEL_PATH)
            model.save_pretrained(settings.BLIP_MODEL_PATH)
            
            logger.info(f"BLIP model downloaded and saved to {settings.BLIP_MODEL_PATH}")
        except Exception as e:
            logger.error(f"Error downloading BLIP model: {str(e)}")
            raise

    def generate_alt_text(self, image: Image.Image, prompt: str) -> str:
        prompt = ""
        try:
            logger.info(f"Generating alt text for image size: {image.size}")
            inputs = self.processor(image, prompt, return_tensors="pt").to(self.device)
            logger.info("Processed image with BLIP processor")
            output = self.model.generate(**inputs)
            logger.info("Generated output from BLIP model")
            return self.processor.decode(output[0], skip_special_tokens=True)
        except Exception as e:
            logger.error(f"Error in generate_alt_text: {str(e)}", exc_info=True)
            raise