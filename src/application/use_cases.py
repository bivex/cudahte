import os
from typing import List
from src.domain.entities import CodeSmell
from src.domain.ports import CodeAnalyzerPort

class AnalyzeFileUseCase:
    def __init__(self, analyzer: CodeAnalyzerPort):
        self.analyzer = analyzer

    def execute(self, file_path: str) -> List[CodeSmell]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        return self.analyzer.analyze_file(file_path)

class AnalyzeDirectoryUseCase:
    def __init__(self, analyzer: CodeAnalyzerPort):
        self.analyzer = analyzer

    def execute(self, dir_path: str) -> List[CodeSmell]:
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        if not os.path.isdir(dir_path):
            raise NotADirectoryError(f"Path is not a directory: {dir_path}")
            
        smells = []
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.cu') or file.endswith('.cuh') or file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    smells.extend(self.analyzer.analyze_file(file_path))
        return smells
