from config import Config
from agents.pipeline import Pipeline
from interfaces.ivalidator import IValidator
from interfaces.iresearcher import IResearcher
from interfaces.imodel import IModel  

class TurtleService:
    def __init__(self, validator: IValidator, researcher: IResearcher, model: IModel):
        self.validator = validator
        self.researcher = researcher
        self.model = model
        self._setup_pipeline()
    
    def _setup_pipeline(self):
        """Pipeline'a agent'ları doğrudan ekle (BaseAgent türemiş olmalılar)"""
        self.pipeline = Pipeline()
        self.pipeline.add_agent(self.validator)   # Validator BaseAgent'den türedi
        self.pipeline.add_agent(self.researcher)  # Researcher BaseAgent'den türedi
        self.pipeline.add_agent(self.model)       # YOLOModel BaseAgent'den türedi

    def identify_turtle(self, file_path: str) -> dict:
        try:
            print("Yüz tanıma süreci başlatıldı...")
            
            result = self.pipeline.execute({"file_path": file_path})
            
            if result.get("stop"):
                return {"status": "error", "message": result.get("error", "Bilinmeyen hata")}
            
            prediction = result.get("prediction", {})
            
            if prediction.get("accuracy", 0) >= Config.MODEL.FINAL_CONFIDENCE_THRESHOLD * 100:
                return {"status": "success", "message": "Başarılı", "prediction": prediction}
            
            return {"status": "warning", "message": "Doğruluk eşiği sağlanamadı", "prediction": prediction}

        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            return {"status": "error", "message": str(e)}