## Introduction
The project implements the Quantum Counting Algorithm, which estimates how many solutions exist in a database before running Grover's search.
The algorithm combines Quantum Phase Estimation with Grover's operator to recover and angle that can be converted into the number of solutions.

For this project, the algorithm is demonstrated on a small example with 3 data qubits and 4 data qubits which correspond to a database of size 8 and 16.

## Project Structure

1. Oracle Circuit 
    - marks the correct state or states
    - changes the phase

2. Diffusion circuit
    - performs the Grover reflection step

3. Full Qauntum Couting circuit
    - combines a counting register, the data register, controlled powers of the Grover operator, the inverse QFT and measurement
    - main circuit that produces the estimated result


# Basic Operations

1. Hadamard gates - create superposition on the counting and data registers
2. Oracle - marks the valid state(s) by a phase flip
3. Diffusion operator - performs the Grover reflection step
4. Controlled powers of the Grover operator - encode phase information into the counting register
5. Inverse QFT - converts that phase information into a measurable binary value
6. Measurement - reads the counting register and allows classical estimation of the number of marked items


## Cost Analysis

The implementation cost can be described using two standard metrics:
1. Gate count - the total number of gates in the circuit.
2. Gate depth - the number of sequential gate layers needed to execute the circuit

In Qiskit, these can be obtained directly from the circuit object using methods such as count_ops() and depth().
For Quantum Counting, the cost grows mainly because of the controlled Grover powers, since the Grover operator must be repeated 1, 2, 4, ... times depending on the counting qubit.
This means the full counting circuit is significantly more expensive than the oracle or diffusion subcircuits taken separately.


## Simulator and Noise Level

The circuit was run in Qiskit AerSimulator, which supports both ideal and noisy simulation.
For a simple realistic test, a depolarizing noise model can be added to two-qubit gates such as cx, which is a common way to approximate gate errors in simulation.
In this project, the simulator is useful because it allows validation of the circuit structure, output distribution and estimated counting result before running on real hardware.


## Conclusion

The Quantum Counting circuit is built from standard blocks — superposition, oracle, Grover iteration, inverse QFT and measurement - but its cost increases quickly because controlled Grover powers must be repeated several times.
For this reason, simulation is the most appropriate environment for this type project: it allows clean verification of the algorithm, basic cost analysis and optional testing under noise without hardware constraints.

