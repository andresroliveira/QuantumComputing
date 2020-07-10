import numpy as np
import math
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

i0 = "000"
n  = 3

ctrl = QuantumRegister(n, "ctrl")
auxl = QuantumRegister(n-1, "auxl")
targ = QuantumRegister(1, "targ")
clas = ClassicalRegister(n, "clas")
circuit = QuantumCircuit(ctrl, auxl, targ, clas)

# ---------- Initial State ------------ #
for i in range(n):
    circuit.h(ctrl[i]);
    
circuit.x(targ[0]);
circuit.h(targ[0]);

# ---------- Grover Circuit ------------ #
t = math.floor(math.pi/4.0 * math.sqrt(2**n))
for _ in range(t):
    # ---------- Oracle ------------ #
    for k in range(n):
        if i0[k] == "0":
            circuit.x(ctrl[k])

    circuit.ccx(ctrl[0], ctrl[1], auxl[0])
    for i in range(2, n):
        circuit.ccx(ctrl[i], auxl[i-2], auxl[i-1])

    circuit.cx(auxl[n-2], targ[0])

    for i in range(n-1, 1, -1):
        circuit.ccx(ctrl[i], auxl[i-2], auxl[i-1])
    circuit.ccx(ctrl[0], ctrl[1], auxl[0])

    for k in range(len(i0)):
        if i0[k] == "0":
            circuit.x(ctrl[k])


    # ---------- Inversion About The Mean ------------ #
    for i in range(n):
        circuit.h(ctrl[i]);
        circuit.x(ctrl[i]);
    
    circuit.s(ctrl[0]) 
    circuit.x(ctrl[0]) 
    circuit.s(ctrl[0])
    circuit.x(ctrl[0])
    circuit.h(ctrl[n-1])

    circuit.ccx(ctrl[0], ctrl[1], ctrl[2])

    circuit.x(ctrl[0])
    circuit.sdg(ctrl[0]) 
    circuit.x(ctrl[0]) 
    circuit.sdg(ctrl[0])
    circuit.h(ctrl[n-1])
    
    for i in range(n):
        circuit.x(ctrl[i]);
        circuit.h(ctrl[i]);

# ---------- Measurement ------------ #
circuit.measure(ctrl, clas);


from qiskit import BasicAer, execute

# ---------- Simulator ------------ #
simulator = BasicAer.get_backend("qasm_simulator")
job = execute(circuit, simulator)
result = job.result()
print(result.get_counts())
