# Technical Report: Parallel Prime Sum

## Introduction

This project implements in C++ and CUDA three versions of a program that computes the sum of all prime numbers below 5,000,000. The first version performs the computation sequentially, the second parallelizes it using C++ threads, and the third parallelizes it using CUDA. All three versions produce the same result: 838,596,693,108.

## Implementation

The solution divides the problem into three implementations that share the same `isPrime` function, which determines whether a number `n` is prime by iterating from 2 up to √n and returning false if any exact divisor is found, or true if the loop completes normally.

The sequential version traverses all integers from 2 to 4,999,999 linearly, checking each one and accumulating the sum. The threaded version divides the range into equal-sized blocks and assigns each block to a distinct thread using `std::thread`, relying on `thread::hardware_concurrency()` to make use of all available cores. Each thread accumulates its partial sum independently and the results are combined at the end. The CUDA version distributes the work across 32 blocks of 512 threads each, using shared memory and a parallel reduction within each block to combine results before writing them to global memory.

## Results

Execution times measured on a MacBook Pro with an M4 Pro chip (14 cores) are as follows:

| Version    | Execution Time | Cores / Threads Used |
| ---------- | -------------- | -------------------- |
| Sequential | 1,222.509 ms   | 1                    |
| Threads    | 152.653 ms     | 14                   |
| CUDA       | 0.014 ms       | 32 × 512 = 16,384    |

The speedup S_p = T_1 / T_p is calculated for each parallel version:

- Threads (p = 14): S_14 = 1,222.509 ms / 152.653 ms ≈ **8.01×**
- CUDA (p = 16,384): S_16384 = 1,222.509 ms / 0.014 ms ≈ **87,322×**

## Analysis

The C++ threaded version achieves a speedup of approximately 8× using 14 cores. Although all available cores were utilized, the observed speedup is roughly equivalent to half the number of threads used, which indicates that the parallelism is not perfect. This is mainly due to two reasons. The first is thread overhead: the time the operating system spends creating each thread, allocating resources, and synchronizing it at the end before combining the results. The second is load imbalance, since larger numbers require more iterations in `isPrime`, threads assigned to higher ranges finish later than the rest, leaving cores idle while they wait.

The CUDA version outperforms both other versions with a speedup of approximately 87,322× over the sequential baseline. This difference in orders of magnitude is explained by the massively parallel execution model of the GPU, which launches 16,384 threads simultaneously. To make full use of that compute, each thread does not limit itself to evaluating a single number; using a stride pattern, each thread processes multiple numbers separated by the total grid size (`blockDim.x * gridDim.x = 16,384`), advancing value by value until the entire range of 5,000,000 numbers is covered. This ensures that no thread remains idle and that the workload is distributed uniformly across all of them. Once each thread accumulates its partial sum, the results are combined within each block through a tree reduction over shared memory, combining results in pairs iteratively until a single value per block is obtained. Finally, the 32 partial results are transferred to the CPU and summed to produce the final result.

## Conclusion

CUDA offers a dramatically superior performance for this type of element-independent computation. However, it is important to note that CUDA's advantage is particularly pronounced here because the problem is highly parallelizable, each number can be evaluated completely independently of all others. For problems with stronger data dependencies or complex control flow, the performance difference between these two technologies could be considerably smaller.

## Use of Generative AI

Generative AI was used as a support tool during the development of this project. Development was limited to the topics covered in class. The use of this tool represented a change in the way problems are solved, as it was possible to obtain clear explanations and detect errors efficiently.
