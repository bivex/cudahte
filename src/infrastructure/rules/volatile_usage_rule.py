import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class VolatileUsageRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitDeclSpecifierSeq(self, ctx):
        text = ctx.getText()
        if "volatile" in text:
            self.smells.append(CodeSmell(
                rule_name="VolatileUsage",
                description="'volatile' keyword detected. Using 'volatile' for synchronization between GPU threads or blocks is unsafe and causes Undefined Behavior. Use atomic operations instead.",
                file_path=self.file_path,
                position=Position(ctx.start.line, ctx.start.column),
                severity="CRITICAL"
            ))
        return self.visitChildren(ctx)
