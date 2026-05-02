# api/app.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # Dosyayı geçici kaydet
    temp_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Model predict çağrısı yapılacak (detaylı kod için ayrı prompt at)
    
    return JSONResponse(content={"prediction": "test", "confidence": 0.85})

@app.get("/")
def root():
    return {"message": "Kaplumbağa Tanıma API"}