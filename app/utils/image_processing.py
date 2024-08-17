import base64
from io import BytesIO
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def decode_base64_image(base64_string):
    try:
        # Remove the "data:image/png;base64," part if it exists
        if 'base64,' in base64_string:
            base64_string = base64_string.split('base64,')[1]
        
        image_data = base64.b64decode(base64_string)
        logger.info(f"Decoded image data length: {len(image_data)}")
        
        image = Image.open(BytesIO(image_data))
        logger.info(f"Image opened successfully. Format: {image.format}, Size: {image.size}, Mode: {image.mode}")
        return image
    except Exception as e:
        logger.error(f"Error decoding base64 image: {str(e)}")
        logger.error(f"First 100 characters of base64 string: {base64_string[:100]}")
        raise

def encode_image_to_base64(image: Image.Image) -> str:
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")