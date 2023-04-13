import qutip
import numpy as np

def X(init):
    op = qutip.Qobj([[0,1],[1,0]])
    res = op * init
    return res

def Y(init):
    op = qutip.Qobj([[0,-1j],[1j,0]])
    res = op * init
    return res

def Z(init):
    op = qutip.Qobj([[1,0],[0,-1]])
    res = op * init
    return res

def H(init):
    op = qutip.Qobj((1/np.sqrt(2))*np.array([[1,1],[1,-1]]))
    res = op * init
    return res

def Rx(init, theta):
    op = qutip.Qobj([[np.cos(theta/2),-np.sin(theta/2)*1j],[-np.sin(theta/2)*1j,np.cos(theta/2)]])
    res = op * init
    return res

def Ry(init, theta):
    op = qutip.Qobj([[np.cos(theta/2),-np.sin(theta/2)],[np.sin(theta/2),np.cos(theta/2)]])
    res = op * init
    return res

def Rz(init,theta):
    op = qutip.Qobj([[np.exp(-1j*theta/2),0],[0,np.exp(1j*theta/2)]])
    res = op * init
    return res

def U_QASM(init, theta,phi,lamda):
    op = qutip.Qobj([[np.cos(theta/2),
                      -np.exp(1j*lamda)*np.sin(theta/2)],
                      [np.exp(1j*phi)*np.sin(theta/2),
                       np.exp(1j*(phi+lamda))*np.cos(theta/2)]])
    print(op)
    res = op * init
    return res
