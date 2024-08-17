from abc import ABC, abstractmethod
from PIL import Image

class ModelInterface(ABC):
    @abstractmethod
    def generate_alt_text(self, image: Image.Image, prompt: str) -> str:
        pass