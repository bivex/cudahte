#include <stdio.h>
#include <cuda.h>

void doSomething() {
    int *d_a;
    cudaMalloc(&d_a, 100);
    // Missing free!
    // No error check!
}

int main() {
    doSomething();
    return 0;
}
