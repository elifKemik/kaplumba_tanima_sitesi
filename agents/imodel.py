from abc import ABC, abstractmethod

class IModel(ABC):
    @abstractmethod
    def predict(self, image_path: str, quality_analysis: dict | None = None) -> dict:
        pass