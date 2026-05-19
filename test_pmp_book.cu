// ============================================================
// PMP Book — Figure 3.11: MatrixMulKernel (MissingRestrict, MissingBoundsCheck)
// Kirk & Hwu, "Programming Massively Parallel Processors" (2010), p.55 Fig 3.11
// ============================================================
__global__ void MatrixMulkernel(float* Md, float* Nd, float* Pd, int Width)
{
    int tx = threadIdx.x;
    int ty = threadIdx.y;
    float Pvalue = 0.0f;
    for (int k = 0; k < Width; ++k)
    {
        float Mdelement = Md[ty * Width + k];
        float Ndelement = Nd[k * Width + tx];
        Pvalue += Mdelement * Ndelement;
    }
    Pd[ty * Width + tx] = Pvalue;
}

// ============================================================
// PMP Book — Figure 5.7: Tiled MatrixMulKernel
// Kirk & Hwu, p.88 Fig 5.7  |
// ============================================================
#define TILE_WIDTH 16
__global__ void MatrixMulKernelTiled(float* Md, float* Nd, float* Pd, int Width)
{
    __shared__ float Mds[TILE_WIDTH][TILE_WIDTH];
    __shared__ float Nds[TILE_WIDTH][TILE_WIDTH];
    int bx = blockIdx.x;  int by = blockIdx.y;
    int tx = threadIdx.x; int ty = threadIdx.y;
    int Row = by * TILE_WIDTH + ty;
    int Col = bx * TILE_WIDTH + tx;
    float Pvalue = 0.0f;
    for (int m = 0; m < Width / TILE_WIDTH; ++m)
    {
        Mds[ty][tx] = Md[Row*Width + (m*TILE_WIDTH + tx)];
        Nds[ty][tx] = Nd[(m*TILE_WIDTH + ty)*Width + Col];
        __syncthreads();
        for (int k = 0; k < TILE_WIDTH; ++k)
            Pvalue += Mds[ty][k] * Nds[k][tx];
        __syncthreads();
    }
    Pd[Row*Width + Col] = Pvalue;
}

// ============================================================
// PMP Book — Figure 6.2: Simple reduction kernel
// Kirk & Hwu, p.102 Fig 6.2
// BUG: __shared__ not explicitly zeroed (only first write = g_idata[...])
//      Uses stride *= 2 stop at blockDim.x — assumes blockDim is power-of-2
// ============================================================
__global__ void reduceKernelFig6_2(float* g_idata, float* g_odata, unsigned int n)
{
    __shared__ float partialSum[256];
    unsigned int t = threadIdx.x;
    partialSum[t] = g_idata[blockIdx.x * blockDim.x + t];
    for (unsigned int stride = 1; stride < blockDim.x; stride *= 2)
    {
        __syncthreads();
        if (t % (2 * stride) == 0)
            partialSum[t] += partialSum[t + stride];
    }
    if (t == 0) g_odata[blockIdx.x] = partialSum[0];
}

// ============================================================
// PMP Book — Figure 6.4: Better reduction kernel
// Kirk & Hwu, p.103 Fig 6.4 — stride >>= 1 variant
// ============================================================
__global__ void reduceKernelFig6_4(float* g_idata, float* g_odata, unsigned int n)
{
    __shared__ float partialSum[256];
    unsigned int t = threadIdx.x;
    partialSum[t] = g_idata[blockIdx.x * blockDim.x + t];
    for (unsigned int stride = blockDim.x / 2; stride > 0; stride >>= 1)
    {
        __syncthreads();
        if (t < stride)
            partialSum[t] += partialSum[t + stride];
    }
    if (t == 0) g_odata[blockIdx.x] = partialSum[0];
}

// ============================================================
// PMP Book — scalarProd exercise kernel
// Kirk & Hwu, p.121 Ex 6.7 — uses shared[256] with
// blockDim=256 (= 2^8) but stride /2 loop has same NonPowerOf2 issue
// if grid size isn't power-of-2 (and shared alloc no explicit init)
// ============================================================
__global__ void scalarProd(float *d_C, float *d_A, float *d_B, int ElementN)
{
    __shared__ float accumResult[256];
    float *A = d_A + ElementN * blockIdx.x;
    float *B = d_B + ElementN * blockIdx.x;
    int tx = threadIdx.x;
    accumResult[tx] = A[tx] * B[tx];
    for (int stride = ElementN / 2; stride > 0; stride >>= 1)
    {
        __syncthreads();
        if (tx < stride)
            accumResult[tx] += accumResult[stride + tx];
    }
    d_C[blockIdx.x] = accumResult[0];
}

// ============================================================
// PMP Book — Exercise 6.9: "Good engineer" reduction
// Kirk & Hwu, p.122 Ex 6.9
// BUG: outer loop uses `n >> 1` (n is data size, not blockDim),
//      if caller passes non-power-of-2 n the loop stops at stride=32
//      and silently drops remainder elements.
// ============================================================
__global__ void reduceKernelGoodEng(float* data, float* result, int n)
{
    extern __shared__ float partialSum[];
    unsigned int tid = threadIdx.x;
    unsigned int i = blockIdx.x * blockDim.x + tid;
    partialSum[tid] = (i < n) ? data[i] : 0.0f;
    __syncthreads();
    for (unsigned int stride = n >> 1; stride >= 32; stride >>= 1)
    {
        __syncthreads();
        if (tid < stride)
            partialSum[tid] += partialSum[tid + stride];
    }
    __syncthreads();
    if (tid < 32)
    {
        partialSum[tid] += partialSum[tid + 16];
        partialSum[tid] += partialSum[tid + 8];
        partialSum[tid] += partialSum[tid + 4];
        partialSum[tid] += partialSum[tid + 2];
        partialSum[tid] += partialSum[tid + 1];
    }
    if (tid == 0) result[blockIdx.x] = partialSum[0];
}

