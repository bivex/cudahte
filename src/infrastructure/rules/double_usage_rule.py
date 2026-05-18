import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class DoubleUsageRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitSimpleTypeSpecifier(self, ctx):
        text = ctx.getText()
        if "double" in text:
            self.smells.append(CodeSmell(
                rule_name="DoubleUsage",
                description="Use of 'double' detected. Double precision is significantly slower than float on most GPUs. Use 'float' if precision is not critical.",
                file_path=self.file_path,
                position=Position(ctx.start.line, ctx.start.column),
                severity="WARNING"
            ))
        return self.visitChildren(ctx)
