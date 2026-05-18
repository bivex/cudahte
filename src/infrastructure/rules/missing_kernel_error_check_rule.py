import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class MissingKernelErrorCheckRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitPostfixExpression(self, ctx):
        text = ctx.getText()
        if "<<<" in text and ">>>" in text:
            p = ctx.parentCtx
            func_def = None
            while p is not None:
                if p.__class__.__name__ == 'FunctionDefinitionContext':
                    func_def = p
                    break
                p = p.parentCtx
                
            if func_def:
                func_text = func_def.getText()
                if "cudaGetLastError" not in func_text and "cudaPeekAtLastError" not in func_text:
                    self.smells.append(CodeSmell(
                        rule_name="MissingKernelErrorCheck",
                        description="Kernel launch is not followed by 'cudaGetLastError()'. Kernel launch failures (e.g., invalid grid/block config) are asynchronous and will be silently ignored without this check.",
                        file_path=self.file_path,
                        position=Position(ctx.start.line, ctx.start.column),
                        severity="CRITICAL"
                    ))

        return self.visitChildren(ctx)
