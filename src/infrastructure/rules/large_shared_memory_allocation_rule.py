import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class LargeSharedMemoryAllocationRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitSimpleDeclaration(self, ctx):
        text = ctx.getText()
        if "__shared__" in text:
            matches = re.findall(r'\[([^\]]+)\]', text)
            for m in matches:
                if m.isdigit():
                    size = int(m)
                    if size > 8192:
                        self.smells.append(CodeSmell(
                            rule_name="LargeSharedMemoryAllocation",
                            description=f"Static shared memory allocation of size '{size}' items. This might easily exceed the default 48KB limit per block and cause the kernel to silently fail to launch.",
                            file_path=self.file_path,
                            position=Position(ctx.start.line, ctx.start.column),
                            severity="CRITICAL"
                        ))
        return self.visitChildren(ctx)
