import os
import hashlib
from collections import defaultdict

# 1. Veri Seti Doğrulama ve Etiket Kontrolü
def verify_dataset():
    data_dir = "data"
    expected_folders = [f"t{i:03d}" for i in range(1, 51)]  # T001 to T050
    existing_folders = [f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))]
    missing_folders = [f for f in expected_folders if f not in existing_folders]

    print("Eksik klasörler:", missing_folders)

    # Her sınıfta kaç fotoğraf var?
    photo_counts = {}
    for folder in existing_folders:
        folder_path = os.path.join(data_dir, folder)
        photos = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        photo_counts[folder] = len(photos)
        print(f"{folder}: {len(photos)} fotoğraf")

    # Aynı fotoğrafın farklı klasörlerde olup olmadığını kontrol et (hash karşılaştırması)
    hash_to_folders = defaultdict(list)
    for folder in existing_folders:
        folder_path = os.path.join(data_dir, folder)
        for photo in os.listdir(folder_path):
            if photo.lower().endswith(('.jpg', '.jpeg', '.png')):
                photo_path = os.path.join(folder_path, photo)
                with open(photo_path, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                hash_to_folders[file_hash].append((folder, photo))

    duplicates = {h: locs for h, locs in hash_to_folders.items() if len(locs) > 1}
    if duplicates:
        print("Yinelenen fotoğraflar bulundu:")
        for h, locs in duplicates.items():
            print(f"Hash {h}: {locs}")
    else:
        print("Yinelenen fotoğraf yok.")

if __name__ == "__main__":
    verify_dataset()