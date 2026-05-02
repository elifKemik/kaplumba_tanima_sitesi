from abc import ABC, abstractmethod

class IResearcher(ABC):
    @abstractmethod
    def analyze(self, data):
        pass