import NoisyEvolution as ne
import numpy as np
import Operations as op
from scipy.linalg import expm
import Gates as g
from lea import *
from qutip import *
from matplotlib.pyplot import *
import SpecialStates as ss
import timeit


class Qubit(object):
    """
    This class  defines an N-qubit system and implements closed dynamics or open system dynamics
    assuming existence of kraus operators. For a linblad simulation use
    Qubitobj class.
    """

    def __init__(self, string, n, no_measurment_qubits=1, left_justified=False):
        """
        :param string: This should be a string of 1's and 0's where 1 is the |1> and
        0 is |0>
        :param n: The number of qubits in the system
        :param no_measurment_qubits:  The number of qubits that will be measured
        :return: Returns the

        Description of class variables
        state: This is the density matrix of the system
        classical_states: This is a dictionary of computational basis states that should have
        has its keys labels of computational basis states and values the corresponding
        probabilities
        projectors: This is a dictionary with keys being labels for the computational basis
        states and the values being the corresponding projectors for that particular
        computational basis state.
        no_measurement_qubits: The number of qubits you intend to measure
        classical_states_history: Has a key values all possible measurement syndromes and keeps a record of their
        probabilities
        """
        oper_dict = {'0': g.b1(), '1': g.b4(), '2': g.id()}

        self.state = op.superkron(oper_dict, val=1, string=string)
        self.n = n
        self.no_measurement_qubits = no_measurment_qubits
        self.measurement_string = op.createlabel(self.no_measurement_qubits, 2)
        for i in range(len(self.measurement_string)):
            if left_justified:
                self.measurement_string[i] = self.measurement_string[i].ljust(self.n, '2')
            else:
                self.measurement_string[i] = self.measurement_string[i].rjust(self.n, '2')
        self.projectors = {i.replace('2', ''): op.superkron(oper_dict, val=1, string=i) for i in
                           self.measurement_string}
        self.classical_states = {i.replace('2', ''): 0 for i in self.measurement_string}
        self.classical_states_history = {i.replace('2', ''): [] for i in self.measurement_string}
        self.hamiltonian = None
        self.dt = None
        self.U = None
        self.xlabel = ''
        self.ylabel = ''
        self.T = None
        self.kraus_operators = []

    def time_step_evolve(self, basis=''):
        """
        :param h: Hamiltonian by which to evolve the system
        :param dt: time step to evolve by could be small or large
        :param basis: Basis of measurement
        :return: returns the state of qubit after evolution
        """
        self.U = expm(-1j * self.hamiltonian * self.dt)
        self.state = np.dot(self.U, np.dot(self.state, op.ctranspose(self.U)))
        for state in self.classical_states:
            # Possibly change basis of measurement before calculating probability history.
            self.measure_basis(pauli_string=basis)
            self.classical_states_history[state].append(np.trace(np.dot(self.state, self.projectors[state])).real)
            self.measure_basis(pauli_string=basis, undo_basis=True)

    def q_decohere(self, k, n):
        self.state = ne.serial_decohere(k, self.state, n)

    def evolve(self, basis='', noise=False):
        """
        :param basis: Basis in which we will do the measurement
        :param noise: Boolean variable if true then evolution becomes noisy
        :return:
        """
        for i in np.arange(0, self.T, self.dt):
            self.q_decohere(self.kraus_operators, self.n)
            self.time_step_evolve(basis=basis)

    def measure(self, return_state=False, basis=''):
        """
        This performs a projective measurement on your n qubit system
        :param return_state: This is a boolean variable, if True it returns the label for
        :param basis: Basis in which to do the measurement. Must be an operator for pauli operator
        the classical state picked after projective measurement
        :return:
        """

        # Calculate the probabilities for all classical states
        for state in self.classical_states:
            # Possibly change the basis for measurement, if basis is empty nothing should happen
            self.measure_basis(pauli_string=basis)
            self.classical_states[state] = np.trace(np.dot(self.state, self.projectors[state])).real
        # Make the probabilities of classical states into numbers between 0 and 100 for Lea
        outcomes = {state: self.classical_states[state] * 100 for state in self.classical_states}
        picked_obj = pmf(outcomes)
        picked_state = picked_obj.random()
        self.state = self.projectors[picked_state]

        if return_state:
            return picked_state

    def operator(self, o):
        """
        :param o: The operator you want applied to the qubit
        :return:  Returns the transformed density matrix after the operation
        """
        self.state = np.dot(o, np.dot(self.state, op.ctranspose(o)))

    def measure_basis(self, pauli_string='', undo_basis=False):
        """
        :param pauli_string: Basis in which to make the measurement
        :param undo_basis: Boolean variable
        :return:
        """
        measurement_operator = 1
        if pauli_string != '' and undo_basis is False:
            for char in pauli_string:
                if char == 'X':
                    measurement_operator = op.superkron(measurement_operator, g.r_y(-np.pi / 2))
                elif char == 'Y':
                    measurement_operator = op.superkron(measurement_operator, g.r_x(np.pi / 2))
                else:
                    measurement_operator = op.superkron(measurement_operator, g.id())
            self.operator(measurement_operator)
        elif pauli_string != '' and undo_basis is True:
            for char in pauli_string:
                if char == 'X':
                    measurement_operator = op.superkron(measurement_operator, g.r_y(np.pi / 2))
                elif char == 'Y':
                    measurement_operator = op.superkron(measurement_operator, g.r_x(-np.pi / 2))
                else:
                    measurement_operator = op.superkron(measurement_operator, g.id())
            self.operator(measurement_operator)
        else:
            pass

    def graph(self, state):
        """
        :param state: Classical state for which we wish to plot results
        :return:
        """
        xlabel(self.xlabel)
        ylabel(self.ylabel)
        t = [i for i in range(0, len(self.classical_states_history[state]))]
        plot(t, self.classical_states_history[state], label='|' + state + '>')
        legend()
        show()


