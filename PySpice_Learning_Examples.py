import numpy as np
import matplotlib as plt
import sys, os
import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit, SubCircuit, SubCircuitFactory
from PySpice.Unit import *
logger = Logging.setup_logging()
# Voltage Divider
circuit = Circuit("Voltage Divider")
circuit.V('input', 'in',circuit.gnd, 10@u_V)
circuit.R(1, 'in', 'out', 9@u_kOhm)
circuit.R(2, 'out', circuit.gnd, 1@u_kOhm)
print("The Circuit/Netlist: \n",circuit)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
print("The simulator: \n",simulator)
anslysis = simulator.operating_point()
print('_' * 66 + "\n")

# Diodes, Raw Spice and Subcircuits
circuit = Circuit("Diode")
circuit.model('MyDiode','D',IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)
circuit.V('input',1,circuit.gnd,10@u_V)
circuit.R(1, 1, 2, 9@u_kOhm)
circuit.Diode(1, 2, 3, model='MyDiode')
circuit.R(2, 3, circuit.gnd, 9@u_kOhm)
circuit.raw_spice = 'D2 23 MyDiode IS=1n' + os.linesep

class MySubCir(SubCircuit):
    __nodes__ = ('t_in','t_out')
    def __init__(self, name, resester = 1@u_kOhm):
        SubCircuit.__init__(self,name,*self.__nodes__)
        self.R(1, 't_in', 't_out', resester)
        self.Diode(1,'t_in','t_out', model='MyDiode')

circuit.subcircuit(MySubCir('sub1',resester = 1@u_kOhm))
circuit.X(1, 'sub1', 3, circuit.gnd)
print("The circuit/netList:\n",circuit)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
print("The simulator: \n",simulator)
print('_' * 66 + "\n")

# basic and costom DC Sweep
circuit = Circuit("basic and costom DC Sweep")
circuit.model('MyDiode','D',IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)
circuit.V('input',1,circuit.gnd,10@u_V)
circuit.Diode(1, 1, 2, model='MyDiode')
circuit.R(1, 2, circuit.gnd, 1@u_kOhm)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
anslysis = simulator.operating_point()
print('Node:',str(anslysis['1']), 'values:',np.array(anslysis['1']))
print('Node:',str(anslysis['2']), 'values:',np.array(anslysis['2']))
