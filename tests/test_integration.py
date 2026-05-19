import unittest
import os
import sys
import subprocess

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestIntegration(unittest.TestCase):
    def test_pmp_book_analysis(self):
        """Run the analyzer on test_pmp_book.cu and check for expected smells."""
        cmd = [
            sys.executable, "-m", "src.infrastructure.cli.main",
            "smells-file", "test_pmp_book.cu"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        output = result.stdout
        
        # Check for at least one critical, warning and info
        self.assertIn("[CRITICAL] MissingBoundsCheckInKernel", output)
        self.assertIn("[CRITICAL] MissingSyncthreadsAfterSharedWrite", output)
        self.assertIn("[WARNING] IncorrectGridDimensionCalculation", output)
        self.assertIn("[WARNING] SharedMemoryUninitializedForAtomics", output)
        self.assertIn("[WARNING] ConstantMemoryWrongCopyMethod", output)
        self.assertIn("[WARNING] GlobalAtomicWithoutSharedIntermediate", output)
        self.assertIn("[WARNING] SynchronousMemcpyWithActiveStreams", output)
        self.assertIn("[INFO] MissingRestrictOnKernelPointers", output)
        self.assertIn("[WARNING] NonPowerOf2ReductionBlock", output)
        self.assertIn("[WARNING] CudaEventResourceLeak", output)

if __name__ == '__main__':
    unittest.main()
