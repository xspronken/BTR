import pytest
import numpy as np
import qutip
from pulser import Register, Sequence, Pulse
from pulser.devices import Chadoq2, MockDevice
from pulser.waveforms import BlackmanWaveform
from pulser_simulation import Simulation, SimConfig
import Code.tests.theoretical_pulses as theory

from Code import gates


i = 2
n = 2
t = 252



@pytest.fixture(params=[qutip.rand_ket(2) for i in range(i)])
def init_state(request):
    return request.param


@pytest.fixture(params=[qutip.rand_ket(2) for i in range(i)])
def init_state_2(request):
    return request.param

@pytest.fixture(params=[(np.random.random()-0.5)*4*np.pi for i in range(n)])
def theta(request):
    return request.param
@pytest.fixture(params=[np.random.random()*2*np.pi for i in range(n)])
def gamma(request):
    return request.param
@pytest.fixture(params=[np.random.random()*2*np.pi for i in range(n)])
def phi(request):
    return request.param

### Sim for gates with no parameter
def sim(init,pulse):
    reg = Register({"q1":np.array([0,0])})
    seq = Sequence(reg,Chadoq2)
    
    pulse(1,seq)

    sim = Simulation(seq)
    
    sim.initial_state = init

    res = sim.run()
    phase = seq.current_phase_ref("q1")

    final = theory.Rz(res.states[-1],-phase)
    return res.states[0], final, res.states[-1]

### Sim for gates with 1 parameter (arbitrary rotation)
def sim_arb(init,pulse,theta):
    reg = Register({"q1":np.array([0,0])})
    seq = Sequence(reg,Chadoq2)
    
    pulse(theta,1,seq)

    sim = Simulation(seq,0.3)
    
    sim.initial_state = init

    res = sim.run()
    phase = seq.current_phase_ref("q1")

    final = theory.Rz(res.states[-1],phase)
    return res.states[0], final, res.states[-1]

### Sim for unitary gates (3 parameters)
def sim_U(init,pulse, gamma, theta, phi):
    reg = Register({"q1":np.array([0,0])})
    seq = Sequence(reg,Chadoq2)
    
    pulse(gamma,theta,phi,1,seq)

    sim = Simulation(seq,0.3)
    
    sim.initial_state = init

    res = sim.run()
    phase = seq.current_phase_ref("q1")
    final = theory.Rz(res.states[-1], phase)
    return res.states[0], final, res.states[-1], res.states



### Sim for gates with no parameter
def sim_multi(init_1,init_2,pulse):
    #add rydberg state manually to init state
    pulser_init_1= qutip.Qobj(np.insert(init_1,0,0))
    pulser_init_2= qutip.Qobj(np.insert(init_2,0,0))

 

    reg = Register({"q0":np.array([0,1]),"q1":np.array([0,0])})

    seq = Sequence(reg,MockDevice)
    
    pulse(0,1,seq)



    sim = Simulation(seq,0.3)
    
    sim.initial_state = qutip.tensor([pulser_init_1,pulser_init_2])
    res = sim.run(None, nsteps= 500000)

    reg_inv = Register({"q0":np.array([0,1]),"q1":np.array([0,0])})

    seq_inv = Sequence(reg,MockDevice)
    
    pulse(1,0,seq_inv)



    sim_inv = Simulation(seq_inv,0.3)
    
    sim_inv.initial_state = qutip.tensor([pulser_init_1,pulser_init_2])

    res_inv = sim_inv.run(None, nsteps= 500000)



    return res.get_state(0,reduce_to_basis="digital", tol=1e-4), res.get_final_state(reduce_to_basis='digital', tol=1e-4), res_inv.get_final_state(reduce_to_basis='digital', tol=1e-4)


####  TEST PAULI GATES ####


# def test_X(init_state):
#     a = theory.X(init_state)
#     b, c = sim(init_state, gates.X)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)


# def test_X1(init_state):
#     a = theory.X(init_state)
#     b, c = sim(init_state, gates.X1)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)

