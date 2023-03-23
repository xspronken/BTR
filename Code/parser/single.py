import openqasm3.ast as oqast
from openqasm3 import parse
from openqasm3.visitor import QASMVisitor


# with open('./qasm_examples/test.qasm', 'r') as file:
#     data = file.read()





qasm = """
gate h q { U(π/2, 0, π) q; }

qubit[2] q;
qubit[2] b;
qubit[3] c;

cnot b, c;
x q, b , c;

"""

ast = parse(qasm)
x = ast.statements[0].__str__()
y = x.replace("),", "), \n\n")
z = y.replace("(", "( \n ")
print(z)
# for x in ast.statements:
#     print(x,"\n")

class RegisterVisitor(QASMVisitor):
    def generic_visit(self, node, context=None):
        super().generic_visit(node, context)

    def visit_QubitDeclaration(self, node, context=None):
        qubits = context["qubits"]
        qubits.append(
            (node.qubit.name, node.size.value)
        )
    def visit_QuantumGateDefinition(self, node, context=None):
        def_gate = context["define gate"]
        
    def visit_QuantumGate(self, node, context=None):
        gates = context["gates"]
        reg = dict(context["qubits"])
        targets = []
        for q in node.qubits:
            if isinstance(q, oqast.Identifier):
                targets.append([
                    (q.name, i)
                    for i in range(reg[q.name])
                ])
            elif isinstance(q, oqast.IndexedIdentifier):
                targets.append([
                    (q.name.name, i.value)
                    for idx in q.indices
                    for i in idx
                ])

        gates.append(
            (node.name.name, targets)
        )


qubits = []
def_gate = []
gates = []
# RegisterVisitor().visit(ast, {"qubits": qubits, "gates": gates})

# print("Registers:")
# for q in qubits:
#     print(q)
# print()

# print("Gates:")
# for g in gates:
#     print(g)
# print()

# #Errors
# Accepted_gates = []
# for g in gates:
#     name, targets = g
#     #Gate specific
#     if name == "cnot":
#         if len(targets) != 2:
#             print(f"CNOT must have two targets: {g}")
    
#     #Broadcast size
#     sizes = [len(t) for t in targets if len(t) != 1]
#     if any(s != sizes[0] for s in sizes):
#         print(f"CNOT targets must broadcast correctly: f{g}")