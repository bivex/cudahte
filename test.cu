#include <stdio.h>
#include <cuda.h>

__global__ void myKernel() {
    int threadId = threadIdx.x;
    
    // Warp Divergence
    if (threadIdx.x % 2 == 0) {
        printf("Even\n");
    } else {
        printf("Odd\n");
    }
}

void doSomething() {
    int *d_a;
    cudaMalloc(&d_a, 100); // Unchecked API & Mem Leak
    
    for (int i = 0; i < 10; i++) {
        cudaMemcpy(d_a, d_a, 100, cudaMemcpyHostToDevice); // Host-Device Transfer inside loop
        myKernel<<<1, 32>>>(); // Suboptimal Block & Grid
        cudaDeviceSynchronize(); // Synchronize inside hot path loop
    }
}

int main() {
    doSomething();
    return 0;
}
