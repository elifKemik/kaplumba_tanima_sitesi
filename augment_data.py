import os
import cv2
import numpy as np
from albumentations import (
    Compose, Rotate, RandomBrightnessContrast, GaussNoise, HorizontalFlip, RandomScale
)

# 3. Data Augmentation
def augment_data():
    data_dir = "data"
    augmented_dir = "augmented"
    os.makedirs(augmented_dir, exist_ok=True)

    # Augmentation pipeline
    transform = Compose([
        Rotate(limit=20, p=0.5),  # ±20°
        RandomScale(scale_limit=0.2, p=0.5),  # zoom 0.8-1.2
        RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.5),  # brightness 0.7-1.3
        HorizontalFlip(p=0.5),
        GaussNoise(var_limit=(10, 50), p=0.5)  # gaussian noise
    ])

    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if os.path.isdir(folder_path):
            aug_folder = os.path.join(augmented_dir, folder)
            os.makedirs(aug_folder, exist_ok=True)

            photos = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            for photo in photos:
                img_path = os.path.join(folder_path, photo)
                img = cv2.imread(img_path)
                if img is None:
                    continue

                # Orijinal kaydet
                cv2.imwrite(os.path.join(aug_folder, photo), img)

                # 10-20 varyasyon üret
                for i in range(15):  # ortalama 15
                    augmented = transform(image=img)['image']
                    aug_name = f"{os.path.splitext(photo)[0]}_aug_{i}.jpg"
                    cv2.imwrite(os.path.join(aug_folder, aug_name), augmented)

    print("Data augmentation tamamlandı.")

if __name__ == "__main__":
    augment_data()