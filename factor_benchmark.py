"""
Project: The Computational Asymmetry of Integer Factorization
Author: Avinash Kumar Thakur (IISER Thiruvananthapuram)
Description: A research-grade benchmark comparing Brute Force (Trial Division) 
             vs. Probabilistic Algorithms (Pollard's Rho) vs. Hardware Optimization (Numba).
"""

import time
import os
import math
import random
import matplotlib.pyplot as plt
from Crypto.Util import number
from numba import jit

# ==========================================
# PART 1: ALGORITHMS IMPLEMENTATION
# ==========================================

def trial_division_python(n):
    """
    [Baseline] Standard Trial Division.
    Complexity: O(sqrt(n))
    
    Description:
    Checks every odd number up to the square root of n. 
    Limited by the Python interpreter's speed (Global Interpreter Lock).
    """
    if n % 2 == 0: return 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return i
        i += 2
    return n

@jit(nopython=True)
def trial_division_numba(n):
    """
    [Hardware Optimization] Numba JIT Trial Division.
    Complexity: O(sqrt(n))
    
    Description:
    Identical math to the Python version, but compiled to Machine Code 
    (LLVM) just-in-time. This runs near C++ speeds but suffers from 
    the same exponential time complexity wall.
    """
    if n % 2 == 0: return 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return i
        i += 2
    return n

def pollards_rho(n):
    """
    [Algorithmic Optimization] Pollard's Rho.
    Complexity: O(n^(1/4))
    
    Description:
    Uses the Birthday Paradox and Floyd's Cycle-Finding Algorithm.
    Instead of checking every number, it looks for a collision in a 
    pseudo-random sequence x = (x^2 + c) % n.
    """
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3
    
    # Retry Mechanism: If the random sequence fails (finds no factor), 
    # we try again with a different random 'c' parameter.
    # This makes the algorithm robust for research use.
    max_retries = 5
    for _ in range(max_retries):
        x = random.randint(2, n - 1)
        y = x
        c = random.randint(1, n - 1)
        g = 1
        
        while g == 1:
            # Tortoise moves 1 step
            x = (pow(x, 2, n) + c) % n
            
            # Hare moves 2 steps
            y = (pow(y, 2, n) + c) % n
            y = (pow(y, 2, n) + c) % n
            
            # Check for collision (common factor)
            g = math.gcd(abs(x - y), n)
            
            if g == n: 
                # Sequence cycle failed (loop found without factor), break to retry
                break
            if g > 1:
                return g # Factor found!
                
    return n # Failed to factor (likely prime or needs more retries)

# ==========================================
# PART 2: BENCHMARKING ENGINE
# ==========================================

def run_research_benchmark():
    # Setup System Info
    cpu_cores = os.cpu_count() or 1
    print(f"System: Detected {cpu_cores} CPU Cores. Initializing Benchmark...")
    
    # Configuration
    # We test bit lengths from 16 to 52. 
    # Note: Python Trial Div will become incredibly slow > 50 bits.
    bit_lengths = list(range(16, 54, 4))
    iterations = 3  # Run each test 3 times and take average for statistical confidence
    
    # Data Storage
    results = {
        'Python_Trial': [],
        'Numba_Trial': [],
        'Pollard_Rho': []
    }

    print(f"\n{'Bits':<6} | {'Py Trial (s)':<15} | {'Numba (s)':<15} | {'Pollard Rho (s)':<15}")
    print("-" * 60)

    for b in bit_lengths:
        # Temporary lists to store the 3 runs for averaging
        t_py_list, t_nb_list, t_rho_list = [], [], []

        for i in range(iterations):
            # Generate fresh semi-prime for every iteration
            p = number.getPrime(b)
            q = number.getPrime(b)
            n = p * q
            
            # --- Warm-up Numba ---
            # JIT compilation takes time on the very first run. 
            # We run a dummy call once before starting the timer for the first batch.
            if b == bit_lengths[0] and i == 0:
                trial_division_numba(n)

            # --- Measure Python Trial ---
            t0 = time.perf_counter()
            trial_division_python(n)
            t_py_list.append(time.perf_counter() - t0)

            # --- Measure Numba Trial ---
            t0 = time.perf_counter()
            trial_division_numba(n)
            t_nb_list.append(time.perf_counter() - t0)

            # --- Measure Pollard's Rho ---
            t0 = time.perf_counter()
            pollards_rho(n)
            t_rho_list.append(time.perf_counter() - t0)

        # Calculate Averages
        avg_py = sum(t_py_list) / iterations
        avg_nb = sum(t_nb_list) / iterations
        avg_rho = sum(t_rho_list) / iterations

        results['Python_Trial'].append(avg_py)
        results['Numba_Trial'].append(avg_nb)
        results['Pollard_Rho'].append(avg_rho)

        print(f"{b:<6} | {avg_py:<15.6f} | {avg_nb:<15.6f} | {avg_rho:<15.6f}")

    # ==========================================
    # PART 3: VISUALIZATION & OUTPUT
    # ==========================================
    
    plt.figure(figsize=(12, 7))
    
    # Plotting
    plt.plot(bit_lengths, results['Python_Trial'], label='Pure Python (O(√n))', marker='o', color='red', linestyle='--')
    plt.plot(bit_lengths, results['Numba_Trial'], label='Hardware Optimized (O(√n))', marker='s', color='orange')
    plt.plot(bit_lengths, results['Pollard_Rho'], label="Pollard's Rho (O(n¹/⁴))", marker='^', color='green', linewidth=2)

    # Styling for Research Paper quality
    plt.yscale('log') # Crucial for showing exponential growth differences
    plt.xlabel('Key Strength (Bit Length of p, q)', fontsize=12)
    plt.ylabel('Execution Time (Seconds) - Log Scale', fontsize=12)
    plt.title('Cryptanalysis Benchmark: Hardware vs. Algorithmic Efficiency', fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, which="both", ls="-", alpha=0.3)
    
    # Saving Logic
    output_filename = 'crypto_benchmark_results.png'
    output_path = os.path.join(os.getcwd(), output_filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    
    print(f"\n[Success] Benchmark complete.")
    print(f"Graph saved to: {output_path}")
    plt.show()

if __name__ == "__main__":
    run_research_benchmark()