class QubitObj(object):
    """
    Does what the Qubit class does but with qutip stuff
    If you want to use qutip, this class automizes a lot of stuff
    Does a linblad equation simulation
    """

    def __init__(self, n, t1_list, t2_list, t3_list, string='', damp=True, phase_damp=True, finite_temp=False,
                 identical_bath=True):
        q0 = basis(2, 0)
        q1 = basis(2, 1)
        self.opt = Options(rhs_reuse=True, store_states=True)
        q_list = []
        q_list1 = []
        if isinstance(string, str):
            for c in string:
                if c == '0':
                    q_list.append(q0)
                    q_list1.append(q0 * q0.dag())
                    self.psi = tensor(*q_list)
                    self.rho = tensor(*q_list1)
                elif c == '1':
                    q_list.append(q1)
                    q_list1.append(q1 * q1.dag())
                    self.rho = tensor(*q_list1)
                    self.psi = tensor(*q_list)
        self.hamiltonian = 0
        self.psi_results = 0
        self.rho_results = 0
        self.operators = []
        self.c_op = {}
        self.dephase_op = {}
        self.create_op = {}
        self.collap = []
        self.x_label = ''
        self.y_label = ''
        self.label = ''
        self.x_axis = []
        self.y_axis = []
        self.n = n
        self.t1 = t1_list
        self.t2 = t2_list
        self.t3 = t3_list
        self.times = 0
        self.annihilate = {'0': qeye(2), '1': destroy(2)}
        self.create = {'0': qeye(2), '1': create(2)}
        self.dephase = {'0': qeye(2), '1': sigmaz()}
        self.final_state = 0
        for i in range(0, n):
            self.c_op[str(i)] = []
            self.create_op[str(i)] = []
            self.dephase_op[str(i)] = []
        self.noise_op(same_bath=identical_bath, relax=damp, dephase=phase_damp, create=finite_temp)

    def evolve(self):
        self.psi_results = mesolve(self.hamiltonian, self.psi, self.times, [], self.operators, options=self.opt)
        self.rho_results = mesolve(self.hamiltonian, self.rho, self.times, self.collap, self.operators,
                                   options=self.opt)
        self.final_state = self.rho_results.states[-1].full()

    def apply_op(self, op):
        self.psi = op * self.psi
        self.rho = op * self.rho * op.dag()

    def graph(self, *args):
        xlabel(self.x_label)
        ylabel(self.y_label)
        plot(*args, label=self.label)
        legend()
        show()

    def noise_op(self, same_bath=True, relax=True, dephase=False, create=False):
        noise_op_string_list = op.generatehamiltoniantring(self.n, '1')
        for qubit, string in enumerate(noise_op_string_list):
            for char in string:
                self.c_op[str(qubit)].append(self.annihilate[char])
                self.dephase_op[str(qubit)].append(self.dephase[char])
                self.create_op[str(qubit)].append(self.create[char])
        for q, q1, q2 in zip(self.c_op, self.dephase_op, self.create_op):
            if relax:
                self.c_op[q] = tensor(*self.c_op[q])
            if dephase:
                self.dephase_op[q1] = tensor(*self.dephase_op[q1])
            if create:
                self.create_op[q2] = tensor(*self.create_op[q2])
                self.collap.append(self.create_op[q2])
        if same_bath:
            if relax:
                for qs in self.c_op:
                    self.c_op[qs] = np.sqrt(1 / self.t1[0]) * self.c_op[qs]
                    self.collap.append(self.c_op[qs])
            if dephase:
                for qs in self.dephase_op:
                    self.dephase_op[qs] = np.sqrt(1 / (2 * self.t2[0])) * self.dephase_op[qs]
                    self.collap.append(self.dephase_op[qs])
            if create:
                for qs in self.dephase_op:
                    self.create_op[qs] = np.sqrt(1 / (self.t3[0])) * self.create_op[qs]
                    self.collap.append(self.create_op[qs])
        if same_bath is False:
            if relax:
                for t1_list, qs in enumerate(self.c_op):
                    self.c_op[qs] = np.sqrt(1 / self.t1[t1_list]) * self.c_op[qs]
                    self.collap.append(self.c_op[qs])
            if dephase:
                for t2_list, qs in enumerate(self.dephase_op):
                    self.dephase_op[qs] = np.sqrt(1 / (2 * self.t2[t2_list])) * self.dephase_op[qs]
                    self.collap.append(self.dephase_op[qs])
            if create:
                for t3_list, qs in enumerate(self.create_op):
                    self.create_op[qs] = np.sqrt(1 / self.t3[t3_list]) * self.create_op[qs]
                    self.collap.append(self.create_op[qs])


