import qubit_class as q
import Gates as g
import Operations as op
import inspect
from itertools import zip_longest
import numpy as np
from collections import OrderedDict

"""
The purpose of this class is to abstract most of the job of making quantum circuits.
The user is supposed to merely use strings for gates and corresponding list of arguments
for gates and get back the unitary operator for that gate
"""


class Circuit(object):
    def __init__(self, state, n=3, measurement_qubits=None):
        """
        :param state: A string for the initial density matrix which will be used for the circuit
        """
        self.qubits = q.Qubit(state, n, no_measurment_qubits=measurement_qubits)
        self.bucket = OrderedDict()  # contains the string of functions for each step
        self.gate_list = {}  # contains a list of functions from the Gates module
        self.get_gates()  # adds "g." to string representation of function
        self.arg_bucket = OrderedDict()  # For each step we have a list of arguments. An element in a list tells us the
        # For the specific function
        self.n = n  # Number of qubits in the circuit

    def get_circuit(self):
        return self.bucket

    def apply_circuit(self):
        """
         Applies all the steps in the bucket
        :return:
        """
        for i in range(0, len(self.bucket)):
            self.apply_step(str(i))

    def add_step(self, gate_string, arg_list=[]):
        """
        :param gate_string: A string of gates with gate names separated by a comma
        :param arg_list: The is a list of arguments each element contains arguments for a specific function
        i.e the first element of list contains argument for first function
        :return:
        """
        # if isinstance(step, str) and isinstance(gate_string, str):
        #     for i in self.arg_bucket:
        #         if step == i:
        #             raise Exception('There is an attempted duplication of step numbers')
        #     self.arg_bucket[step] = {}
        #     self.bucket[step] = list(gate_string.split(','))
        #     # if arg_list:
        #     for m, i in zip_longest(self.bucket[step], arg_list):
        #         self.arg_bucket[step][m] = i
        # else:
        #     return 'Please use strings for step and gate_string arguments'

        if not self.arg_bucket:
            if isinstance(gate_string, str):
                self.arg_bucket['0'] = {}
                self.bucket['0'] = list(gate_string.split(','))
                for m, i in zip_longest(self.bucket['0'], arg_list):
                    self.arg_bucket['0'][m] = i
            else:
                raise Exception('PLEASE USE STRINGS FOR gate_string ARGUMENTS')
        else:
            previous_step = int(next(reversed(self.arg_bucket)))
            next_step = str(previous_step + 1)

            if isinstance(gate_string, str):
                self.arg_bucket[next_step] = {}
                self.bucket[next_step] = list(gate_string.split(','))
                for m, i in zip_longest(self.bucket[next_step], arg_list):
                    self.arg_bucket[next_step][m] = i
            else:
                raise Exception('PLEASE USE STRINGS FOR gate_string ARGUMENTS')

    def delete_step(self, step):
        """
        :param step: Should be string deletes the step in the bucket you do not want
        :return:
        """
        del self.bucket[step]

    def get_gates(self):
        """
        :return: Returns a dictionary of  from Gates module
        """
        list = dir(g)
        for i in list:
            if i[0] != '_' and i != 'array':
                self.gate_list[i] = 'g.' + i

    def apply_step(self, step):
        """
        :param step: The step in the circuit
        :return:  Applies the operator for a particular step in the circuit to the qubit 
        density matrix
        """
        if isinstance(step, str):
            o = self.step_operator(step)
            self.qubits.operator(o)
        else:
            return 'Argument should be a string'

    def step_operator(self, step):
        """
        :param step: The step in the circuit
        :return: Returns a the operator for the particular step in the circuit
        """
        op_list = []
        if isinstance(step, str):
            for s in self.bucket[step]:
                op_list.append(self.gate_list[s])
            operators = list(map(eval, op_list))
            for i in range(len(operators)):
                if self.check_signature(operators[i]) is not []:
                    arg = self.arg_bucket[step][operators[i].__name__]
                    operators[i] = operators[i](*arg)
                else:
                    operators[i] = operators[i]()
        o = op.superkron(*operators)
        return o

    def check_signature(self, func):
        """
        This function checks to see if func requires arguments
        :param func: The function we would like to examine
        :return: List of the arguments
        """
        sig = inspect.signature(func)
        arg_list = list(sig.parameters)
        return arg_list

    def circuit_unitary(self):
        """
        :return: Returns the unitary for the circuit
        """
        out = np.eye(2 ** self.n, dtype='complex128')
        for i in self.bucket:
            out = np.dot(out, self.step_operator(i))
        out = op.ctranspose(out)
        return out

    def apply_unitary(self):
        """
        Applies unitary to the quantum state

        """
        U = self.circuit_unitary()
        self.qubits.operator(U)


