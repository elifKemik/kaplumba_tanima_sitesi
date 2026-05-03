from config import Config


class PredictionValidator:
    """Prediction sonuçlarını doğrular ve formatlar - SRP: Validation responsibility"""
    
    @staticmethod
    def is_confident(confidence: float) -> bool:
        """Confidence threshold kontrolü
        
        Args:
            confidence: Model tahmininin güven puanı (0-1)
        
        Returns:
            bool: Güven puanı eşik değerinin üstündeyse True
        """
        return confidence >= Config.MODEL.FINAL_CONFIDENCE_THRESHOLD
    
    @staticmethod
    def format_result(prediction_id: str, confidence: float, 
                     is_registered: bool = True) -> dict:
        """Prediction sonucunu formatla
        
        Args:
            prediction_id: Tahmin edilen kaplumbağa ID'si
            confidence: Güven puanı (0-1 aralığında)
            is_registered: Kaplumbağa veri setinde var mı?
        
        Returns:
            dict: Formatlanmış tahmin sonucu
        """
        if not is_registered:
            return {
                "id": "unknown",
                "accuracy": round(confidence * 100, 2),
                "status": "not_registered",
                "message": "Bu kaplumbağa veri setinde kayıtlı değil"
            }
        
        if PredictionValidator.is_confident(confidence):
            return {
                "id": prediction_id,
                "accuracy": round(confidence * 100, 2),
                "status": "identified"
            }
        
        return {
            "id": "unknown",
            "accuracy": round(confidence * 100, 2),
            "status": "not_identified"
        }
