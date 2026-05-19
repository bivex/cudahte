import sys
import os
import re

# This rule doesn't use ANTLR because it's for checking architectural integrity in Python files
# but we implement it as a port to be consistent with our design.

class ArchitecturalCudaLeakRule:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.smells = []

    def get_smells(self):
        return self.smells

    def visit(self, tree):
        # We don't use the tree, we just check the file content
        normalized_path = os.path.normpath(self.file_path).replace('\\', '/')
        if "/src/domain" in normalized_path or "/src/application" in normalized_path:
            try:
                with open(self.file_path, 'r') as f:
                    lines = f.readlines()
                    cuda_keywords = ['cuda.h', 'cudaMalloc', 'cudaFree', 'cudaMemcpy', 'cudaError_t', 'cudaSuccess']
                    for i, line in enumerate(lines):
                        for keyword in cuda_keywords:
                            if keyword in line:
                                from src.domain.entities import CodeSmell, Position
                                self.smells.append(CodeSmell(
                                    rule_name="ArchitecturalCudaLeak",
                                    description=f"Clean Architecture Violation: CUDA-specific dependency '{keyword}' found in Domain/Application layer. Logic should depend on Ports, not Infrastructure.",
                                    file_path=self.file_path,
                                    position=Position(i + 1, 0),
                                    severity="CRITICAL"
                                ))
                                break # One smell per line is enough
            except Exception:
                pass