if __name__ == '__main__':
    # This should create a 3 qubit GHZ circuit
    xxx = op.superkron(g.x(), g.x(), g.x())
    c = Circuit('000', measurement_qubits=3)
    c.add_step('h,id,id', arg_list=[[], [], []])
    c.add_step('c_u', arg_list=[[g.x(), 3, 1, 2]])
    c.add_step('c_u', arg_list=[[g.x(), 3, 2, 3]])
    c.apply_unitary()
    ghz = c.qubits.state
    # print('GHZ unitary: ', c.circuit_unitary())
    # print('GHZ state : ', ghz)

    # This should be a Toffoli gate circuit

    d = Circuit('110', measurement_qubits=3)
    d.add_step('x,id,id', arg_list=[[], [], []])
    d.add_step('id,id,r_y', arg_list=[[], [], [g.pi / 4]])
    d.add_step('c_u', arg_list=[[g.x(), 3, 2, 3]])
    d.add_step('id,id,r_y', arg_list=[[], [], [g.pi / 4]])
    d.add_step('id,id,x', arg_list=[[], [], []])
    d.add_step('c_u', arg_list=[[g.x(), 3, 1, 3]])
    d.add_step('id,id,r_y', arg_list=[[], [], [-g.pi / 4]])
    d.add_step('c_u', arg_list=[[g.x(), 3, 2, 3]])
    d.add_step('id,id,r_y', arg_list=[[], [], [-g.pi / 4]])
    # print(d.circuit_unitary())

    f = Circuit('00', n=2, measurement_qubits=2)
    f.add_step('id,phase', arg_list=[[], [-g.pi / 2]])
    f.add_step('c_u', arg_list=[[g.x(), 2, 1, 2]])
    f.add_step('id,phase', arg_list=[[], [0]])
    f.add_step('id,r_y', arg_list=[[], [-g.pi / 2]])
    f.add_step('c_u', arg_list=[[g.x(), 2, 1, 2]])
    f.add_step('id,r_y', arg_list=[[], [g.pi / 2]])
    f.add_step('id,phase', arg_list=[[], [g.pi / 2]])
    # print(f.circuit_unitary())

    # Should create a three qubit cluster state
    e = Circuit('000', n=3, measurement_qubits=3)
    e.add_step('h,h,h', arg_list=[[], [], []])
    e.add_step('c_u', arg_list=[[g.z(), 3, 1, 2]])
    e.add_step('c_u', arg_list=[[g.z(), 3, 2, 3]])
    e.apply_circuit()
    cluster = e.qubits.state
    # print(cluster)
    # print(np.trace(np.dot(xxx, cluster)))

    # 3 qubit ghz state with 2 ancilla
    r = Circuit('00000', n=5, measurement_qubits=2)
    r.add_step('h,id,id,id,id', arg_list=[[], [], [], [], []])
    r.add_step('c_u', arg_list=[[g.x(), 5, 1, 2]])
    r.add_step('c_u', arg_list=[[g.x(), 5, 2, 3]])
    r.apply_circuit()
    r.add_step('c_u', arg_list=[[g.x(), 5, 1, 4]])
    r.apply_circuit()
    print(r.qubits.classical_states)




