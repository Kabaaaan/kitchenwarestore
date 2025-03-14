import os
from PIL import Image

class PhotoManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def save_photo(self, photo, filename):
        """Сохраняет фотографию в указанной директории."""
        photo_path = os.path.join(self.base_dir, filename)
        photo.save(photo_path)
        return photo_path

    def load_photo(self, filename):
        """Загружает фотографию из указанной директории."""
        photo_path = os.path.join(self.base_dir, filename)
        if os.path.exists(photo_path):
            return Image.open(photo_path)
        else:
            raise FileNotFoundError(f"Файл {filename} не найден в директории {self.base_dir}")

    def list_photos(self):
        """Возвращает список всех фотографий в директории."""
        return [f for f in os.listdir(self.base_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]

    def resize_photo(self, filename, width, height):
        """Изменяет размер фотографии и сохраняет её."""
        photo = self.load_photo(filename)
        resized_photo = photo.resize((width, height))
        resized_filename = f"resized_{filename}"
        return self.save_photo(resized_photo, resized_filename)
