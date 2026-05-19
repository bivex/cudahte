import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class NonPowerOf2ReductionBlockRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitFunctionDefinition(self, ctx):
        func_text = ctx.getText()

        is_reduction = ('/=' in func_text or '/ 2' in func_text or '>>1' in func_text) and '__shared__' in func_text

        if not is_reduction:
            return self.visitChildren(ctx)

        block_sizes = re.findall(r'blockDim\.\w+\s*/\s*2|threadsPerBlock\s*/\s*2', func_text)

        define_matches = re.findall(r'#define\s+\w+\s+(\d+)', func_text)
        for size_str in define_matches:
            size = int(size_str)
            if size > 0 and (size & (size - 1)) != 0:
                self.smells.append(CodeSmell(
                    rule_name="NonPowerOf2ReductionBlock",
                    description=f"Reduction pattern uses block size {size} which is not a power of 2. Iterative halving (i /= 2) with non-power-of-2 sizes causes integer division to skip elements, producing incorrect results.",
                    file_path=self.file_path,
                    position=Position(ctx.start.line, ctx.start.column),
                    severity="WARNING"
                ))

        return self.visitChildren(ctx)