# def test_Y(init_state):
#     a = theory.Y(init_state)
#     b, c = sim(init_state, gates.Y)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)


# def test_Y1(init_state):
#     a = theory.Y(init_state)
#     b, c = sim(init_state, gates.Y1)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)

# def test_Z(init_state):
#     a = theory.Z(init_state)
#     b, c = sim(init_state, gates.Z)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)


# def test_Z1(init_state):
#     a = theory.Z(init_state)
#     b, c = sim(init_state, gates.Z1)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)

# def test_H(init_state):
#     a = theory.H(init_state)
#     b, c = sim(init_state, gates.H)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)

### ARBITRARY ROTATION GATES ###
# def test_Rz(init_state,theta):
#     a = theory.Rz(init_state, theta)
#     _, c,d = sim_arb(init_state, gates.Rz, theta)
#     print('init \n',init_state)
#     print('theory \n', a)
#     print('pulser \n', d)
#     # b = qutip.Bloch()
#     # b.add_states(e,'point',alpha=0.1)
#     # b.add_states([init_state,a,c])
#     # b.save(f"/home/xavier/Documents/BTR/Code/tests/img/Rx-{theta}.png")

#     np.testing.assert_almost_equal(a[0],c[0], decimal=5)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=5)


# def test_Ry(init_state,theta):
#     a = theory.Ry(init_state,theta)
#     _, c, e = sim_arb(init_state, gates.Ry1,theta)
#     # b = qutip.Bloch()
#     # b.add_states(e,'point',alpha=0.1)
#     # b.add_states([init_state,a,c])
#     # b.save(f"/home/xavier/Documents/BTR/Code/tests/img/Ry-{theta}.png")
#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)



# def test_Rz(init_state,theta):
#     a = theory.Rz(init_state,theta)
#     print(theta)
#     _, c, e = sim_arb(init_state, gates.Rz,theta)
#     print('init',init_state)
#     print('thoery', a)
#     print('pulse',c)
#     print('pulse',e)
#     # b = qutip.Bloch()
#     # b.add_states(e,'point',alpha=0.1)
#     # b.add_states([init_state,a,c])
#     # b.save(f"/home/xavier/Documents/BTR/Code/tests/img/Rz-{theta}.png")
#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)




# def test_UQASM_abs(init_state,gamma,theta,phi):
#     a = theory.U_QASM(init_state,gamma,theta,phi)
#     _, c = sim_U(init_state, gates.QASM_U,gamma,theta,phi)
#     print("init", init_state)
#     print("thoery",a)
#     print( "sim",c)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)

# def test_UQASM(init_state,gamma,theta,phi):
#     init = str(init_state)
#     a = theory.U_QASM(init_state,gamma,theta,phi)
#     _, c , e, f = sim_U(init_state, gates.QASM_U,gamma,theta,phi)
#     print("init", init_state)
#     print("theory",a)
#     print( "sim",e)
#     # b = qutip.Bloch()
#     # b.add_states(f,'point',0.1)
#     # b.add_states([init_state, a, c])
#     # b.save(f"/home/xavier/Documents/BTR/Code/tests/img/{gamma}{theta}{phi}.png")


#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)


# def test_I(init_state):
#     print(theta)
#     a = theory.I(init_state)
#     b, c = sim(init_state, gates.I)
#     print('init',b)
#     print('thoery', a)
#     print('pulse',c)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)
#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)


def test_CNOT(init_state,init_state_2):
    a, b,c = sim_multi(init_state,init_state_2, gates.CNOT)
    e = theory.CNOT(a)
    f = theory.CNOT_inv(a)

    np.testing.assert_almost_equal(b[0],e[0], decimal=5)
    np.testing.assert_almost_equal(b[1],e[1],decimal=5)
    np.testing.assert_almost_equal(c[0],f[0], decimal=5)
    np.testing.assert_almost_equal(c[1],f[1],decimal=5)
    
    
    