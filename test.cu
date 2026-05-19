#include <stdio.h>
#include <cuda.h>

volatile int flag = 0; // Volatile usage smell

// Step 12: Constant memory
__constant__ float const_data[256];

__global__ void myKernel(float* data) {
    // Uncoalesced Memory Access smell
    data[threadIdx.x * 32] = 1.0f;

    __shared__ float s_data[1024];
    s_data[threadIdx.x * 32] = 0.0f; // Bank Conflict

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

// Step 8: Missing bounds check in kernel
__global__ void addKernel(int *a, int *b, int *c) {
    int tid = threadIdx.x + blockIdx.x * blockDim.x;
    c[tid] = a[tid] + b[tid]; // No bounds check!
}

// Step 9: Missing __syncthreads after shared write
__global__ void sharedWriteKernel(float* output) {
    __shared__ float cache[256];
    cache[threadIdx.x] = threadIdx.x * 2.0f;
    // Missing __syncthreads() here!
    output[blockIdx.x * blockDim.x + threadIdx.x] = cache[255 - threadIdx.x];
}

// Step 11: Shared memory uninitialized for atomics
__global__ void histoKernel(unsigned char* buffer, unsigned int* histo, int size) {
    __shared__ unsigned int temp[256];
    // Missing: temp[threadIdx.x] = 0;
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    int stride = blockDim.x * gridDim.x;
    while (i < size) {
        atomicAdd(&temp[buffer[i]], 1);
        i += stride;
    }
    __syncthreads();
    atomicAdd(&(histo[threadIdx.x]), temp[threadIdx.x]);
}

// Step 13: Global atomic without shared intermediate
__global__ void badHistoKernel(unsigned char* buffer, unsigned int* histo, int size) {
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    int stride = blockDim.x * gridDim.x;
    while (i < size) {
        atomicAdd(&(histo[buffer[i]]), 1); // Direct global atomic - contention!
        i += stride;
    }
}

void doSomething() {
    int *d_a;
    cudaMallocManaged(&d_a, 100); // Managed memory without prefetch
    cudaMalloc(&d_a, 100); // Unchecked API & Mem Leak

    // Step 12: Constant memory wrong copy method
    float host_data[256];
    cudaMemcpy(const_data, host_data, sizeof(float) * 256, cudaMemcpyHostToDevice); // Wrong!

    // Step 14: Synchronous memcpy with active streams
    cudaStream_t stream1;
    cudaStreamCreate(&stream1);
    cudaMemcpy(d_a, d_a, 100, cudaMemcpyHostToDevice); // Sync copy with streams active!

    // Missing cudaGetLastError check below (MissingKernelErrorCheck)
    myKernel<<<1, 30>>>(); // Suboptimal Block (not multiple of 32)

    // Step 10: Incorrect grid dimension calculation
    int N = 1000;
    int blocks = N / 256; // Wrong: rounds down, should be (N + 255) / 256

    // Step 17: Event resource leak
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start, 0);
    cudaEventRecord(stop, 0);
    cudaEventSynchronize(stop);
    // Missing: cudaEventDestroy(start);
    // Missing: cudaEventDestroy(stop);

    for (int i = 0; i < 10; i++) {
        cudaMemcpyAsync(d_a, d_a, 100, cudaMemcpyHostToDevice, 0); // Default stream usage
        myKernel<<<1, 32, 0, 0>>>( ); // Default stream usage explicitly
        myKernel<<<1, 32>>>( ); // Default stream usage implicitly
        cudaDeviceSynchronize(); // Synchronize inside hot path loop
    }

    cudaStreamDestroy(stream1);
}

// Step 16: Non-power-of-2 reduction block size
#define REDUCE_BLOCK_SIZE 100
__global__ void reduceKernel(float* input, float* output, int N) {
    __shared__ float sdata[100];
    int tid = threadIdx.x;
    int i = blockIdx.x * blockDim.x + tid;
    sdata[tid] = 0.0f;
    while (i < N) {
        sdata[i] += input[i];
        i += blockDim.x;
    }
    __syncthreads();
    for (int s = blockDim.x / 2; s > 0; s >>= 1) {  // Non-power-of-2: 100/2=50, 50/2=25...
        if (tid < s) sdata[tid] += sdata[tid + s];
        __syncthreads();
    }
    if (tid == 0) output[blockIdx.x] = sdata[0];
}

int main() {
    cudaSetDevice(0); // Hardcoded device ID
    cudaThreadSynchronize(); // Deprecated API
    doSomething();
    return 0;
}
