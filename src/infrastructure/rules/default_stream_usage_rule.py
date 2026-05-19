import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class DefaultStreamUsageRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitPostfixExpression(self, ctx):
        text = ctx.getText()
        
        # 1. Check kernel launches: <<<grid, block, shared, stream>>>
        if "<<<" in text and ">>>" in text:
            match = re.search(r'<<<([^>]+)>>>', text)
            if match:
                params = [p.strip() for p in match.group(1).split(',')]
                # If stream parameter (4th) is missing or is '0' or 'NULL'
                if len(params) < 4 or params[3] in ['0', 'NULL', 'nullptr']:
                    self.smells.append(CodeSmell(
                        rule_name="DefaultStreamUsage",
                        description="Kernel launched in the default (NULL) stream. This prevents overlapping with other kernels or memory transfers. Use custom streams for concurrency.",
                        file_path=self.file_path,
                        position=Position(ctx.start.line, ctx.start.column),
                        severity="WARNING"
                    ))
        
        # 2. Check cudaMemcpyAsync(..., stream)
        if "cudaMemcpyAsync" in text:
            # Match the arguments. Typically 5 arguments: dst, src, size, kind, stream
            # We look at the last argument
            match = re.search(r'cudaMemcpyAsync\((.*)\)', text)
            if match:
                args = [a.strip() for a in match.group(1).split(',')]
                if len(args) < 5 or args[4] in ['0', 'NULL', 'nullptr']:
                    self.smells.append(CodeSmell(
                        rule_name="DefaultStreamUsage",
                        description="'cudaMemcpyAsync' called in the default stream. Memory transfer will block other operations in the same stream. Use a custom stream.",
                        file_path=self.file_path,
                        position=Position(ctx.start.line, ctx.start.column),
                        severity="WARNING"
                    ))
                    
        return self.visitChildren(ctx)
