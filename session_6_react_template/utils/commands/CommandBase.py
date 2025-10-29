from abc import ABC, abstractmethod

class CommandBase(ABC):
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass
