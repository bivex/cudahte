from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import CodeSmell

class CodeAnalyzerPort(ABC):
    @abstractmethod
    def analyze_file(self, file_path: str) -> List[CodeSmell]:
        pass
