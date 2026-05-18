import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class SlowMathFunctionRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitUnqualifiedId(self, ctx):
        text = ctx.getText()
        slow_math = {'sin', 'cos', 'exp', 'log', 'sqrt'}
        if text in slow_math:
            self.smells.append(CodeSmell(
                rule_name="SlowMathFunction",
                description=f"Usage of standard math function '{text}'. Consider using intrinsic functions like '__{text}f' or compiling with '--use_fast_math'.",
                file_path=self.file_path,
                position=Position(ctx.start.line, ctx.start.column),
                severity="WARNING"
            ))
        return self.visitChildren(ctx)
