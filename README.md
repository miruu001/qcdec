# qcdec
Quantum Counting algorithm project - course project for QCDEC

## How it works
The project implements Quantum Counting, which estimates how many marked items exist in a database before running Grover’s search. The algorithm uses Quantum Phase Estimation on the Grover operator, then decodes the measured phase into an estimate of M, the number of solutions.

## Project structure
1. A phase oracle subcircuit - circuit1.qasm
2. A diffusion subcircuit -  circuit2.qasm
3. A full Quantum Counting circuit -  circuit3.qasm
4. Composer screenshots showing the implemented circuits - circuit1.png, circuit2.png & circuit3.png
5. A Python/Qiskit simulation used to decode the measured result - quantum_counting.py
