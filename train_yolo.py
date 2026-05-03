from ultralytics import YOLO
from config import Config
import os

def train_yolo():
    # Veri seti klasörü
    data_dir = "data"
    if not os.path.exists(data_dir):
        raise ValueError("Data klasörü bulunamadı.")

    # Model yükle ve eğit (data klasörü doğrudan kullan)
    model = YOLO(Config.MODEL.MODEL_PATH)
    model.train(
        data='./data/',
        epochs=Config.MODEL.EPOCHS,
        imgsz=Config.MODEL.IMG_SIZE,
        batch=Config.MODEL.BATCH_SIZE
    )

    # Eğitilmiş modeli kaydet
    model.save(Config.MODEL.TRAINED_MODEL_PATH)
    print("YOLO eğitimi tamamlandı.")

if __name__ == "__main__":
    train_yolo()