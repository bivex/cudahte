#include <stdio.h>
#include <cuda.h>

volatile int flag = 0; // Volatile usage smell

__global__ void myKernel() {
    __shared__ float huge_arr[16384]; // Large shared memory allocation smell

    // Integer overflow in index
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    
    // Warp Divergence
    if (threadIdx.x % 2 == 0) {
        printf("Even\n");
        // Syncthreads in divergent code -> Deadlock
        __syncthreads();
    } else {
        printf("Odd\n");
    }

    // Double usage
    double d_val = 1.0;
    
    // Slow math function
    float result = sin(d_val);
}

void doSomething() {
    int *d_a;
    cudaMalloc(&d_a, 100); // Unchecked API & Mem Leak
    
    // Missing cudaGetLastError check below (MissingKernelErrorCheck)
    myKernel<<<1, 30>>>(); // Suboptimal Block (not multiple of 32)
    
    for (int i = 0; i < 10; i++) {
        cudaMemcpyAsync(d_a, d_a, 100, cudaMemcpyHostToDevice, 0); // Default stream usage
        myKernel<<<1, 32, 0, 0>>>( ); // Default stream usage explicitly
        myKernel<<<1, 32>>>( ); // Default stream usage implicitly
        cudaDeviceSynchronize(); // Synchronize inside hot path loop
    }
}

int main() {
    cudaSetDevice(0); // Hardcoded device ID
    cudaThreadSynchronize(); // Deprecated API
    doSomething();
    return 0;
}
