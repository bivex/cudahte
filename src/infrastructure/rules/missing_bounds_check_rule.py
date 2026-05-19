import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class MissingBoundsCheckRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        try:
            with open(file_path, 'r') as f:
                self.source_lines = f.read().split('\n')
        except:
            self.source_lines = []

    def get_smells(self):
        return self.smells

    def _get_function_source(self, start_line):
        lines = self.source_lines
        if start_line - 1 >= len(lines):
            return ""
        brace_depth = 0
        result = []
        for i in range(start_line - 1, len(lines)):
            result.append(lines[i])
            brace_depth += lines[i].count('{') - lines[i].count('}')
            if brace_depth <= 0 and '{' in ''.join(result):
                break
        return '\n'.join(result)

    def visitFunctionDefinition(self, ctx):
        func_text = self._get_function_source(ctx.start.line)

        if '__global__' not in func_text:
            return self.visitChildren(ctx)

        has_thread_index = ('threadIdx' in func_text and 'blockIdx' in func_text
                           and 'blockDim' in func_text)
        if not has_thread_index:
            return self.visitChildren(ctx)

        has_bounds_check = bool(re.search(
            r'if\s*\([^)]*(?:threadIdx|blockIdx|tid|idx|index)\s*<',
            func_text
        ))

        if not has_bounds_check:
            self.smells.append(CodeSmell(
                rule_name="MissingBoundsCheckInKernel",
                description="Kernel computes a thread index and accesses arrays without a bounds check (e.g., 'if (tid < N)'). Excess threads from grid rounding will cause out-of-bounds access.",
                file_path=self.file_path,
                position=Position(ctx.start.line, ctx.start.column),
                severity="CRITICAL"
            ))

        return self.visitChildren(ctx)
