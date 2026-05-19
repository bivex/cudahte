import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "parser"))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position


class SharedMemoryUninitializedAtomicRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        try:
            with open(file_path, "r") as f:
                self.source_text = f.read()
        except:
            self.source_text = ""

    def get_smells(self):
        return self.smells

    @staticmethod
    def _strip_comments(text: str) -> str:
        """Remove // and /* */ comments so regexes are not fooled by commented code."""
        text = re.sub(r"//.*", "", text)
        text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
        return text

    def visitFunctionDefinition(self, ctx):
        line = ctx.start.line
        func_text = self._get_function_source(line)
        clean_text = self._strip_comments(func_text)

        if "__shared__" not in clean_text:
            return self.visitChildren(ctx)

        atomic_ops = [
            "atomicAdd",
            "atomicSub",
            "atomicExch",
            "atomicMin",
            "atomicMax",
            "atomicInc",
            "atomicDec",
            "atomicCAS",
            "atomicAnd",
            "atomicOr",
            "atomicXor",
        ]

        has_any_atomic = any(op in clean_text for op in atomic_ops)
        if not has_any_atomic:
            return self.visitChildren(ctx)

        shared_vars = re.findall(
            r"__shared__\s+(?:unsigned\s+)?(?:const\s+)?(?:\w+\s+){1,3}(\w+)\s*\[",
            clean_text,
        )

        for var in shared_vars:
            for op in atomic_ops:
                if op in clean_text:
                    is_used_in_atomic = re.search(
                        op + r"\s*\(\s*&\s*" + re.escape(var), clean_text
                    )
                    if is_used_in_atomic:
                        has_init = bool(
                            re.search(
                                re.escape(var) + r"\[[^\]]*\]\s*=\s*0", clean_text
                            )
                        )
                        if not has_init:
                            self.smells.append(
                                CodeSmell(
                                    rule_name="SharedMemoryUninitializedForAtomics",
                                    description=f"__shared__ variable '{var}' is used with atomic operations without zero-initialization. Shared memory contents are undefined at kernel start, producing incorrect results.",
                                    file_path=self.file_path,
                                    position=Position(ctx.start.line, ctx.start.column),
                                    severity="WARNING",
                                )
                            )
                        break

        return self.visitChildren(ctx)

    def _get_function_source(self, start_line):
        lines = self.source_text.split("\n")
        if start_line - 1 < len(lines):
            remaining = "\n".join(lines[start_line - 1 :])
            match = re.search(r"__global__.*?^\}", remaining, re.MULTILINE | re.DOTALL)
            if match:
                return match.group(0)
            brace_depth = 0
            result = []
            for line in lines[start_line - 1 :]:
                result.append(line)
                brace_depth += line.count("{") - line.count("}")
                if brace_depth <= 0 and "{" in "".join(result):
                    break
            return "\n".join(result)
        return ""
