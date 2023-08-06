from numpy import zeros, dot, savetxt, array, kron, pi, exp, conjugate
from numpy.linalg import eig
from numpy import genfromtxt
import matplotlib.pyplot as plt
import qutip as qt
import Gates as g
from numpy import trace, cos, sin, arcsin, random, sqrt
# from quantum_CSD_compiler.DiagUnitaryExpander import *
# from quantum_CSD_compiler.MultiplexorExpander import *
# from quantum_CSD_compiler.Tree import *
# from for_IBM_devices.Qubiter_to_IBMqasm2_5q import *
import numpy as np
import os
import glob


def checknormkraus(k, n):
    """
    Makes sure that the kraus matrices are properly normalized and therefore preserve probability
    :param k: A 3 dimensional array of shape(m,2^n,2^n). m is the number of kraus matrices
    :param n: The number of qubits
    :return: Should return identity
    """
    out = zeros((pow(2, n), pow(2, n)), dtype=complex)
    for x in range(len(k)):
        out += dot(ctranspose(k[x]), k[x])
    return out


def blockshaped(arr, nrows, ncols):
    """
    Return an array of shape (n, nrows, ncols) where
    n * nrows * ncols = arr.size

    If arr is a 2D array, the returned array looks like n subblocks with
    each subblock preserving the "physical" layout of arr.
    """
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols)
               .swapaxes(1,2)
               .reshape(-1, nrows, ncols))


