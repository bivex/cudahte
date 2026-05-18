import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.application.use_cases import AnalyzeFileUseCase, AnalyzeDirectoryUseCase
from src.infrastructure.parsers.antlr_cuda_analyzer import AntlrCudaAnalyzer
from src.infrastructure.rules.cuda_api_error_check_rule import CudaApiErrorCheckRule
from src.infrastructure.rules.memory_leak_rule import MemoryLeakRule
from src.infrastructure.rules.host_device_transfer_in_loop_rule import HostDeviceTransferInLoopRule
from src.infrastructure.rules.warp_divergence_rule import WarpDivergenceRule
from src.infrastructure.rules.suboptimal_grid_block_rule import SuboptimalGridBlockRule
from src.infrastructure.rules.cuda_device_synchronize_rule import CudaDeviceSynchronizeInHotPathRule
from src.infrastructure.rules.syncthreads_in_divergent_code_rule import SyncthreadsInDivergentCodeRule
from src.infrastructure.rules.integer_overflow_in_index_rule import IntegerOverflowInIndexRule
from src.infrastructure.rules.kernel_launch_in_loop_rule import KernelLaunchInLoopRule
from src.infrastructure.rules.double_usage_rule import DoubleUsageRule
from src.infrastructure.rules.slow_math_function_rule import SlowMathFunctionRule
from src.infrastructure.rules.missing_kernel_error_check_rule import MissingKernelErrorCheckRule
from src.infrastructure.rules.large_shared_memory_allocation_rule import LargeSharedMemoryAllocationRule
from src.infrastructure.rules.volatile_usage_rule import VolatileUsageRule

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
    rules = [
        CudaApiErrorCheckRule, 
        MemoryLeakRule,
        HostDeviceTransferInLoopRule,
        WarpDivergenceRule,
        SuboptimalGridBlockRule,
        CudaDeviceSynchronizeInHotPathRule,
        SyncthreadsInDivergentCodeRule,
        IntegerOverflowInIndexRule,
        KernelLaunchInLoopRule,
        DoubleUsageRule,
        SlowMathFunctionRule,
        MissingKernelErrorCheckRule,
        LargeSharedMemoryAllocationRule,
        VolatileUsageRule
    ]
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
