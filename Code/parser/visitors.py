import openqasm3.ast as oqast
from openqasm3 import parse
from openqasm3.visitor import QASMVisitor

def get_value(x):
    if isinstance(x, oqast.IntegerLiteral):
        return x.value
    elif isinstance(x, oqast.Identifier):
        return x.name
    elif isinstance(x, oqast.BinaryExpression):
        return (get_value(x.rhs),x.op,get_value(x.lhs))

class RegisterVisitor(QASMVisitor):
    #TODO reset, measure, bits
    def generic_visit(self, node, context=None):
        super().generic_visit(node, context)

    def visit_QubitDeclaration(self, node, context=None):
        if not context.get("qubits") is None:
            qubits = context["qubits"]
            qubits.append(
                (node.qubit.name, node.size.value)
            )
    
        
    def visit_QuantumGate(self, node, context=None):
        if context.get("gate expression") is not None:
            g = context["gate expression"]
            tmp1 = []
            for q in node.qubits:
                if isinstance(q, oqast.Identifier):
                    tmp = []
                    for id in g.arguments:
                        tmp.append(get_value(id))
                    tmp1.append((g.name.name,tmp))
                # elif isinstance(q, oqast.IndexedIdentifier):
                #     tmp = []
                #     if not g.name.name in def_gate:
                #         print("not defined yet error")
                #     tmp1.append((g.name.name, ))
            return tmp1
        if context.get("gates") is not None:
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


    def visit_QuantumGateDefinition(self, node, context=None):
        if context.get("define gate") is not None:
            def_gate = context["define gate"]
            temp_gate = []
            
            for g in node.body:
                if isinstance(g, oqast.QuantumGate):
                    data = RegisterVisitor.visit_QuantumGate(self,node, {"define gate": def_gate, 'gate expression': g, "temp_gate": temp_gate})
                    temp_gate.append(data)

                    print(data)
            def_gate.append((node.name.name, len(node.qubits),temp_gate))