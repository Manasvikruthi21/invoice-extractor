from abc import ABC, abstractmethod


class BaseLLM(ABC):

    @abstractmethod
    def extract_invoice(self, text: str):
        pass