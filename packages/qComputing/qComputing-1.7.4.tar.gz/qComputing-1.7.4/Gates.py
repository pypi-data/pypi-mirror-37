from numpy import array, sqrt, kron, zeros, pi, dot, trace, asarray, identity
from numpy import testing,linalg
import Operations as op
from scipy.linalg import expm
from cmath import exp
import SpecialStates as ss
from itertools import product


def x():
    out = array([[0, 1], [1, 0]])
    return out


def h():
    out1 = 1/sqrt(2)*array([[1, 1], [1, -1]])
    return out1


def id():
    out2 = array([[1, 0], [0, 1]])
    return out2


def y():
   out3 = array([[0, -1j], [1j, 0]])
   return out3


def z():
    out4 = array([[1, 0], [0, -1]])
    return out4


def cnot():
    out5 = array([[1, 0, 0, 0, ], [0, 1, 0, 0, ], [0, 0, 1, 0], [0, 0, 0, 1]])
    return out5


def cz():
    out6 = array([[1, 0, 0, 0, ], [0, 1, 0, 0, ], [0, 0, 1, 0], [0, 0, 0, -1]])
    return out6


def r_x(theta):
    out7 = expm(-1j*theta*x()/2)
    return out7


def r_y(theta):
    out8 = expm(-1j*theta*y()/2)
    return out8


def r_z(theta):
    out8 = expm(-1j*theta*z()/2)
    return out8


def r_i(theta):
    out9 = expm(-1j*theta*id()/2)
    return out9


def phase(theta):
    out10 = array([[1, 0], [0, exp(1j*theta)]])
    return out10


def b1():
    out = array([[1, 0], [0, 0]])
    return out


def b2():
    out = array([[0, 1], [0, 0]])
    return out


def b3():
    out = array([[0, 0], [1, 0]])
    return out


def b4():
    out = array([[0, 0], [0, 1]])
    return out


def swap():
    out =array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    return out


def q_Hamiltonian(ham, n, s):
    """
    :param ham: hamiltonian by which the qubits will evolve by
    :param s : must be a string of ones e.g 010 represents id (tensor)ham(tensor)id while 10 represents ham(tensor) id
    :param n : The length of the string. This determines how many zeros there will be
    :return:
    """

    label = op.generatehamiltoniantring(n, s)
    a = zeros((pow(2, n), pow(2, n)), dtype=complex)
    terms = {
         "0": id(),
         "1": ham
     }
    for qubit in range(len(label)):
        tmp = 1
        for digit in label[qubit]:
            tmp = kron(tmp, terms[digit])
        a += tmp
    return a


def e_ij(tup, i, j):
    """
    :param tup: Dimension of your matrix
    :param i: The row your 1 will appear
    :param j: The column your 1 will appear
    :return: This returns a matrix with 1 in some spot (i,j) and zeros else where
    """
    k = zeros(tup)
    k[i-1, j-1] = 1
    return k


def c_u(u, n, i, j):
    """
    This creates a controlled unitary operation on n qubits
    :param u: Unitary matrix
    :param n: The number of qubits to be used
    :param i: the position of control qubit for the controlled operation
    :param j: the position of target qubit for the controlled operation
    :return:  the controlled operation
    """
    term_1 = {
        "0": id(),
        "1": e_ij((2, 2), 1, 1)
    }
    term_2 = {
        "0": id(),
        "2": u,
        "1": e_ij((2, 2), 2, 2)
    }

    # What happens when the control qubit is in the zero state
    label_1 = op.generatetensorstring(n, i)
    cu_1 = op.superkron(term_1, val=1, string=label_1)

    # What happens when the control bit is in the one state
    label_2 = op.controlgatestring(n, ('1', i), ('2', j))
    cu_2 = op.superkron(term_2, val=1, string=label_2)

    return cu_1 + cu_2


def reversed_cu(u, n, i, j):
    """
        This creates a controlled unitary operation on n qubits
        :param u: Unitary matrix
        :param n: The number of qubits to be used
        :param i: the position of control qubit for the controlled operation
        :param j: the position of target qubit for the controlled operation
        :return:  the controlled operation
        """
    term_1 = {
        "0": id(),
        "1": e_ij((2, 2), 1, 1)
    }
    term_2 = {
        "0": id(),
        "2": u,
        "1": e_ij((2, 2), 2, 2)
    }

    # What happens when the control qubit is in the zero state
    label_1 = op.generatetensorstring(n, i)
    label_1 = ''.join(list(reversed(label_1)))
    cu_1 = op.superkron(term_1, val=1, string=label_1)

    # What happens when the control bit is in the one state
    label_2 = op.controlgatestring(n, ('1', i), ('2', j))
    label_2 = ''.join(list(reversed(label_2)))
    cu_2 = op.superkron(term_2, val=1, string=label_2)

    return cu_1 + cu_2


