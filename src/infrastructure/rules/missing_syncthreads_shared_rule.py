import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "parser"))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position


class MissingSyncthreadsAfterSharedWriteRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        try:
            with open(file_path, "r") as f:
                self.source_lines = f.read().split("\n")
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
            brace_depth += lines[i].count("{") - lines[i].count("}")
            if brace_depth <= 0 and "{" in "".join(result):
                break
        return "\n".join(result)

    @staticmethod
    def _strip_comments(text: str) -> str:
        """Remove // and /* */ comments so that keyword checks are not fooled."""
        text = re.sub(r"//.*", "", text)
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        return text

    def visitFunctionDefinition(self, ctx):
        func_text = self._get_function_source(ctx.start.line)
        clean_text = self._strip_comments(func_text)

        if "__shared__" not in clean_text:
            return self.visitChildren(ctx)

        if "__syncthreads" in clean_text:
            return self.visitChildren(ctx)

        shared_vars = re.findall(r"__shared__\s+\S+\s+(\w+)\s*\[", clean_text)
        if not shared_vars:
            shared_vars = re.findall(r"__shared__\s+\w+\s+\w+\s+(\w+)", clean_text)
        if not shared_vars:
            shared_vars = re.findall(r"__shared__\s+\w+\s+(\w+)", clean_text)

        if shared_vars:
            self.smells.append(
                CodeSmell(
                    rule_name="MissingSyncthreadsAfterSharedWrite",
                    description="__shared__ memory is written and read without an intervening __syncthreads(). Without a barrier, threads may read stale or uninitialized data from other threads.",
                    file_path=self.file_path,
                    position=Position(ctx.start.line, ctx.start.column),
                    severity="CRITICAL",
                )
            )

        return self.visitChildren(ctx)
