# qcdec
Quantum Counting algorithm project - course project for QCDEC

### Goal
This project shows the implementation of the Quantum Counting Algorithm in QISKIT that checks if a solution exists in the database before running Grover's algorithm.

### Files
- 'quantum_counting.py' - Qiskit simulation of the Quantum Couting Algorithm + Grover circuit
- 'circuit1.qasm' - **Phase oracle** (3 qubits): marks |111⟩ with a −1 phase using the H·CCX·H sandwich. The first building block
- 'circuit1.png' - Composer view of the **phase oracle**, showing the H·CCX·H gate sequence and the statevector [0.75, −0.25, …] confirming |111⟩ has been phase-tagged
- 'circuit2.qasm' - **Grover diffusion operator** (3 qubits): implements 2|s⟩⟨s|−I, reflecting amplitudes about the uniform superposition. The second building block of the Grover operator Q
- 'circuit2.png' - Composer view of the **Grover diffusion operator**, showing the statevector [1, 0, 0, …] confirming amplitude amplification on |000⟩ after one iteration
- 'circuit3.qasm' - **Full Quantum Counting circuit** (6 qubits: 3 counting + 3 data, N=8): combines QPE, controlled-Q^(2^j), and the inverse QFT to estimate the number of marked solutions M
- 'circuit3.png' - Composer view of the **full Quantum Counting circuit**, showing the probability histogram with peak at |100⟩, which decodes to M ≈ 1 solution in the N=8 database

