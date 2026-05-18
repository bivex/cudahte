import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class IntegerOverflowInIndexRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitSimpleDeclaration(self, ctx):
        text = ctx.getText()
        # Look for a declaration that starts with 'int' and contains blockIdx.x * blockDim.x + threadIdx.x
        if text.startswith("int") and "blockIdx" in text and "blockDim" in text and "threadIdx" in text:
            self.smells.append(CodeSmell(
                rule_name="IntegerOverflowInIndex",
                description="Global thread index calculated using 'int'. For large arrays (N > 2^31), this causes integer overflow. Use 'size_t' instead.",
                file_path=self.file_path,
                position=Position(ctx.start.line, ctx.start.column),
                severity="CRITICAL"
            ))
        return self.visitChildren(ctx)
