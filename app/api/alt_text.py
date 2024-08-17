from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models.blip_base import BLIPBase
from utils.image_processing import decode_base64_image
from .auth import get_api_key
import logging
from fastapi import Request
from pydantic import BaseModel
from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Request
from models.blip_base import BLIPBase
from utils.image_processing import decode_base64_image
import logging
import base64
from typing import Dict
import asyncio

logger = logging.getLogger(__name__)

router = APIRouter()
model = BLIPBase()



class ImageUrl(BaseModel):
    url: str
    detail: str = None

class Content(BaseModel):
    type: str
    text: str = None
    image_url: ImageUrl = None

class Message(BaseModel):
    role: str
    content: List[Content]

class AltTextRequest(BaseModel):
    model: str
    messages: List[Message]
    max_tokens: int



class AltTextResponse(BaseModel):
    choices: List[dict]

class AltTextResponse(BaseModel):
    choices: List[Dict[str, Dict[str, str]]]

async def generate_alt_text_with_timeout(image, prompt, timeout=30):
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(model.generate_alt_text, image, prompt),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Alt text generation timed out")

@router.post("/generate_alt_text", response_model=AltTextResponse)
async def generate_alt_text(request: AltTextRequest, api_key: str = Depends(get_api_key)):
    try:
        logger.info(f"Received request: {request}")

        # Extract image and prompt from the request
        content = request.messages[0].content
        prompt = next(item.text for item in content if item.type == 'text')
        image_url = next(item.image_url.url for item in content if item.type == 'image_url')

        logger.info(f"Extracted prompt: {prompt}")
        logger.info(f"Extracted image URL (first 100 chars): {image_url[:100]}")

        # Decode base64 image
        image = decode_base64_image(image_url)

        # Generate alt text
        alt_text = await generate_alt_text_with_timeout(image, prompt)

        # Format response to match OpenAI's format
        response = {
            "choices": [
                {
                    "message": {
                        "content": alt_text
                    }
                }
            ]
        }

        return response
    except Exception as e:
        logger.error(f"Error generating alt text: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error generating alt text: {str(e)}")