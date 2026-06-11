/*
File: threads.cpp
Author: Eduardo Hernández Alonso
*/

#include <iostream>
#include <iomanip>
#include <cmath>
#include <chrono>
#include <thread>
#include <vector>

using namespace std;
using namespace std::chrono;

#define SIZE 5000000

bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i <= sqrt(n); i++) {
        if (n % i == 0) return false;
    }
    return true;
}

void sumPrimesInBlock(int start, int end, long long &partialSum) {
    long long sum = 0;
    for (int n = start; n < end; n++) {
        if (isPrime(n)) sum += n;
    }
    partialSum = sum;
}

long long parallelSum(int size, unsigned int numThreads) {
    vector<thread> threads;
    vector<long long> partialSums(numThreads, 0);

    int chunkSize = size / numThreads;

    for (unsigned int i = 0; i < numThreads; i++) {
        int start = 2 + i * chunkSize;
        int end = (i == numThreads - 1) ? size : start + chunkSize;
        threads.emplace_back(sumPrimesInBlock, start, end, ref(partialSums[i]));
    }

    for (auto &t : threads) {
        t.join();
    }

    long long sum = 0;
    for (long long partial : partialSums) {
        sum += partial;
    }

    return sum;
}

int main(int argc, char* argv[]) {
    long long sum;

    high_resolution_clock::time_point startTime, endTime;
    double timeElapsed;

    cout << "Starting...\n";
    startTime = high_resolution_clock::now();

    unsigned int numThreads = thread::hardware_concurrency();

    sum = parallelSum(SIZE, numThreads);

    endTime = high_resolution_clock::now();
    timeElapsed = duration<double, milli>(endTime - startTime).count();

    cout << "Number of threads used: " << numThreads << std::endl;
    cout << "Sum of primes below 5,000,000: " << sum << std::endl;
    cout << "time = " << fixed << setprecision(3)
         << timeElapsed << " ms" << std::endl;

    return 0;
}
