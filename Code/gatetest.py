
import numpy as np
import pytest
import qutip
from pulser import Pulse, Sequence, Register
from pulser.devices import Chadoq2
from pulser.waveforms import BlackmanWaveform
from pulser_simulation import Simulation


def raman_pulse(amplitude, detuning, phase, postphase, seq, target,duration = 252):
    pulse = Pulse.ConstantDetuning(
        BlackmanWaveform(duration, amplitude), detuning, phase, post_phase_shift=postphase)
    
    if "raman" not in seq.declared_channels:
        seq.declare_channel("raman", "raman_local", target)
    else:
        seq.target(target, "raman")

    seq.add(pulse, "raman", "wait-for-all")

# Unitary gate as defined in pulser docs
#U(gamma,theta,phi) = Rz(gamma)Rx(theta)Rz(phi) = Rz(gamma+phi)Rz(-phi)Rx(theta)Rz(phi)
def U(gamma, theta, phi, target,seq):
    target = "q" + str(target)
    raman_pulse(theta,0,phi,gamma+phi,seq,target)


# Pulser arbitrary rotation gates
def Rx(theta, target, seq):
    if theta >= 0:
        #Rz(0)Rz(-0)Rx(theta)Rz(0) = Rx(theta)
        U(0,theta,0,target, seq)
    else:
        #Rz(0)Rz(-pi)Rx(-theta)Rz(+pi) = Rx(theta)
        U(-np.pi,-theta,np.pi,target, seq)
        
def Ry(theta, target, seq):
    if theta >= 0:
        #Rz(-pi/2+pi/2 = 0)Rz(pi/2)Rx(theta)Rz(-pi/2) = Ry(theta)
        U(np.pi/2,theta,-np.pi/2,target, seq)
    else:
        #Rz(pi/2-pi/2 = 0)Rz(-pi/2)Rx(-theta)Rz(+pi/2) = Ry(theta)
        U(-np.pi/2,-theta,np.pi/2,target, seq)


# Rz gates use 2 pulses to avoid the sign flip that comes witha single 2pi pulse
def Rz(theta, target, seq):
    #Rz(theta/2)Rz(0)Rx(2pi = 0)Rz(0) = Rz(theta/2)
    U(theta/2,2*np.pi,0, target, seq)
    U(theta/2,2*np.pi,0, target, seq)

#second Rz implemetation
# def Rz(theta, target, seq):
#     # Rz(theta/2+theta/2 = theta)Rz(-theta/2)Rx(2pi = 0)Rz(theta/2) = Rz(theta)
#     U(theta/2,2*np.pi,theta/2, target, seq)
#     U(0,2*np.pi,0, target, seq)


# Theoretical arbitrary rotation gates
def Rx_theory(init, theta):
    op = qutip.Qobj([[np.cos(theta/2),-np.sin(theta/2)*1j],[-np.sin(theta/2)*1j,np.cos(theta/2)]])
    res = op * init
    return res

def Ry_theory(init, theta):
    op = qutip.Qobj([[np.cos(theta/2),-np.sin(theta/2)],[np.sin(theta/2),np.cos(theta/2)]])
    res = op * init
    return res

def Rz_theory(init,theta):
    op = qutip.Qobj([[np.exp(-1j*theta/2),0],[0,np.exp(1j*theta/2)]])
    res = op * init
    return res

# Test paramters 
# 5 random initial states 
@pytest.fixture(params=[qutip.rand_ket(2) for i in range(5)])
def init_state(request):
    return request.param


# 5 random values of theta betweem -2pi and 2pi
@pytest.fixture(params=[(np.random.random()-0.5)*4*np.pi for i in range(5)])
def theta(request):
    return request.param

# Run pulser simulation with random initial state
def sim(init,pulse,theta):
    reg = Register({"1":np.array([0,0])})
    seq = Sequence(reg,Chadoq2)
    
    pulse(theta,1,seq)

    sim = Simulation(seq,0.3)
    
    sim.initial_state = init

    res = sim.run()

    return res.states[0], res.states[-1]





def test_Rx(init_state,theta):
    a = Rx_theory(init_state,theta)
    b, c = sim(init_state,Rx,theta)
    

    np.testing.assert_almost_equal(a[0],c[0], decimal=4)
    np.testing.assert_almost_equal(a[1],c[1],decimal=4)


def test_Ry(init_state,theta):
    a = Ry_theory(init_state,theta)
    _, c = sim(init_state,Ry,theta)

    np.testing.assert_almost_equal(a[0],c[0], decimal=4)
    np.testing.assert_almost_equal(a[1],c[1],decimal=4)

def test_Rz(init_state,theta):
    a = Rz_theory(init_state,theta)
    print(theta)
    b, c = sim(init_state,Rz,theta)
    
    print('init',init_state,'pulser init', b)
    print('theory', a)
    print('pulse',c)

    np.testing.assert_almost_equal(a[0],c[0], decimal=4)
    np.testing.assert_almost_equal(a[1],c[1],decimal=4)

def test_Rz_probability(init_state,theta):
    a = Rz_theory(init_state,theta)
    print(theta)
    _, c = sim(init_state,Rz,theta)

    np.testing.assert_almost_equal(np.abs(a[0]),np.abs(c[0]), decimal=4)
    np.testing.assert_almost_equal(np.abs(a[1]),np.abs(c[1]),decimal=4)

