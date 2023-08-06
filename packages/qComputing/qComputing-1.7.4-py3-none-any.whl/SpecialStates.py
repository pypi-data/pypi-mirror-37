import numpy as np
import qubit_class as qubit
import Operations as op
import Gates as g
import qutip as qt
# from sympy import*
# from sympy.physics.quantum import *


def clusterstate(n, noisy=False, kraus=None):
    """
    This creates a cluster state
    :param n: This is the number of qubits in the system
    :param string: This is the string that determines the state of the initial system. e.g
    '0000' produces 4 qubit state being all in the ground state while '01010' produces a five qubits with
    qubits being in ground and excited states alternately
    :param ar: This is a list of numbers that specifies the various control and target position
    e.g clusterstate(4, '0000', [1,3,2,4]) creates two control operations with first qubit being the control and the third qubit
    being the target and the second operation has second being the control with the fourth qubit being the target.
    :param noisy: If true decoherence is added between gate applications
    :param kraus: This will be a 3 dimensional array of kraus matrices
    :return: returns the state of the qubit after the controlled z operations. This should be a cluster state

    """
    string = '0'*n
    q = qubit.Qubit(string, n)
    q.state = np.dot(g.multi_hadamard(n), np.dot(q.state, g.multi_hadamard(n)))
    if noisy is False:
        for i in range(1, n+1):
            controlgate = g.c_u(g.z(), n, i, i+1)
            q.state = np.dot(controlgate, np.dot(q.state, op.ctranspose(controlgate)))
    else:
        for i in range(1, n+1):
            controlgate = g.c_u(g.z(), n, i, i+1)
            q.q_decohere(kraus, n)
            q.state = np.dot(controlgate, np.dot(q.state, op.ctranspose(controlgate)))
    return q


def ghz_state(n, noisy=False, kraus=None):
    """
    This creates an n qubit ghz state
    :param n:  The number of qubits in the state
    :param string: The string for the initial state of the density matrix e.g '000' produces a state where all
    the three qubits are in the ground state while '111' produces a state where all the qubits are the excited state
    :param ar: This is a list of numbers that specifies the various control and target position
    e.g ghz_state(4, '0000', [1,2,1,3,1,4]) creates two control operations with first qubit being the
    control and the second qubit being the target and the second operation has first being the control
    with the third qubit being the target third operation has the first qubit being the control and the
    fourth qubit being the target
     :param noisy: If true decoherence is added between gate applications
    :param kraus: This will be a 3 dimensional array of kraus matrices
    :return: returns the state of the qubit after the controlled x operations. This should be a ghz state.
    """
    string = '0'*n
    q = qubit.Qubit(string, n)
    h_gate = op.superkron(g.h(), np.eye(pow(2, n-1)))
    q.state = np.dot(h_gate, np.dot(q.state, h_gate))
    if noisy is False:
        for i in range(1, n+1):
            controlgate = g.c_u(g.x(), n, i, i + 1)
            q.state = np.dot(controlgate, np.dot(q.state, op.ctranspose(controlgate)))
    else:
        for i in range(1, n+1):
            controlgate = g.c_u(g.x(), n, i, i + 1)
            q.q_decohere(kraus, n)
            q.state = np.dot(controlgate, np.dot(q.state, op.ctranspose(controlgate)))

    return q


def purestate(string):
    """
    Creates a simple computational basis pure state using a string variable. e.g
    '000' produces a three qubit states with all being in the zero state while
    '100' produces three qubits with the first being in the excited state and the rest in the
    ground state.
    :param string:
    :return:
    """
    try:
        q = qubit.Qubit(string, len(string))
        return q
    except TypeError:
        return 'Please input string'


