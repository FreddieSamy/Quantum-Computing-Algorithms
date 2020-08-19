#!/usr/bin/env python
# coding: utf-8

# In[99]:


def getStateVector(SystemStateVector,qubit):
    """
    calculates the state vector of a specific qubit using the state vector of the system 
    according to the equation   prob(qubit[i]=1)=sum(probabilities of the states that contain qubit[i]=1)
                                state vector = [sqrt(prob(qubit[i]=0)), sqrt(prob(qubit[i]=1))]
    """
    from math import sqrt,log2
    num_qubits=int(log2(len(SystemStateVector)))
    ProbOfOne=0
    for i in range(len(SystemStateVector)):
        pos = str(("{0:0"+str(num_qubits).replace('.0000', '')+"b}").format(i))[::-1]
        if pos[qubit] == '1':
            ProbOfOne += abs(SystemStateVector[i])**2
    return [sqrt(1-ProbOfOne), sqrt(ProbOfOne)]


# In[100]:


import numpy as np
from qiskit import QuantumCircuit,QuantumRegister,ClassicalRegister,Aer,execute
from qiskit.quantum_info import partial_trace

stateToSend=[np.sqrt(0.70), np.sqrt(0.30)] 
#stateToSend=[1, 0] 

Alice_Qubits = QuantumRegister(2)    #qubit 0 and qubit 1
Bob_Qubit = QuantumRegister(1)       #qubit 2
creg1_Alice = ClassicalRegister(1)   #classical register 0
creg2_Alice = ClassicalRegister(1)   #classical register 1

circuit = QuantumCircuit(Alice_Qubits,Bob_Qubit,creg1_Alice,creg2_Alice)

#initialize the qubit 0 "the 1st qubit for Alice" with the given state
circuit.initialize(stateToSend,Alice_Qubits[0]) 
circuit.barrier()

#Entanglement between qubit 1 "the 2nd qubit for Alice" and qubit 2 "Bob qubit"
circuit.h(Alice_Qubits[1])
circuit.cx(Alice_Qubits[1],Bob_Qubit)
circuit.barrier()

#Alice measurements
circuit.cx(Alice_Qubits[0],Alice_Qubits[1])
circuit.h(Alice_Qubits[0])
circuit.barrier()

circuit.measure(Alice_Qubits[0], creg1_Alice)
circuit.measure(Alice_Qubits[1], creg2_Alice)
circuit.barrier()

#Bob correction step
circuit.x(Bob_Qubit).c_if(creg2_Alice, 1)
circuit.z(Bob_Qubit).c_if(creg1_Alice, 1)

#get the state vector of the system
backend = Aer.get_backend('statevector_simulator')
systemState = execute(circuit,backend).result().get_statevector()

#extract qubit 2 "Bob qubit" state vector using getStateVector() function
BobQubitStateVector = getStateVector(systemState,2)

print(circuit.draw('text'))

print("\nAlice sent state vector : ",stateToSend)

print("\nBob received state vector : ",BobQubitStateVector)

print("\nreceived correct data : ",BobQubitStateVector==stateToSend)


# In[ ]:




