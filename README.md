#  The Computational Asymmetry of Integer Factorization

[![Language](https://img.shields.io/badge/Language-Python%203.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Optimization](https://img.shields.io/badge/Optimization-Numba%20JIT-orange.svg)](http://numba.pydata.org/)

**Author:** Avinash Kumar Thakur  
**Institution:** IISER Thiruvananthapuram (BS-MS Dual Degree)  
**Research Area:** Cryptography & Computational Number Theory

---

##  Abstract
The security of the **RSA cryptosystem** relies fundamentally on the intractability of the **Integer Factorization Problem** (IFP). This project provides an empirical analysis of the "Computational Gap" between key generation (polynomial time) and key breaking (exponential time). 

By benchmarking **Hardware Acceleration (Numba JIT)** against **Algorithmic Efficiency (Pollard's Rho)**, this study demonstrates that while hardware improvements offer linear speedups, only probabilistic algorithms can effectively reduce the time complexity class of the problem.

---

##  Algorithms Analyzed

### 1. Trial Division (Baseline)
The deterministic brute-force approach. It checks every odd integer $i$ such that $3 \le i \le \sqrt{n}$.
* **Complexity:** $O(\sqrt{n})$ or $O(2^{k/2})$ where $k$ is the bit-length.
* **Limitation:** Becomes computationally infeasible for $n > 50$ bits on standard hardware.

### 2. Numba-Accelerated Trial Division (Hardware Optimization)
Utilizes **Just-In-Time (JIT)** compilation to convert Python bytecode into optimized machine code (LLVM).
* **Speedup:** ~100x faster than pure Python.
* **Insight:** Despite the speedup, the complexity remains $O(\sqrt{n})$. The curve is steeper, but the "wall" is hit at the same complexity class.

### 3. Pollard's Rho Algorithm (Algorithmic Optimization)
A probabilistic algorithm introduced by John Pollard (1975). It utilizes the **Birthday Paradox** to find a factor by detecting a cycle in the pseudo-random sequence $x_{i+1} \equiv (x_i^2 + c) \pmod n$.
* **Complexity:** Expected time $O(n^{1/4})$.
* **Significance:** This represents a fundamental shift in algorithmic power, capable of factoring numbers significantly larger than Trial Division.

---

## Results & Visualization

The benchmark compares execution time across bit-lengths ranging from **16-bit to 54-bit** semi-primes.

![Benchmark Graph](https://github.com/Avinash001003/Factorization-Complexity-Benchmark/blob/main/factor_asymmetry.png)
*(Figure 1: Log-scale comparison showing the divergence between Exponential Growth (Trial Division) and Heuristic Search (Pollard's Rho).)*

### Key Observations:
1.  **The Divergence Point:** At ~32 bits, Pollard's Rho begins to outperform even the hardware-accelerated Trial Division.
2.  **The Slope:** On a logarithmic scale, the slope of Pollard's Rho is significantly flatter ($0.25$ slope vs $0.5$ slope), validating the theoretical complexity gap.

---

##  Reproduction Steps

### 1. Prerequisites
Ensure the environment is set up for high-performance computing.
```bash
pip install -r requirements.txt
# Or install manually:
pip install numba pycryptodome matplotlib
