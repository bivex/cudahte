import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class GlobalMemoryCoalescingRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitPostfixExpression(self, ctx):
        text = ctx.getText()
        if "[" in text and "]" in text:
            is_in_kernel = False
            p = ctx.parentCtx
            while p is not None:
                if p.__class__.__name__ == 'FunctionDefinitionContext':
                    func_text = p.getText()
                    if "__global__" in func_text or "__device__" in func_text:
                        is_in_kernel = True
                    break
                p = p.parentCtx
            
            if is_in_kernel:
                match = re.search(r'\[([^\]]+)\]', text)
                if match:
                    index_expr = match.group(1)
                    if "threadIdx.x" in index_expr and "*" in index_expr:
                        parts = index_expr.split("*")
                        for part in parts:
                            p_strip = part.strip()
                            if p_strip.isdigit() and int(p_strip) > 1:
                                self.smells.append(CodeSmell(
                                    rule_name="UncoalescedMemoryAccess",
                                    description=f"Potential uncoalesced memory access: index '{index_expr}' uses threadIdx.x with a stride > 1. This causes multiple memory transactions per warp.",
                                    file_path=self.file_path,
                                    position=Position(ctx.start.line, ctx.start.column),
                                    severity="CRITICAL"
                                ))
                                break
        return self.visitChildren(ctx)
