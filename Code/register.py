import numpy as np
from pulser import Sequence, Register
from pulser.devices import Chadoq2


def atoms_inline(size, spacing):
    reg_dict = {}
    for i in range(size):
        reg_dict["q" + str(i)] = np.array([0 + i * spacing, 0.0])
    reg = Register(reg_dict)
    seq = Sequence(reg, Chadoq2)
    return reg, seq
