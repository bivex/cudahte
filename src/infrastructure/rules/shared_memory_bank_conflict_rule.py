import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class SharedMemoryBankConflictRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        self.shared_vars = set()

    def get_smells(self):
        return self.smells

    def visitSimpleDeclaration(self, ctx):
        text = ctx.getText()
        if "__shared__" in text:
            # Naive extraction of variable name
            # Pattern: __shared__ type name[...]
            match = re.search(r'__shared__\s+\w+\s+(\w+)', text)
            if match:
                self.shared_vars.add(match.group(1))
        return self.visitChildren(ctx)

    def visitPostfixExpression(self, ctx):
        text = ctx.getText()
        if "[" in text and "]" in text:
            # Check if the base of the expression is a known shared variable
            base_name = text.split('[')[0]
            if base_name in self.shared_vars:
                match = re.search(r'\[([^\]]+)\]', text)
                if match:
                    index_expr = match.group(1)
                    # Pattern: threadIdx.x * 32 (or multiple of 32)
                    if "threadIdx.x" in index_expr and "*" in index_expr:
                        parts = index_expr.split("*")
                        for part in parts:
                            p_strip = part.strip()
                            if p_strip.isdigit() and int(p_strip) % 32 == 0 and int(p_strip) > 0:
                                self.smells.append(CodeSmell(
                                    rule_name="SharedMemoryBankConflict",
                                    description=f"Potential shared memory bank conflict: index '{index_expr}' on shared variable '{base_name}' uses a stride of {p_strip}. This causes all threads in a warp to access the same bank.",
                                    file_path=self.file_path,
                                    position=Position(ctx.start.line, ctx.start.column),
                                    severity="WARNING"
                                ))
                                break
        return self.visitChildren(ctx)
