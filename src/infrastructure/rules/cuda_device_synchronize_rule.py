import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class CudaDeviceSynchronizeInHotPathRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitUnqualifiedId(self, ctx):
        text = ctx.getText()
        if text == "cudaDeviceSynchronize":
            # Check if inside a loop
            p = ctx.parentCtx
            in_loop = False
            while p is not None:
                if p.__class__.__name__ == 'IterationStatementContext':
                    in_loop = True
                    break
                p = p.parentCtx

            if in_loop:
                self.smells.append(CodeSmell(
                    rule_name="CudaDeviceSynchronizeInHotPath",
                    description="'cudaDeviceSynchronize()' called inside a loop. This completely blocks the CPU and breaks async pipelines.",
                    file_path=self.file_path,
                    position=Position(ctx.start.line, ctx.start.column),
                    severity="WARNING"
                ))

        return self.visitChildren(ctx)
