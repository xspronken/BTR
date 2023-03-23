include "stdgates.inc";
qubit[4] q;
reset q;
x q[0];
cnot q[1], a[0];
