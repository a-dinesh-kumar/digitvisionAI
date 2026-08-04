import os
import re
import io
import base64
import uuid
from typing import Tuple
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename: str) -> bool:
    """Checks if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def decode_base64_image(base64_data: str) -> Image.Image:
    """
    Decodes a base64 encoded image string (e.g. from HTML5 canvas) into a PIL Image.
    
    Args:
        base64_data: Raw or data-URI base64 string
        
    Returns:
        PIL.Image.Image object
    """
    if not base64_data:
        raise ValueError("Empty image data provided.")
        
    # Remove header if present (e.g. 'data:image/png;base64,')
    if ',' in base64_data:
        base64_data = base64_data.split(',', 1)[1]
        
    # Remove invalid characters
    base64_data = re.sub(r'[^A-Za-z0-9+/=]', '', base64_data)
    
    image_bytes = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_bytes))
    return image

def save_upload(file_storage: FileStorage) -> Tuple[str, str]:
    """
    Saves an uploaded Werkzeug FileStorage file to the uploads directory with a safe UUID prefix.
    
    Returns:
        Tuple of (original_filename, saved_file_path)
    """
    filename = secure_filename(file_storage.filename or '')
    if not filename:
        filename = f"upload_{uuid.uuid4().hex[:8]}.png"
        
    unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    file_storage.save(file_path)
    return filename, file_path
