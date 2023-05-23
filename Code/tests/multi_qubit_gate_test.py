import pytest
import numpy as np
import qutip
from pulser import Register, Sequence, Pulse
from pulser.devices import Chadoq2, MockDevice
from pulser.waveforms import BlackmanWaveform
from pulser_simulation import Simulation, SimConfig

from pulser.register.special_layouts import TriangularLatticeLayout

import Code.tests.theoretical_pulses as theory

from Code import gates 


i = 1
n = 2
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



### Sim for gates with no parameter
def sim(init_1,init_2,init_3,pulse):
    pulser_init_1= qutip.Qobj(np.insert(init_1,0,0))
    pulser_init_2= qutip.Qobj(np.insert(init_2,0,0))
    pulser_init_3= qutip.Qobj(np.insert(init_3,0,0))
 

    reg = Register({"q0":np.array([0,-0.5]),"q1":np.array([0,0.5]),"q2":np.array([0.5,0])})

    seq = Sequence(reg,MockDevice)
    
    pulse(1,2,seq)
    pulse(0,1,seq)
    pulse(0,2,seq)

    sim = Simulation(seq,0.3)
    
    # sim.initial_state = qutip.tensor([pulser_init_1,pulser_init_2,pulser_init_3])

    res = sim.run(None, nsteps= 5000000)


    return res.states[0], res.states[-1],res.get_state(0,reduce_to_basis="digital"), res.get_final_state(reduce_to_basis='digital')



####  TEST PAULI GATES ####
tri_layout = TriangularLatticeLayout(n_traps=3, spacing=4)



def test_CZ(init_state_1,init_state_2,init_state_3):
    # a = theory.Rz(init_state,theta)
    b, c, d, e = sim(init_state_1,init_state_2,init_state_3, gates.CZ)
    print('init', b, 'init_d', d)
    print('final',c,'final_d', e)





