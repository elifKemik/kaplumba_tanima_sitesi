# 🐢 Caretta Caretta Yüz Tanıma Sistemi

Kaplumbağaların yüzlerindeki benzersiz leke desenlerini kullanarak onları birbirinden ayırt eden bir yapay zeka sistemi.

## 📌 Proje Hakkında

Her insanın parmak izi gibi, her kaplumbağanın yüzü de farklıdır. Bu proje, kaplumbağaların yüz fotoğraflarından hangi kaplumbağa olduğunu tespit eder.

**Sistemin başarısı fotoğraf kalitesine çok bağlı.**  
- Kaliteli fotoğraflarda **%70+** doğruluk  
- Düşük kaliteli fotoğraflarda **%20-30** doğruluk  
- Hedef **%60** → kaliteli fotoğraflarda hedef aşılıyor

---

## 🏗️ Proje Yapısı (Multi-Agent Mimarisi)

| Agent | Görevi |
|-------|--------|
| **Validator** | Dosyayı kontrol eder (uzantı, boyut) |
| **Researcher** | Fotoğraf kalitesini analiz eder (parlaklık, netlik) |
| **YOLOModel** | Kaplumbağayı tanır |
| **TurtleService** | Tüm agent'ları yönetir (Orchestrator) |

---

## 🚀 Kurulum

### 1. Projeyi klonla
git clone https://github.com/kullanici_adin/kaplumba_tanima.git
cd kaplumba_tanima

### 2. Sanal ortam oluştur
python -m venv .venv
.venv\Scripts\activate

### 3. Gereksinimleri yükle
pip install -r requirements.txt

### 4. Veri setini indir
Veri seti 235 MB olduğu için GitHub'a yüklenemedi. Google Drive linkinden indirip data/ klasörüne çıkartın.

### 5. Modeli eğit
python train_yolo.py

### 6. Uygulamayı başlat
python -m uvicorn main:app --reload --port 8000

### 7. Tarayıcıda aç
http://localhost:8000

---

## 📊 Sonuçlar

| Metrik | Değer |
|--------|-------|
| Toplam kaplumbağa | 44 |
| Toplam fotoğraf | 1096 |
| Model doğruluk (30 epoch) | %53 |
| Threshold | %45 |

---

## 🛠️ Kullanılan Teknolojiler

- YOLOv8 - Kaplumbağa tanıma modeli
- FastAPI - Web arayüzü ve API
- Ultralytics - YOLO implementasyonu
- OpenCV - Görüntü işleme

---


