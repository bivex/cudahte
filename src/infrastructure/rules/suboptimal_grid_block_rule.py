import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class SuboptimalGridBlockRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visitPostfixExpression(self, ctx):
        text = ctx.getText()
        if "<<<" in text and ">>>" in text:
            # Try to extract the <<<grid, block>>> part
            match = re.search(r'<<<([^>]+)>>>', text)
            if match:
                config = match.group(1).split(',')
                if len(config) >= 2:
                    grid = config[0].strip()
                    block = config[1].strip()
                    
                    if block.isdigit():
                        block_size = int(block)
                        
                        # Warn if block size is not a multiple of 32
                        if block_size % 32 != 0:
                            self.smells.append(CodeSmell(
                                rule_name="SuboptimalGridBlock",
                                description=f"Block size '{block_size}' is not a multiple of 32 (warp size). This leads to underutilized warps.",
                                file_path=self.file_path,
                                position=Position(ctx.start.line, ctx.start.column),
                                severity="WARNING"
                            ))
                        
                        # Warn if block size is a small constant (e.g. < 128)
                        elif block_size < 128:
                            self.smells.append(CodeSmell(
                                rule_name="SuboptimalGridBlock",
                                description=f"Suboptimal block size '{block_size}' in kernel launch. Consider using ideally 128 or 256 for better occupancy.",
                                file_path=self.file_path,
                                position=Position(ctx.start.line, ctx.start.column),
                                severity="WARNING"
                            ))
                        
                        # Warn if grid is hardcoded to 1 and block is small
                        if grid == '1' and block_size <= 1024:
                            self.smells.append(CodeSmell(
                                rule_name="SuboptimalGridBlock",
                                description=f"Kernel launched with a single block (grid=1, block={block}). The GPU will be severely underutilized.",
                                file_path=self.file_path,
                                position=Position(ctx.start.line, ctx.start.column),
                                severity="WARNING"
                            ))
        return self.visitChildren(ctx)
