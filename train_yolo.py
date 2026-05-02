from ultralytics import YOLO
import os

def train_yolo():
    # Veri seti klasörü
    data_dir = "data"
    if not os.path.exists(data_dir):
        raise ValueError("Data klasörü bulunamadı.")

    # Model yükle ve eğit (data klasörü doğrudan kullan)
    model = YOLO('yolov8n-cls.pt')
    model.train(data='./data/', epochs=30, imgsz=224, batch=16)

    # Eğitilmiş modeli kaydet
    model.save('yolo_trained.pt')
    print("YOLO eğitimi tamamlandı.")

if __name__ == "__main__":
    train_yolo()