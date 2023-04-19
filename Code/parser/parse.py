import openqasm3.ast as oqast
from openqasm3 import parse
from openqasm3.visitor import QASMVisitor
import visitors


# with open('./qasm_examples/test.qasm', 'r') as file:
#     data = file.read()
# gate h q { U(π/2, 0, π) q; }
qasm = """



gate x a { U(π, 0, π) a; }
gate y a { U(π, π/2, π/2) a; 
        U(π, π/2, π/2) a;
}



"""
qasm1 = """
// Pauli gate: bit and phase flip
gate y a { U(π, π/2, π/2) a; }
// Pauli gate: phase flip
gate z a { p(π) a; }
qubit[2] q;
qubit[2] b;
qubit[3] c;

cnot b, c;
x q, b , c"""

ast = parse(qasm)
# print(ast)
qubits = []
gates = []
Defined_gates = []# "U","x","y", "z", "h",'rx',"rz","ry","cx", "cnot" "cz"
Defined_single_target = [] # "U","x","y", "z", "h",'rx',"rz","ry"
Defined_two_target = [] #"cx", "cnot" "cz"
visitors.RegisterVisitor().visit(ast, {"qubits": qubits, "gates": gates ,"define gate": Defined_gates})

print("Registers:")
for q in qubits:
    print(q)
print()

print("Gates:")
for g in gates:
    print(g)
print()
print("DefinedGates:")
for g in Defined_gates:
    print(g)



# #Errors

for g in gates:
    name, targets = g
    #Gate specific
    if name in Defined_single_target:
        if len(targets) != 2:
                print(f"{name} must have one target: {g}")
    if name == "cnot":
        if len(targets) != 2:
            print(f"CNOT must have two targets: {g}")
    
    #Broadcast size
    sizes = [len(t) for t in targets if len(t) != 1]
    if any(s != sizes[0] for s in sizes):
        print(f"CNOT targets must broadcast correctly: f{g}")