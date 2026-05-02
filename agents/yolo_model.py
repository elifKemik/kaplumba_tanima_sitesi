import os
import numpy as np
from ultralytics import YOLO
from sklearn.metrics.pairwise import cosine_similarity
from interfaces.imodel import IModel

class YOLOModel(IModel):
    def __init__(self, model_path="yolov8n-cls.pt", embeddings_path="yolo_embeddings.npy"):
        # Eğitilmiş model varsa kullan
        trained_model = "yolo_trained.pt"
        if os.path.exists(trained_model):
            self.model_path = trained_model
        else:
            self.model_path = model_path
        self.embeddings_path = embeddings_path
        self.model = YOLO(self.model_path)  # YOLOv8 classification model
        self.embeddings = {}  # {label: avg_embedding}
        self.labels = []
        self.threshold = 0.35  # Confidence threshold for identification
        self._load_or_compute_embeddings()

    def _load_or_compute_embeddings(self):
        if os.path.exists(self.embeddings_path):
            self.embeddings = np.load(self.embeddings_path, allow_pickle=True).item()
        else:
            self._compute_embeddings()

    def _compute_embeddings(self):
        # Veri setinden embedding hesapla (data/ kullan)
        data_dir = "data"
        if not os.path.exists(data_dir):
            raise ValueError("Data klasörü bulunamadı.")

        self.labels = sorted(os.listdir(data_dir))
        for label in self.labels:
            folder_path = os.path.join(data_dir, label)
            embeddings = []
            for img_name in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img_name)
                # YOLO ile predict, probabilities'i embedding olarak kullan
                results = self.model.predict(img_path, verbose=False)
                if results and len(results) > 0:
                    probs = results[0].probs.data.cpu().numpy()  # Probability vector
                    embeddings.append(probs)
            if embeddings:
                self.embeddings[label] = np.mean(embeddings, axis=0)

        np.save(self.embeddings_path, self.embeddings)

    def predict(self, image_path: str, quality_analysis: dict | None = None) -> dict:
        # YOLO ile predict
        results = self.model.predict(image_path, verbose=False)
        if not results or len(results) == 0:
            return {"id": "unknown", "accuracy": float(0), "status": "not_identified"}

        probs = results[0].probs.data.cpu().numpy()
        predicted_class_idx = np.argmax(probs)
        confidence = probs[predicted_class_idx]

        # Label map (YOLO'nun class names'ini kullan, ama bizim labels ile eşle)
        if hasattr(results[0], 'names'):
            predicted_label = results[0].names[predicted_class_idx]
        else:
            predicted_label = self.labels[predicted_class_idx] if predicted_class_idx < len(self.labels) else "unknown"

        # Eksik sınıflar kontrolü
        expected_labels = [f"t{i:03d}" for i in range(1, 51)]
        if predicted_label not in expected_labels:
            return {"id": "unknown", "accuracy": float(0), "status": "not_registered", "message": "Bu kaplumbağa veri setinde kayıtlı değil"}

        # Threshold kontrol
        if confidence >= self.threshold:
            return {"id": predicted_label, "accuracy": float(round(float(confidence) * 100, 2)), "status": "identified"}
        else:
            return {"id": "unknown", "accuracy": float(round(float(confidence) * 100, 2)), "status": "not_identified"}