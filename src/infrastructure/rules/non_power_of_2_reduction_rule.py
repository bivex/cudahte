import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "parser"))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position


class NonPowerOf2ReductionBlockRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        try:
            with open(file_path, "r") as f:
                self.source_text = f.read()
                self.source_lines = self.source_text.split("\n")
        except:
            self.source_text = ""
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

    def visitFunctionDefinition(self, ctx):
        func_lines = self._get_function_source(ctx.start.line)

        # Detect reduction pattern: shared memory + iterative halving loop
        is_reduction = (
            "/=" in func_lines or "/ 2" in func_lines or ">>" in func_lines
        ) and "__shared__" in func_lines
        if not is_reduction:
            return self.visitChildren(ctx)

        # Scan the full source for #define block-size constants, the function text,
        # and 3 lines before the function declaration (to catch #define placed just before).
        search_start = max(0, ctx.start.line - 4)
        search_text = "\n".join(self.source_lines[search_start:]) + "\n" + func_lines

        define_sizes = re.findall(r"#define\s+\w+\s+(\d+)", search_text)

        # Also find variable assignments used as block size in the function
        block_var_assigns = re.findall(
            r"(?:blockDim\.\w+|block_size|THREADS|threadsPerBlock)\s*=\s*(\d+)",
            func_lines,
        )

        # Also find array sizes in __shared__ declarations
        shared_array_sizes = re.findall(r"__shared__\s+\w+\s+\w+\[(\d+)\]", func_lines)

        all_sizes = set(int(s) for s in define_sizes + block_var_assigns + shared_array_sizes)

        for size in all_sizes:
            if size > 0 and (size & (size - 1)) != 0:
                self.smells.append(
                    CodeSmell(
                        rule_name="NonPowerOf2ReductionBlock",
                        description=(
                            f"Reduction pattern uses block size {size} which is not a power of 2. "
                            f"Iterative halving (i /= 2) with non-power-of-2 sizes causes integer "
                            f"division to skip elements, producing incorrect results."
                        ),
                        file_path=self.file_path,
                        position=Position(ctx.start.line, ctx.start.column),
                        severity="WARNING",
                    )
                )

        return self.visitChildren(ctx)
