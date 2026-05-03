from typing import List, Dict, Any
from agents.base_agent import BaseAgent

class Pipeline:
    """Agent'ları sırayla çalıştıran pipeline - OCP uyumlu"""
    
    def __init__(self):
        self.agents: List[BaseAgent] = []
    
    def add_agent(self, agent: BaseAgent):
        """Pipeline'a yeni agent ekle (OCP: mevcut kod değişmez)"""
        self.agents.append(agent)
        return self  # Zincirleme için
    
    def execute(self, initial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tüm agent'ları sırayla çalıştır"""
        data = initial_data
        for agent in self.agents:
            print(f"Çalışıyor: {agent.get_name()}")
            data = agent.process(data)
            if data.get("stop"):  # Acil durdurma
                break
        return data