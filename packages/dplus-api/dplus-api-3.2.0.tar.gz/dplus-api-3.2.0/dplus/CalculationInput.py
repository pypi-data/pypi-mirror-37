from __future__ import print_function
import json

from dplus.State import State, DomainPreferences
from dplus.FileReaders import SignalFileReader

class CalculationInput(State):
    """
    A base class of the parameters for dplus generate or fit.
    """
    def __init__(self,graph=None, x=None, y=None, use_gpu=True):
        super().__init__()

        self.use_gpu = use_gpu

        if graph:
            self.load_graph(graph)
        else:
            if x:
                self.x = x
            if y:
                self.y = y


    @property
    def use_gpu(self):
        """
        boolean flag, determines whether run the fit/generate calculation with or without gpu.

        :return: boolean value
        """
        return self._use_gpu

    @use_gpu.setter
    def use_gpu(self, flag):
        assert isinstance(flag, bool)
        self._use_gpu = flag
        if not self.DomainPreferences.use_grid:
            print("When using GPU, use_grid must be enabled. Enabling automatically.")
            self.DomainPreferences.use_grid=True

    @property
    def x(self):
        """
        x vector, float array of the qs values

        :return: array of floats
        """
        return self.DomainPreferences._x

    @x.setter
    def x(self, x):
        """
        x vector, float array of the qs values

        :return: array of floats
        """
        self.DomainPreferences._x = x

    @property
    def args(self):
        """
        build the arguments params for D+ backed from CalculationInput fields.

        :return: The json dict that is send to D+ backed
        """

        return dict(args=dict(state=self.serialize(),
                              x=self.x,
                              y=self.y,
                              mask=self._mask),
                    options=dict(useGPU=self.use_gpu))

    @property
    def y(self):
        """

        :return: complex array of the intensity values for fitting
        """
        return self.DomainPreferences._y

    @y.setter
    def y(self, y):
        """
        x vector, float array of the qs values

        :return: array of floats
        """
        self.DomainPreferences._y = y

    @property
    def _filenames(self):
        return self._get_all_filenames()

    @property
    def _mask(self):
        # as of right now, the c++ code only has nomask, which is an array of zeros
        try:
            return [0] * len(self.y)
        except TypeError: #y=None
            return None

    def load_graph(self, graph):
        '''
        can receive an unordered graph, and create ordered x and y arrays

        :param graph: dictionary of x_key:y_val (can be unordered)
        '''
        items = list(graph.items())
        items.sort(key=lambda item: item[0])
        self.x = [item[0] for item in items][:]
        self.y = [item[1] for item in items][:]

    @staticmethod
    def copy_from_state(state):
        '''
        creates a CalculationInput based on an existing state

        :param state: a State class instance
        :return: new CalculationInput instance
        '''
        old_dict = state.serialize()
        new_input = CalculationInput()
        new_input.load_from_dictionary(old_dict)
        return new_input


    @staticmethod
    def _web_load(args_dict):
        stateInput = CalculationInput()
        try:
            stateInput.load_from_dictionary(args_dict["state"])
        except Exception as e:
            raise ValueError("Invalid state")
        stateInput.x = args_dict["x"]
        try:
            if args_dict["y"]: #is not None
                stateInput.y = args_dict["y"]
        except KeyError: #y not in state
            pass
        return stateInput

    @staticmethod
    def load_from_state_file(filename):
        """
        receives the location of a file that contains a serialized parameter tree (state) and creates instance of /
        CalculationInput from the file.

        :param filename: location of a state file
        :return: CalculationInput instance
        """
        with open(filename, 'r') as statefile:
            input = json.load(statefile)
        stateInput = CalculationInput()
        stateInput.load_from_dictionary(input)
        return stateInput

    @staticmethod
    def _load_from_args_file(filename):
        with open(filename, 'r') as statefile:
            input = json.load(statefile)
        return CalculationInput._web_load(input["args"])

    def load_signal_file(self, signal_filename):
        '''
        recieve signal filename and load the x vector and y vector from the signal file.

        :param signal_filename:
        '''
        s = SignalFileReader(signal_filename)
        self.x = s.x_vec
        self.y = s.y_vec

    @staticmethod
    def load_from_PDB(filename, qmax):
        """
        receives the location of a PDB file and qmax, and automatically creates a guess at the grid size based on the pdb.

        :param filename: location of a PDB file
        :param qmax: The max q value for the creation of the pdb grid size
        :return: instance of GenerateInput
        """

        def _calculate_grid_size(pdbfile, q):
            import numpy as np
            x, y, z = _get_x_y_z_window(pdbfile)
            max_len = np.sqrt(x * x + y * y + z * z)
            max_len /= 10  # convert from nm to angstrom
            density = int(max_len) / np.pi
            grid_size = int(2 * q * density + 3)
            grid_size /= 10
            grid_size += 1
            grid_size = int(grid_size)
            grid_size *= 10
            if grid_size < 20:
                grid_size = 20  # minimum grid size
            return grid_size

        def _get_x_y_z_window(file):
            x_coords = []
            y_coords = []
            z_coords = []
            for line in file:
                record_name = line[0:6]
                if record_name in ["ATOM  ", "HETATM"]:
                    x_coords.append(float(line[30:38]))
                    y_coords.append(float(line[38:46]))
                    z_coords.append(float(line[46:54]))
            x_len = max(x_coords) - min(x_coords)
            y_len = max(y_coords) - min(y_coords)
            z_len = max(z_coords) - min(z_coords)
            return x_len, y_len, z_len

        with open(filename) as pdbfile:  # checks file exists
            if not filename.endswith(".pdb"):
                raise NameError("Not a pdb file")
            grid_size = _calculate_grid_size(pdbfile, qmax)

        from dplus.DataModels.models import PDB
        c=CalculationInput()
        pdb=PDB(filename)
        pdb.centered=True
        pdb.anomfilename=""
        pdb.use_grid=True
        c.add_model(pdb)
        c.DomainPreferences.grid_size=grid_size
        c.DomainPreferences.convergence=0.001
        c.DomainPreferences.orientation_iterations=1000000
        c.DomainPreferences.use_grid=True
        c.qmax=qmax
        c.use_gpu=True

        return c


def ____storage():
    '''
                    textBoxGridSize->Text = Double(grid_size).ToString();

                    /*
                    actualGridSize = gridSize / 2 + Extras;

                    long long i = actualGridSize;
                    totalsz = (phiDivisions * i * (i + 1) * (3 + thetaDivisions + 2 * thetaDivisions * i)) / 6;
                    totalsz++;    // Add the origin
                    totalsz *= 2;    // Complex
                    */

                    long long i = (grid_size / 2) + 3;
                    long long totalSize = (6 * i * (i + 1) * (3 + 3 + 2 * 6 * i)) / 6;
                    totalSize++;
                    totalSize *= 2;

                    long long numBytes = sizeof(double) * totalSize;

                    double mbs = double(numBytes) / (1024.*1024.);

                    textBoxMemReq->Text = Int32(mbs+0.5).ToString();

                    textBoxMemReq->BackColor = System::Drawing::Color::LimeGreen;
                    labelWarning->Text = "";

                    if (mbs > 250.)
                    {
                        textBoxMemReq->BackColor = System::Drawing::Color::Yellow;
                        labelWarning->Text = "Note: You may want to consider using the hybrid method.";
                    }

                    if (mbs > 1000.)
                    {
                        textBoxMemReq->BackColor = System::Drawing::Color::Red;
                        labelWarning->Text = "Caution: You should consider using the hybrid method.";
                    }
                '''
    pass








