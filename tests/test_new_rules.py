import unittest
import os
import sys
import textwrap
from antlr4 import InputStream, CommonTokenStream

# Add project root and parser to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'parser')))

from CUDALexer import CUDALexer
from CUDAParser import CUDAParser
from src.infrastructure.rules.missing_bounds_check_rule import MissingBoundsCheckRule
from src.infrastructure.rules.missing_syncthreads_shared_rule import MissingSyncthreadsAfterSharedWriteRule
from src.infrastructure.rules.incorrect_grid_dimension_rule import IncorrectGridDimensionRule
from src.infrastructure.rules.shared_memory_uninitialized_atomic_rule import SharedMemoryUninitializedAtomicRule
from src.infrastructure.rules.constant_memory_copy_rule import ConstantMemoryCopyRule
from src.infrastructure.rules.global_atomic_contention_rule import GlobalAtomicContentionRule
from src.infrastructure.rules.sync_memcpy_with_streams_rule import SyncMemcpyWithStreamsRule
from src.infrastructure.rules.missing_restrict_rule import MissingRestrictOnKernelPointersRule
from src.infrastructure.rules.non_power_of_2_reduction_rule import NonPowerOf2ReductionBlockRule
from src.infrastructure.rules.cuda_event_leak_rule import CudaEventLeakRule

class TestNewRules(unittest.TestCase):
    def _get_tree(self, code):
        input_stream = InputStream(code)
        lexer = CUDALexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = CUDAParser(stream)
        return parser.translationUnit()

    def _analyze(self, rule_class, code):
        code = textwrap.dedent(code).strip()
        tree = self._get_tree(code)
        rule = rule_class("test.cu")
        # Ensure all rules have the source
        rule.source_text = code
        rule.source_lines = code.split('\n')
        rule.visit(tree)
        return rule.get_smells()

    def test_missing_bounds_check(self):
        code = """
        __global__ void kernel(float* data, int n) {
            int tid = threadIdx.x + blockIdx.x * blockDim.x;
            data[tid] = 1.0f; // Missing bounds check
        }
        """
        smells = self._analyze(MissingBoundsCheckRule, code)
        self.assertTrue(any("bounds check" in s.description for s in smells))

    def test_missing_syncthreads(self):
        code = """
        __global__ void kernel(float* data) {
            __shared__ float sdata[256];
            sdata[threadIdx.x] = data[threadIdx.x];
            float val = sdata[threadIdx.x + 1]; // Missing __syncthreads()
        }
        """
        smells = self._analyze(MissingSyncthreadsAfterSharedWriteRule, code)
        self.assertTrue(any("syncthreads" in s.description for s in smells))

    def test_incorrect_grid_dim(self):
        code = """
        void launch() {
            dim3 grid(N / 256); // Incorrect grid dim
            for (int i = 0; i < N / 256; ++i) {
                // This division inside a loop should be IGNORED by the rule
            }
        }
        """
        smells = self._analyze(IncorrectGridDimensionRule, code)
        self.assertTrue(any("integer division" in s.description for s in smells))
        # Ensure only 1 smell is found (the one in dim3, not the one in for loop)
        self.assertEqual(len(smells), 1)

    def test_shared_mem_uninit_atomic(self):
        code = """
        __global__ void kernel(int* data) {
            __shared__ int counter[1];
            atomicAdd(&counter[0], 1); // Uninitialized shared atomic
        }
        """
        smells = self._analyze(SharedMemoryUninitializedAtomicRule, code)
        self.assertTrue(any("zero-initialization" in s.description for s in smells))

    def test_constant_mem_copy(self):
        code = """
        __constant__ float c_data[256];
        void host() {
            cudaMemcpy(c_data, h_data, 256, cudaMemcpyHostToDevice); // Wrong copy method
        }
        """
        smells = self._analyze(ConstantMemoryCopyRule, code)
        self.assertTrue(any("cudaMemcpyToSymbol" in s.description for s in smells))

    def test_global_atomic_contention(self):
        code = """
        __global__ void kernel(int* global_counter) {
            atomicAdd(global_counter, 1); // Global atomic contention
        }
        """
        smells = self._analyze(GlobalAtomicContentionRule, code)
        self.assertTrue(any("shared memory intermediate" in s.description for s in smells))

    def test_sync_memcpy_with_streams(self):
        code = """
        void host() {
            cudaStream_t s;
            cudaStreamCreate(&s);
            cudaMemcpy(d, h, n, cudaMemcpyHostToDevice); // Sync memcpy with active stream
        }
        """
        smells = self._analyze(SyncMemcpyWithStreamsRule, code)
        self.assertTrue(any("Synchronous 'cudaMemcpy' used when CUDA streams are active" in s.description for s in smells))

    def test_missing_restrict(self):
        code = """
        __global__ void kernel(float* a, float* b, float* c) {
            // Missing __restrict__ (This comment used to break the test!)
        }
        """
        smells = self._analyze(MissingRestrictOnKernelPointersRule, code)
        self.assertTrue(any("__restrict__" in s.description for s in smells))

    def test_non_power_of_2_reduction(self):
        code = """
        __global__ void kernel() {
            __shared__ float sdata[100]; // Non power of 2
            for (int i = 50; i > 0; i >>= 1) {
                sdata[threadIdx.x] += sdata[threadIdx.x + i];
            }
        }
        """
        smells = self._analyze(NonPowerOf2ReductionBlockRule, code)
        self.assertTrue(any("not a power of 2" in s.description for s in smells))

    def test_cuda_event_leak(self):
        code = """
        void host() {
            cudaEvent_t e;
            cudaEventCreate(&e);
            // Missing cudaEventDestroy
        }
        """
        smells = self._analyze(CudaEventLeakRule, code)
        self.assertTrue(any("cudaEventDestroy" in s.description for s in smells))

if __name__ == '__main__':
    unittest.main()
