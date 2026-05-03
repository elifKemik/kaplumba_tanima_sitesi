from abc import ABC, abstractmethod
from typing import Optional

class IModel(ABC):
    @abstractmethod
    def predict(self, image_path: str, quality_analysis: Optional[dict] = None) -> dict:
        """Kaplumbağa tahmini yapar
        
        Args:
            image_path: Fotoğraf yolu
            quality_analysis: Researcher'dan gelen kalite analizi (opsiyonel)
        
        Returns:
            dict: Tahmin sonucu (id, accuracy, status)
        """
        pass