import base64
from typing import Union

def encode_image_to_base64(image_content: Union[bytes, str]) -> str:
    """Convierte bytes de imagen a una cadena base64."""
    if not image_content:
        return ""
    
    if isinstance(image_content, str):
        return image_content
        
    return base64.b64encode(image_content).decode('utf-8')