def ghz_qobj(n, density_matrix=False, noise=False, T1=None, T2=None, ham=None,
             time=None):
    """
    :param n:
    :param density_matrix:
    :param noise:
    :param T1: Should be a list of T1 times
    :param T2: Should be a list of T2 times
    :param ham: Hamiltonian for evolution
    :return:
    """
    q0 = qt.basis(2, 0)
    x = qt.sigmax()
    q_list = [q0 for i in range(0, n)]
    psi = qt.tensor(*q_list)
    if density_matrix is False:
        psi = qt.qip.snot(n, 0) * psi
        for i in range(0, n-1):
            psi = qt.qip.controlled_gate(x, n, 0, i+1) * psi
        return psi
    if density_matrix:
        rho = psi * psi.dag()
        rho = qt.qip.snot(n, 0)* rho * qt.qip.snot(n, 0)
        for i in range(0, n-1):
            rho = qt.qip.controlled_gate(x, n, 0, i+1) * rho * qt.qip.controlled_gate(x, n, 0, i+1)
        return rho
    if noise:
        q = qubit.QubitObj(n, T1, T2, [10**(-9)], string='0'*n,damp=True, phase_damp=True)
        q.hamiltonian = ham
        q.times = time
        q.evolve()
        q.apply_op(qt.qip.snot(n, 0))
        q.evolve()
        for i in range(0, n - 1):
            q.apply_op(qt.qip.controlled_gate(x, n, 0, i + 1))
            q.evolve()
        return q.rho


def cluster_obj(n, density_matrix=False, noise=False, T1=None, T2=None, ham=None,
             time=None):
    q0 = qt.basis(2, 0)
    z = qt.sigmaz()
    q_list = [q0 for i in range(0, n)]
    psi = qt.tensor(*q_list)
    if density_matrix is False:
        psi = qt.qip.hadamard_transform(n) * psi
        for i in range(0, n-1):
            psi = qt.qip.controlled_gate(z, n, i, i+1) * psi
        return psi
    if density_matrix:
        rho = psi*psi.dag()
        rho = qt.qip.hadamard_transform(n) * rho * qt.qip.hadamard_transform(n)
        for i in range(0, n-1):
            rho = qt.qip.controlled_gate(z, n, i, i+1)* rho * qt.qip.controlled_gate(z, n, i, i+1)
        return rho
    if noise:
        q = qubit.QubitObj(n, T1, T2, [10 ** (-9)], string='0' * n, damp=True, phase_damp=True)
        q.hamiltonian = ham
        q.times = time
        q.evolve()
        q.apply_op(qt.qip.hadamard_transform(n))
        q.evolve()
        for i in range(0, n - 1):
            q.apply_op(qt.qip.controlled_gate(z, n, i, i + 1))
            q.evolve()
        return q.rho


def pure_obj(n, density_matrix=False):
    q0 = qt.basis(2, 0)
    q_list = [q0 for i in range(0, n)]
    psi = qt.tensor(*q_list)
    if density_matrix is False:
        return psi
    if density_matrix:
        return psi * psi.dag()


if __name__ == "__main__":

    state = clusterstate(3)
    # ghzstate = ghz_state(3)
    # print(ghz_qobj(3, density_matrix=True))
    # print(cluster_obj(2, density_matrix=True))
    # h = Matrix([[1, 1], [1, -1]])*1/sqrt(2)
    # o = Matrix([[1, 0], [0, 0]])
    # i = Matrix([[0, 0], [0, 1]])
    # id_gate = Matrix([[1, 0], [0, 1]])
    # z = Matrix([[1, 0], [0, -1]])
    # x = Matrix([[0, 1], [1, 0]])
    # cz = TensorProduct(o, id_gate, id_gate) + TensorProduct(i, z, id_gate)
    # cx = TensorProduct(o, id_gate, id_gate) + TensorProduct(i, x, id_gate)
    # cz_23 = TensorProduct(id_gate, o, id_gate) + TensorProduct(id_gate, i, z)
    # cx_13 = TensorProduct(o, id_gate, id_gate) + TensorProduct(i, id_gate, x)
    # multi_h = TensorProduct(h, h, h)
    # h_g = TensorProduct(h, id_gate, id_gate)
    # init_state = TensorProduct(o, o, o)
    # cluster = cz_23*(cz*(multi_h*init_state*multi_h**-1)*cz**-1)*cz_23**-1
    # ghz = cx_13*(cx * (h_g * init_state * h_g ** -1) * cx ** -1) * cx_13 ** -1
    # print(state.state)
    # print("The ghz state is : ", ghzstate.state)
    # pprint(cluster)



