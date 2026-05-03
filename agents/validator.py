import os
import cv2
from config import Config  # 🔥 EKLENDI
from interfaces.ivalidator import IValidator
from agents.base_agent import BaseAgent

class Validator(BaseAgent, IValidator):
    def get_name(self) -> str:
        return "Validator"
    
    def process(self, data: dict) -> dict:
        """Pipeline için process metodu"""
        file_path = data.get("file_path")
        is_valid = self.validate(file_path)
        data["validation"] = {"success": is_valid}
        if not is_valid:
            data["stop"] = True
            data["error"] = "Geçersiz dosya"
        return data
    
    def validate(self, file_path: str) -> bool:
        # Dosya uzantısı kontrolü (Config'den al)
        if not file_path.lower().endswith(Config.VALIDATION.ALLOWED_EXTENSIONS):
            return False

        # Dosya boyutu kontrolü (Config'den al)
        if os.path.getsize(file_path) >= Config.VALIDATION.MAX_FILE_SIZE:
            return False

        # Görüntü boş mu kontrolü (OpenCV ile)
        image = cv2.imread(file_path)
        if image is None:
            return False

        return True