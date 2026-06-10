OPENQASM 2.0;
include "qelib1.inc";

qreg count[3];
qreg data[3];
creg c[3];

// Step 1: superposition
h count[0]; h count[1]; h count[2];
h data[0];  h data[1];  h data[2];

// Step 2: Controlled-Q^1 (controlled on count[0])
ch count[0], data[2];
ccx data[0], data[1], data[2];
ch count[0], data[2];
ch count[0], data[0]; ch count[0], data[1]; ch count[0], data[2];
cx count[0], data[0]; cx count[0], data[1]; cx count[0], data[2];
ch count[0], data[2];
ccx data[0], data[1], data[2];
ch count[0], data[2];
cx count[0], data[0]; cx count[0], data[1]; cx count[0], data[2];
ch count[0], data[0]; ch count[0], data[1]; ch count[0], data[2];
barrier count[0],count[1],count[2],data[0],data[1],data[2];

// Step 3: Controlled-Q^2 (2x, controlled on count[1])
ch count[1], data[2]; ccx data[0],data[1],data[2]; ch count[1], data[2];
ch count[1],data[0]; ch count[1],data[1]; ch count[1],data[2];
cx count[1],data[0]; cx count[1],data[1]; cx count[1],data[2];
ch count[1],data[2]; ccx data[0],data[1],data[2]; ch count[1],data[2];
cx count[1],data[0]; cx count[1],data[1]; cx count[1],data[2];
ch count[1],data[0]; ch count[1],data[1]; ch count[1],data[2];
ch count[1], data[2]; ccx data[0],data[1],data[2]; ch count[1], data[2];
ch count[1],data[0]; ch count[1],data[1]; ch count[1],data[2];
cx count[1],data[0]; cx count[1],data[1]; cx count[1],data[2];
ch count[1],data[2]; ccx data[0],data[1],data[2]; ch count[1],data[2];
cx count[1],data[0]; cx count[1],data[1]; cx count[1],data[2];
ch count[1],data[0]; ch count[1],data[1]; ch count[1],data[2];
barrier count[0],count[1],count[2],data[0],data[1],data[2];

// Step 4: Controlled-Q^4 (4x, controlled on count[2]) — omitted for brevity,
// same block repeated 4 times with count[2] as control

// Step 5: Inverse QFT on count[0..2]
swap count[0], count[2];
h count[0];
cp(-pi/2) count[1], count[0];
h count[1];
cp(-pi/4) count[2], count[0];
cp(-pi/2) count[2], count[1];
h count[2];

// Step 6: measure
measure count[0] -> c[0];
measure count[1] -> c[1];
measure count[2] -> c[2];