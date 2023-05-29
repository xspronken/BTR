import pytest
import numpy as np
import qutip
from qutip.qip.circuit import QubitCircuit

from pulser import Register, Sequence, Pulse
from pulser.devices import Chadoq2, MockDevice
from pulser.waveforms import BlackmanWaveform
from pulser_simulation import Simulation, SimConfig

from pulser.register.special_layouts import TriangularLatticeLayout

import Code.tests.theoretical_pulses as theory

from Code import gates 


i = 1

t = 252



@pytest.fixture(params=[qutip.rand_ket(2) for i in range(i)])
def init_state_1(request):
    return request.param

@pytest.fixture(params=[qutip.rand_ket(2) for i in range(i)])
def init_state_2(request):
    return request.param

@pytest.fixture(params=[qutip.rand_ket(2) for i in range(i)])
def init_state_3(request):
    return request.param

@pytest.fixture(params=[qutip.rand_ket(2) for i in range(i)])
def init_state_4(request):
    return request.param


def qutip_sim(init_state_1,init_state_2,init_state_3,init_state_4, gate):
    init = qutip.tensor([init_state_1,init_state_2,init_state_3,init_state_4])
    qc = QubitCircuit(N=4)
    qc.add_gate(gate, targets=[1], controls=0)
    qc.add_gate(gate, targets=[2], controls=3)


    result = qc.run(state=init)
    
    return  init,result



### Sim for gates with no parameter
def sim(init_1,init_2,init_3,init_4,pulse):
    #add rydberg state manually to init state
    pulser_init_1= qutip.Qobj(np.insert(init_1,0,0))
    pulser_init_2= qutip.Qobj(np.insert(init_2,0,0))
    pulser_init_3= qutip.Qobj(np.insert(init_3,0,0))
    pulser_init_4= qutip.Qobj(np.insert(init_4,0,0))
 

    reg = Register({"q0":np.array([0,1]),"q1":np.array([0,0]),"q2":np.array([1,0]),"q3":np.array([1,1])})

    seq = Sequence(reg,MockDevice)
    
    pulse(0,1,seq)
    pulse(3,2,seq)


    sim = Simulation(seq,0.3)
    
    sim.initial_state = qutip.tensor([pulser_init_1,pulser_init_2,pulser_init_3,pulser_init_4])

    res = sim.run(None, nsteps= 5000000)



    return res.get_state(0,reduce_to_basis="digital", tol=1e-4), res.get_final_state(reduce_to_basis='digital', tol=1e-4)



def test_Rydberg(init_state_1,init_state_2,init_state_3, init_state_4):

    a, b = sim(init_state_1,init_state_2,init_state_3,init_state_4, gates.CNOT)
    c, d = qutip_sim(init_state_1,init_state_2,init_state_3,init_state_4, "CNOT")
    print('init', a)
    print('pulser', b)
    print('theory init', c)  
    print('theory',d)





