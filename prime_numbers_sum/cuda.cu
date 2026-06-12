/*
File: cuda.cu
Author: Eduardo Hernández Alonso
*/

#include <iostream>
#include <iomanip>
#include <chrono>
#include <algorithm>
#include <cuda_runtime.h>

using namespace std;
using namespace std::chrono;

#define SIZE 5000000
#define THREADS 512
#define BLOCKS 32
#define N 10

__device__ bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; (long long)i * i <= n; i++) {
        if (n % i == 0) return false;
    }
    return true;
}

__global__ void sumPrimes(long long *results) {
    __shared__ long long cache[THREADS];

    int tid = threadIdx.x + (blockIdx.x * blockDim.x);
    int cacheIndex = threadIdx.x;

    long long acum = 0;
    while (tid < SIZE) {
        if (isPrime(tid)) {
            acum += tid;
        }

        tid += blockDim.x * gridDim.x;
    }

    cache[cacheIndex] = acum;

    __syncthreads();

    int i = blockDim.x / 2;
    while (i > 0) {
        if (cacheIndex < i) {
            cache[cacheIndex] += cache[cacheIndex + i];
        }
        __syncthreads();
        i /= 2;
    }

    if (cacheIndex == 0) {
        results[blockIdx.x] = cache[cacheIndex];
    }
}

int main(int argc, char *argv[]) {
    long long *results, *d_r;

    high_resolution_clock::time_point start, end;
    double timeElapsed;

    results = new long long[BLOCKS];

    cudaMalloc((void **)&d_r, BLOCKS * sizeof(long long));

    cout << "Starting...\n";
    timeElapsed = 0;
    for (int j = 0; j < N; j++) {
        start = high_resolution_clock::now();

        sumPrimes<<<BLOCKS, THREADS>>>(d_r);

        end = high_resolution_clock::now();
        timeElapsed +=
            duration<double, std::milli>(end - start).count();
    }

    cudaMemcpy(results, d_r, BLOCKS * sizeof(long long), cudaMemcpyDeviceToHost);

    long long sum = 0;
    for (int i = 0; i < BLOCKS; i++) {
        sum += results[i];
    }

    cout << "sum of primes below " << SIZE << " = " << sum << std::endl;
    cout << "avg time = " << fixed << setprecision(3)
         << (timeElapsed / N) << " ms" << std::endl;

    cudaFree(d_r);

    delete[] results;

    return 0;
}