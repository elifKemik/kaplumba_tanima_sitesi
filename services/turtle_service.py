from interfaces.ivalidator import IValidator
from interfaces.iresearcher import IResearcher
from agents.imodel import IModel

CONFIDENCE_THRESHOLD = 0.60

class TurtleService:
    def __init__(self, validator: IValidator, researcher: IResearcher, model: IModel):
        self.validator = validator
        self.researcher = researcher
        self.model = model

    def identify_turtle(self, file_path: str) -> dict:
        try:
            print("Yüz tanıma süreci başlatıldı...")

            # Doğrulama aşaması
            print("Doğrulama aşaması...")
            is_valid = self.validator.validate(file_path)
            if not is_valid:
                print("Doğrulama başarısız: Geçersiz dosya")
                return {"status": "error", "message": "Geçersiz dosya"}

            print("Doğrulama başarılı")

            # Kalite analizi aşaması
            print("Kalite analizi aşaması...")
            analysis = self.researcher.analyze(file_path)
            if analysis["status"] == "fail":
                print(f"Kalite analizi başarısız: {analysis['message']}")
                return {"status": "warning", "message": analysis['message']}

            warning_message = None
            if analysis["status"] == "warning":
                warning_message = analysis["message"]
                print("Düşük kalite uyarısı")
                print(f"Kalite analizi uyarısı: {warning_message}")
            else:
                print(f"Kalite analizi başarılı: {analysis['message']}")

            # Model tahmini aşaması
            print("Model tahmini aşaması...")
            prediction = self.model.predict(file_path, analysis)
            print(f"Model tahmini: {prediction}")

            # JSON serializable hale getir (numpy.float32 → float)
            if 'accuracy' in prediction:
                prediction['accuracy'] = float(prediction['accuracy'])

            if prediction.get("accuracy", 0) >= CONFIDENCE_THRESHOLD * 100:
                return {"status": "success", "message": "Durum: Başarılı, Kaplumbağa Tanımlandı", "prediction": prediction}

            return {"status": "warning", "message": "Durum: Başarısız, doğruluk eşiği sağlanamadı", "prediction": prediction}

        except Exception as e:
            print(f"Hata oluştu: {str(e)}")
            return {"status": "error", "message": str(e)}