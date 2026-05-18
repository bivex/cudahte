import sys
import os

# Add parser to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from antlr4 import FileStream, CommonTokenStream
from CUDALexer import CUDALexer
from CUDAParser import CUDAParser
from src.domain.ports import CodeAnalyzerPort
from src.domain.entities import CodeSmell
from typing import List

class AntlrCudaAnalyzer(CodeAnalyzerPort):
    def __init__(self, rules):
        self.rules = rules

    def analyze_file(self, file_path: str) -> List[CodeSmell]:
        try:
            input_stream = FileStream(file_path, encoding='utf-8')
            lexer = CUDALexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = CUDAParser(stream)
            tree = parser.translationUnit()

            smells = []
            for rule_class in self.rules:
                rule_instance = rule_class(file_path)
                rule_instance.visit(tree)
                smells.extend(rule_instance.get_smells())
            return smells
        except Exception as e:
            # Domain dictates we don't throw technical exceptions back unless necessary
            print(f"Failed to parse {file_path}: {e}", file=sys.stderr)
            return []
