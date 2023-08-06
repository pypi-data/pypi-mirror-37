import math
import numpy as np
import os

PI = 3.14159265358979323846  # math.pi
encoding = 'ascii'
npDouble = np.float64


def sph2cart(r, theta, phi):
    return [
        r * math.sin(theta) * math.cos(phi),
        r * math.sin(theta) * math.sin(phi),
        r * math.cos(theta)
    ]

def cart2sph(x, y, z):
    # note that a faster vectorized version of this can be found at:
    # https://stackoverflow.com/questions/4116658/faster-numpy-cartesian-to-spherical-coordinate-conversion/4116803#4116803
    XsqPlusYsq = x ** 2 + y ** 2
    r = math.sqrt(XsqPlusYsq + z ** 2)  # r
    elev = math.atan2(z, math.sqrt(XsqPlusYsq))  # theta
    az = math.atan2(y, x)  # phi
    return r, elev, az

class Grid:
    '''
    This class is described in pages 12-15 of the paper

    The class Grid is initialized with `q_max` and `grid_size`.
    It is used to create/describe a grid of `q`, `theta`, `phi` angle values.
    These values can be described using two sets of indexing:

    1. The overall index `m`
    2. The individual angle indices `i`, `j`, `k`
    '''
    def __init__(self, q_max, grid_size):
        if grid_size % 2:
            raise ValueError("Grid size must be even")
        self.q_max = q_max
        self.grid_size = grid_size
        self.extra_shells = 3

    @property
    def step_size(self):
        '''
        The difference between q's in the grid.

        :return: double q_max/N
        '''
        return npDouble(self.q_max / (self.N))

    @property
    def N(self):
        return int(self.grid_size / 2)

    @property
    def actual_size(self):
        return self.N + self.extra_shells

    def _G_i_q(self, i):
        return 6 * i + 12 * i ** 2 + 6 * i ** 3

    def create_grid(self):
        '''
        a generator that returns q, theta, phi angles in phi-major order
        '''
        for i in range(0, self.N + 4):
            if i == 0:
                yield 0, 0, 0
                continue
            J_i = (3 * i) + 1
            K_ij = 6 * i
            for j in range(0, J_i):
                for k in range(0, K_ij):
                    yield self.angles_from_indices(i, j, k)

    def angles_from_indices(self, i, j, k):
        '''
         receives angle indices i,j,k and returns their q, theta, and phi angle values.

        :param i: angle indice i
        :param j: angle indice j
        :param k: angle indice k
        :return: q, theta, and phi angle values
        '''
        if i == 0:
            return 0, 0, 0
        q = npDouble(i * self.step_size)
        theta_ij = npDouble((j * PI) / (3 * i))
        phi_ijk = npDouble((k * PI) / (3 * i))
        return q, theta_ij, phi_ijk

    def indices_from_index(self, m):
        '''

        :param m: receives an overall index m.
        :return: individual q, theta, and phi indices: i, j, k
        '''
        if m == 0:
            return 0, 0, 0
        i = math.floor((m / 6) ** (1. / 3.))
        if m > self._G_i_q(i):
            i += 1
        R_i = m - self._G_i_q(i - 1) - 1
        j = math.floor(R_i / (6 * i))
        k = R_i - 6 * i * j
        return i, j, k

    def angles_from_index(self, m):
        '''

        :param m: receives an overall index m
        :return: returns the matching q, theta, and phi angle values
        '''
        i, j, k = self.indices_from_index(m)
        q, theta, phi = self.angles_from_indices(i, j, k)
        return q, theta, phi

    def index_from_indices(self, i, j, k):
        '''
        receives angle indices i,j,k and returns the overall index m that matches them.

        :param i: angle indices i
        :param j: angle indices j
        :param k: angle indices k
        :return: overall index m that matches the given i,j,k
        '''
        if i == 0:
            return 0
        return 6 * (i - 1) + 12 * (i - 1) ** 2 + 6 * (i - 1) ** 3 + 6 * i * j + k + 1

    def indices_from_angles(self, q, theta, phi):
        '''
        receives angles q, theta, phi, ands returns the matching indices i,j,k.

        :param q: q angle
        :param theta: theta angle
        :param phi: phi angle
        :return: return indices i, j, k of given q, thta and phi
        '''

        eps=0.000001
        i=math.floor(q/self.step_size + eps)

        phiPoints = 6.0 * i
        thePoints = 3.0 * i

        j = math.floor((theta / PI) * thePoints + eps)
        k = math.floor((phi  / (PI*2)) * phiPoints + eps)

        return i, j, k

    def index_from_angles(self, q, theta, phi):
        '''
        receives angles q, theta, phi and returns the matching overall index m.

        :param q: q angle
        :param theta: theta angle
        :param phi: phi angle
        :return: matching overall index m
        '''
        i,j,k = self.indices_from_angles(q, theta, phi)
        return self.index_from_indices(i,j,k)

