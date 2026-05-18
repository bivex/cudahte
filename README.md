# CUDA Code Smells Analyzer

A Python-based static analysis tool designed to detect "code smells" and critical issues in NVIDIA CUDA (`.cu`, `.cuh`) files. 

This project leverages [ANTLR4](https://www.antlr.org/) for accurate parsing of CUDA C++ grammar and is structured using **Clean Architecture** principles to ensure clear separation of concerns, high maintainability, and easy extensibility.

## Features

- Parse CUDA source code using an ANTLR4-generated AST.
- Detect potentially unchecked CUDA API calls.
- Detect naive potential memory leaks (mismatched `cudaMalloc` / `cudaFree` counts).
- Clean Architecture (Domain, Application, Infrastructure layers).

## Detected Code Smells

| Rule Name | Description | Severity |
| :--- | :--- | :--- |
| **UncheckedCudaAPI** | CUDA API calls (e.g., `cudaMalloc`, `cudaMemcpy`, `cudaFree`, `cudaDeviceSynchronize`) should have their return values checked for errors. This rule detects if the call is not wrapped in a checking macro (like `CHECK`, `EXPECT`, `assert`) or assigned to a variable within 8 levels of the AST. | CRITICAL |
| **PotentialMemoryLeak** | A naive heuristic that triggers if the number of `cudaMalloc` calls in a file is greater than the number of `cudaFree` calls. | WARNING |
| **WarpDivergence** | Detects potential warp divergence by checking if an `if` statement's condition explicitly depends on `threadIdx` or `blockIdx` using equality or modulo operators. | CRITICAL |
| **HostDeviceTransferInLoop** | Detects if `cudaMemcpy` is called inside an iteration statement (`for`, `while`, `do-while`), which leads to massive PCIe bottlenecking. | CRITICAL |
| **SuboptimalGridBlock** | Checks kernel launch parameters `<<<grid, block>>>`. It flags a warning if the `block` size is hardcoded to a value `< 128`, or if the `grid` is just `1`. | WARNING |
| **CudaDeviceSynchronizeInHotPath** | Detects if `cudaDeviceSynchronize()` is called inside a loop, which blocks the CPU from doing any other work and breaks async pipelines. | WARNING |
| **SyncthreadsInDivergentCode** | Calling `__syncthreads()` inside a divergent branch (`if` statements depending on thread indices) can cause a deadlock. Ensures all threads reach the barrier. | CRITICAL |
| **IntegerOverflowInIndex** | Detects global thread index calculation (`blockIdx.x * blockDim.x + threadIdx.x`) assigned to an `int`. For large arrays, this causes integer overflow. Recommends using `size_t`. | CRITICAL |
| **KernelLaunchInLoop** | Detects kernel launches (`<<<...>>>`) inside loops. Launch overhead multiplies by iterations; recommends batching or using CUDA Graphs. | CRITICAL |
| **DoubleUsage** | Detects usage of `double` precision. Double precision is significantly slower than float on most consumer GPUs. Recommends using `float` if precision is not critical. | WARNING |
| **SlowMathFunction** | Detects standard math functions (e.g., `sin`, `cos`, `sqrt`) that might not be optimal. Recommends using intrinsic fast functions (e.g., `__sinf`) or compiling with `--use_fast_math`. | WARNING |

*Note: New rules can be easily added by implementing a new `CUDAParserVisitor` in `src/infrastructure/rules/` and registering it in `src/infrastructure/cli/main.py`.*

## Architecture

This project strictly adheres to Clean Architecture:

- **Domain (`src/domain/`)**: Contains core entities (`CodeSmell`, `Position`) and abstract ports (`CodeAnalyzerPort`). Contains NO dependencies on ANTLR or the CLI.
- **Application (`src/application/`)**: Contains Use Cases (`AnalyzeFileUseCase`, `AnalyzeDirectoryUseCase`) that orchestrate the analysis workflow.
- **Infrastructure (`src/infrastructure/`)**: 
  - **CLI**: The command-line interface (`main.py`).
  - **Parsers**: `AntlrCudaAnalyzer`, an adapter that implements `CodeAnalyzerPort` and encapsulates the ANTLR parsing logic.
  - **Rules**: Specific ANTLR visitors that traverse the AST to find code smells.

## Setup and Installation

1. **Clone the repository:**
   Ensure you initialize the submodules to fetch the ANTLR grammar.
   ```bash
   git clone --recursive <repository-url>
   cd <repository-dir>
   ```

2. **Set up a Python Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install antlr4-python3-runtime==4.13.2
   ```

4. **(Optional) Re-generate the ANTLR Parser:**
   If you modify the grammar in `parser/*.g4`, regenerate the Python parser using the `antlr4` tool:
   ```bash
   cd parser
   antlr4 -Dlanguage=Python3 -visitor CUDALexer.g4 CUDAParser.g4
   ```

## Usage

Activate your virtual environment before running the tool:

```bash
source venv/bin/activate
```

### Analyze a Single File
```bash
python src/infrastructure/cli/main.py smells-file <path_to_file.cu>
```

### Analyze a Directory
Recursively scans for `.cu` and `.cuh` files.
```bash
python src/infrastructure/cli/main.py smells-dir <path_to_directory>
```

### Example Output

```text
[CRITICAL] UncheckedCudaAPI at test.cu:6:4
    CUDA API call 'cudaMalloc' is potentially unchecked. Always check the return value of CUDA API calls.

[WARNING] PotentialMemoryLeak at test.cu:0:0
    Found 1 'cudaMalloc' calls but only 0 'cudaFree' calls in file.
```
