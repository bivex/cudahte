import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "parser"))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position


class CudaEventLeakRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        self._processed = False
        try:
            with open(file_path, "r") as f:
                self.source_text = f.read()
        except:
            self.source_text = ""

    def get_smells(self):
        if not self._processed:
            self._processed = True
            self._find_leaks()
        return self.smells

    def _find_leaks(self):
        created = {}
        for match in re.finditer(r"cudaEventCreate\s*\(\s*&\s*(\w+)", self.source_text):
            var = match.group(1)
            line = self.source_text[: match.start()].count("\n") + 1
            created[var] = line

        destroyed = set()
        for m in re.finditer(r"cudaEventDestroy\s*\(\s*(\w+)", self.source_text):
            line_start = self.source_text.rfind("\n", 0, m.start()) + 1
            line_before = self.source_text[line_start : m.start()]
            if "//" in line_before or "/*" in line_before:
                continue
            destroyed.add(m.group(1))

        for var, line in created.items():
            if var not in destroyed:
                self.smells.append(
                    CodeSmell(
                        rule_name="CudaEventResourceLeak",
                        description=f"'cudaEventCreate' called for '{var}' but no matching 'cudaEventDestroy' found. GPU event resources are finite and should be released.",
                        file_path=self.file_path,
                        position=Position(line, 0),
                        severity="WARNING",
                    )
                )
