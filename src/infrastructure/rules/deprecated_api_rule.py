import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class DeprecatedApiRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitUnqualifiedId(self, ctx):
        text = ctx.getText()
        # List of some common deprecated or discouraged CUDA APIs
        deprecated_apis = {
            "cudaThreadSynchronize": "Use 'cudaDeviceSynchronize()' instead.",
            "cudaThreadExit": "Use 'cudaDeviceReset()' instead.",
            "cudaBindTexture": "Use Texture Objects API (cudaCreateTextureObject) instead.",
            "cudaUnbindTexture": "Use Texture Objects API (cudaDestroyTextureObject) instead.",
            "cudaGetTextureAlignmentOffset": "Texture References are legacy; use Texture Objects.",
            "cudaMallocPitch": "Consider if 'cudaMalloc' or 'cudaMalloc3D' fits better for modern workloads."
        }
        
        if text in deprecated_apis:
            self.smells.append(CodeSmell(
                rule_name="DeprecatedAPI",
                description=f"CUDA API '{text}' is deprecated or discouraged. {deprecated_apis[text]}",
                file_path=self.file_path,
                position=Position(ctx.start.line, ctx.start.column),
                severity="WARNING"
            ))
                
        return self.visitChildren(ctx)
