Academic License Agreement

The D+ software ("Software") has been developed by the contributing researchers from the group of Prof. Uri Raviv, ("Developers") of the Hebrew University of Jerusalem ("HUJ") and made available through HUJ for your internal, non-profit research use.

HUJ and the Developers allow researchers at your institution to run, display, copy and modify Software on the following conditions:

The Software remains at your institution and is not published, distributed, or otherwise transferred or made available to other than institution employees and students involved in research under your supervision.

You agree to make results generated using Software available to other academic researchers for non-profit research purposes. If you wish to obtain Software for any commercial purposes, including fee-based service projects, you will need to execute a separate licensing agreement with Yissum Research Development Company of the Hebrew University of Jerusalem Ltd. and pay a fee. In that case, please contact: uri.raviv@mail.huji.ac.il or info@yissum.co.il.

You retain in Software and any modifications to Software, the copyright, trademark, or other notices pertaining to Software as provided by HUJ and the Developers.

You provide the Developers with feedback on the use of the Software in your research, and that the Developers and HUJ are permitted to use any information you provide in making changes to the Software. All bug reports and technical questions shall be sent to the email address: uri.raviv@mail.huji.ac.il.

You acknowledge that the Developers, HUJ and its licensees may develop modifications to the Software that may be substantially similar to your modifications of the Software, and that the Developers, HUJ and its licensees shall not be constrained in any way by you in Developer's, HUJ's or its licensees' use or management of such modifications. You acknowledge the right of the Developers and HUJ to prepare and publish modifications to the Software that may be substantially similar or functionally equivalent to your modifications and improvements, and if you obtain patent protection for any modification or improvement to the Software you agree not to allege infringement of your patent by the Developers, HUJ or by any of HUJ's or Yissum's licensees obtaining and using modifications or improvements to the Software from HUJ or the Developers or attempt to enjoin the use of such modifications or improvements to the Software.

You agree to acknowledge the contribution Developers and the Software make to your research, and cite appropriate references about the Software in your publications. In particular, please cite the paper: Ginsburg A, Ben-Nun T, Asor R, Shemesh A, Ringel I, Raviv U. Reciprocal grids: a hierarchical algorithm for computing solution x-ray scattering curves from supramolecular complexes at high resolution. Journal of chemical information and modeling. 2016; 56 (8) :1518-1527.

You and your institution assume all risk associated with using the Software at your institution. The Software is experimental in nature and is made available as a research courtesy "AS IS," without obligation by HUJ or the Developers to provide accompanying services or support.

HUJ AND THE DEVELOPERS EXPRESSLY DISCLAIM ANY AND ALL WARRANTIES REGARDING THE SOFTWARE, WHETHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES PERTAINING TO NON-INFRINGEMENT, MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE.


Customer Service
For any questions, please contact Prof. Uri Raviv
Phone: +972-2-6586030
Email: uri.raviv@mail.huji.ac.il


