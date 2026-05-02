from abc import ABC, abstractmethod

class IValidator(ABC):
    @abstractmethod
    def validate(self, data):
        pass