// ============================================================
// PMP Book — Exercise 4.2: BlockTranspose
// Kirk & Hwu, p.75 Ex 4.2
// BUG: baseIdx computed and used with no bounds check
//      blockA write then read without intervening __syncthreads()
// ============================================================
#define BLOCK_SIZE 16
__global__ void BlockTranspose(float* A_elements, int A_width, int A_height)
{
    __shared__ float blockA[BLOCK_SIZE][BLOCK_SIZE];
    int baseIdx = blockIdx.x * BLOCK_SIZE + threadIdx.x;
    baseIdx += (blockIdx.y * BLOCK_SIZE + threadIdx.y) * A_width;
    blockA[threadIdx.y][threadIdx.x] = A_elements[baseIdx];
    A_elements[baseIdx] = blockA[threadIdx.x][threadIdx.y];
}

// ============================================================
// PMP Book — Figure 8.12: constant memory naive copy
// Kirk & Hwu, p.159 Fig 8.12 — uses cudaMemcpy() with __constant__
// (book shows this as naive approach; our rule flags it)
// ============================================================
#define CHUNK_SIZE 256
__constant__ float kx_c[CHUNK_SIZE];
__constant__ float ky_c[CHUNK_SIZE];
__constant__ float kz_c[CHUNK_SIZE];

void copy_chunk_bad(float* kx, float* ky, float* kz, int i)
{
    cudaMemcpy(kx_c, kx + i*CHUNK_SIZE, 4*CHUNK_SIZE, cudaMemcpyHostToDevice);
    cudaMemcpy(ky_c, ky + i*CHUNK_SIZE, 4*CHUNK_SIZE, cudaMemcpyHostToDevice);
    cudaMemcpy(kz_c, kz + i*CHUNK_SIZE, 4*CHUNK_SIZE, cudaMemcpyHostToDevice);
}

// Figure 8.13 kernel
__global__ void cmpFHd_kernel(
    float* rPhi, float* iPhi,
    float* rMu, float* iMu,
    float* x, float* y, float* z,
    int M, int N)
{
    int n = blockIdx.x * 128 + threadIdx.x;
    float xn_r = x[n];  float yn_r = y[n];  float zn_r = z[n];
    float rFHdn_r = rPhi[n];  float iFHdn_r = iPhi[n];
    for (int m = 0; m < M; m++) {
        float expFHd = 2.0f*3.14159f*(kx_c[m]*xn_r + ky_c[m]*yn_r + kz_c[m]*zn_r);
        rFHdn_r += rMu[m]*cosf(expFHd) - iMu[m]*sinf(expFHd);
        iFHdn_r += iMu[m]*cosf(expFHd) + rMu[m]*sinf(expFHd);
    }
    rPhi[n] = rFHdn_r;  iPhi[n] = iFHdn_r;
}

// ============================================================
// PMP Book — Figure 4.7 host code
// Kirk & Hwu, p.68 Fig 4.7 — uses integer division for grid dim
// ============================================================
void host_bad_launch(float* d_A, float* d_B, float* d_C)
{
    scalarProd<<<VECTOR_N, ELEMENT_N>>>(d_C, d_A, d_B, ELEMENT_N);
    // Fig 4.7: integer division in gridDim — rounds down, leaves elements unprocessed
    dim3 dimGrid(1024 / TILE_WIDTH, 1024 / TILE_WIDTH);
    dim3 dimBlock(TILE_WIDTH, TILE_WIDTH);
}

// ============================================================
// PMP Book — Chapter 9: Atomics
// Figure 9.3: Histogram with global atomics (GlobalAtomicContention)
// ============================================================
__global__ void histogram_kernel(unsigned char* buffer, long size, unsigned int* histo)
{
    int i = threadIdx.x + blockIdx.x * blockDim.x;
    int stride = blockDim.x * gridDim.x;
    while (i < size) {
        atomicAdd(&(histo[buffer[i]]), 1); // BUG: Global atomic contention
        i += stride;
    }
}

// ============================================================
// SharedMemoryUninitializedAtomic (implied by atomics discussion)
// ============================================================
__global__ void shared_histogram_bad(unsigned char* buffer, long size, unsigned int* histo)
{
    __shared__ unsigned int temp[256];
    // BUG: temp[threadIdx.x] is NOT initialized to zero
    atomicAdd(&temp[buffer[threadIdx.x]], 1);
    __syncthreads();
    atomicAdd(&(histo[threadIdx.x]), temp[threadIdx.x]);
}

// ============================================================
// SynchronousMemcpyWithActiveStreams
// ============================================================
void stream_memcpy_bad(float* d_A, float* h_A, int size)
{
    cudaStream_t stream;
    cudaStreamCreate(&stream);
    // ... kernel launch in stream ...
    // BUG: sync memcpy while stream is active
    cudaMemcpy(d_A, h_A, size, cudaMemcpyHostToDevice);
}

// ============================================================
// NonPowerOf2ReductionBlock
// ============================================================
__global__ void reduction_bad_size(float* data)
{
    __shared__ float sdata[100]; // BUG: 100 is not power of 2
    unsigned int t = threadIdx.x;
    for (unsigned int stride = 50; stride > 0; stride >>= 1) {
        __syncthreads();
        if (t < stride) sdata[t] += sdata[t + stride];
    }
}

// ============================================================
// CudaEventLeak
// ============================================================
void event_leak_bad()
{
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    // BUG: no cudaEventDestroy
}
