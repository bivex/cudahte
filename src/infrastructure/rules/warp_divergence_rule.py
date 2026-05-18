import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class WarpDivergenceRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitSelectionStatement(self, ctx):
        # A selection statement is an 'if' or 'switch'
        text = ctx.getText()
        if text.startswith("if"):
            # Check if condition contains threadIdx, blockIdx, etc.
            # We can find the condition by looking at children
            condition_text = ""
            for i in range(ctx.getChildCount()):
                child = ctx.getChild(i)
                if child.__class__.__name__ == 'ConditionContext':
                    condition_text = child.getText()
                    break
            
            if "threadIdx" in condition_text or "blockIdx" in condition_text:
                # Naive check if it creates divergence (e.g. modulo, equality with threadIdx)
                if "%" in condition_text or "==" in condition_text or ">" in condition_text or "<" in condition_text:
                    self.smells.append(CodeSmell(
                        rule_name="WarpDivergence",
                        description=f"Potential warp divergence: Branching condition '{condition_text}' depends on thread/block IDs.",
                        file_path=self.file_path,
                        position=Position(ctx.start.line, ctx.start.column),
                        severity="CRITICAL"
                    ))

        return self.visitChildren(ctx)
