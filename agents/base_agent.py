from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """Pipeline'da çalışan temel agent sınıfı - OCP uyumlu"""
    
    @abstractmethod
    def process(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Her agent bu metodu implement eder. 
        data dict olarak gelir, işlenmiş dict olarak döner.
        
        Args:
            data: İşlenecek veri sözlüğü
            
        Returns:
            Dict[str, Any]: İşlenmiş veri sözlüğü
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """Agent adını döndür (loglama için)
        
        Returns:
            str: Agent adı
        """
        pass