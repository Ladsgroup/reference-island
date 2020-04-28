# TODO: Import pipe type for typehinting

from abc import ABC, abstractmethod


class AbstractPump(ABC):
    @abstractmethod
    def run(self, pipe) -> None:
        raise NotImplementedError