def qft(n):
    """
    :param n: The number of qubits
    :return:  outputs the quantum fourier transform for n qubits
    """
    w = exp(1j*2*pi/n)
    dft = zeros((n, n), dtype=complex)
    for i in range(0, n):
        for k in range(0, n):
            dft[i, k] = pow(w, i*k)
    return dft*1/sqrt(n)


def bakersmap(n):
    """
    :param n: The number of qubits
    :return:
    """
    q = qft(n)
    q_1 = qft(n/2)
    out = op.ctranspose(q)*kron(id(), q_1)

    return out


def multi_hadamard(n):
    temp = 1
    for i in range(0, n):
        temp = kron(temp, h())
    return temp


def pauli_group(n, full=False, normalize=True):
    """
    :param n: number of qubits
    :param full: If true returns the full pauli group for n qubits including group elements that differ by center
    of the group
    :param normalize: If true returns pauli group elements so that group are normalized
    :return: Returns a dictionary of unitary representation of the single qubit pauli group
    """
    if normalize:
        pauli_matrix = {'I': id() / sqrt(2), 'X': x() / sqrt(2), 'Y': y() / sqrt(2), 'Z': z() / sqrt(2)}  
    else:
        pauli_matrix = {'I': id(), 'X': x(), 'Y': y(), 'Z': z()}
    center = {'i': 1j, '-i': -1j, '1': 1, '-1': -1}
    pauli_labels = [''.join(i) for i in product('IXYZ', repeat=n)]
    qubit_group = {}
    pauli_dict ={}
    if full is False:
        for pl in pauli_labels:
            pauli_dict[pl] = op.superkron(pauli_matrix, val=1, string=pl)
    else:
        for i in center:
            for p in pauli_dict:
                qubit_group[str(i)+str(p)] = dot(center[i], pauli_dict[p])

    return pauli_dict


def pauli_expansion(rho, pauli_d):
    """
    Pauli terms contributing to density matrix rho
    :param rho: The density matrix for which you need the pauli expansion
    :param pauli_d: The n qubit pauli group in which you write your density matrix expansion
    :return:
    """

    pauli_terms = {}
    for i in pauli_d:
        r = (trace(dot(rho,pauli_d[i])))
        if r != 0:
            pauli_terms[i] = r

    return pauli_terms


def stabilizer(stabilizer, n, ancilla_label):
    """
    Stabilizer must contain only X and Z operators

    :param stabilizer: The stabilizer you want to measure
    :param ancilla_label: The ancilla_label qubit used to measure the stabilizer
    :param n: The number of data qubits in the circuit
    :return: A unitary that represents a quantum circuit that is used to measure a specific stabilizer,
    using CNOT and Hadamard gates
    """

    # The numbering of qubits starts from 1 rather than 0
    stabilizer_dict = {}
    oper_dict = {'0': id(), '1': h()}
    unitary = identity(pow(2, n))
    for counter, s in enumerate(stabilizer, 1):
        if s == 'I' or s == 'i':
            continue
        else:
            stabilizer_dict[counter] = s

    for s in stabilizer_dict:
        if stabilizer_dict[s] == 'Z' or stabilizer_dict[s] == 'z':
            unitary = dot(unitary, c_u(x(), n, s, ancilla_label))
        elif stabilizer_dict[s] == 'X' or stabilizer_dict[s] == 'x':
            string = op.generatehamiltoniantring(n, '1', onestring=True, pos=s-1, pad='0')
            unitary = dot(unitary, op.superkron(oper_dict, val=1, string=string))
            unitary = dot(unitary, c_u(x(), n, s, ancilla_label))
            unitary = dot(unitary, op.superkron(oper_dict, val=1, string=string))
    return unitary


if __name__ == '__main__':

    d = stabilizer('ZIZ', 5, 4)
    # print('Unitary from measure_stabilizer: ', d)
    # a = op.superkron(h(), id(), id())
    # b = op.superkron(id(), h(), id())
    e = c_u(x(), 5, 1, 4)
    f = c_u(x(), 5, 3, 4)
    # g = dot(a, dot(e, a))
    # i = dot(b, dot(f, b))
    j = dot(f, e)

    # print('Unitary to check: ', j)
    print('norm between matrices : ',  linalg.norm(d-j))










