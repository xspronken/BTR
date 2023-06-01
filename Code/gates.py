import numpy as np

from pulser import Pulse, Sequence, Register
from pulser.devices import Chadoq2
from pulser.waveforms import BlackmanWaveform

# duration of pulses for each channel
raman_duration = 252
rydberg_duration = 252

def raman_pulse(area, detuning, phase, postphase, duration, seq, target):
    pulse = Pulse.ConstantDetuning(
        BlackmanWaveform(duration, area), detuning, phase, post_phase_shift=postphase)
    
    if "raman" not in seq.declared_channels:
        seq.declare_channel("raman", "raman_local", target)
    else:
        seq.target(target, "raman")

    seq.add(pulse, "raman", "wait-for-all")


#Unitary gate
def U(gamma, theta, phi, target,seq):
    target = "q" + str(target)
    raman_pulse(theta,0,phi,gamma+phi,raman_duration,seq,target)


#QASM Unitary
def QASM_U(theta, phi, lamda, target, seq):
    if theta >= 0:
        U(phi-np.pi/2,theta,lamda-np.pi/2, target, seq)
    else:
        U(phi-np.pi/2,-theta,lamda+np.pi/2, target, seq)


#Pauli Gates
def Y(target, seq):
    U(0,np.pi,np.pi,target, seq)

def X( target, seq):
    U(-np.pi/2,np.pi,np.pi/2,target, seq)
  
def Z(target, seq):
    U(-np.pi/2,2*np.pi,np.pi/2, target, seq)


# Hadamard gate
def H(target, seq):
    U(np.pi/2,np.pi/2,np.pi/2,target,seq)


def Rx(theta, target, seq):
    if theta >= 0:
        U(0,theta,0,target, seq)
    else:
        U(-np.pi,-theta,np.pi,target, seq)

def Ry(theta, target, seq):
    if theta >= 0:
        U(np.pi/2,theta,-np.pi/2,target, seq)
    else:
        U(-np.pi/2,-theta,np.pi/2,target, seq)

def Rz(theta, target, seq):
    U(theta,0,0, target, seq)

# Identity gate
def I(target, seq):
    X(target, seq)
    X(target, seq)
    X(target, seq)
    X(target, seq)

# Control-Z gate
def CZ(control, target, seq):
    target = "q" + str(target)
    control = "q" + str(control)

    # pulses
    pi_pulse = Pulse.ConstantDetuning(
        BlackmanWaveform(rydberg_duration, np.pi), 0.0, 0
    )
    twopi_pulse = Pulse.ConstantDetuning(
        BlackmanWaveform(rydberg_duration, 2 * np.pi), 0.0, 0
    )

    # Perform a single-qubit Identity gate in order to get the right state basis in the simulation
    if seq.declared_channels == {}:
        I(0, seq)

    if "ryd" not in seq.declared_channels:
        seq.declare_channel("ryd", "rydberg_local", control)
    else:
        seq.target(control, "ryd")

    # add pulses to sequence
    seq.add(
        pi_pulse, "ryd", "wait-for-all"
    )  # Wait for state preparation to finish.
    seq.target(target, "ryd")  # Changes to target qubit
    seq.add(twopi_pulse, "ryd")
    seq.target(control, "ryd")  # Changes back to control qubit
    seq.add(pi_pulse, "ryd")

# Control-NOT gate
def CNOT(control, target, seq):
    H(target, seq)
    CZ(control, target, seq)
    H(target, seq)

