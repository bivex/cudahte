import sys
import os
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'parser'))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position

class IncorrectGridDimensionRule(CUDAParserVisitor):
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

        named_divisors = [
            'blockDim\\.x', 'blockDim\\.y', 'blockDim\\.z',
            'threadsPerBlock', 'THREADS', 'BLOCK_SIZE', 'block_size',
            'TPB', 'numThreads', 'NUM_THREADS'
        ]
        all_patterns = named_divisors + [r'256', r'128', r'512', r'1024', r'64']

        for divisor in all_patterns:
            pattern = r'(\w+)\s*/\s*(' + divisor + r')\b'
            for match in re.finditer(pattern, self.source_text):
                numerator = match.group(1)
                denom_expr = match.group(2)

                if numerator in ['2', '4', '8', '16', 'i']:
                    continue

                line_num = self.source_text[:match.start()].count('\n') + 1

                ceiling_check = (
                    numerator + '+' + denom_expr + '-1' in self.source_text or
                    numerator + ' + ' + denom_expr + ' - 1' in self.source_text
                )

                if not ceiling_check:
                    self._reported = True
                    self.smells.append(CodeSmell(
                        rule_name="IncorrectGridDimensionCalculation",
                        description=f"Grid dimension uses integer division '{match.group(0)}' which rounds down. Use ceiling division '({numerator} + {denom_expr} - 1) / {denom_expr}' to ensure all elements are processed.",
                        file_path=self.file_path,
                        position=Position(line_num, 0),
                        severity="WARNING"
                    ))
                    break

            if self._reported:
                break

        return self.visitChildren(ctx)
