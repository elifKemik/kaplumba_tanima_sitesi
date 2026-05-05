from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
import uvicorn
from services.turtle_service import TurtleService
from agents.validator import Validator
from agents.researcher import Researcher
from agents.yolo_model import YOLOModel
from fastapi.responses import HTMLResponse
import shutil
import os

app = FastAPI(title="Caretta Caretta Yüz Tanıma API", version="1.0.0")
templates = Jinja2Templates(directory="templates")

# Dependency Injection: Servis ve agent'ları başlat
validator = Validator()
researcher = Researcher()
model = YOLOModel()  # Yeni YOLO Model
service = TurtleService(validator, researcher, model)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Yüz tanıma için fotoğraf yükleyin.
    Süreç: Validator -> Researcher -> Identifier
    """
    # Geçici dosya olarak kaydet
    file_path = f"temp_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # TurtleService ile tam süreci çalıştır
        result = service.identify_turtle(file_path)

        return result

    except Exception as e:
        return {"status": "error", "message": f"Beklenmeyen hata: {str(e)}"}
    finally:
        # Geçici dosyayı temizle
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/", response_class=HTMLResponse)
async def root():
    # index.html dosyasını doğrudan okuyoruz, böylece Jinja2 hatası devre dışı kalıyor
    with open("templates/index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return content
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)