if __name__ == '__main__':
    # q = QubitObj(4, [0.5, 0.3], [0.5, 0.6], [10**(-9), 10**(-9)], string='1111',
    #              identical_bath=True)
    # q.times = np.linspace(0, 1, 10000)
    # q.hamiltonian = tensor(sigmaz(), sigmaz(), sigmaz(),sigmaz())
    # q.operators.append(tensor(sigmay(), sigmay(),sigmay(), sigmay()))
    # q.rho = ss.cluster_obj(4, density_matrix=True)
    # q.x_axis = q.times
    # q.evolve()
    # print(q.rho_results.expect[0])
    # q.y_axis = q.rho_results.expect[0]
    # q.label = 'Probability of $\sigma_z$'
    # q.graph(q.times, q.y_axis)

    init = '1'
    oper_dict = {'0': g.z()}
    E = [np.array([[1, 0], [0, np.cos(np.pi/20)]]), np.array([[0, np.sin(np.pi/20)], [0, 0]])]
    k = ne.generic_kraus(1, classical_error=False, opers=E)
    q2 = Qubit(init, 1, no_measurment_qubits=1)
    q2.dt = 0.01
    q2.T = 1
    # k = ne.kraus_ad(q2.n, 0.001, 10 ** (-2))
    # k = ne.kraus_exact(q2.n, q2.dt, 10**(-6), 10**(-6), markovian=True)
    q2.kraus_operators= k
    q2.xlabel='time'
    q2.ylabel = 'Probability'
    q2.hamiltonian = 0.5*op.superkron(oper_dict, val=1, string='0')
    q2.evolve(basis='Z', noise=True)
    q2.graph('1')
