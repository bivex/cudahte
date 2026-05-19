import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class UnifiedMemoryPrefetchRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitUnqualifiedId(self, ctx):
        text = ctx.getText()
        if text == "cudaMallocManaged":
            # Check if current function contains cudaMemPrefetchAsync
            p = ctx.parentCtx
            func_def = None
            while p is not None:
                if p.__class__.__name__ == 'FunctionDefinitionContext':
                    func_def = p
                    break
                p = p.parentCtx
                
            if func_def:
                func_text = func_def.getText()
                if "cudaMemPrefetchAsync" not in func_text:
                    self.smells.append(CodeSmell(
                        rule_name="UnifiedMemoryWithoutPrefetch",
                        description="'cudaMallocManaged' used without 'cudaMemPrefetchAsync'. Data will be moved via slow Page Faults. Use prefetching for better performance.",
                        file_path=self.file_path,
                        position=Position(ctx.start.line, ctx.start.column),
                        severity="WARNING"
                    ))
        return self.visitChildren(ctx)
