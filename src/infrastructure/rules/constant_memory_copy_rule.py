import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class ConstantMemoryCopyRule(CUDAParserVisitor):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        self._reported = False
        try:
            with open(file_path, 'r') as f:
                self.source_text = f.read()
        except:
            self.source_text = ""

    def get_smells(self):
        return self.smells

    def visitTranslationUnit(self, ctx):
        if self._reported:
            return self.visitChildren(ctx)

        constant_vars = set()
        for match in re.finditer(r'__constant__\s+\S+\s+(\w+)', self.source_text):
            constant_vars.add(match.group(1))

        if not constant_vars:
            return self.visitChildren(ctx)

        for var in constant_vars:
            pattern = r'cudaMemcpy\s*\(\s*' + re.escape(var) + r'\s*[,]'
            if re.search(pattern, self.source_text):
                self._reported = True
                self.smells.append(CodeSmell(
                    rule_name="ConstantMemoryWrongCopyMethod",
                    description=f"'cudaMemcpy' used with __constant__ variable '{var}'. Use 'cudaMemcpyToSymbol()' instead — constant memory resides in a separate address space.",
                    file_path=self.file_path,
                    position=Position(1, 0),
                    severity="WARNING"
                ))
                break

        return self.visitChildren(ctx)
