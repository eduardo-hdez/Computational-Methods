/* 
File: sequential.cpp
Author: Eduardo Hernández Alonso
*/

#include <iostream>
#include <iomanip>
#include <cmath>
#include <chrono>

using namespace std;
using namespace std::chrono;

#define SIZE 5000000
#define N    10

bool isPrime(int n) {
    if (n < 2) return false;
    for (int i = 2; i <= sqrt(n); i++) {
        if (n % i == 0) return false;
    }
    return true;
}

int main(int argc, char* argv[]) {
    long long sum;

    high_resolution_clock::time_point startTime, endTime;
    double timeElapsed;

    cout << "Starting...\n";
    timeElapsed = 0;
    for (int j = 0; j < N; j++) {
        sum = 0;
        startTime = high_resolution_clock::now();

        for (int n = 2; n < SIZE; n++) {
            if (isPrime(n)) sum += n;
        }

        endTime = high_resolution_clock::now();
        timeElapsed +=
            duration<double, milli>(endTime - startTime).count();
    }

    cout << "Sum of primes below 5,000,000: " << sum << std::endl;
    cout << "avg time = " << fixed << setprecision(3)
         << (timeElapsed / N) << std::endl;

    return 0;
}