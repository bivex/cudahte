import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class MissingRestrictOnKernelPointersRule(CUDAParserVisitor):
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

    @staticmethod
    def _strip_comments(text: str) -> str:
        """Remove // and /* */ comments so regexes are not fooled by commented code."""
        text = re.sub(r"//.*", "", text)
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        return text

    def visitFunctionDefinition(self, ctx):
        func_text = self._get_function_source(ctx.start.line)
        clean_text = self._strip_comments(func_text)

        if '__global__' not in clean_text:
            return self.visitChildren(ctx)

        if '__restrict__' in clean_text or '__restrict' in clean_text:
            return self.visitChildren(ctx)

        header_end = func_text.find('{')
        if header_end < 0:
            return self.visitChildren(ctx)

        header = func_text[:header_end]
        param_section = re.search(r'\(([^)]*)\)', header)
        if param_section:
            params = param_section.group(1)
            pointer_count = params.count('*')
            if pointer_count >= 2:
                self.smells.append(CodeSmell(
                    rule_name="MissingRestrictOnKernelPointers",
                    description=f"Kernel has {pointer_count} pointer parameters without '__restrict__' qualifiers. Without __restrict__, the compiler assumes pointers may alias, preventing load/store reordering and other optimizations.",
                    file_path=self.file_path,
                    position=Position(ctx.start.line, ctx.start.column),
                    severity="INFO"
                ))

        return self.visitChildren(ctx)
