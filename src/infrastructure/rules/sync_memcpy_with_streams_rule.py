import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class SyncMemcpyWithStreamsRule(CUDAParserVisitor):
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

        if 'cudaStreamCreate' not in self.source_text:
            return self.visitChildren(ctx)

        for match in re.finditer(r'cudaMemcpy\s*\(', self.source_text):
            start = match.start()
            segment = self.source_text[start:start+200]

            if 'cudaMemcpyAsync' in self.source_text[max(0, start-20):start+20]:
                continue

            if any(kw in segment for kw in ['cudaMemcpyHostToDevice',
                                             'cudaMemcpyDeviceToHost',
                                             'cudaMemcpyDeviceToDevice']):
                line_num = self.source_text[:start].count('\n') + 1
                self._reported = True
                self.smells.append(CodeSmell(
                    rule_name="SynchronousMemcpyWithActiveStreams",
                    description="Synchronous 'cudaMemcpy' used when CUDA streams are active. This blocks the CPU and prevents copy/kernel overlap. Use 'cudaMemcpyAsync()' with a stream parameter.",
                    file_path=self.file_path,
                    position=Position(line_num, 0),
                    severity="WARNING"
                ))
                break

        return self.visitChildren(ctx)