class Amplitude(Grid):
    '''
    The class `Amplitude`, by contrast, can be used to build an amplitude and then save that amplitude as an amplitude file,
    which can then be opened in D+ (or sent in a class AMP) but it itself cannot be added directly to the Domain parameter tree.
    '''
    def __init__(self, q_max, grid_size):
        super().__init__(q_max, grid_size)
        self._values = np.array([], dtype=np.float64)
        self.external_headers = None
        self.__description = ""
        self.filename = ""

    def create_grid(self, func):
        '''
        Amplitude overrides grid's `create_grid` method. Amplitude's `create_grid` requires a function as an argument.
        This function must receive q, theta, phi and return two values, representing the real and imaginary parts of a complex number.
        The values returned can be a tuple, an array, or a python complex number (A+Bj).
        These values are then saved to the Ampltiude's `values` property, and can also be accessed through the `complex_amplitudes_array`
        property as a numpy array of numpy complex types.

        :param func: a function that receives q, theta, phi and return two values, representing the real and imaginary parts of a complex number.
        '''
        values=[]
        for q, theta, phi in super().create_grid():
            try:
                res= func(q, theta, phi)
            except Exception as e:
                raise ValueError("You must provide a function which receives q, theta, phi")
            try:
                values.append(res[0])
                values.append(res[1])
            except:
                try:
                    values.append(res.real)
                    values.append(res.imag)
                except:
                    raise ValueError("You must provide a function which returns a complex number in two parts")
        self._values = np.float64(values)

    @property
    def values(self):
        '''
        array that contains the grid intensity values as 2 values - real and imaginary

        :return: values array
        '''
        if len(self._values):
            return self._values
        else:
            raise ValueError("Amplitude values empty-- has not been initialized yet")

    @property
    def complex_amplitude_array(self):
        '''
        returns the values array as complex array.

        :return: complex array
        '''
        complex_arr = np.zeros((int(self._values.__len__() / 2), 1), dtype=np.complex)
        for index in range(0, complex_arr.__len__()):
            complex_arr[index] = self.values[2 * index] + 1j * self.values[2 * index + 1]
        return complex_arr

    @property
    def default_header(self):
        '''
        Return the default file headers values for amplidute class.

        :return: file headers of amplitude
        '''
        descriptor = "#@".encode(encoding)
        header = "# created from a Python function\n"
        header += "# " + "\\"*80 +"\n"
        header += "# User description:" + self.description + "\n"
        header += "# " + "\\" * 80 + "\n"
        header += "# Grid was used.\n"
        header += "# N^3; N = " + str(self.N) + "\n"
        header += "# qMax= " + str(self.q_max) + "\n"
        header += "# Grid step size = " + str(self.step_size) + "\n"
        header += "\n"

        headlen =np.uint32( 2*1 + 4 +  1 + len(header) *1 + 1) # descriptor + unsigned int +  \n + header length + \n
        header_list = [descriptor, headlen, "\n".encode(encoding), header.encode(encoding) ,"\n".encode(encoding)]
        step_size = np.array([self.step_size], dtype=np.float64)
        added_list=[
            (str(13) + "\n").encode(encoding),  # version
            (str(16) + "\n").encode(encoding),  # size of double
            (str(int(self.actual_size)) + "\n").encode(encoding),  # "tmp grid size"
            (str(int(self.extra_shells)) + "\n").encode(encoding),
            step_size.tobytes()  # note that this does not get new line
        ]
        return header_list + added_list
    @property
    def headers(self):
        '''
        Returns the headers - default if amplitude was created nt python API or external if amplitude was created from a file.
        :return:
        '''
        if self.external_headers:
            return self.external_headers
        else:
            return self.default_header

    @property
    def description(self):
        if self.__description:
            return self.__description
        return "None"

    @description.setter
    def description(self, val):
        edit = val.replace("\n", "\n# ")
        self.__description ="\n# "+ edit

    def save(self, filename):
        '''
         The function will save the information of the Amplitude class to an Amplitude file which can then be
         passed along to D+ to calculate its signal or perform fitting.

        :param filename: new amplitude file name
        '''
        with open(filename, 'wb') as f:
            for header in self.headers:
                f.write(header)
            amps = np.float64(self._values)
            amps.tofile(f)
        self.filename= os.path.abspath(filename)

    @staticmethod
    def load(filename):
        '''
        A static method, `load`,  which receives a filename of an Amplitude file, and returns an Amplitude instance
        with the values from that file already loaded.

        :param filename: filename of an Amplitude file
        :return: instance of Amplitude class.
        '''
        def _peek(File, length):
            pos = File.tell()
            data = File.read(length)
            File.seek(pos)
            return data

        has_headers = False
        headers = []
        with open(filename, "rb+") as f:
            if _peek(f, 1).decode('ascii') == '#':
                desc = f.read(2)
                tempdesc = desc.decode('ascii')
                if (tempdesc[1] == '@'):
                    has_headers = True
                else:
                    tmphead = f.readline()
                    headers.append(desc + tmphead)

            if has_headers:
                offset = np.fromfile(f, dtype=np.uint32, count=1, sep="")
                del_aka_newline = f.readline()  # b"\n"

                while _peek(f, 1).decode('ascii') == '#':
                    headers.append(f.readline())
                if offset > 0:
                    f.seek(offset[0], 0)

            version_r = f.readline().rstrip()
            version = int(version_r.decode('ascii'))
            size_element_r = f.readline().rstrip()
            size_element = int(size_element_r.decode('ascii'))

            if size_element != int(2 * np.dtype(np.float64).itemsize):
                raise ValueError("error in file: " + filename + "dtype is not float64\n")

            tmpGridsize_r = f.readline().rstrip()
            tmpGridsize = int(tmpGridsize_r.decode('ascii'))  # I

            tmpExtras_r = f.readline().rstrip()
            extra_shells = int(tmpExtras_r.decode('ascii'))  # extra shells
            grid_size = (tmpGridsize - extra_shells) * 2  # grid_size

            actualGridSize = grid_size / 2 + extra_shells  # I

            i = actualGridSize
            totalsz = int((6 * i * (i + 1) * (3 + 3 + 2 * 3 * i)) / 6)
            totalsz = totalsz + 1
            totalsz = totalsz * 2
            step_size = np.fromfile(f, dtype=np.float64, count=1, sep="")
            q_max = np.float64 (step_size * (grid_size / 2.0))

            amp_values = np.fromfile(f, dtype=np.float64, count=totalsz, sep="")

            header_List = []
            if has_headers:
                pos = 0
                header_List.append(desc)
                pos = pos + len(desc)

                header_List.append(offset[0].tobytes())
                pos = pos + len(offset[0].tobytes())
                header_List.append(del_aka_newline)
                pos = pos + len(del_aka_newline)

                for i in headers:
                    header_List.append(i)
                    pos = pos + len(i)
                header_List.append(del_aka_newline)
                header_List.append(del_aka_newline)
                pos = pos + 2 * len(del_aka_newline)

                pos = np.int32(pos)
                if pos != offset[0]:
                    header_List[1] = pos.tobytes()

                header_List.append(version_r + b"\n")
                header_List.append(size_element_r + b"\n")
                header_List.append(tmpGridsize_r + b"\n")
                header_List.append(tmpExtras_r + b"\n")
                header_List.append(step_size.tobytes())

            amp = Amplitude(q_max, grid_size)
            amp.extra_shells = extra_shells
            amp._values = amp_values
            amp.external_headers = header_List
            return amp
