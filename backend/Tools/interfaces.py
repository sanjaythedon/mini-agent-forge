from abc import ABC, abstractmethod


class Tool(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass
    