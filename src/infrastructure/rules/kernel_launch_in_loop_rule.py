import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class KernelLaunchInLoopRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitPostfixExpression(self, ctx):
        text = ctx.getText()
        if "<<<" in text and ">>>" in text:
            p = ctx.parentCtx
            in_loop = False
            while p is not None:
                if p.__class__.__name__ == 'IterationStatementContext':
                    in_loop = True
                    break
                p = p.parentCtx

            if in_loop:
                self.smells.append(CodeSmell(
                    rule_name="KernelLaunchInLoop",
                    description="Kernel launched inside a loop. Launch overhead (~5-10μs) multiplies by iterations. Consider batching or using CUDA Graphs.",
                    file_path=self.file_path,
                    position=Position(ctx.start.line, ctx.start.column),
                    severity="CRITICAL"
                ))
        return self.visitChildren(ctx)
