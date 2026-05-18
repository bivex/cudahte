#include <stdio.h>
#include <cuda.h>

__global__ void myKernel() {
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
    
    for (int i = 0; i < 10; i++) {
        cudaMemcpy(d_a, d_a, 100, cudaMemcpyHostToDevice); // Host-Device Transfer inside loop
        myKernel<<<1, 32>>>(); // Suboptimal Block & Grid AND Kernel launch inside loop
        cudaDeviceSynchronize(); // Synchronize inside hot path loop
    }
}

int main() {
    doSomething();
    return 0;
}
