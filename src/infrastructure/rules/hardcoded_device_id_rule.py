import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class HardcodedDeviceIdRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitUnqualifiedId(self, ctx):
        text = ctx.getText()
        if text == "cudaSetDevice":
            p = ctx.parentCtx
            # Move up to find the argument list
            depth = 0
            while p is not None and depth < 3:
                p_text = p.getText()
                if "(" in p_text and ")" in p_text:
                    # Extract arguments
                    match = re.search(r'cudaSetDevice\(([^)]+)\)', p_text)
                    if match:
                        arg = match.group(1).strip()
                        if arg.isdigit():
                            self.smells.append(CodeSmell(
                                rule_name="HardcodedDeviceId",
                                description=f"Hardcoded device ID '{arg}' used in 'cudaSetDevice'. This can cause failures on systems where device {arg} is unavailable. Query available devices first.",
                                file_path=self.file_path,
                                position=Position(ctx.start.line, ctx.start.column),
                                severity="WARNING"
                            ))
                        break
                p = p.parentCtx
                depth += 1
                
        return self.visitChildren(ctx)
