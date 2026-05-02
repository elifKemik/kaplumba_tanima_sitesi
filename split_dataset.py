import os
import shutil
from sklearn.model_selection import train_test_split
import pandas as pd

# 2. Eğitim/Test Ayrımı (DOĞRU ŞEKİLDE)
def split_dataset():
    data_dir = "data"
    train_dir = "data_train"
    test_dir = "data_test"

    # Klasörleri oluştur
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Veri toplama
    data = []
    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        if os.path.isdir(folder_path):
            photos = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            for photo in photos:
                data.append((photo, folder))

    df = pd.DataFrame(data, columns=['path', 'label'])

    # Stratified split: her sınıftan %80 eğitim, %20 test
    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['label'], random_state=42)

    # Her sınıftan test setine en az 1 fotoğraf gitmeli (stratify garantiler)
    print("Eğitim seti sınıf dağılımı:")
    print(train_df['label'].value_counts())
    print("Test seti sınıf dağılımı:")
    print(test_df['label'].value_counts())

    # Dosyaları kopyala
    for _, row in train_df.iterrows():
        label = row['label']
        src = row['path']
        dst_dir = os.path.join(train_dir, label)
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy(src, dst_dir)

    for _, row in test_df.iterrows():
        label = row['label']
        src = row['path']
        dst_dir = os.path.join(test_dir, label)
        os.makedirs(dst_dir, exist_ok=True)
        shutil.copy(src, dst_dir)

    print("Eğitim/Test ayrımı tamamlandı.")

if __name__ == "__main__":
    split_dataset()