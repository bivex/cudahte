import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class CudaApiErrorCheckRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitUnqualifiedId(self, ctx):
        text = ctx.getText()
        cuda_apis = ['cudaMalloc', 'cudaMemcpy', 'cudaFree', 'cudaDeviceSynchronize']
        
        if text in cuda_apis:
            p = ctx.parentCtx
            is_checked = False
            depth = 0
            while p is not None and depth < 8:
                p_text = p.getText()
                if 'CHECK' in p_text or 'check' in p_text or '=' in p_text or 'if(' in p_text or 'assert' in p_text or 'EXPECT' in p_text:
                    is_checked = True
                    break
                p = p.parentCtx
                depth += 1

            if not is_checked:
                line = ctx.start.line
                column = ctx.start.column
                self.smells.append(CodeSmell(
                    rule_name="UncheckedCudaAPI",
                    description=f"CUDA API call '{text}' is potentially unchecked. Always check the return value of CUDA API calls.",
                    file_path=self.file_path,
                    position=Position(line, column),
                    severity="CRITICAL"
                ))

        return self.visitChildren(ctx)
