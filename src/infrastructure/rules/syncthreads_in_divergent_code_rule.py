import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class SyncthreadsInDivergentCodeRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitUnqualifiedId(self, ctx):
        text = ctx.getText()
        if text == "__syncthreads":
            p = ctx.parentCtx
            in_divergent = False
            while p is not None:
                if p.__class__.__name__ == 'SelectionStatementContext':
                    condition_text = ""
                    for i in range(p.getChildCount()):
                        child = p.getChild(i)
                        if child.__class__.__name__ == 'ConditionContext':
                            condition_text = child.getText()
                            break
                    if "threadIdx" in condition_text or "blockIdx" in condition_text:
                        in_divergent = True
                        break
                p = p.parentCtx

            if in_divergent:
                self.smells.append(CodeSmell(
                    rule_name="SyncthreadsInDivergentCode",
                    description="Calling '__syncthreads()' inside a divergent branch can cause a deadlock. Ensure all threads in a block reach the barrier.",
                    file_path=self.file_path,
                    position=Position(ctx.start.line, ctx.start.column),
                    severity="CRITICAL"
                ))

        return self.visitChildren(ctx)
