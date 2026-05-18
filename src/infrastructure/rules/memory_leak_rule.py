import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class MemoryLeakRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        self.allocations = 0
        self.frees = 0

    def get_smells(self):
        # This is a naive file-level check. A real check would track scopes and variable names.
        if self.allocations > self.frees:
            self.smells.append(CodeSmell(
                rule_name="PotentialMemoryLeak",
                description=f"Found {self.allocations} 'cudaMalloc' calls but only {self.frees} 'cudaFree' calls in file.",
                file_path=self.file_path,
                position=Position(0, 0),
                severity="WARNING"
            ))
        return self.smells

    def visitUnqualifiedId(self, ctx):
        text = ctx.getText()
        if text == "cudaMalloc":
            self.allocations += 1
        elif text == "cudaFree":
            self.frees += 1
        return self.visitChildren(ctx)
