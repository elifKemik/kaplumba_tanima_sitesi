import os
import numpy as np
from ultralytics import YOLO
from sklearn.metrics.pairwise import cosine_similarity
from config import Config
from interfaces.imodel import IModel
from agents.base_agent import BaseAgent
from agents.prediction_validator import PredictionValidator

class YOLOModel(BaseAgent, IModel):
    def __init__(self, model_path=None, embeddings_path=None):
        # Config'den default değerleri al
        if model_path is None:
            model_path = Config.MODEL.MODEL_PATH
        if embeddings_path is None:
            embeddings_path = Config.MODEL.EMBEDDINGS_PATH
        
        # Eğitilmiş model varsa kullan
        trained_model = Config.MODEL.TRAINED_MODEL_PATH
        if os.path.exists(trained_model):
            self.model_path = trained_model
        else:
            self.model_path = model_path
        
        self.embeddings_path = embeddings_path
        self.model = YOLO(self.model_path)
        self.embeddings = {}
        self.labels = []
        self.threshold = Config.MODEL.YOLO_PREDICTION_THRESHOLD
        self._load_or_compute_embeddings()

    def get_name(self) -> str:
        """BaseAgent için - agent adı"""
        return "YOLOModel"
    
    def process(self, data: dict) -> dict:
        """Pipeline için process metodu"""
        file_path = data.get("file_path")
        quality_analysis = data.get("quality_analysis")
        prediction = self.predict(file_path, quality_analysis)
        data["prediction"] = prediction
        return data

    def _load_or_compute_embeddings(self):
        if os.path.exists(self.embeddings_path):
            self.embeddings = np.load(self.embeddings_path, allow_pickle=True).item()
        else:
            self._compute_embeddings()

    def _compute_embeddings(self):
        data_dir = "data"
        if not os.path.exists(data_dir):
            raise ValueError("Data klasörü bulunamadı.")

        self.labels = sorted(os.listdir(data_dir))
        for label in self.labels:
            folder_path = os.path.join(data_dir, label)
            embeddings = []
            for img_name in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img_name)
                results = self.model.predict(img_path, verbose=False)
                if results and len(results) > 0:
                    probs = results[0].probs.data.cpu().numpy()
                    embeddings.append(probs)
            if embeddings:
                self.embeddings[label] = np.mean(embeddings, axis=0)

        np.save(self.embeddings_path, self.embeddings)

    def predict(self, image_path: str, quality_analysis: dict | None = None) -> dict:
        # quality_analysis'i kullanmıyorsan ignore et
        results = self.model.predict(image_path, verbose=False)
        if not results or len(results) == 0:
            return PredictionValidator.format_result("unknown", 0.0, is_registered=True)

        probs = results[0].probs.data.cpu().numpy()
        predicted_class_idx = np.argmax(probs)
        confidence = probs[predicted_class_idx]

        if hasattr(results[0], 'names'):
            predicted_label = results[0].names[predicted_class_idx]
        else:
            predicted_label = self.labels[predicted_class_idx] if predicted_class_idx < len(self.labels) else "unknown"

        # t50 -> t050 formatına çevir
        if predicted_label.startswith("t") and len(predicted_label) == 3:
            predicted_label = f"t{int(predicted_label[1:]):03d}"

        return PredictionValidator.format_result(predicted_label, float(confidence), is_registered=True)