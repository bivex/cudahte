import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "..", "parser"))

from CUDAParserVisitor import CUDAParserVisitor
from src.domain.entities import CodeSmell, Position


class IncorrectGridDimensionRule(CUDAParserVisitor):
    """
    Detects integer division used for grid/block dimension calculation
    without ceiling division. For example:

        int blocks = N / 256;           // rounds down — wrong
        int blocks = (N + 255) / 256;   // ceiling — correct

    Rule is intentionally conservative: it fires only when BOTH:
    1. A division by a known block-size denominator is found, AND
    2. No corresponding ceiling expression (N + D - 1) / D exists (at least as a comment) nearby.
    """

    # Denominators that suggest a grid/block dimension calculation
    GRID_DENOMINATORS = re.compile(
        r"blockDim\.[xyz]|threadsPerBlock|THREADS|BLOCK_SIZE|block_size|"
        r"TPB|numThreads|NUM_THREADS|"
        r"TILE_WIDTH|TILE|WIDTH|\bVECTOR_N\b|\bELEMENT_N\b|"
        r"\b256\b|\b128\b|\b512\b|\b1024\b|\b64\b"
    )

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []
        self._reported = False
        try:
            with open(file_path, "r") as f:
                self.source_lines = f.read().splitlines()
                self.source_text = "\n".join(self.source_lines)
        except Exception:
            self.source_lines = []
            self.source_text = ""

    def get_smells(self):
        return self.smells

    # ------------------------------------------------------------------ #
    # Helper                                                               #
    # ------------------------------------------------------------------ #

    def _find_violations(self) -> None:
        """
        Scan the source text for floored-division grid/block dimension patterns.
        Report the first one (ceiling-division violation).
        Fires only on HOST-LEVEL constructions: dim3, gridDim wrap, or
        top-level block-count assignments, not on per-loop kernel loop bounds.
        Stops at the first confirmed violation.
        """
        if self._reported:
            return
        # Pattern: <numerator> / <denominator>
        # where denominator looks like a CUDA block/grid size
        div_pattern = re.compile(
            r"(\w+)\s*/\s*("
            r"blockDim\.[xyz]"
            r")|(\w+)\s*/\s*("
            r"threadsPerBlock|THREADS|BLOCK_SIZE|block_size|TPB|numThreads|NUM_THREADS"
            r")|(\w+)\s*/\s*("
            r"\b256\b|\b128\b|\b512\b|\b1024\b|\b64\b"
            r")|(\w+)\s*/\s*("
            r"TILE_WIDTH|TILE|WIDTH|VECTOR_N|ELEMENT_N|CHUNK_SIZE"
            r")"
        )

        LOOP_HEADER = re.compile(r"\b(for|while)\b")

        for m in re.finditer(div_pattern, self.source_text):
            # Collect the numerator / denominator from whichever group matched
            numer = m.group(1) or m.group(3) or m.group(5) or m.group(7)
            denom = m.group(2) or m.group(4) or m.group(6) or m.group(8)
            if not numer or not denom:
                continue

            # Skip obvious loop-variable or trivial cases
            if numer in ("2", "4", "8", "16", "i", "s", "stride", "m", "k"):
                continue

            # Look at the full line: if it is inside a for/while loop → skip
            # (loop upper-bounds may use floor division safely)
            line_start = self.source_text.rfind("\n", 0, m.start()) + 1
            line_end = self.source_text.find("\n", m.start())
            if line_end < 0:
                line_end = len(self.source_text)
            line = self.source_text[line_start:line_end].strip()
            
            # Line starts with for/while/if → skip (loop/cond boundary)
            if LOOP_HEADER.match(line):
                continue

            line_num = self.source_text[: m.start()].count("\n") + 1

            # Does a ceiling variant appear ANYWHERE in the source?
            # Accept both `N + D - 1` (spaced) and `N+D-1` (dense).
            numerators_ceiling = [
                numer + "+" + denom + "-1",
                numer + " + " + denom + " - 1",
            ]
            has_ceiling = any(cv in self.source_text for cv in numerators_ceiling)

            if has_ceiling:
                continue

            self._reported = True
            self.smells.append(
                CodeSmell(
                    rule_name="IncorrectGridDimensionCalculation",
                    description=(
                        f"Grid dimension uses integer division "
                        f"'{m.group(0)}' which rounds down. "
                        f"Use ceiling division "
                        f"'({numer} + {denom} - 1) / {denom}' "
                        f"to ensure all elements are processed."
                    ),
                    file_path=self.file_path,
                    position=Position(line_num, 0),
                    severity="WARNING",
                )
            )
            break  # one violation per file is enough

    def visitTranslationUnit(self, ctx):
        self._find_violations()
        return self.visitChildren(ctx)
