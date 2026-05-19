# Tests for CUDA Code Smells Analyzer

This directory contains unit and integration tests for the CUDA Code Smells Analyzer.

## Running Tests

Ensure you have the virtual environment activated:

```bash
source venv/bin/activate
```

### Run All Tests
You can run all tests using `unittest` discovery:

```bash
python3 -m unittest discover tests
```

### Run Specific Test Files
```bash
python3 tests/test_new_rules.py
python3 tests/test_integration.py
```

## Test Structure

- `test_new_rules.py`: Unit tests for the 10 recently added rules using code snippets.
- `test_integration.py`: Integration test that runs the full CLI analyzer against `test_pmp_book.cu`.
- `test_pmp_book.cu`: A collection of CUDA code examples from the "Programming Massively Parallel Processors" book used for integration testing.
