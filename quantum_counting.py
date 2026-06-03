# ============================================================
# Quantum Counting Algorithm — Qiskit Implementation
# Sources:
#   [1] arXiv:2310.07428 — Chung & Nepomechie (2023)
#   [2] Brassard, Hoyer, Mosca, Tapp, quant-ph/0005055
#   [3] github.com/jwei302/Quantum-Counting (MIT BWSI)
# ============================================================

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit_aer import AerSimulator
import numpy as np

# ── Phase Oracle ──────────────────────────────────────────────
def build_oracle_3q():
    """Marks |111⟩ with a -1 phase. 1 solution in 8."""
    qc = QuantumCircuit(3, name="Oracle_3q")
    qc.h(2)
    qc.ccx(0, 1, 2)   # CCX + surrounding H converts bit-flip to phase-flip
    qc.h(2)
    return qc.to_gate()

def build_oracle_4q():
    """Marks |1111⟩ and |1110⟩ with -1 phase. 2 solutions in 16."""
    qc = QuantumCircuit(4, name="Oracle_4q")
    # Mark |1111⟩
    qc.h(3)
    qc.mcx([0, 1, 2], 3)
    qc.h(3)
    # Mark |1110⟩ (flip q3 so it looks like |1111⟩ to the oracle)
    qc.x(3)
    qc.h(3)
    qc.mcx([0, 1, 2], 3)
    qc.h(3)
    qc.x(3)
    return qc.to_gate()

# ── Grover Diffusion (2|s⟩⟨s| − I) ──────────────────────────
def build_diffusion(n):
    qc = QuantumCircuit(n, name="Diffusion")
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc.to_gate()

# ── Grover Operator Q = Diffusion · Oracle ────────────────────
def build_grover_op(n, oracle_gate):
    qc = QuantumCircuit(n, name="Grover_Q")
    qc.append(oracle_gate, range(n))
    qc.append(build_diffusion(n), range(n))
    return qc.to_gate()

# ── QPE Circuit ───────────────────────────────────────────────
def quantum_counting_circuit(n_count, n_data, oracle_gate):
    """
    n_count: counting qubits (precision of phase estimation)
    n_data : data qubits (3 or 4)
    """
    count_reg = QuantumRegister(n_count, name="count")
    data_reg  = QuantumRegister(n_data,  name="data")
    creg      = ClassicalRegister(n_count, name="c")
    qc = QuantumCircuit(count_reg, data_reg, creg)

    # Superposition on both registers
    qc.h(count_reg)
    qc.h(data_reg)

    # Controlled-Q^(2^j) for each counting qubit
    grover_gate = build_grover_op(n_data, oracle_gate)
    for j in range(n_count):
        ctrl_g = grover_gate.control(1)
        for _ in range(2 ** j):
            qc.append(ctrl_g, [count_reg[j]] + list(data_reg))

    # Inverse QFT on counting register
    iqft = QFT(n_count, inverse=True, do_swaps=True)
    qc.append(iqft.to_gate(label="IQFT"), count_reg)

    qc.measure(count_reg, creg)
    return qc

# ── Decode measurement → M ────────────────────────────────────
def decode(counts, n_count, n_data):
    N = 2 ** n_data
    top = max(counts, key=counts.get)
    k   = int(top[::-1], 2)          # Qiskit is little-endian; reverse for value
    theta = np.pi * k / (2 ** n_count)
    M = N * (np.sin(theta) ** 2)
    return k, theta, M

# ── Run simulations ───────────────────────────────────────────
sim = AerSimulator()

print("=== 3-QUBIT DATABASE (n=3, N=8) ===")
print("Oracle: marks |111⟩ → expected M ≈ 1")
qc3 = quantum_counting_circuit(n_count=4, n_data=3, oracle_gate=build_oracle_3q())
c3 = sim.run(qc3, shots=4096).result().get_counts()
k3, t3, M3 = decode(c3, 4, 3)
print(f"  Top bitstring : {max(c3, key=c3.get)}")
print(f"  Measured k    : {k3}")
print(f"  Theta         : {t3:.4f} rad")
print(f"  Estimated M   : {M3:.3f}  (expected ~1.0)")
print(f"  Solution exists? {'YES — proceed with Grover' if M3 > 0.5 else 'NO'}")
print()

print("=== 4-QUBIT DATABASE (n=4, N=16) ===")
print("Oracle: marks |1111⟩, |1110⟩ → expected M ≈ 2")
qc4 = quantum_counting_circuit(n_count=4, n_data=4, oracle_gate=build_oracle_4q())
c4 = sim.run(qc4, shots=4096).result().get_counts()
k4, t4, M4 = decode(c4, 4, 4)
print(f"  Top bitstring : {max(c4, key=c4.get)}")
print(f"  Measured k    : {k4}")
print(f"  Theta         : {t4:.4f} rad")
print(f"  Estimated M   : {M4:.3f}  (expected ~2.0)")
print(f"  Solution exists? {'YES — proceed with Grover' if M4 > 0.5 else 'NO'}")
print()

# Optional: draw circuits
print("Circuit diagram (3-qubit):")
print(qc3.draw(output='text', fold=120))