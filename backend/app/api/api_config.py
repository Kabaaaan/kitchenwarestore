from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / 'static'
IMAGES_DIR = STATIC_DIR / 'images'
PLACEHOLDER_PATH = IMAGES_DIR / 'placeholder.png'
IMAGE_EXTENSIONS = [".jpg",".jpeg",".png",]

ACCESS_DENIED_MESSAGE = "Access denied: You do not have permission to perform this action."