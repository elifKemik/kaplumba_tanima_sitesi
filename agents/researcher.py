import cv2
import numpy as np
from interfaces.iresearcher import IResearcher
from agents.base_agent import BaseAgent

class Researcher(BaseAgent, IResearcher):
    def get_name(self) -> str:
        return "Researcher"
    
    def process(self, data: dict) -> dict:
        """Pipeline için process metodu"""
        file_path = data.get("file_path")
        analysis = self.analyze(file_path)
        data["quality_analysis"] = analysis
        
        if analysis.get("status") == "fail":
            data["stop"] = True
            data["error"] = analysis.get("message")
        
        return data
    
    def analyze(self, file_path: str) -> dict:
        image = cv2.imread(file_path)
        if image is None:
            return {"status": "fail", "brightness": None, "sharpness": None, "message": "Görüntü yüklenemedi"}

        # Parlaklık analizi: Görüntünün ortalama piksel değeri
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = gray.mean()

        # Netlik analizi: Laplacian varyansı
        sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

        status = "success"
        message = "Analiz tamamlandı"

        # Parlaklık kontrolü
        if brightness < 50:
            status = "fail"
            message = "Çok karanlık görsel"
        elif brightness > 220:
            status = "fail"
            message = "Çok parlak görsel"

        # Netlik kontrolü
        if sharpness < 0.5:
            status = "fail"
            message = "Resim tamamen boş veya okunamaz"
        elif sharpness < 2:
            if status == "success":
                status = "warning"
                message = "Görüntü kalitesi düşük ancak işleme devam ediliyor"
            else:
                message += " ve görüntü kalitesi düşük ancak işleme devam ediliyor"
        elif sharpness < 10:
            if status == "success":
                status = "warning"
                message = "Düşük kalite, yine de devam ediliyor"
            else:
                message += " ve düşük kalite, yine de devam ediliyor"

        return {"status": status, "brightness": brightness, "sharpness": sharpness, "message": message}