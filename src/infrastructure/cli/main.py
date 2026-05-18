import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.application.use_cases import AnalyzeFileUseCase, AnalyzeDirectoryUseCase
from src.infrastructure.parsers.antlr_cuda_analyzer import AntlrCudaAnalyzer
from src.infrastructure.rules.cuda_api_error_check_rule import CudaApiErrorCheckRule
from src.infrastructure.rules.memory_leak_rule import MemoryLeakRule

def print_smells(smells):
    if not smells:
        print("No critical smells detected.")
        return

    for smell in smells:
        print(f"[{smell.severity}] {smell.rule_name} at {smell.file_path}:{smell.position.line}:{smell.position.column}")
        print(f"    {smell.description}")
        print()

def main():
    parser = argparse.ArgumentParser(description="Python Smells Analyzer for .cu files")
    subparsers = parser.add_subparsers(dest="command", required=True)

    file_parser = subparsers.add_parser("smells-file", help="Analyze a single .cu file")
    file_parser.add_argument("file", help="Path to the .cu file")

    dir_parser = subparsers.add_parser("smells-dir", help="Analyze a directory of .cu files")
    dir_parser.add_argument("dir", help="Path to the directory")

    args = parser.parse_args()

    # Wire up the analyzer with our rules
    rules = [CudaApiErrorCheckRule, MemoryLeakRule]
    analyzer = AntlrCudaAnalyzer(rules)

    smells = []
    if args.command == "smells-file":
        use_case = AnalyzeFileUseCase(analyzer)
        try:
            smells = use_case.execute(args.file)
        except Exception as e:
            print(f"Error analyzing file: {e}", file=sys.stderr)
            sys.exit(1)
            
    elif args.command == "smells-dir":
        use_case = AnalyzeDirectoryUseCase(analyzer)
        try:
            smells = use_case.execute(args.dir)
        except Exception as e:
            print(f"Error analyzing directory: {e}", file=sys.stderr)
            sys.exit(1)

    print_smells(smells)

if __name__ == "__main__":
    main()
