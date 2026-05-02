import os
import cv2
from interfaces.ivalidator import IValidator

class Validator(IValidator):
    def validate(self, file_path: str) -> bool:
        # Dosya uzantısı kontrolü
        if not file_path.lower().endswith(('.jpg', '.png')):
            return False

        # Dosya boyutu kontrolü (5MB'dan küçük mü?)
        if os.path.getsize(file_path) >= 5 * 1024 * 1024:
            return False

        # Görüntü boş mu kontrolü (OpenCV ile)
        image = cv2.imread(file_path)
        if image is None:
            return False

        return True