Description-Content-Type: UNKNOWN
Description: ן»¿This document was last updated on July 25 2018, for version 3.1.4
        
        # The Dplus Python API
        
        
        The D+ Python API allows using the D+ backend from Python, instead of the ordinary D+ application.
        
        The Python API works on both Windows and Linux.
        
        ## Installation
        
        Installing the Python API is done using PIP:
        
            pip install dplus-api
            
        The API was tested with Python 3.5 and newer. It *may* work with older versions of Python, although Python 2 
        is probably not supported.
        
        ## Overview
         
        Some notes:
         
        Throughout the manual, code examples are given with filenames, such as "mystate.state".
        To run the example code for yourself, these files must be located in the same directory as the script itself,
         or alternately the code can be modified to contain the full path of the file's location.
        
        Throughout the manual, we mention "state files". A state file is a 
        JavaScript Object Notation (JSON) format file (https://www.json.org/), 
        which describes the parameter tree and calculation settings of the D+ computation.
        
        It is unnecessary to write a state file yourself. 
        State files can either be generated from within the python interface (with the function `export_all_parameters`),
        or created from the D+ GUI (by selecting File>Export All Parameters from within the D+ GUI).
        
        **The overall flow of the Python API is as follows:**
        
        1. The data to be used for the calculation is built by the user in an instance of the `CalculationInput` class. 
        `CalculationInput` is a child class of the class `State`, which represents a program state. A `State` includes both program 
        preferences such as `DomainPreferences`, and a parameter tree composed of `Models`.
        
        2. The calculation input is then passed to a `CalculationRunner` class (either `LocalRunner` or `WebRunner`),
        and the calculation function is called (`generate`, `generate_async`, `fit`, or `fit_async`).
        
        3. The `CalculationRunner` class returns an instance of a `CalculationResult` class, 
        either `FitResult` or `GenerateResult`.
        
        Here is a very simple example of what this might look like in main.py:
        
        ```
        from dplus.CalculationInput import CalculationInput
        from dplus.CalculationRunner import LocalRunner
        
        calc_data = CalculationInput.load_from_state_file("mystate.state")
        runner = LocalRunner()
        result = runner.generate(calc_data)
        print(result.graph)
        ```
        
        A detailed explanation of the class types and their usage follows.
        
        
        ## CalculationRunner
        
        There are two kinds of `CalculationRunners`, Local and Web.
        
        The `LocalRunner` is intended for users who have the D+ executable files installed on their system. It takes two optional
        initialization arguments:
        
        * `exe_directory` is the folder location of the D+ executables. 
        By default, its value is `None`. On Windows, a value of `None` will 
        lead to the python interface searching the registry for an installed D+ on its own, but on linux the executable 
        directory *must* be specified. 
        * `session_directory` is the folder where the arguments for the calculation are stored, as well as the output results,
        Amplitude files, and protein data bank (PDB) files, from the C++ executable. 
        By default, its value is `None`, and an automatically generated 
        temporary folder will be used. 
        
        ```
        from dplus.CalculationRunner import LocalRunner
        
        exe_dir = r"C:\Program Files\D+\bin"
        sess_dir = r"sessions"
        runner = LocalRunner(exe_dir, sess_dir)
        #also possible:
        #runner = LocalRunner()
        #runner = LocalRunner(exe_dir)
        #runner = LocalRunner(session_directory=sess_dir)
        ```
        
        The WebRunner is intended for users accessing the D+ server. It takes two required initialization arguments, with no
        default values:
        
        * `url` is the address of the server.
        * `token` is the authentication token granting access to the server. 
        
        ```
        from dplus.CalculationRunner import WebRunner
        
        url = r'http://localhost:8000/'
        token = '4bb25edc45acd905775443f44eae'
        runner = WebRunner(url, token)
        ```
        
        Both runner classes have the same four methods: 
        
        `generate(calc_data)`, `generate_async(calc_data)`, `fit(calc_data)`, and `fit_async(calc_data)`.
        
        All four methods take the same single argument, `calc_data` - an instance of a `CalculationData` class.
        
        `generate` and `fit` return a `CalculationResult`.
        
        `generate_async` and `fit_async` return a `RunningJob`.
        
        When using `generate` or `fit` the program will wait until the call has finished and returned a result, before continuing. 
        Their asynchronous counterparts (`generate_async` and `fit_async`) allow D+ calculations to be run in the background 
        (for example, the user can call `generate_async`, tell the program to do other things, 
        and then return and check if the computation is finished). 
        
        
        #### RunningJob
        
        The user should not be initializing this class. When returned from an async function
         (`generate_async` or `fit_async`) in `CalculationRunner`, the user can 
        use the following methods to interact with the `RunningJob` instance:
        
        * `get_status()`: get a JSON dictionary reporting the job's current status
        * `get_result(calc_data)`: get a `CalculationResult`. Requires a copy of the `CalculationInput` used to create the job. 
        Should only be called when the job is completed. It is the user's responsibility to verify job completion with `get_status` 
        before calling. 
        * `abort()`: end a currently running job
        
        ```
        from dplus.CalculationInput import CalculationInput
        from dplus.CalculationRunner import LocalRunner
        
         calc_data = CalculationInput.load_from_state_file("mystate.state")
         runner = LocalRunner()
         job = runner.generate_async(calc_data)
         start_time = datetime.datetime.now()
         status = job.get_status()
         while status['isRunning']:
             status = job.get_status()
             run_time = datetime.datetime.now() - start_time
             if run_time > datetime.timedelta(seconds=50):
                 job.abort()
                 raise TimeoutError("Job took too long")
         result = job.get_result(calc_data)
        ```
        
        
        
        ## State
        The state class contains an instance of each of three classes: DomainPreferences, FittingPreferences, and Domain. 
        They are described in the upcoming sections.
        
        It has the methods:
        
        * `get_model`: get a model by either its `name` or its pointer, `model_ptr`.
        * `get_models_by_type`: returns a list of `Models` with a given `type_name`, for example, `UniformHollowCylinder`.
        * `get_mutable_params`: returns a list of `Parameters` in the state class, whose property `mutable` is `True`.
        * `get_mutable_parameter_values`: returns a list of floats, matching the values of the mutable parameters.
        * `set_mutable_parameter_values`: given a list of floats, sets the mutable parameters of the `State` (in the order given by 
        `get_mutable_parameter_values`).
        * `export_all_parameters`: given a filename, will save the calculation `State` to that file.
        * `add_model`: a convenience function to help add models to the parameter tree of a 'State'. It receives the model and optionally 
        a population index (default 0), and will insert that model into the population.
        * `add_amplitude`: a convenience function specifically for adding instances of the `Amplitude` class, described below. 
        It creates an instance of an `AMP` class with the filename of the `Amplitude`. Then, in addition to calling `add_model` with that `AMP` instance, 
        it also changes the `DomainPreferences` of the `State` (specifically, `grid_size`, `q_max`, and `use_grid`), to match the properties of the `Amplitude`.
        It returns the 'AMP' instance it created.	
        
        State, _and every class and sub class contained within state_ (for example: preferences, models, parameters), all have the functions 
        `load_from_dictionary` and `serialize`.
        
        `load_from_dictionary` sets the values of the various fields within a class to match those contained within a suitable dictionary. 
        It can behave recursively as necessary, for example, with a model that has children.
        
        `serialize` saves the contents of a class to a dictionary. Note that there may be additional fields in the dictionary
        beyond those described in this document, because some defunct (outdated, irrelevant, or not-yet-implemented) fields are 
        still saved in the serialized dictionary.
        
        
        
        #### DomainPreferences
        The DomainPreferences class contains properties that are copied from the D+ interface. Their usage is explained in 
        the D+ documentation.
        
        We create a new instance of DomainPreferences by calling the python initialization function:
        
        `dom_pref= DomainPreferences()`
        
        There are no arguments given to the initialization function, and all the properties are set to default values:
        
        |Property Name | Default Value | Allowed values|
        |---|---|---|
        |`signal_file`|	`""`|"", or a valid file location|
        |`convergence`|	0.001||
        |`grid_size`|	100|Even integer greater than 20|
        |`orientation_iterations`|	100||
        |`orientation_method`|	`"Monte Carlo (Mersenne Twister)"`|`"Monte Carlo (Mersenne Twister)", "Adaptive (VEGAS) Monte Carlo", "Adaptive Gauss Kronrod"`|
        |`use_grid`|	`False`| `True`, `False`|
        |`q_max`|	7.5|Positive number. If signal file is provided, must match highest x value|
        
        Any property can then be easily changed, for example, 
        
        `dom_pref.q_max= 10`
        
        If the user tries to set a property to an invalid value (for example, setting q_max to something other than a positive number) they will get an error.
        
        If a signal file is provided, the value of q_max will automatically be set to the highest x value in the signal file.
        
        
        #### Fitting Preferences
        The `FittingPreferences` class contains properties that are copied from the D+ interface. Their usage is explained in the D+ documentation.
        
        We create a new instance of FittingPreferences by calling the python initialization function:
        
        `fit_pref= FittingPreferences()`
        
        There are no arguments given to the initialization function, and all the properties are set to default values:
        
        |Property Name | Default Value |Allowed Values|Required when|
        |---|---|---|---|
        |`convergence`|	0.1| Positive numbers||
        |`der_eps`|	0.1| Positive numbers||
        |`fitting_iterations`|	20|Positive integers||
        |`step_size`|0.01| Positive numbers||
        |`loss_function`|`"Trivial Loss"`| `"Trivial Loss","Huber Loss","Soft L One Loss","Cauchy Loss","Arctan Loss","Tolerant Loss"`||
        |`loss_func_param_one`|0.5|Number|Required for all `loss_function` values except "Trivial Loss"|
        |`loss_func_param_two`|0.5|Number|Required when `loss_function` is "Tolerant Loss"|
        |`x_ray_residuals_type`|`"Normal Residuals"`|`"Normal Residuals","Ratio Residuals","Log Residuals"`||
        |`minimizer_type`|`"Trust Region"`|`"Line Search","Trust Region"`||
        |`trust_region_strategy_type`|`"Dogleg"`|`"Levenberg-Marquardt","Dogleg"`|`minimizer_type` is `"Trust Region"`|
        |`dogleg_type`|`"Traditional Dogleg"`|`"Traditional Dogleg","Subspace Dogleg"`|`trust_region_strategy_type` is `"Dogleg"`|
        |`line_search_type`|`"Armijo"`|`"Armijo","Wolfe"`|`minimizer_type` is `"Line Search"`|
        |`line_search_direction_type`|`"Steepest Descent"`|`"Steepest Descent","Nonlinear Conjugate Gradient","L-BFGS","BFGS"`|`minimizer_type` is `"Line Search"`. if `line_search_type` is `"Armijo"`, cannot be `"BFGS"` or `"L-BFGS"`. |
        |`nonlinear_conjugate_gradient_type`|`""`|`"Fletcher Reeves","Polak Ribirere","Hestenes Stiefel"`|`linear_search_direction_type` is `"Nonlinear Conjugate Gradient"`|
        
        Any property can then be easily changed, for example,
        
        `fit_pref.convergence= 0.5`
        
        If the user tries to set a property to an invalid value they will get an error.
        
        
        #### Domain
        
        The Domain class describes the parameter tree. 
        
        The root of the tree is the `Domain` class. This class contains an array of `Population` classes. 
        Each `Population` can contain a number of `Model` classes. Some models have children, which are also models.
        
        ##### Models
        
        `Domain` and `Population` are two special kinds of models.
        
        The `Domain` model is the root of the parameter tree, which can contain multiple populations. 
        Populations can contain standard types of models.
        
        The available standard model classes are:
        
        * `UniformHollowCylinder`
        * `Sphere`
        * `SymmetricLayeredSlabs`
        * `AsymmetricLayeredSlabs`
        * `Helix`
        * `DiscreteHelix`
        * `SpacefillingSymmetry`
        * `ManualSymmetry`
        * `PDB`- a PDB file
        * `AMP`- an amplitude grid file
        
        You can create any model by calling its initialization. 
        
        Please note that models are dynamically loaded from those available in D+. 
        Therefore, your code editor may underline the model in red even if the model exists.
        
        All models have `location_params` (Location Parameters) and  `extra_params` (Extra Parameters). 
        Some models (that support layers) also contain `layer_params` (Layer Parameters).
        These are all collection of instances of the `Parameter` class, and can be accessed from 
        `model.location_params`, `model.extra_params`, and `model.layer_params`, respectively.
        
        All of these can be modified. They are accessed using dictionaries.
        Example:
        
        ```
        from dplus.DataModels.models import UniformHollowCylinder
        
        uhc=UniformHollowCylinder()
        uhc.layer_params[1]["Radius"].value=2.0
        uhc.extra_params["Height"].value=3.0
        uhc.location_params["x"].value=2
        ```
        
        For additional information about which models have layers and what the various parameters available for each model are,
        please consult the D+ User's Manual.
        
        ###### Parameters
        
        The `Parameter` class contains the following properties:
        
        `value`: a float whose default value is `0`
        
        `sigma`: a float whose default value is `0`
        
        `mutable`: a boolean whose default value is `False`
        
        `constraints`: an instance of the `Constraints` class, its default value is the default `Constraints`
        
        Usage:
        
        ```  
        p=Parameter()  #creates a parameter with value: '0', sigma: '0', mutable: 'False', and the default constraints.
        p=Parameter(7) #creates a parameter with value: '7', sigma: '0', mutable: 'False', and the default constraints.
        p=Parameter(sigma=2) #creates a parameter with value: '0', sigma: '2', mutable: 'False', and the default constraints.
        p.value= 4  #modifies the value to be 4.
        p.mutable=True #modifies the value of mutable to be 'True'.
        p.sigma=3 #modifies sigma to be 3.
        p.constraints=Constraints(min_val=5) #sets constraints to a 'Constraints' instance whose minimum value (min_val) is 5.
        ```
        ###### Constraints
        
        The `Constraints` class contains the following properties:
        
        `MaxValue`: a float whose default value is `infinity`.
        
        `MinValue`: a float whose default value is `-infinity`.
        
        The usage is similar to 'Parameter' class, for example:
        
        ```
        c=Constraints(min_val=5) #creates a 'Constraints' instance whose minimum value is 5 and whose maximum value is the default ('infinity').
        ```
        
        ## CalculationInput
        
        The CalculationInput class inherits from the `State` class and therefore has access to all its functions and properties.
        
        In addition, it contains the following properties of its own:
        
        * `x`: an array of q values
        * `y`: an array of intensity values from a signal, optional. Used for running fitting.
        * `use_gpu`: a boolean whose default value is True, representing whether D+ should use the GPU
        * `args`: a json dictionary of the arguments required to run generate.exe or fit.exe
        
        the function `load_graph` can load x and y values from an ordered or unordered dictionary of x:y pairs
        the function `load_signal_file` can load x and y values from an existing signal file
        
        
        A new instance of CalculationInput can be created simply by calling its constructor.
        
        An empty constructor will cause CalculationInput to be created with default values derived from the default State.
        
        Alternately, the constructor can be called with either `graph` or `x` and/or `y` provided as arguments,
        and these will then be used to overrie the default values derived from the default state.
        
        In addition, CalculationInput has the following static methods to create an instance of GenerateInput:
        
        * `load_from_state_file` receives the location of a file that contains a serialized parameter tree (state)
        * `load_from_PDB` receives the location of a PDB file, and automatically creates a guess at the best state parameters
         based on the PDB 
         * `copy_from_state` returns a new `CalculationInput` based on an existing state or `CalculationInput`
        
        ```
        from dplus.CalculationInput import CalculationInput
        gen_input=CalculationInput()
        ```
        
        ```
        from dplus.CalculationInput import CalculationInput
        gen_input=CalculationInput.load_from_state_file('sphere.state')
        ```
        
        ```
        from dplus.CalculationInput import CalculationInput
        signal = SignalFileReader("signal_file.out")
        fit_input = CalculationInput(x=signal.x_vec, y=signal.y_vec)
        ```
        
        
        ## Amplitudes
        
        In the module `Amplitudes` there is the class `Grid` and the class `Amplitude` which inherits from Grid.
        
        **Please note**: The class Amplitude is a purely Python class, not to be confused with the class AMP from Dplus.DataModels.Models
        
        The class `AMP` contains a filename pointing to an amplitude file, an extra parameter scale, a boolean centered, and it can be
        serialized and sent as part of the Domain parameter tree to D+. 
        
        The class `Amplitude`, by contrast, can be used to build an amplitude and then save that amplitude as an amplitude file,
        which can then be opened in D+ (or sent in a class AMP) but it itself cannot be added directly to the Domain parameter tree. 
        If you want to add it, you must save the amplitude to a file first using the `save` method, 
        and then you can use the State's function `add_amplitude`, to add it to the tree.
        
        
        The class `Grid` is initialized with `q_max` and `grid_size`. 
        
        `Grid` is used to create/describe a grid of `q`, `theta`, `phi` angle values. 
        
        These values can be described using two sets of indexing:
        
        1. The overall index `m`
        2. The individual angle indices `i`, `j`, `k`
        
        The `Grid` is created in spherical coordinates in reciprocal space.
        It has `N` shells, and the parameter`grid_size` is equal to `2N`.
        The  index  `i` represents the shell number that is related to `q` , which is the magnitude of the scattering vector.
        `q_max` is the largest `q`  value. The index `j` corresponds to the polar (`theta`) angle on the `i`th shell, and the index `k` corresponds to the azimuthal angle, `phi` , of the `j`th polar angle on the `i`th shell. The `Grid`  is nonuniform and the `i`th shell contains 6i(3i+1) points in its `theta`-`phi`  plane.
        The index `m` is a single index that describe each point on the `Grid` .
        The index starts at the origin of the `Grid`, where `m=0` , and continues to the next shells, whereas each shell is arranged in a `phi`-major storage order.
        There is a one-to-one relation between the two  indexing methods.
        
        `Grid`has the following methods:
        
        * `create_grid`: a generator that returns `q`, `theta`, `phi` angles in `phi`-major order
        * `indices_from_index`: receives an overall index `m`, and returns the individual `q`, `theta`, and `phi` indices: `i`, `j`, `k`
        * `angles_from_index`: receives an overall index `m`, and returns the matching `q`, `theta`, and `phi` angle values
        * `angles_from_indices`: receives angle indices `i`,`j`,`k` and returns their `q`, `theta`, and `phi` angle values
        * `index_from_indices`: receives angle indices `i`,`j`,`k` and returns the overall index `m` that matches them
        * `indices_from_angles`: receives angles `q`, `theta`, `phi`, ands returns the matching indices `i`,`j`,`k`
        * `index_from_angles`: receives angles `q`, `theta`, `phi` and returns the matching overall index `m`
        
        
        ```
        from dplus.Amplitudes import Grid
        
        g=Grid(5, 100)
        for q,theta,phi in g.create_grid():
            print(g.index_from_angles(q, theta, phi))
        ```
        
        The class Amplitude inherits from Grid. It is a class intended to describe the amplitude of a model/function, and can 
        save these values to an amplitude file (that can be read by D+) and can also read amplitude files (like those created by D+)
        
        Like a grid, Amplitude is initialized with q_max and grid_size.
         
        `Amplitude` overrides the `create_grid` method of `Grid`. `create_grid` of `Amplitude` requires a function as an argument. 
        This function must receive `q`, `theta`, and `phi`, and returns two values, representing the real and imaginary parts of the `amplitude`'s complex number. 
        The values can be returned as a tuple (a sequence of immutable Python objects), an array, or a Python complex number (A+Bj).
        These values are then saved to the `Ampltiude`'s `values` property, and can also be accessed through the `complex_amplitude_array` 
        property as a `numpy` array of `numpy` complex types.
        
        These values are then saved to the Ampltiude's `values` property, and can also be accessed through the `complex_amplitudes_array`
        property as a numpy array of numpy complex types.
        
        Alternately, Amplitude has a static method, `load`,  which receives a filename of an Amplitude file, and returns an Amplitude instance
        with the values from that file already loaded.
        
        Finally, there is the method `save`, which will save the information in the Amplitude class to an Amplitude file which can then be 
        passed along to D+ to calculate its signal or perform fitting.
        
        It has the following properties:
        
        * `headers`: a list that contains data about the class
        * `description`: an optional string the user can fill with data about the amplitude class (for example what the type of the model). The description property will be added to the headers.
        ```
        from dplus.Amplitudes import Amplitude
        my_amp=Amplitude.load("myamp.amp")
        for c in my_amp.complex_amplitude_array:
            print(c)
        ```
        
        ```
        from dplus.Amplitudes import Amplitude
        
        def my_func(q, theta, phi):
            return q+1, 0
        
        a=Amplitude(7.5, 200)
        a.description= "An exmaple amplitude"						 
        a.create_grid(my_func)
        a.save("myfile.amp")
        ```
        
        There are examples of using Amplitudes to implement models similar to D+ in the additional examples section.
        
        The module Amplitudes also contains two convenience functions for converting between cartesian and spherical coordinates:
        
        * `sph2cart` receives r, theta, phi and returns x, y, z
        * `cart2sph` receives x, y, z and returns r, theta, phi
        
        ```
        from dplus.Amplitudes import sph2cart, cart2sph
        
        q, theta, phi = cart2sph(1,2,3)
        x, y, z = sph2cart(q,theta,phi)
        
        ```
        
        ## CalculationResult
        
        The CalculationResult class is returned by the CalculationRunner. 
        The user should generally not be instantiating the class themselves. 
        
        The base `CalculationResult` class is inherited by `GenerateResult` and `FitResult`
        
        `CalculationResult` has the following properties:
        
        * `graph`: an OrderedDict whose keys are x values and whose values are y values.
        * `y`: The raw list of y values from the results JSON
        * `error` : returns the JSON error report from the dplus run
        
        In addition, CalculationResults has the following functions:
        
        * `get_amp(model_ptr, destination_folder)`: returns the file location of the amplitude file for given `model_ptr`. 
        `destination_folder` has a default value of `None`, but if provided, the amplitude file will be copied to that location,
        and then have its address returned. 
        * `get_amps(destionation_folder)`: returns an array of file locations for every amplitude file created during the D+
        calculation process. `destination_folder` has a default value of `None`, but if provided, the amplitude files
        will be copied to that location.  
        * `get_pdb(mod_ptr, destination_folder)`: returns the file location of the PDB file for given `model_ptr`. 
        `destination_folder` has a default value of `None`, but if provided, the PDB file will be copied to that location,
        and then have its address returned 
        * `save_to_out_file(filename)`: receives file name, and saves the results to the file.
        
        In addition to the above:
         
        `GenerateResult` has a property `headers`, created by D+ to describe 
        the job that was run. It is an Ordered Dictionary, whose keys are ModelPtrs and whose values are the header associated. 
        
        `FitResult` has two additional properties,
        * `parameter_tree`: A JSON of parameters (can be used to create a new `state` with state's `load_from_dictionary`). 
        Only present in fitting, not generate, results
        * `result_state`: a `CalculationInput` whose `Domain` contains the optimized parameters obtained from the fitting
        
        
        ## FileReaders
        
        The API contains a module FileReaders. 
        
        Presently all it contains is `SignalFileReader`, which can be initialized with a path to a signal file (eg a .out or .dat file) 
        and will read that file into its `x_vec`, `y_vec`, and `graph` properties.
        
        
        ## Additional Usage examples
        
        
        ***Example One***
        
        ```
        from dplus.CalculationInput import CalculationInput
        from dplus.CalculationRunner import LocalRunner
        
        exe_directory = r"C:\Program Files\D+\bin"
        sess_directory = r"session"
        runner= LocalRunner(exe_directory, sess_directory)
        
        input=CalculationInput.load_from_state_file('spherefit.state')
        result=runner.fit(input)
        print(result.graph)
        ```
        
        Comments:
        This program loads a state file from `spherefit.state`, runs fitting with the local runner, and print the graph of the result.
        
        ***Example Two***
        
        ```
        from dplus.CalculationInput import CalculationInput
        from dplus.CalculationRunner import LocalRunner
        from dplus.DataModels import ModelFactory, Population
        from dplus.State import State
        from dplus.DataModels.models import UniformHollowCylinder
        
        sess_directory = r"session"
        runner= LocalRunner(session_directory=sess_directory)
        
        uhc=UniformHollowCylinder()
        caldata = CalculationInput()
        caldata.Domain.populations[0].add_model(uhc)
        
        result=runner.generate(caldata)
        print(result.graph)
        ```
        
        ***Example Three***
        
        ```
        from dplus.CalculationRunner import LocalRunner
        from dplus.CalculationInput import CalculationInput
        
        runner=LocalRunner()
        caldata=CalculationInput.load_from_PDB('1JFF.pdb', 5)
        result=runner.generate(caldata)
        print(result.graph)
        ```
        
        ***Example Four***
        
        ```
        from dplus.CalculationRunner import LocalRunner
        from dplus.CalculationInput import CalculationInput
        runner=LocalRunner()
        input = CalculationInput.load_from_state_file("uhc.state")
        cylinder = input.get_model("test_cylinder")
        
        print("Original radius is ", cylinder.layer_params[1]['Radius'].value)
        result = runner.generate(input)
        
        input.load_graph(result.graph)
        cylinder = input.get_model("test_cylinder")
        cylinder.layer_params[1]['Radius'].value = 2
        cylinder.layer_params[1]['Radius'].mutable = True
        input.FittingPreferences.convergence = 0.5
        input.use_gpu = True
        fit_result = runner.fit(input)
        optimized_input= fit_result.result_state
        result_cylinder=optimized_input.get_model("test_cylinder")
        print(fit_result.parameter_tree)
        print("Result radius is ", result_cylinder.layer_params[1]['Radius'].value)
        
        ```
        
        Comments: 
        `fit_result.result_state` is the optimized state (i.e. the optimized parameter tree) that is returned from the fitting (`runner.fit(input)`). You can fetch the cylinder whose name is "test_cylinder" from that parameter tree, to see what its new optimized parameters are.
        
        
        ### Implementing Models using Amplitudes
        
        For the purpose of these exmaples the models are implemented with minimal default parameters, in a realistic usage 
        scenario the user would set those parameters as editable properties to be changed at his convenience.
        
        ```
        from dplus.Amplitudes import Amplitude
        import math
        
        class UniformSphere:
            def __init__(self):
                self.extraParams=[1,0]
                self.ED=[333, 400]
                self.r=[0,1]
        
            @property
            def nLayers(self):
                return len(self.ED)
        
            def calculate(self, q, theta, phi):
                cos=math.cos
                sin=math.sin
                nLayers=self.nLayers
                ED=self.ED
                extraParams=self.extraParams
                r=self.r
                def closeToZero(x):
                    return (math.fabs(x) < 100.0 * 2.2204460492503131E-16)
        
                if closeToZero(q):
                    electrons = 0.0
                    for i in range( 1, nLayers):
                        electrons += (ED[i] - ED[0]) * (4.0 / 3.0) * math.pi * (r[i] ** 3 - r[i-1] ** 3)
                    return (electrons  * extraParams[0] + extraParams[1], 0.0)
        
                res = 0.0
        
                for i in range(nLayers-1):
                    res -= (ED[i] - ED[i + 1]) * (cos(q * r[i]) * q * r[i] - sin(q * r[i]))
                res -= (ED[nLayers - 1] - ED[0]) * (cos(q * r[nLayers - 1]) * q * r[nLayers - 1] - sin(q * r[nLayers - 1]))
        
                res *= 4.0 * math.pi / (q*q * q)
        
                res *= extraParams[0] #Multiply by scale
                res += extraParams[1] #Add background
        
                return (res, 0.0)
        
        sphere=UniformSphere()
        a=Amplitude(7.5, 200)
        a.create_grid(sphere.calculate)
        a.save("sphere.amp")
        
        input = CalculationInput()
        amp_model = input.add_amplitude(a)
        amp_model.centered=True
        runner=LocalRunner()
        result=runner.generate(input)
        ```
        
        ```
        
        class SymmetricSlab:
            def __init__(self):
                self.scale=1
                self.background=0
                self.xDomain=10
                self.yDomain=10
                self.ED=[333, 280]
                self.width=[0,1]
                self.OrganizeParameters()
        
            @property
            def nLayers(self):
                return len(self.ED)
        
            def OrganizeParameters(self):
                self.width[0] = 0.0
                self.xDomain *= 0.5
                self.yDomain *= 0.5
                for i in range(2, self.nLayers):
                    self.width[i] += self.width[i - 1];
        
            def calculate(self, q, theta, phi):
                def closeToZero(x):
                    return (math.fabs(x) < 100.0 * 2.2204460492503131E-16)
                from dplus.Amplitudes import sph2cart
                from math import sin, cos
                from numpy import sinc
                import numpy as np
                qx, qy, qz = sph2cart(q, theta, phi)
                res= np.complex128(0+0j)
                if(closeToZero(qz)):
                    for i in range(self.nLayers):
                        res += (self.ED[i] - self.ED[0]) * 2. * (self.width[i] - self.width[i - 1])
                    return res * 4. * sinc(qx * self.xDomain) * self.xDomain * sinc(qy * self.yDomain) * self.yDomain
        
                prevSin = np.float64(0.0)
                currSin=np.float64(0.0)
                for i in range(1, self.nLayers):
                    currSin = sin(self.width[i] * qz)
                    res += (self.ED[i] - self.ED[0]) * 2. * (currSin - prevSin) / qz
                    prevSin = currSin
                res *= 4. * sinc((qx * self.xDomain)/np.pi) * self.xDomain * sinc((qy * self.yDomain)/np.pi) * self.yDomain
                return res * self.scale + self.background #Multiply by scale and add background
        
        
        
        from dplus.Amplitudes import Amplitude
        from dplus.State import State
        from dplus.CalculationRunner import LocalRunner
        from dplus.CalculationInput import CalculationInput
        sphere = SymmetricSlab()
        a = Amplitude(7.5, 80)
        a.create_grid(sphere.calculate)
        
        ```
        
        ### Python Fitting
        It is possible to fit a curve using the results from Generate and numpy's built in minimization/curve fitting functions.
        All that is requires is wrapping the interface code so that it receives and returns parameters the way scipy expects (eg as numpy arrays)
         
        An example follows:
        
        ```
        import numpy as np
        from scipy import optimize
        from dplus.CalculationInput import CalculationInput
        from dplus.CalculationRunner import LocalRunner
        
        input=CalculationInput.load_from_state_file(r"2_pops.state")
        generate_runner=LocalRunner()
        
        def run_generate(xdata, *params):
            '''
            scipy's optimization algorithms require a function that receives an x array and an array of parameters, and
            returns a y array.
            this function will be called repeatedly, until scipy's optimization has completed.
            '''
            input.set_mutable_parameter_values(params) #we take the parameters given by scipy and place them inside our parameter tree
            generate_results=generate_runner.generate(input) #call generate
            return np.array(generate_results.y) #return the results of the generate call
        
        x_data=input.x
        y_data=input.y
        p0 = input.get_mutable_parameter_values()
        method='lm' #lenenberg-marquadt (see scipy documentation)
        popt, pcov =optimize.curve_fit(run_generate, x_data, y_data, p0=p0, method=method)
        
        #popt is the optimized set of parameters from those we have indicated as mutable
        #we can insert them back into our CalculationInput and create the optmized parameter tree
        input.set_mutable_parameter_values(popt)
        #we can run generate to get the results of generate with them
        best_results=generate_runner.generate(input)
        ```
        
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: Environment :: Console
Classifier: Intended Audience :: Science/Research
Classifier: License :: Other/Proprietary License
Classifier: Operating System :: OS Independent
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3.4
Classifier: Topic :: Scientific/Engineering :: Chemistry
