import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class GlobalAtomicContentionRule(CUDAParserVisitor):
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

        atomic_ops = ['atomicAdd', 'atomicSub', 'atomicExch', 'atomicMin',
                      'atomicMax', 'atomicInc', 'atomicDec', 'atomicCAS']
        has_global_atomic = False
        for op in atomic_ops:
            if op in func_text:
                has_global_atomic = True
                break

        if not has_global_atomic:
            return self.visitChildren(ctx)

        if '__shared__' in func_text:
            return self.visitChildren(ctx)

        self.smells.append(CodeSmell(
            rule_name="GlobalAtomicWithoutSharedIntermediate",
            description="Atomic operations on global memory without shared memory intermediate. When many threads compete for few memory locations, use shared memory atomics first, then merge to global. This avoids severe contention.",
            file_path=self.file_path,
            position=Position(ctx.start.line, ctx.start.column),
            severity="WARNING"
        ))

        return self.visitChildren(ctx)
