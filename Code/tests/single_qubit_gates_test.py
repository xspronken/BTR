import pytest
import numpy as np
import qutip
from pulser import Register, Sequence, Pulse
from pulser.devices import Chadoq2
from pulser.waveforms import BlackmanWaveform
from pulser_simulation import Simulation, SimConfig
import Code.gates as gates
import Code.tests.theoretical_pulses as theory



n = 3
t = 252

@pytest.fixture(params=[qutip.rand_ket(2) for i in range(n)])
def init_state(request):
    return request.param

@pytest.fixture(params=[(np.random.random()-0.5)*4*np.pi for i in range(n)])
def gamma(request):
    return request.param
@pytest.fixture(params=[np.random.random()*2*np.pi for i in range(n)])
def theta(request):
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

    return res.states[0], res.states[-1]

### Sim for gates with 1 parameter (arbitrary rotation)
def sim_arb(init,pulse,theta):
    reg = Register({"q1":np.array([0,0])})
    seq = Sequence(reg,Chadoq2)
    
    pulse(theta,1,seq)

    sim = Simulation(seq)
    
    sim.initial_state = init

    res = sim.run()

    return res.states[0], res.states[-1]  

### Sim for unitary gates (3 parameters)
def sim_U(init,pulse, gamma, theta, phi):
    reg = Register({"q1":np.array([0,0])})
    seq = Sequence(reg,Chadoq2)
    
    pulse(gamma,theta,phi,1,seq)

    sim = Simulation(seq)
    
    sim.initial_state = init

    res = sim.run()

    return res.states[0], res.states[-1]


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
# def test_Rx(init_state,theta):
#     a = theory.Rx(init_state,theta)
#     b, c = sim_arb(init_state, gates.Rx,theta)
#     print('init',b)
#     print('thoery', a)
#     print('pulse',c)
    
#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)


# def test_Rx1(init_state,theta):
#     a = theory.Rx(init_state,theta)
#     b, c = sim_arb(init_state, gates.Rx1,theta)
#     print('init',b)
#     print('thoery', a)
#     print('pulse',c)
    
#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)

# def test_Ry(init_state,theta):
#     a = theory.Ry(init_state,theta)
#     b, c = sim_arb(init_state, gates.Ry,theta)
#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)

# def test_Ry1(init_state,theta):
#     a = theory.Ry(init_state,theta)
#     b, c = sim_arb(init_state, gates.Ry1,theta)
#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)

def test_Rz_abs(init_state,theta):
    a = theory.Rz(init_state,theta)
    b, c = sim_arb(init_state, gates.Rz,theta)
    print('init',b)
    print('thoery', a)
    print('pulse',c)
    np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
    np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)

def test_Rz(init_state,theta):
    a = theory.Rz(init_state,theta)
    b, c = sim_arb(init_state, gates.Rz,theta)
    print('init',b)
    print('thoery', a)
    print('pulse',c)
    np.testing.assert_almost_equal(a[0],c[0], decimal=4)
    np.testing.assert_almost_equal(a[1],c[1],decimal=4)

    

# def test_UQASM_abs(init_state,gamma,theta,phi):
#     a = theory.U_QASM(init_state,gamma,theta,phi)
#     _, c = sim_U(init_state, gates.QASM_U,gamma,theta,phi)
#     print("init", init_state)
#     print("thoery",a)
#     print( "sim",c)
#     np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
#     np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)

# def test_UQASM(init_state,gamma,theta,phi):
#     a = theory.U_QASM(init_state,gamma,theta,phi)
#     b, c = sim_U(init_state, gates.QASM_U,gamma,theta,phi)
#     print("init", init_state)
#     print("thoery",a)
#     print( "sim",c)
#     np.testing.assert_almost_equal(a[0],c[0], decimal=4)
#     np.testing.assert_almost_equal(a[1],c[1],decimal=4)