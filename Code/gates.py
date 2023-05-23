import numpy as np

from pulser import Pulse, Sequence, Register
from pulser.devices import Chadoq2
from pulser.waveforms import BlackmanWaveform

# duration of pulses for each channel
raman_duration = 250
rydberg_duration = 250


def raman_pulse(amplitude, detuning, phase, postphase, duration, seq, target):
    pulse = Pulse.ConstantDetuning(
        BlackmanWaveform(duration, amplitude), detuning, phase, post_phase_shift=postphase)
    
    if "raman" not in seq.declared_channels:
        seq.declare_channel("raman", "raman_local", target)
    else:
        seq.target(target, "raman")

    seq.add(pulse, "raman", "wait-for-all")


# Pauli X-gate
def X(target, seq):
    target = "q" + str(target)

    pulse = Pulse.ConstantDetuning(
        BlackmanWaveform(raman_duration, np.pi), 0.0, 3 * np.pi / 2
    )

    if "raman" not in seq.declared_channels:
        seq.declare_channel("raman", "raman_local", target)
    else:
        seq.target(target, "raman")

    seq.add(pulse, "raman", "wait-for-all")

# Pauli Y-gate
def Y(target, seq):
    target = "q" + str(target)
    pulse = Pulse.ConstantDetuning(
        BlackmanWaveform(raman_duration, np.pi), 0.0, np.pi
    )
    if "raman" not in seq.declared_channels:
        seq.declare_channel("raman", "raman_local", target)
    seq.target(target, "raman")
    seq.add(pulse, "raman")



# Pauli Z-gate
def Z(target, seq):
    target = "q" + str(target)
    pulse = Pulse.ConstantDetuning(
        BlackmanWaveform(raman_duration, 2 * np.pi), 0.0, np.pi / 2
    )
    if "raman" not in seq.declared_channels:
        seq.declare_channel("raman", "raman_local", target)
    seq.target(target, "raman")
    seq.add(pulse, "raman")


# Hadamard gate
def H(target, seq):
    U(np.pi/2,np.pi/2,np.pi/2,target,seq)


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


########   COMBINATORY GATES #########


# Identity gate
def I(target, seq):
    X(target, seq)
    X(target, seq)
    X(target, seq)
    X(target, seq)


# Control-NOT gate
def CNOT(control, target, seq):
    H(target, seq)
    CZ(control, target, seq)
    H(target, seq)


#Unitary gate

def U(gamma, theta, phi, target,seq):
    target = "q" + str(target)
    raman_pulse(theta,0,phi,gamma+phi,raman_duration,seq,target)

def Rx(theta, target, seq):
    if theta >= 0:
        U(0,theta,0,target, seq)
    else:
        U(0,-theta,np.pi,target, seq)

def Rx1(theta, target, seq):
    if theta >= 0:
        U(0,theta,0,target, seq)
    else:
        U(-np.pi,-theta,np.pi,target, seq)

def Ry(theta, target, seq):
    if theta >= 0:
        U(0,theta,3*np.pi/2,target, seq)
    else:
        U(0,-theta,np.pi/2,target, seq)

def Ry1(theta, target, seq):
    if theta >= 0:
        U(np.pi/2,theta,-np.pi/2,target, seq)
    else:
        U(-np.pi/2,-theta,np.pi/2,target, seq)


def Rz(theta, target, seq):
    U(theta,0,0, target, seq)





def Y1(target, seq):
    U(0,np.pi,np.pi,target, seq)

def X1( target, seq):
    U(-np.pi/2,np.pi,np.pi/2,target, seq)
  
def Z1(target, seq):
    U(0,2*np.pi,np.pi/2, target, seq)
    U(np.pi,2*np.pi,np.pi/2, target, seq)

def Z1(target, seq):
    U(0,2*np.pi,np.pi/2, target, seq)
    U(np.pi,2*np.pi,np.pi/2, target, seq)

    

#QASM Unitary

def QASM_U(theta, phi, lamda, target, seq):
    if theta >= 0:
        U(phi-np.pi/2,theta,lamda-np.pi/2, target, seq)
    else:
        U(phi-np.pi/2,-theta,lamda+np.pi/2, target, seq)