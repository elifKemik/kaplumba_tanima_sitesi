import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import cosine_similarity
from agents.imodel import IModel

# 4. Model Pipeline (ÇÖZÜM ODAKLI)
class CNNModel(IModel):
    def __init__(self, model_path="turtle_model.h5", embeddings_path="embeddings.npy"):
        self.model_path = model_path
        self.embeddings_path = embeddings_path
        self.model = None
        self.embeddings = {}  # {label: avg_embedding}
        self.labels = []
        self._load_or_train_model()

    def _load_or_train_model(self):
        if os.path.exists(self.model_path):
            self.model = tf.keras.models.load_model(self.model_path)
            if os.path.exists(self.embeddings_path):
                self.embeddings = np.load(self.embeddings_path, allow_pickle=True).item()
        else:
            self._train_model()

    def _train_model(self):
        # ResNet50 ile transfer learning
        base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        x = GlobalAveragePooling2D()(base_model.output)
        x = Dense(512, activation='relu')(x)  # Embedding layer
        model = Model(inputs=base_model.input, outputs=x)

        # Freeze base layers
        for layer in base_model.layers:
            layer.trainable = False

        # Eğitim verisi
        train_dir = "augmented"  # Augmented data kullan
        if not os.path.exists(train_dir):
            raise ValueError("Augmented data bulunamadı.")

        train_ds = tf.keras.utils.image_dataset_from_directory(
            train_dir,
            image_size=(224, 224),
            batch_size=32,
            label_mode='int'
        )

        # Compile
        model.compile(optimizer='adam', loss='mse')  # Dummy loss for embedding

        # Eğitim (basit, gerçekte daha iyi yap)
        model.fit(train_ds, epochs=10)

        self.model = model
        self._compute_embeddings(train_dir)
        self.model.save(self.model_path)
        np.save(self.embeddings_path, self.embeddings)

    def _compute_embeddings(self, data_dir):
        self.labels = sorted(os.listdir(data_dir))
        for label in self.labels:
            folder_path = os.path.join(data_dir, label)
            embeddings = []
            for img_name in os.listdir(folder_path):
                img_path = os.path.join(folder_path, img_name)
                img = tf.keras.utils.load_img(img_path, target_size=(224, 224))
                img_array = tf.keras.utils.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0)
                img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
                embedding = self.model.predict(img_array, verbose=0)
                embeddings.append(embedding.flatten())
            if embeddings:
                self.embeddings[label] = np.mean(embeddings, axis=0)

    def predict(self, image_path: str, quality_analysis: dict | None = None) -> dict:
        # Embedding hesapla
        img = tf.keras.utils.load_img(image_path, target_size=(224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = tf.keras.applications.resnet50.preprocess_input(img_array)
        embedding = self.model.predict(img_array, verbose=0).flatten()

        # Cosine similarity ile karşılaştır
        best_label = None
        best_score = -1
        for label, avg_emb in self.embeddings.items():
            score = cosine_similarity([embedding], [avg_emb])[0][0]
            if score > best_score:
                best_score = score
                best_label = label

        # 5. Eksik Sınıflar İçin Özel Mantık
        expected_labels = [f"t{i:03d}" for i in range(1, 51)]
        if best_label not in expected_labels:
            return {"id": "unknown", "accuracy": 0, "status": "not_registered", "message": "Bu kaplumbağa veri setinde kayıtlı değil"}

        # Threshold = 0.6
        if best_score >= 0.6:
            return {"id": best_label, "accuracy": round(best_score * 100, 2), "status": "identified"}
        else:
            return {"id": "unknown", "accuracy": round(best_score * 100, 2), "status": "not_identified"}