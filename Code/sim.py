import numpy as np
import matplotlib.pyplot as plt
import qutip
from itertools import product
from pulser import Pulse, Sequence, Register
from pulser.devices import Chadoq2
from pulser_simulation import Simulation, SimConfig
from pulser.waveforms import BlackmanWaveform,ConstantWaveform
import gates

def get_Final_State(data):
  x = "{:.6f}"
  return [x.format(np.real(data[-1])),
          x.format(np.imag(data[-1])),
          x.format(np.abs(data[-1]**2))]
def Plot_States(qubits, smrate, seq, simconf = None):

    simul = Simulation(seq, sampling_rate=smrate)

    if qubits > 0:
      res = simul.run()
      if qubits ==1:
          data1=[ket.overlap(qutip.ket('0')) for ket in res.states]
          data2=[ket.overlap(qutip.ket('1')) for ket in res.states]

          print(res.states[0],res.states[-1])
          fig,axs = plt.subplots(2,figsize=(8,8))
          state1 = get_Final_State(data1)
         
          axs[0].plot(np.real(data1))
          axs[0].plot(np.imag(data1))
          axs[0].plot(np.abs(data1)**2)
          axs[0].legend([fr'real, final value: {state1[0]}',
                         fr'imaginary final value: {state1[1]}',
                         fr'probability final value: {state1[2]}'])
          axs[0].set(xlabel = r"Time [ns]", 
                     ylabel=fr'$ \langle\,0|\, \psi(t)\rangle$')
          

          state2 = get_Final_State(data2)

          axs[1].plot(np.real(data2))
          axs[1].plot(np.imag(data2))
          axs[1].plot(np.abs(data2)**2)
          axs[1].legend([fr'real, final value: {state2[0]}',
                         fr'imaginary, final value: {state2[1]}',
                         fr'probability, final value: {state2[2]}'])
          axs[1].set( xlabel = r"Time [ns]", 
                     ylabel=fr'$ \langle\,1 |\, \psi(t)\rangle$')

      else:
          fig,axs = plt.subplots(2**qubits,figsize=(15,10+2**qubits))
          for i in range(2**qubits):
            bra = format(i,"0"+str(qubits)+"b") #converts i to binary since each binary number represents one of the 2**qubit states that can be measured
            qutip_bra= "".join([str((int(x) + 1) % 10) for x in bra])#adds 1 to each digit in order to adapt to qutip's different conventions
            
            data=[ket.overlap(qutip.ket("01",3)) for ket in res.states]
            state = get_Final_State(data)
            
            
            axs[i].plot(np.real(data))
            axs[i].plot(np.imag(data))
            axs[i].plot(np.abs(data)**2)
            axs[i].legend([fr'real, final value: {state[0]}',
                         fr'imaginary, final value: {state[1]}',
                         fr'probability, final value: {state[2]}'])
            axs[i].set(xlabel = r"Time [ns]", 
                       ylabel=fr'$ \langle\,{bra}|\, \psi(t)\rangle$')
      plt.show()
    else:
       raise ValueError('Not a valid amount of qubits')
    # print(res.states[0],res.states[1250],res.states[500],res.states[1175],res.states[1250],res.states[1500],res.states[-1])
    return res

def atoms_inline(size,spacing):
    reg_dict = {}
    for i in range(size):
        reg_dict["q"+str(i)] = np.array([0+i*spacing,0.])
    reg = Register(reg_dict)
    seq = Sequence(reg, Chadoq2)
    return reg,seq

qubits = 1 # gets very slow above 4-5 qubits
spacing = 4 #micrometers

#duration of pulses for each channel in nanoseconds
raman_duration = 250 
rydberg_duration = 250 

reg1, seq1 = atoms_inline(qubits,spacing)

gates.Rx(np.pi/2,0,seq1)
gates.Ry(np.pi/12,0,seq1)
# gates.Y(0,seq1)
# gates.X(0,seq1)
res = Plot_States(qubits, 1,  seq1)

reg, seq = atoms_inline(qubits,spacing)
gates.QASM_U(np.pi/2,-np.pi/2,np.pi/2,0,seq)
gates.QASM_U(np.pi/12,0,0,0,seq)
# gates.QASM_U(np.pi,np.pi/2,np.pi/2,0,seq)
# gates.QASM_U(np.pi,0,np.pi,0,seq)



res = Plot_States(qubits, 1, seq)