from abc import ABC, abstractmethod


class PipeInterface(ABC):
    @abstractmethod
    def flow(self, data: dict) -> dict:
        return {}
