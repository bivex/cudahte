#include <cuda.h>

__global__ void myKernel() {}

void test() {
    myKernel<<<1, 32>>>();
}
