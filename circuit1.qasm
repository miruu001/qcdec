OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];

// Phase oracle: marks |111> with -1 phase
// H · CCX · H converts bit-flip to phase-flip
h q[2];
ccx q[0], q[1], q[2];
h q[2];