def unblockshaped(arr, h, w):
    """
    Return an array of shape (h, w) where
    h * w = arr.size

    If arr is of shape (n, nrows, ncols), n sublocks of shape (nrows, ncols),
    then the returned array preserves the "physical" layout of the sublocks.
    """
    n, nrows, ncols = arr.shape
    return (arr.reshape(h//nrows, -1, nrows, ncols)
               .swapaxes(1,2)
               .reshape(h, w))


def dec2base(n, base):
    """
    Gets gives you a string in base less than 20
    :param n: The number you have
    :param base: The base you want
    :return:  The string containing giving the base m representation
    """
    convertstring = "0123456789ABCDEF"
    if n < base:
        return convertstring[n]
    else:
        return dec2base(n // base, base) + convertstring[n % base]


def createlabel(q, n):
    """
    Create a string of labels for making kraus matrices
    :param q: Number of qubits also the length of the label string
    :param n: Number of distinct kraus matrices for one qubit
    :return: A list of labels
    """
    # When using dec2base function make sure to pad the string with the right number of zeros e.g for base 3 dec2base
    # gives 1 rather than 01 if we were dealing with 2 qubits.
    # The number of kraus matrices or labels is  n^q

    label = []
    for i in range(pow(n, q)):
        label.append(dec2base(i, n))

    # Next we make sure that each element in the label list has length the number of qubits if not add a zero
    for x in range(len(label)):
        if len(label[x]) < q:
            label[x] = label[x].zfill(q)
        else:
            break
    return label


def padded_dec2base(n, q, base):
    """
       Gets gives you a string in base less than 20
       :param n: The number you have
       :param q: The number of qubits in system or determines the number of zeros to pad i.e
       if n=3 and q=3 the function will return 011 rather than 11
       :param base: The base you want
       :return:  The string containing giving the base m representation
       """
    convertstring = "0123456789ABCDEF"
    if n < base:
        return convertstring[n].zfill(q)
    else:
        return (dec2base(n // base, base) + convertstring[n % base]).zfill(q)


def ctranspose(A):
    """
    :param A: Matrix A
    :return: Conjugate transpose of A
    """
    out = A.conjugate().transpose()
    return out


def frange(start, end, step):
    tmp = start
    while tmp < end:
        yield tmp
        tmp += step


def write_to_file(name, *args):
    """
    :param name: A string that is the name of the file to which the data will be written to
    :param args: list of arguments with entries being data e.g arg[0] = time where time is a list of times
    :return:
    """

    data = array(args).T
    file = open(name, 'w+')
    savetxt(name, data, fmt=['%.5f', '%.5f'])
    file.close()


def load_data(f='', use_cols=[], xlabel='', ylabel='',scatter=False,contour=False, connect=False,
              errorbar=False, std_col=None, data_domain=None, labo=[], title='',
              return_data=False, graph=False, multiple_files=None, file_stem='', folder=None,
              file_list = None, color_list=None, combine=False):
    """
    This function has two uses, it either loads the data and plots it if val=1 or it just gets the data from
     the data file and puts it into arrays which it returns
    :param f: String varible containing name of the file
    :param scatter: Boolean variable , make True if scatter plot is desired
    :param connect: Boolean variable, make True if connected plot is desired
    :param errorbar: Boolean variable, make True if verticle error bars are desired
    :param std_col: Should be integer. Specifies which column in file will represent
    the errorbars
    :param contour: Boolean variable, make True if contour plot is desired
    :param use_cols: Which columns in the file do you want to work with. Must
    be a list
    :param data_domain: This is filled in when the x axis data is not part of
    the file i.e defined externally
    :param labo : This is the label for the graph
    :param title: The title of the graph
    :param graph: Boolean expression, make True if you want to graph data.
    :param return_data: Boolean expression, make True if you want to simply
    return specific columns from file. Columns will be in a list
    :param xlabel: xlabel for the graph
    :param ylabel: ylabel for the graph
    :param multiple_files: Boolean expression, make True if data is going to
    be retrieved from many data files in a folder
    :param file_stem: Used if multiples_files is True, contains a string
    that the set of files all have
    :param folder: Folder which contains the files. Used if multiple files
    is True
    :param color_list: List of colors to use for graphs
    :param combine: Boolean expression, if true data from data files is combined
    :return:
    """

    def combine_data(data_files_dict):
        """
        This combines data from different files so that the first column of file 1 is concatenated with first column
        oof file 2 and so on
        :param data_files_dict:
        :return:
        """
        key_list = list(data_files_dict.keys())
        no_col = len(data_files_dict[key_list[0]])
        combined = []
        for n in range(0, no_col):
            d = np.empty(shape=[0, 1])
            for k in data_files_dict:
                d = np.append(d, data_files_dict[k][n])
            combined.append(d)
        return combined

    def data_graph(graph=False):
        """
        Gets data from folder or list of files or file and graphs it in
        some manner
        :param graph:
        :return:
        """
        def axes_data(use_cols1, data1, domain=None):
            if domain is not None:
                axis = [0] * (2 * len(use_cols1))
                for k in range(len(use_cols1)):
                    axis[2 * k] = domain
                    axis[2 * k + 1] = data1[k]
                return axis
            else:
                axis = [data1[k] for k in use_cols1]
                return axis
        if graph:
            axes = axes_data(use_cols, data, domain=data_domain)
            if scatter:
                for i in range(int(len(axes)/2)):
                    if i % 2 == 0:
                        plt.scatter(axes[2*i], axes[2*i+1], color_list[i],
                                 label=labo[i])
                    else:
                        plt.scatter(axes[2 * i], axes[2 * i + 1], color_list[i]
                                 ,label=labo[i])

            if connect:
                for i in range(int(len(axes)/2)):
                    if i % 2 == 0:
                        plt.plot(axes[2*i], axes[2*i+1], color_list[i],
                                 label=labo[i])
                    else:
                        plt.plot(axes[2 * i], axes[2 * i + 1], color_list[i]
                                 , label=labo[i])

            if errorbar:
                plt.errorbar(*axes, yerr=data[std_col], fmt='o', label=labo)
            if contour:
                from mpl_toolkits.mplot3d import Axes3D
                from matplotlib import cm
                from matplotlib.ticker import LinearLocator, FormatStrFormatter
                fig = plt.figure()
                ax = fig.gca(projection='3d')
                z = axes[2][:100]
                len_z = len(z)
                n = np.sqrt(len_z)
                x = np.arange(0, n)
                y = x
                x, y = np.meshgrid(x,y)
                two_dz = z.reshape((int(n), int(n)))
                surf = ax.plot_surface(x,y,two_dz,cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
                # Customize the z axis.
                ax.set_zlim(0, 0.18)
                ax.zaxis.set_major_locator(LinearLocator(10))
                ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

                # Add a color bar which maps values to colors.
                fig.colorbar(surf, shrink=0.5, aspect=5)
                # heat_map = plt.pcolor(two_dz)
                # heat_color = plt.colorbar(heat_map, orientation = 'horizontal')
                # heat_color.set_label('Average Fidelity')

            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)
            plt.legend()
            plt.show()

    if multiple_files and folder is not None:
        os.chdir(folder)
        files = sorted(glob.glob(file_stem))
        for g in files:
            data = genfromtxt(g, dtype=float, unpack=True)
            data_graph(graph)
    elif multiple_files and file_list:
        if combine:
            file_dictionary = {g: genfromtxt(g, dtype=float, unpack=True) for g in file_list}
            data = combine_data(file_dictionary)
            data_graph(graph)
        else:
            for g in file_list:
                data = genfromtxt(g, dtype=float, unpack=True)
                data_graph(graph)

    else:
        data = genfromtxt(f, dtype=float, unpack=True)
        data_graph(graph)

    if return_data:
        retrieved = [data[k] for k in use_cols]
        return retrieved


def generateDictKeys(string, n, step=1):
    """
    This was written as a quick and easy way of producing keys for a dictionary.
    :param string: Base String on which to attach numerals
    :param n: Number of strings to generate with '{}{}'.format(string,n) being the last string generated
    :return: yields strings like "a1" or "a2" if string= 'a' and n>2
    """
    if type(string) != str or type(n) != int:
        raise ValueError('Please input string and integer for first and second argument')
    elif step == 1:
        keylist = [string+str(i) for i in range(n)]
        return keylist
    else:
        keylist = [string+str(i) for i in range(0, n*step, step)]
        return keylist


def generatehamiltoniantring(n, s, onestring=None, pos=None, pad=None):
    """
    This generates a string that is used to construct tensor products terms in Hamiltonian with a certain kind of
    interaction term. For example suppose we have an ising Hamiltonian with 4 qubits. We generate strings in a
    list 1100, 0110,0011. The zero will be used to tensor an identity and the 1 will be used to tensor the pauli
    matrix.
    :param n: The number of qubits we have in our system
    :param s: This is a string of 1's that determines how local our hamiltonian is. So a three body interaction
    means we need '111' or a two body interaction will be '11'
    :param onestring: If you would rather generate one string than a list of strings
    :param pos: The position where the string s should start  (only if onestring is not none)
    :param pad: Rather than padding with zeros you could pad with some other number (only if onestring
    is not none)
    :return: Returns a list of strings that will be used to create the Hamiltonian
    """
    label = []
    if onestring is None:
        if isinstance(s, str):
            for i in range(0, n):
                strs = s
                strs = strs.ljust(n-i, '0')
                strs = strs.rjust(n, '0')
                label.append(strs)
        else:
            print('Please enter string for second variable and integer for first')
        return label
    else:
        strs = s
        strs = strs.ljust(n - pos, pad)
        strs = strs.rjust(n, pad)
        return strs


def controlgatestring(n, control_pos1, target_pos2, additionaloptstring = ''):
    """
    :param n: The length of the string
    :param control_pos1: This must be a tuple that specifies which qubit is control and its position
     (string,number)
    :param target_pos2:  This must be a tuple that specifies which qubit is target and its position
    :param additionaloptstring: Gives the user freedom to add string unique string after second position
    :return:
    """
    out = ''

    if isinstance(control_pos1, tuple) and isinstance(target_pos2, tuple):
        control, pos1 = control_pos1
        target, pos2 = target_pos2
        for i in range(0, n):
            if i == pos1-1:
                out += control
            elif i == pos2-1:
                out += target
            elif additionaloptstring != '' and i > pos2-1:
                out += additionaloptstring
            else:
                out += '0'
    else:
        print("Please make sure that you have provided a tuple with the 1st arg being a string and 2nd being a number")

    return out


def generatetensorstring(n, *args):
    """
    This is a function like generatehamiltonianstring except it allows for the possibility that we could have
    different operators in the interaction placed at arbitrary place. Plus this does not generate a list
    but just one string. IZIIXIY needs string '0100203'. Can't handle a term like 'IZZZ' because we need
    string '0111' because for each  operator other than identity label is incremented.
    :param n: The number of qubits in the system
    :param args: list of arguments stating positions for where numbers other than 0 should go.
    :return: returns a string
    """
    out = ''
    label = 0
    arg = array(args) - 1

    for i in range(0, n):
        if i in arg:
            label += 1
            out += str(label)
        else:
            out += '0'
    return out


def partial_trace(n, m, k):
    """
    This is the partial trace operator

    :param n: Number of qubits in the system
    :param m: The position of the qubit to trace
    :param k: label for the kth basis for the traced out qubit, label begins from 1
    :return: Returns the matrix that helps trace out the mth qubit
    """
    out = 1
    tensor_label = generatetensorstring(n, m)
    # print('In partial_trace this is tensor_label string : ', tensor_label)
    terms = {"0": g.id(), "1": g.e_ij((2, 1), k, 1)}

    out = superkron(terms, string=tensor_label, val=1)
    return out


def trace_qubits(n, rho, qubit_list):
    """
    :param n: Number of qubits in the system
    :param rho: The system from which trace out qubits
    :param qubit_list: List of qubits to trace out. Labels should begin from 1
    :return: Returns a reduced density matrix
    """

    # def perform_trace(m, rho_red, label_list):
    #     """
    #     :param m: number of qubits remaining in the system
    #     :param q: qubit label
    #     :param rho_red: A density matrix that we want to perform the reduced density matrix over
    #     :return: Returns the reduced density matrix after one qubit has been traced out
    #     """
    #     basis_labels = [1, 2]
    #     reduced_matrix = zeros((pow(2, m - 1), pow(2, m - 1)))
    #     ptrace_op = []
    #
    #     if len(label_list) != 0:
    #         q = random.choice(label_list)
    #
    #  Put tracing out operators in dictionary
    #         for b in basis_labels:
    #             ptrace_op.append(partial_trace(m, q, b))
    #
    #  Perform the tracing out operation
    #         for b in range(0, len(ptrace_op)):
    #             reduced_matrix += dot(ptrace_op[b].T, dot(rho_red, ptrace_op[b]))
    #         label_list.remove(q)
    #         return perform_trace(m-1, reduced_matrix, label_list)
    #     else:
    #         return rho_red
    basis_labels = [1, 2]
    reduced_matrix = zeros((pow(2, n - 1), pow(2, n - 1)))
    ptrace_op = []
    # print('Shape of rho :', rho.shape)
    # print(' Shape of reduced_matrix : ', reduced_matrix.shape)
    if len(qubit_list) != 0:
        # q = random.choice(qubit_list)
        q = max(qubit_list)
        # print('The random qubit to trace over: ', q)

        # Put tracing out operators in dictionary
        for b in basis_labels:
            ptrace_op.append(partial_trace(n, q, b))

            # Perform the tracing out operation
        for b in range(0, len(ptrace_op)):
            # print('Pre calculated matrix shape: ', dot(ptrace_op[b].T, dot(rho, ptrace_op[b])).shape)
            reduced_matrix += dot(ptrace_op[b].T, dot(rho, ptrace_op[b]))
        qubit_list.remove(q)
        return trace_qubits(n - 1, reduced_matrix, qubit_list)
    else:
        return rho


def subblock(u, p1, p2):
    """
    :param u: In put matrix
    :param p1: this is a tuple that determines the top left element of sub-block
    :param p2: this is a tuple that determines the bottom right element of sub-block
    :return: Returns the sub-block
    """
    if isinstance(p1, tuple) and isinstance(p2, tuple):
        r, c = p1
        r1, c1 = p2
        out = u[r:r1, c:c1]
    else:
        print("Please enter tuple for second and third argument")

    return out


def generateUnitary():
    """
    :return: Returns a random 2 by 2  unitary matrix
    """
    u = zeros((2,2), dtype=complex)
    zeta = random.random()  # result after calculating sine and cosine
    theta = arcsin(zeta)
    phi = random.uniform(0, 2*pi)  # angle for first phase
    chi = random.uniform(0, 2*pi)  # angle for second phase
    rho = random.uniform(0, 2*pi)

    a = exp(1j*phi)*cos(theta)
    b = exp(1j*chi)*sin(theta)
    u[0, 0] = a
    u[0, 1] = b
    u[1, 0] = -conjugate(b)
    u[1, 1] = conjugate(a)

    return dot(exp(1j*rho), u)


def gram_schmidt(A):
    """
    :param A: Matrix that does not have orthornormal column
    :param row_vecs:
    :param norm:
    :return:
    """
    for i in range(0, len(A)):
        for j in range(0, i):
            A[:, i] = A[:, i] - (dot(A[:, i].T, A[:, j])) / (dot(A[:, j].T, A[:, j]))*A[:, j]
        A[:, i] = A[:, i] / sqrt(dot(A[:, i].T, A[:, i]))

    return A


def superkron(*args, val=0,  string=''):
    """
    This generalization of kron can be used in 2 ways. It can straight forwardly take the tensor product of
    operators given the arguments i.e superkron(I,Z,X) will return the tensor product of I, Z and X.
    It can also do something more general. It can accept a dictionary of operators and a string variable
    that specifies in which order the operators in the dictionary should be tensored. E.G
    operdict = {'0': I, '1': X} and  string = '010. Then superkron(operdict, val=1,string)
    produces tensor product superkron(I,X,I)

    :param args: List of operators to calculate tensor product of
    :param val: A val=0 makes function calculate tensor product of operators given, val=1 adds extra
    bells and whistles described in doc string above
    :param string: The order in which operators given in the operdict dictionary will be tensored
    :return: The tensor product of operators
    """

    out = 1
    if val == 0:
        for i in range(len(args)):
            out = kron(out, args[i])
    else:
        for digit in string:
            out = kron(out, args[0][digit])
    return out


def computational_basis(q, n, dict=False):
    """
    :param n: type of qudit. Set n=2 for qubit
    :param q: Number of qubits
    :return: List of one dimensional arrays corresponding to the computational basis states
    """
    zero = np.array([1, 0])
    one = np.array([0, 1])
    basis_labels = createlabel(q, n)
    operators = {'0': zero, '1': one}
    basis_list = [np.array([superkron(operators, val=1, string=i)])for i in basis_labels]

    return basis_list


def realify(vec):
    """
    Gets a complex vector in C^d and produces a real vector in R^2d
    :param vec: This should be a row vector
    :return:
    """
    realified = []
    a = vec.tolist()
    for i in a[0]:
        real_part = i.real
        realified.append(real_part)
    for i in a[0]:
        imag_part = i.imag
        realified.append(imag_part)
    realified = np.array(realified)
    return realified


def construct_preunitary(arr, array_list):
    """
    Useful when constructing unitaries to make quantum states. It needs to be
    input into gram schmidt orthogonalization method
    :param arr:
    :param array_list:
    :return:
    """
    s = array_list[1].shape
    preunitary = np.array([])
    preunitary = np.append(preunitary, arr)
    preunitary = preunitary.reshape(1, s[1])
    for i in range(1, len(array_list)):
        preunitary = np.hstack((preunitary, array_list[i]))
    preunitary = preunitary.reshape(s[1], s[1]).T
    return preunitary


def makeQobj(*args):
    """
    :param args: This is a list of matrices than must be turned into Qobj in order that they can be used in the
    qutip package
    :return: returns list of Qobj in the order in which they were created. E.g makeQobj(A,B) returns a list
    l = [Qobj(A),Qobj(B)]
    """
    try:
        if isinstance(*args, list):
            l = [qt.Qobj(args[0][i]) for i in range(len(args[0]))]
        elif isinstance(*args, dict):
            l = {name: qt.Qobj(args[0][name])for name in args[0]}
        else:
            l = qt.Qobj(args[0])
        return l
    except TypeError:
        print("The input must be a list or dictionary of operators or a single operator")


def direct_sum(matrices):
    """
    :param matrices: List of matrices
    :return: The direct sum of the matrices
    """
    temp = []
    for m in matrices:
        temp.append(m.shape)
    M = zeros(tuple(map(sum, zip(*temp))), dtype=complex)
    M[:matrices[0].shape[0], :matrices[0].shape[1]] = matrices[0]
    for l in range(0, len(matrices), 2):
        if l != len(matrices)-1:
            M[matrices[l].shape[0]:matrices[l].shape[0] + matrices[l+1].shape[0],
            matrices[l].shape[1]:matrices[l].shape[1] + matrices[l+1].shape[1]] = matrices[l+1]
        else:
            M[M.shape[0]-matrices[l].shape[0]:, M.shape[1]-matrices[l].shape[1]:] = matrices[l]
    return M


def fidelity(rho, rho_1, error=False):
    """
    :param rho: First density matrix
    :param rho_1: Second density matrix
    :param error: If true returns 1 - fidelity otherwise simply returns fidelity
    :return:  Return the fidelity of two matrices in variable out
    """
    out = 0
    if error is False:
        out = trace(dot(rho, rho_1)).real
    else:
        out = 1 - trace(dot(rho, rho_1)).real

    return out

#
# def gatecompiler(file_prefix, unitary, num_bits):
#     """
#     :param file_prefix:
#     :param unitary
#     :param num_bits:
#     :return:
#     """
#
#     emb = CktEmbedder(num_bits, num_bits)
#     t = Tree(True, file_prefix, emb, unitary, verbose=False)
#     t.close_files()
#     style = 'exact'
#     MultiplexorExpander(file_prefix, num_bits, style)
#     DiagUnitaryExpander(file_prefix + '_X1', num_bits, style)
#     SEO_reader(file_prefix + '_X2', num_bits)


def eigen(A):
    """
    :param A: This is matrix
    :return: Returns the eigenvalues with corresponding eigen vectors
    """
    v, w = eig(A)
    shape_size = w.shape
    eigenvector_list = [array([w[:, i]]) for i in range(0, shape_size[1])]
    return v, eigenvector_list


def read_file(file, line_count=1, readline=None):
    """
    :param file: file name
    :param line_count: The number of lines in the file
    Note first line is indexed as 0
    :param readline: The line to read
    line by line
    :return:
    """

    with open(file, 'r') as f:
        if readline is None:
            line = f.read()
            return line
        else:
            for i, lines in enumerate(f):
                if i == readline-1:
                    return lines


def file_linecount(file):
    """
    :param file: file name
    :return: Number of lines in a file
    """
    linecount = sum(1 for line in open(file))
    return linecount


def remove_line(file, string=[]):
    """
    Removes specific words from files and returns the file with same name but bad lines
    are removed
    :param file:
    :param string:
    :return:
    """
    with open(file, 'r') as f, open('tmp.txt', '+a') as new_f:
        for line in f:
            clean = True
            for word in string:
                if word in line:
                    clean = False
                if clean is True:
                    new_f.write(line)
    os.remove(file)
    os.rename('tmp.txt', file)


# def unitary_to_qasm(file_prefix1, u, n, unwanted_words):
#     """
#     :param file_prefix1:
#     :param u:
#     :param n:
#     :param unwanted_words: remove lines which have unwanted words
#     :return: name of file with qasm code
#     """
#     gatecompiler(file_prefix1, u, n)
#     remove_line(file_prefix1 + '_X2_' + str(n) + '_eng.txt', unwanted_words)
#     Qubiter_to_IBMqasm2_5q(file_prefix1 + '_X2', n, write_qubiter_files=True)
#     return file_prefix1 + '_X2_' + 'qasm2.txt'


def save_to_file(name='', **kwargs):
    """
    Write data to file in column format. Each keyword is a column
    :param name: A string that is the name of the file to which the data will be written to
    """
    string = ''
    for k in kwargs:
        string += '{' + k + '}' + '      '
    string += '\n'
    file = open(name, 'a')
    file.write(string.format(**kwargs))
    file.close()


def splice(L, n):
    """
    This does not return a subsequence of the list but simply splices the list into n parts. The elements themselves
    will in general not be in the original order
    :param L:  The list you would like to splice
    :param n: The number of pieces you would like the list to be spliced in
    :return:  The spliced list
    """

    list_of_indices = [i for i in range(0, len(L))]
    spliced_list = [list_of_indices[i::n] for i in range(n)]
    return spliced_list


if __name__ == '__main__':

    # a = read_file('/home/amara/Dropbox/Python Files/BQP2.5/projects/qvector_files/zero_state_ibm.qasm')
    # print(a)

    # unitary_to_qasm('/home/amara/Dropbox/Python Files/qComputing/Gate Compiler Files/x',
    #                 g.cnot(),2, 'PHAS')
    # file = '/home/amara/Dropbox/Python Files/Data/Qvector/average_fidelity/average_fidelity_5_17.txt'
    # load_data(f=file, use_cols=[0, 1, 2], graph=True, contour=True, xlabel="units of $\pi/10$",
    #           ylabel='units of $\pi/10$')
    # print('List of computational basis state: ', computational_basis(3, 2))
    # print('Labels for classical states: ', createlabel(3, 2))
    from SpecialStates import ghz_state, clusterstate, purestate, cluster_obj
    ghz = ghz_state(5)
    cluster = clusterstate(4)
    clu = cluster_obj(4, density_matrix=True)
    print(clu.ptrace([3, 2]))
    print(trace_qubits(4, cluster.state, [1, 2]))

    # print(reduce_ghz)
    # print('Partial Trace :', clu.ptrace(1))
