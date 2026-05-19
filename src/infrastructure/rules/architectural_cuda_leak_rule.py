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
        # Check if the file is in domain or application layers
        if "src/domain" in self.file_path or "src/application" in self.file_path:
            try:
                with open(self.file_path, 'r') as f:
                    content = f.read()
                    # Look for CUDA keywords or headers
                    cuda_keywords = ['cuda.h', 'cudaMalloc', 'cudaFree', 'cudaMemcpy', 'cudaError_t', 'cudaSuccess']
                    for keyword in cuda_keywords:
                        if keyword in content:
                            # Find line number (naive)
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if keyword in line:
                                    from src.domain.entities import CodeSmell, Position
                                    self.smells.append(CodeSmell(
                                        rule_name="ArchitecturalCudaLeak",
                                        description=f"Clean Architecture Violation: CUDA-specific dependency '{keyword}' found in Domain/Application layer. Logic should depend on Ports, not Infrastructure.",
                                        file_path=self.file_path,
                                        position=Position(i + 1, 0),
                                        severity="CRITICAL"
                                    ))
            except Exception:
                pass
