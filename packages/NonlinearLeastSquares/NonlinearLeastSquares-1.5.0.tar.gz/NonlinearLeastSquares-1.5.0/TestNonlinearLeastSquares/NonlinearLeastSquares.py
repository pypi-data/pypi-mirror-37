__version__ = '1.5.0'
__author__  = "Avinash Kak (kak@purdue.edu)"
__date__    = '2018-October-10'
__url__     = 'https://engineering.purdue.edu/kak/distNonlinearLeastSquares/NonlinearLeastSquares-1.5.0.html'
__copyright__ = "(C) 2018 Avinash Kak. Python Software Foundation."


__doc__ = '''

NonlinearLeastSquares.py

Version: ''' + __version__ + '''
   
Author: Avinash Kak (kak@purdue.edu)

Date: ''' + __date__ + '''


@title
CHANGE LOG:

  Version 1.5.0:

    This version adds a new class, ProjectiveCamera, to the module for
    demonstrating how nonlinear least-squares can be used for estimating
    structure of a scene from the data recorded with a camera in motion.
    For the example code that is included with the module, we assume that
    the cameras are calibrated.  For a simulated demonstration, you can
    create calibrated cameras from a generic instance of the
    ProjectiveCamera class that is then subject to various translational
    and rotational transformations.  Since sparse bundle adjustment code is
    not yet incorporated in the module, you can only solve very simple
    scene structure problems with this version --- problems with no more
    than, say, half a dozen points in world 3D.  Despite this limitation on
    scene complexity, I expect this version of the module to serve an
    educational purpose in classes on computer vision.

  Version 1.1.1:

    This version includes constructor options to control the size and the
    position of the graphics for displaying the results of nonlinear
    least-squares optimization.

  Version 1.1:

    This version fixes a bug in the synthetic data generator function used
    for illustrating the functionality of the NonlinearLeastSquares class.
    Changes also made to the information that is printed out when the
    module is run in the debug mode.

  Version 1.0:

    In the form of a class named NonlinearLeastSquares, this module
    provides a domain agnostic implementation of nonlinear least-squares
    algorithms (gradient-descent and Levenberg-Marquardt) for fitting a
    model to observed data.  Typically, the model involves several
    parameters and each observed data element can be expressed as a
    function of those parameters plus noise.  The goal of nonlinear
    least-squares is to estimate the best values for the parameters given
    all of the observed data.  In order to illustrate how to use the
    NonlinearLeastSquares class, the module also comes with another class,
    OptimizeSurfaceFit, whose job is to fit the best surface (of a
    specified analytical form) to noisy height data over the XY-plane. The
    model in this case is the analytical description of the surface and the
    goal of nonlinear least-squares is to estimate the best values for the
    parameters in the analytical description.


@title
USAGE:

    Although the main NonlinearLeastSquares class is domain agnostic, in
    this section I'll demonstrate its use with two domain specific classes
    that are supplied with the module: OptimizedSurfaceFit and
    ProjectiveCamera.  The former is for fitting optimized analytically
    specified surfaces to noisy data over a plane and the latter is for
    optimally estimating the structure of a scene from the data recorded
    with a calibrated camera in motion.

    USAGE FOR OPTIMAL SURFACE FITTING:

    You need to create an instance of the NonlinearLeastSquares class as
    shown in line (A) below.  In addition, you need to create an instance
    of a domain-specific class such as OptimizedSurfaceFit as is shown at
    line (B) below.  Note that in the example shown in line (B), the
    domain-specific class has two duties: (1) to synthetically generate
    noisy height data; and (2) to call on NonlinearLeastSquares to fit an
    optimized model to the synthetically generated data.

        optimizer =  NonlinearLeastSquares(                              #(A)
                         max_iterations = 400,
                         delta_for_jacobian = 0.000001,
                         delta_for_step_size = 0.0001,
                     )

        surface_fitter = OptimizedSurfaceFit(                             #(B)                
                                gen_data_synthetically = True,
                                datagen_functional = "7.8*(x - 0.5)**3 + 2.2*(y - 0.5)**2",
                                data_array_size = (16,16),
                                how_much_noise_for_synthetic_data = 0.7,
                                model_functional = "a*(x-b)**3 + c*(y-d)**2",
                                initial_param_values = {'a':2.0, 'b':0.4, 'c':0.8, 'd':0.4},
                                display_needed = True,
                                debug = True,
                         )

        surface_fitter.set_constructor_options_for_optimizer(optimizer)  #(C)

        result = surface_fitter.calculate_best_fitting_surface('lm')     #(D)

        or 

        result = surface_fitter.calculate_best_fitting_surface('gd')     #(E)

    In line (C), it is the job of the OptimizedSurfaceFit instance as
    constructed in line (B) to export the domain-related information (after
    it is packaged under the hood into a domain-agnostic form) to the
    instance of NonlinearLeastSquares that was constructed in line (A).
    The information that the OptimizedSurfaceFit instance conveys to the
    NonlinearLeastSquares instance includes:

        1) The observed noisy data vector.  This vector is denoted X in the
           NonlinearLeastSquares class.  The same notation is used for the
           observed data vector in the usage-example class
           OptimizedSurfaceFit.

        2) The initial values to be used for the parameters of the model.

        3) A vector of the predicted values for each of the data elements
           in X, all in functional form involving the parameters of the
           model.  This vector is denoted Fvec in the NonlinearLeastSquares
           class.

        4) The display function to be used for plotting the partial and the
           final results if at all such results can be displayed in the
           form of a 2D or 3D graphic with Python's matplotlib library.

    Finally, the statement in line (D) lets you call on the
    Levenberg-Marquardt algorithm for estimating the model parameters. If
    you would rather use the more basic gradient-descent algorithm for that
    purpose, your call will look like what is shown in line (E).


    USAGE FOR ESTIMATING THE STRUCTURE OF A SCENE WITH 
    A CAMERA IN MOTION:

    You again need to create an instance of the NonlinearLeastSquares class
    as shown in line (F) below.  In addition, you need to create an
    instance of a class like ProjectiveCamera shown at line (G) below.

    explained in the Introduction section of this document.  For example,
    for finding the parameters of a model that you wish to fit to noisy
    height data over the xy-plane, for the domain specific class you would
    create an instance of the OptimizedSurfaceFit class as shown in line
    (B) below.  Note that in the example shown in line (B), the
    domain-specific class has two duties: (1) to synthetically generate
    noisy height data; and (2) to call on NonlinearLeastSquares to fit an
    optimized model to the synthetically generated data.


        optimizer =  NonlinearLeastSquares.NonlinearLeastSquares(
                                             max_iterations = 400,
                                             delta_for_jacobian = 0.000001,
                                             delta_for_step_size = 0.0001,
                     )
        
        camera = ProjectiveCamera.ProjectiveCamera(
                             camera_type = 'finite_projective',
                             alpha_x = 1000.0,
                             alpha_y = 1000.0,
                             x0 = 300.0,
                             y0 = 250.0,
                 )
        camera.initialize()

        world_points = camera.make_world_points_for_triangle()
        world_points_xformed = camera.apply_transformation_to_generic_world_points(world_points, ..... )
        ##  Now move the camera to different positions and orientations and then
        result = camera.get_scene_structure_from_camera_motion('lm')
        ....
        ....

    In solving these types of problems, sometimes it is possible to
    explicitly declare the Jacobian matrix that is used by nonlinear
    least-squares algorithms.  This matrix is of size Nxp where N is the
    total number of observations in the data vector X and p the number of
    parameters in the model. The (i,j)-th element of the Jacobian matrix is
    the partial derivative of the i-th element of the predictor vector Fvec
    with respect to the j-th model parameter.  If you wish to supply this
    matrix explicitly to NonlinearLeastSquares (as opposed to letting
    NonlinearLeastSquares estimate it numerically), you must use your
    domain knowledge to first construct the Jacobian matrix in your own
    domain-specific class and then convey it to an instance of
    NonlinearLeastSquares through the constructor option
    'jacobian_functionals_array' of the latter.  [See the definition of the
    method set_jacobian_functionals_array() of the NonlinearLeastSquares
    class.]  


@title
INTRODUCTION:

    Nonlinear least-squares is a widely used set of algorithms for fitting
    a model to noisy data through the minimization of a cost function.  The
    observed data is represented as a vector (denoted X in this module) and
    how the model would predict each element of X by another vector that is
    denoted Fvec.  As you would expect, each element of Fvec is a function
    of the parameters of the model.  The goal of nonlinear least-squares is
    to find the best possible values for the parameters, best in the sense
    of minimizing a cost function that is almost always the square of the
    vector norm of the difference between X and Fvec.

    The simplest approach to solving a nonlinear least-squares problem is
    Gradient Descent (GD).  The mental imagery that best explains GD is to
    think of all of the model parameters as constituting a hyperplane and
    the cost function as a surface over the hyperplane.  Gradient descent
    consists of starting at some point in the hyperplane, looking straight
    up at the surface, and walking in the direction of the steepest descent
    on the surface. At each point on the hyperplane, you make the size of
    your next step proportional to the value of the gradient on the
    cost-function surface.  Assuming there are no local minima to trap your
    progress, GD will eventually take you to the point on the hyperplane
    that is directly below the global minimum for the cost function.

    Even when getting trapped in a local minimum is not an issue (because,
    let's say, you made a good choice for the starting point), the basic
    gradient-descent algorithm suffers from the shortcoming that the closer
    you get to the minimum, the smaller your steps will be, and, therefore,
    the slower your progress toward the destination.

    One way to get round this problem with gradient-descent is to use the
    Gauss-Newton formula to make a direct jump to the minimum --- assuming
    you are already sufficiently close to it.  However, should you
    inadvertently try to make a Gauss-Newton jump when still far from the
    minimum, your algorithm could become numerically unstable and crash.

    The algorithm that does a good job of combining the numerical
    robustness of gradient-descent with the speed of Gauss-Newton, while
    making sure that the latter is not invoked too early, is the
    Levenberg-Marquardt (LM) algorithm. Given a start point on the
    hyperplane spanned by the model parameters, LM starts by taking a GD
    step. In subsequent iterations, before committing itself to a step, LM
    checks whether or not that step can safely be taken with GN.  If not,
    it steers the path toward GD.  However, if the condition for taking the
    GN step safely is satisfied, it goes ahead with that.  In this manner,
    LM can get to the minimum in a small number of steps, often under 10,
    whereas for the same problem and the same start point, GD might take
    more than a hundred.
    
    The NonlinearLeastSquares class in this module provides implementations
    for both the basic Gradient Descent and the more efficient
    Levenberg-Marquardt algorithms for getting to the minimum of a cost
    function.

    From a programming standpoint, the most notable feature of
    NonlinearLeastSquares is that it is domain agnostic.  That is, you
    should be able to use NonlinearLeastSquares for solving any problem
    that requires a GD or an LM solution for finding the optimum values for
    a set of model parameters through the minimization of a cost function.

    The fact that NonlinearLeastSquares is generic implies that you have to
    write a class of your own for the specific domain in which you wish to
    use NonlinearLeastSquares.  The domain specific class that you create
    must export to NonlinearLeastSquares values for the following options
    in its constructor:

    -- The observed data vector.  This vector is denoted X in the
       NonlinearLeastSquares class. 

    -- The initial values to be used for the parameters of the model.

    -- A vector of the predicted values for each of the data elements in X,
       all in functional form involving the parameters of the model.  This
       vector is denoted Fvec in the NonlinearLeastSquares class.

    -- The display function to be used for plotting the partial and the
       final results if at all such results can be displayed in the form of
       a 2D or 3D graphic with Python's matplotlib library.

    And, if you wish for NonlinearLeastSquares to use your analytically
    specified partial derivatives in the Jacobian matrix that it needs for
    the next-step calculations, your domain-specific class must also export
    that matrix to NonlinearLeastSquares.  In the absence of a
    user-supplied Jacobian matrix, NonlinearLeastSquares estimates it
    numerically. [See the implementation code for the OptimizedSurfaceFit
    class supplied with this module --- that class is an example of a
    domain-specific class that uses NonlinearLeastSquares for carrying out
    the needed optimization --- for how your own domain-specific class can
    construct a Jacobian matrix in a functional form and supply it to
    NonlinearLeastSquares.]

    The NonlinearLeastSquares class provides several setter methods that
    your own domain-specific class can use to convey the above-mentioned
    information to NonlinearLeastSquares.

    To illustrate how you may wish to write your domain specific class,
    this module also comes with two additional classs named
    OptimizedSurfaceFit and ProjectiveCamera, the first for fitting
    surfaces to noisy data over an xy-plane and the second for estimating
    the structure of a 3D scene from the data recorded by a camera in
    motion.


@title
METHODS:

    Constructing an instance of NonlinearLeastSquares:

        optimizer =  NonlinearLeastSquares(   
                         X = None,
                         Fvec = None,
                         num_measurements = None,
                         num_parameters = None,
                         initial_params_dict = None, 
                         initial_param_values_file = None, 
                         jacobian_functionals_array = None,
                         delta_for_jacobian = 0.000001,
                         delta_for_step_size = 0.0001,
                         max_iterations = 200,
                     )

        In most usage scenarios, though, you are likely to call
        NonlinearLeastSquares directly with just the following constructor
        options and let your own domain specific class set the other
        options at run time.  That is, in your own code, you will first
        create an instance of NonlinearLeastSquares through the following
        call to its constructor:

        optimizer =  NonlinearLeastSquares(             
                         max_iterations = 400,
                         delta_for_jacobian = 0.000001,
                         delta_for_step_size = 0.0001,
                     )

        and subsequently have your own domain-specific class call the
        various setter methods of NonlinearLeastSquares for giving values
        to its other constructor options.  As to which setter methods your
        own class should call is presented in the rest of this section.

@title
CONSTRUCTOR OPTIONS:

        debug:

            When set to True, it prints out a lot of information at each
            iteration of the nonlinear least-squares algorithm invoked.

        display_function:

            If the problem you are trying to solve with nonlinear
            least-squares allows for the result of optimization to be
            visualized, use this constructor option to supply a reference
            to the function you would like to be used for such
            visualization.
    
        Fvec:
    
            This must be set to a numpy vector (actually a numpy matrix
            with just one column) whose elements are the "predictors" for
            the corresponding values of the X vector.  (We use the symbol
            'X' to denote the vector of measured data, as you will soon
            see.)  Each element of Fvec will be a function of some or all
            of the model parameters.

        initial_params_dict:
    
            This is set to a dictionary whose keys are the model parameters
            and whose values the initial values for the model parameters.
            The initial values for the model parameters specify the point
            in the parameter hyperplane where you want to start the descent
            to the minimum.

        initial_param_values_file:

            If your problem involves a very large number of parameters, it
            may be more convenient to place all their initial values in a
            text file.  Each parameter and its initial value must be in a
            line all by itself.  See the file "initial_params_gd2.txt" in
            the Examples directory for how this file needs to be formatted.

        jacobian_functionals_array:

            If you wish to specify the partial derivatives of the
            functional elements in the Fvec vector with respect to the
            model parameters, you can supply those as a numpy chararray
            through this constructor option.

        num_measurements:

            This is simply the number of data values (meaning the 
            number of measurements) in X.
    
        num_parameters:
    
            This is the number of model parameters that you wish to calculate
            with nonlinear least-squares.

        X:

            This variable must be set to a numpy vector (actually a numpy
            matrix with just one column) whose elements constitute the
            observed data.  The number of elements in X would equal the
            number of data values that you are using for calculating the
            optimum values of the model parameters.

@title
METHODS:

    (1)  grad_descent():

         This is the implementation of the basic gradient-descent
         algorithm.

    (2)  leven_marq():

         This is the implementation of the Levenberg-Marquardt algorithm
         mentioned in the Introduction section.

    (3)  set_debug():

         This allow your own domain-specific class to set the 'debug'
         attribute of an instance of NonlinearLeastSquares.

    (4)  set_display_function():

         Some problem domains allow the result of a nonlinear least-squares
         calculation to be displayed with 2D or 3D graphics.  For example,
         if the goal is to fit an analytical form (in the form of, say, a
         polynomial) to noisy height data over a flat plane and you use the
         nonlinear least-squares algorithm to calculate the best values for
         the parameters of the analytical form, you should be able to
         visualize the quality of your results by displaying both the
         original noisy data and the model you fit to the data.  When such a
         visualization of the results is possible, you can pass the
         definition of the your display function through this setter
         function.

    (5)  set_Fvec():

         This method expects for its main argument a numpy matrix with a
         single column whose each element must be a functional form predicts
         the corresponding element in the measurement vector X.  These
         functional forms will be functions of the model parameters.

    (6)  set_initial_params():

         This method expects for its main argument a dictionary of
         <key,value> pairs in which the keys are the model parameters and
         the the corresponding values the initial values to be given to
         those parameters.

    (7)  set_jacobian_functionals_array():

         This method expects for its argument an Nxp matrix of functionals
         for the partial derivatives needed for the Jacobian matrix.  N is
         the number of data elements in the X vector and p is the number of
         parameters in the model.  To elaborate, if you are using nonlinear
         least-squares to fit an optimal surface to noisy height values
         over the xy-plane, your X vector will be a single-column numpy
         matrix and each row of this vector would correspond to one height
         value at some (x,y) point. The corresponding row in the argument
         jacobian_functionals_array contains p functionals, with each
         functional being a partial derivative of the model functional
         (with its x and y set according to where the height was recorded)
         with respect to the parameter corresponding to the column index.

    (8)  set_num_measurements():

         This method sets the number of data elements in the X vector in
         the instance of the NonlinearLeastSquares on which the method is
         invoked.

    (9)  set_num_parameters():

         This method sets the number of model parameters that will be used
         in the nonlinear least-squares optimization.

    (10) set_X():

         This method sets the data vector, in the form of a numpy matrix
         consisting of only one column, in an instance of
         NonlinearLeastSquares.  This is the data to which you which you
         want to fit a given model and you want NonlinearLeastSquares to
         estimate the best values for the parameters of the model.


@title
USING NonlinearLeastSquares -- OPTIMIZED SURFACE FITTING:

    This section presents a class named OptimizedSurfaceFit to illustrate
    how you can use the functionality of NonlinearLeastSquares in your own
    code.  The goal of OptimizedSurfaceFit is to fit a model surface to
    noisy height data over the xy-plane in the xyz-coordinate frame, with
    the model surface being described by a polynomial function.  Here are
    some examples of such polynomials:

           "a*(x-b)**2 + c*(y-d)**2 + e"

           "a*x**2 + c*y**2"

           "a*x + b*y + c"
    
    where the value returned by the polynomial for given values of the
    coordinate pair (x,y) is the height above the xy-plane at that point.
    Given the sort of a model surface shown above, the problem becomes one
    of optimally estimating the value for the model parameters from the
    noisy observed data.  If vector X represents the measured data over a
    set of (x,y) points in the form of a vector of observations, we can now
    write for the cost function:

          d^2    =    || X  -  Fvec ||^2

    where Fvec is a vector of the predictions as dictated by the model at
    each of the (x,y) point.  That is, each element of the Fvec vector is a
    prediction for the corresponding element of the measurement vector X.
    The quantity d^2 is the square of the vector norm of the prediction
    error, meaning the difference between the observations in X and the
    predictions in Fvec.  Given X and Fvec vectors, We can call on
    NonlinearLeastSquares to help us find the best values for the
    parameters of the model surface.

    A typical call to OptimizedSurfaceFit's constructor looks like:

        surface_fitter = OptimizedSurfaceFit(                         
                                gen_data_synthetically = True,
                                datagen_functional = "7.8*(x - 0.5)**3 + 2.2*(y - 0.5)**2",
                                data_array_size = (16,16),
                                how_much_noise_for_synthetic_data = 0.7,
                                model_functional = "a*(x-b)**3 + c*(y-d)**2",
                                initial_param_values = {'a':2.0, 'b':0.4, 'c':0.8, 'd':0.4},
                                display_needed = True,
                                display_size = (12,8),                 
                                display_position = (500,300),
                                debug = True,
                         )

    or, if you wish to also supply the partial derivatives of the model
    functional that can be used by OptimizedSurfaceFit for specifying the
    the Jacobian matrix to NonlinearLeastSquares, like

        surface_fitter = OptimizedSurfaceFit(
                                gen_data_synthetically = True,
                                datagen_functional = "7.8*(x - 0.5)**3 + 2.2*(y - 0.5)**2",
                                data_array_size = (16,16), 
                                how_much_noise_for_synthetic_data = 0.5,
                                model_functional = "a*(x-b)**3 + c*(y-d)**2",
                                initial_param_values = {'a':2.0, 'b':0.4, 'c':0.8, 'd':0.4},
                                partials_for_jacobian = {'a':'(x-b)**2', 
                                                         'b':'-2*a*(x-b)', 
                                                         'c':'(y-d)**2', 
                                                         'd':'-2*c*(y-d)'},            
                                display_needed = True,
                                display_size = (12,8),                 
                                display_position = (500,300),
                                debug = True,
                         )
    
    With regard to the constructor option 'partials_for_jacobian', it is
    important to realize that what is passed to OptimizedSurfaceFit's
    constructor is not directly the Nxp Jacobian matrix (where N is the
    number of observations in X and p the number of parameters in the
    model).  Instead, it is a set of partial derivatives of the model
    functional with respect to the parameters of the functional.  However,
    OptimizedSurfaceFit knows how to translate into an Nxp numpy chararray
    of the functionals needed for the Jacobian.

    The constructor options for the OptimizedSurfaceFit class:

        data_array_size:                      

           The synthetic height that is generated by OptimizedSurfaceFit is
           over a unit square in the xy-plane. Both the x and the y
           coordinates of this square range over the interval 0.0 to 1.0.
           If you set this constructor option to, say, (16,16), the unit
           square will be sampled over a 16x16 grid.

        datagen_functional:           

            When gen_data_synthetically is set to True, you must supply an
            algebraic expression in the form of a string that
            OptimizedSurfaceFit can use to generate the height data.  Here
            is an example of what such a string looks like:

                       "7.8*(x - 0.5)**3 + 2.2*(y - 0.5)**2"

            You can call any function inside the string that the Python
            math library knows about.

        debug:

            This flag is passed on to NonlinearLeastSquares.  When set to
            True, it causes that class to display useful information during
            each iteration of the nonlinear least-squares algorithm.

        display_needed:

            Fitting optimal surfaces to height data lends itself well to 3D
            visualization.  So if you'd like to see the the surfaces that
            correspond to the optimal values for the model parameters, set
            this constructor option to True.

        display_position:

            It is set to a tuple of two integers, with the first integer
            specifying the horizontal coordinate and the second the
            vertical coordinate of the upper left corner of the display.
            These two coordinate values are with respect to the upper left
            corner of your terminal screen. Horizontal coordinates are
            positive to the right and vertical coordinates positive
            pointing down.  Setting this constructor parameter is optional.
            If not set, matplotlib will use its default values.

        display_size:

            It is set to a tuple of two integers, with the first integer
            specifying the width and the second the height of the display.
            Setting this constructor parameter is optional.  If not set,
            matplotlib will use its default values.

        gen_data_synthetically:

            If set to True, OptimizedSurfaceFit can generate the measurement
            height data for your synthetically according to the function
            you specify through the constructor option 'datagen_functional'.

        how_much_noise_for_synthetic_data:                    

           This option controls the amount of noise that is added to the
           height data generated according to the datagen_functional.  The
           best way to give a meaningful value to this construction option
           is to set to some fraction of the largest coefficient in the
           datagen_functional.

        initial_param_values:   

           Through this option, you can transmit to OptimizedSurfaceFit your
           initial guesses for the values of the parameters in the model
           functional.  If you cannot think of a guess, you try setting all
           the parameters to zero.  OptimizedSurfaceFit conveys your initial
           values for the parameters to the NonlinearLeastSquares class.
           You express the initial values in the form of a dictionary,
           whole keys are the name of the parameters and whose values the
           initial values to be given to those parameters.

        initial_param_values_file:

           If the number of parameters in the problem you are addressing is
           large, it may be more convenient to supply the initial values
           for the parameters through a text file. 

        measured_data_file:

           If the amount of measured data is large, it may be more convenient
           to feed it into the module through a text file.

        model_functional:                        

           This is the algebraic expression that we want to fit to the
           noisy height data.  OptimizedSurfaceFit will call on
           NonlinearLeastSquares to estimate the best values for the
           parameters of this algebraic expression.  For example, if the
           model_functional is "a*(x-b)**3 + c*(y-d)**2", the
           NonlinearLeastSquares will find the best possible values for the
           parameters a, b, c, and d --- best in the sense of minimizing
           the cost function described previously.

        model_functional_file:

           If the model functional is too long and/or too complex to be
           specified as an option directly in a call to the constructor,
           you can also place it in a text file through the
           model_functional_file option.

        optimizer:

           Through this constructor option, you can have an instance
           variable of the same name to hold a reference to an instance of
           NonlinearLeastSquares.

        partials_for_jacobian:

           Although the NonlinearLeastSquares class can numerically
           estimate the partial derivatives of the element of the Fvec
           vector with respect to the model parameters, with this option
           you can supply your own analytical forms for the partial
           derivatives that OptimizedSurfaceFit can convert into a Jacobian
           matrix before transmitting it to NonlinearLeastSquares.

    Here are the methods defined for OptimizedSurfaceFit:

        (1) construct_Fvec():

            This method constructs the Fvec vector that
            NonlinearLeastSquares needs for comparing with the measurement
            vector X. Each element of Fvec is a prediction for the
            corresponding element of X and this prediction is a functional
            form involving model parameters.

        (2) construct_jacobian_array_in_functional_form():

            This method is used only when the user supplies analytical
            forms for the partial derivatives of the model functional with
            respect to each of the model parameters.  (When the user does
            not supply such partial derivatives, NonlinearLeastSquares
            estimates the Jacobian through numerical approximations.)

        (3) display_function()

            The problem addressed by OptimizedSurfaceFit lends itself well
            to visualization of the quality of the results returned by
            NonlinearLeastSquares.  With the definition for this method
            that is provided, you can see how well the model parameters
            estimated by NonlinearLeastSquares fit the noisy height data.

        (4) gen_data():

            This method generates the height data over the xy-plane
            according to the analytical form that is supplied to it as its
            main argument.  We refer to this analytical form as the 'model
            functional'.

        (5) get_initial_params_from_file():

            If you want to use model functions that have a large number of
            parameters, it might be easier to place their values in a text
            file and have OptimizedSurfaceFit get it from the file by using
            this method.

        (6) get_measured_data_from_text_file():

            If you would like to supply the height data through a text file
            (rather than have the class generate it automatically for you),
            then this is the method to call for reading in the data from
            the file.  The method assumes that that individual data
            elements are separated by whitespace characters (space, tab,
            newline, etc.).  Since OptimizedSurfaceFit knows about the size
            of the array both along the x-coordinate and along the
            y-coordinate, it knows how to interpret the data in the text
            file.

        (7) get_model_functional_from_file():

            If the model functional is too long, you can get
            OptimizedSurfaceFit to read it from a text file by using this
            option.

        (8) set_constructor_options_for_optimizer()

            The responsibility of this method is to take all of the user
            supplied information and reconstitute it into a form that is
            needed by NonlinearLeastSquares taking into account the
            peculiarities of your domain.


@title
USING NonlinearLeastSquares -- ESTIMATING SCENE STRUCTURE:

    This section presents a class named ProjectiveCamera to illustrate how
    you can use the functionality of NonlinearLeastSquares in your own code
    for estimating the structure of a 3D scene from the data recorded by a
    camera in motion. [NOTE: Since sparse bundle adjustment (SBA) is not
    yet a part of the module, the code can only handle a small number of
    scene points at the moment.  I plan to include SBA in a future version
    of this module.]

    To create a simulated structure-from-camera-motion demonstration with
    this module, you must first create an instance the ProjectiveCamera
    class.  A typical call to ProjectiveCamera's constructor looks like:

        camera = ProjectiveCamera.ProjectiveCamera(
                             camera_type = 'finite_projective',
                             alpha_x = 1000.0,
                             alpha_y = 1000.0,
                             x0 = 300.0,
                             y0 = 250.0,
                 )
        camera.initialize()
        camera.print_camera_matrix()

    This returns a camera whose optic axis is aligned with the world-Z axis
    and whose image plane is parallel to the world-XY plane. The parameters
    'alpha_x' and 'alpha_y' are for the focal length of the camera in terms
    of the image sampling intervals along the x-axis and along the y-axis,
    respectively.  The parameters 'x0' and 'y0' are for the coordinates of
    the point in the camera image plane where the optic axis penetrates the
    image plane with respect to the origin in the image plane (which is
    usually a corner of the image).

        world_points = camera.make_world_points_for_triangle()
        world_points_xformed = camera.apply_transformation_to_generic_world_points( world_points, \
                                                                    (0,0,0), (0.0,0.0,5000.0), 1.0)

    which generates a triangle defined by its three vertices from a method
    defined for the ProjectiveCamera class and then moves the scene
    triangle along the optic axis of the camera (the world-Z axis) by 5000
    units.  After the transformation, the three vertices are at the
    coordinates (3000,3000,5000), (4000,3000,5000), and (4000,5000,5000).

    Subsequently, you must move the camera to different positions and
    orientations and use the camera matrix constructed by the
    ProjectiveCamera instance to project the world triangle into the camera
    images. You are going to need the following two methods defined for the
    ProjectiveCamera class for these camera motions:

        rotate_previously_initialized_camera_around_x_axis( theta_x_delta )

        translate_a_previously_initialized_camera( (0.0,y_motion_delta,0.0) )

    At each camera position/orientation achieved with the above two methods, you
    can record the pixels with the following call:

        pixels = camera.get_pixels_for_a_sequence_of_world_points( world_points_xformed )

    Subsequently, you must make the following call:

        construct_X_vector( all_pixels )        

    where 'all_pixels' is the set of all the pixel recorded in all the
    positions of the camera.

    You would also need to create a Prediction Vector, Fvec, for the
    observed data whose elements are predictor functionals in terms of the
    scene parameters that need to be estimated.  This is achieved with a 
    call like:

        construct_Fvec_for_calibrated_cameras( camera_params_dict )

    Now you are ready to call the following method:

        get_scene_structure_from_camera_motion('lm')

    which will invoke the Levenberg-Marquardt method on the
    NonlinearLeastSquares class to estimate the scene structure.

    The constructor options for the ProjectiveCamera class:

        camera_type:

           You can only set this constructor option to 'finite_projective'
           in the current version of the module.  Eventually, I intend
           to include 'orthographic' as another possibility for this
           option.

        alpha_x:
        alpha_y:

           These options are for the focal length in terms of the image
           sampling intervals used along the image x-axis and along the
           image y-axis, respectively.

        x0:
        y0:

           These options are for the coordinates of the point in the camera
           image plane where the optic axis penetrates the image plane with
           respect to the origin in the image plane (which is usually a
           corner of the image).

        camera_rotation:

           Using the (roll,pitch,yaw) convention you can specify the
           rotation for the camera in the constructor itself.  However, for
           experimenting with structure-from-camera-motion experiments, it
           is easier to first construct a camera in its generic pose and to
           then call the rotate and translate methods on it in order to
           move to a different position and orientation.

        camera_translation:

           Using a triple to indicate displacements along the world-X,
           world-Y, and world-Z, you can specify a translation for the
           camera in the constructor itself.  However, for experimenting
           with structure-from-camera-motion experiments, it is easier to
           first construct a camera in its generic pose and to then call
           the rotate and translate methods on it in order to move to a
           different position and orientation.


    Here are the methods defined for ProjectiveCamera:

        (1) add_new_camera_to_list_of_cameras():

            You will find this utility method useful for enumerating all
            the different camera positions you will be using in a simulated
            structure-from-camera-motion experiment.

        (2) apply_transformation_to_generic_world_points()

            After you have constructed a scene object (typically just a
            simple shape like a triangle or a tetrahedron), you can call on
            this method to change its position and the pose in the world
            frame.  The method takes FOUR arguments: (1) The scene
            structure in the form of a list of homogeneous coordinates for
            the world points on the object.  (2) The first is a triple that
            specifies the rotation using the (roll,pitch,yaw)
            convention. (3) The second argument is a triple for the
            displacement along the world-X, world-Y, and world-Z
            coordinates. (4) The scale factor by which you want to expand
            or shrink the scene object.

        (3) construct_Fvec_for_calibrated_cameras(camera_params_dict)

            This method constructs the prediction vector Fvec vector that
            NonlinearLeastSquares needs for comparing with the measurement
            vector X. Each element of Fvec is a prediction for the
            corresponding element of X and this prediction is a functional
            form involving the structure parameters.
            
        (4) construct_parameter_vec_for_calibrated_cameras()

            This method constructs an ordered list of the SYMBOLIC NAMES to
            be used for each of the coordinates for the scene points that
            need to be estimated.  This list looks like 
            "['X_0', 'Y_0', 'Z_0', 'X_1', 'Y_1', 'Z_1', 'X_2' ......]"

        (5) construct_structure_ground_truth()

            This method packages the scene world points in a way that makes
            it convenient to output in your terminal window the estimated
            coordinates for the scene points, the ground-truth value for
            those coordinates, and the initial guesses supplied for them.

        (6) construct_X_vector(all_pixels)

            As mentioned in the Introduction, we use the notation X to
            represent a vector of all the observed data.  For a
            structure-from-camera-motion problem, the observed data
            consists of all the pixels in all of the camera positions.
            This method orders the x- and the y-coordinates of all the
            recorded pixels in the same fashion as the order given to the
            scene points in world-3D.  

        (7) display_structure()

            This method is used to display in the form of a Matplotlib
            figure the following three things simultaneously: the estimated
            scene structure, the actual world points used for the scene
            object, and the initial guesses supplied for those coordinates
            to the nonlinear least-squares algorithm.  The three parameters
            for this method are named 'structure_points_estimated',
            'world_points_xformed', and 'initial_values_supplied'.

        (8) get_all_cameras()

            This utility method is convenient for getting hold of all the
            cameras that supplied the data for solving the structure-from-
            camera-motion problem.  We consider an instance of
            ProjectiveCamera at each of its positions in world-3D as a
            distinct camera.  So if you move the camera to, say, 20
            different locations, you are in effect using 20 cameras.

        (9) get_pixels_for_a_sequence_of_world_points()

            For any given camera position, this method applies the
            corresponding camera matrix to each world point, which must be
            in homogeneous coordinates, in the sequence of world points
            supplied to the method as its argument.

        (10) get_scene_structure_from_camera_motion('lm')

            This is the method you must call for estimating the scene
            structure after you have collected all the pixel data from all
            the different positions of the camera.  Obviously, before you
            can call this method, you would need to construct the
            observation vector X from the pixel data the predictor vector
            Fvec from the parameters of the cameras at each of their
            positions.

        (11) initialize()
    
            This method packs the constructor options supplied to the
            ProjectiveCamera constructor in the form of the camera's
            intrinsic parameter matrix K.  If a translation and/or a
            rotation is specified for the camera through the constructor,
            those are also incorporated in the 3x4 camera matrix P put
            together by this method.
        
        (12) make_world_points_for_triangle()

            This method returns a scene object that consists of a triangle
            in world 3D. I have found a triangle defined by its three world
            points to be convenient for testing the basic logic of the
            algorithm for solving a structure-from-camera-motion problem.
            The triangle returned by this method can be subject to any
            orientation changing and position changing transformation.
        
        (13) make_world_points_from_tetrahedron_generic()

            Like the previous method, this method returns world points on a
            tetrahedron in world 3D that you can subsequently use for your
            simulated structure-from-moving-camera experiment.

        (14) print_camera_matrix()

            This utility method is convenient for displaying the 3x4 camera
            matrix for any or all of the positions of the camera.

        (15) rotate_previously_initialized_camera_around_world_X_axis()

            This method incrementally rotates the camera clockwise around
            the world-X axis by an angle 'theta' in degrees that is
            supplied to the method as its argument.

        (16) rotate_previously_initialized_camera_around_world_Y_axis()

            This method incrementally rotates the camera clockwise around
            the world-Y axis by an angle 'theta' in degrees that is
            supplied to the method as its argument.

        (17) set_constructor_options_for_optimizer( optimizer )

            A ProjectiveCamera instances uses this method to pass on to
            NonlinearLeastSquares all the information needed by the latter
            (such as the observed data vector X and the prediction vector
            Fvec) for constructing an optimum estimate of the scene
            structure.  The argument 'optimizer' that this method takes is
            an instance of NonlinearLeastSquares.

        (18) set_initial_values_for_params()

            Every nonlinear least-squares algorithm needs a starting guess
            for whatever it is that is being estimated.  In most cases, you
            would construct a random guess for the parameters and supply
            those values to this method in the form of a dictionary in
            which each key is the symbolic name of one of the parameters
            being estimated and the value a random guess for the parameter.

        (19) set_params_list( params_arranged_list )
            
            You will use this method to pass on to the instance of
            ProjectiveCamera an ordered list of the parameters you want
            estimated with nonlinear least-squares.

        (20) translate_a_previously_initialized_camera()

            This method incrementally displaces the camera by 'translation'
            that is supplied to it as its argument. The argument
            'translation' consists of a triple of real numbers that stand
            for a displacement along the world-X, along the world-Y, and
            along the world-Z.


@title
THE ExamplesOptimizedSurfaceFit DIRECTORY:

    See the 'ExamplesOptimizedSurfaceFit' directory in the distribution for
    examples of how you can use the NonlinearLeastSquares class for solving
    optimization problems.  These examples are based on the domain specific
    class OptimizedSurfaceFit that knows about fitting model surfaces to
    noisy height data over a flat plane.  You will see the following four
    scripts in this directory:

        leven_marq.py

        grad_descent.py    

        leven_marq_with_partial_derivatives.py

        grad_descent_with_partial_derivatives.py

    For the first two scripts, the NonlinearLeastSquares instance used will
    estimate the needed Jacobian matrix through appropriate numerical
    approximation formulas applied to the elements of the Fvec vector.  On
    the other hand, for the third and the fourth scripts, your own
    domain-specific class must construct the Jacobian matrix, in the form
    of an array of functions. In the case of the domain-specific class
    OptimizedSurfaceFit that comes with this module, this Jacobian matrix is
    constructed from the user-supplied partial derivatives for the model
    functional.

    In order to become familiar with the NonlinearLeastSquares class, you
    might wish to play with the four scripts listed above by:

    -- Trying different functional forms for the 'datagen_functional' for
       different shaped surfaces.

       When you change the algebraic form of 'datagen_functional' for the
       OptimizedSurfaceFit class, make sure that you also change the
       algebraic form supplied for 'model_functional'.  Note that nonlinear
       least-squares can only calculate the parameters of a model
       functional that best fit the noisy height data; it cannot conjure up
       a new mathematical form for the surface.  So the basic mathematical
       form of the 'model_functional' must be the same as that of the
       'datagen_functional'.

    -- Trying different degrees of noise.  

       As mentioned elsewhere, when you supply a numerical value for the
       constructor option 'how_much_noise_for_synthetic_data' for the
       OptimizedSurfaceFit class, the number you enter should be in
       proportion to the largest numerical coefficient in the 'datagen'
       functional.  Change this numerical value and see what happens to the
       quality of the final results.

    -- Try different values for the initial values of the model parameters.

       Since, depending on where the search for the optimum solution is
       started, all nonlinear least-squares methods can get trapped in a
       local minimum, see what happens when you change these initial
       values.
      
    -- Try different algebraic expressions for the 'model_functional'
       constructor option for the OptimizedSurfaceFit class.  But note that
       if you change the algebraic form of this functional, you must also
       change the algebraic form of the 'datagen_functional' option.

    -- Try running the example with and without the partial derivatives
       that are supplied through the 'partials_for_jacobian' option for the
       OptimizedSurfaceFit class.


@title
THE ExamplesStructureFromCameraMotion DIRECTORY:

    See the 'ExamplesStructureFromCameraMotion' directory in the
    distribution for two example scripts that show how you can use the
    NonlinearLeastSquares module for estimating the structure of a 3D from
    the images recorded by a moving camera.  Both these example use the
    functionality packed in the ProjectiveCamera class that comes with
    Version 1.5 of this module.  You will see the following two scripts in
    this directory:

        sfm_with_calibrated_cameras_translations_only.py

        sfm_with_calibrated_cameras_translations_and_rotations.py

    where the prefix "sfm" stands for "structure from motion".

    As the names of the scripts imply, we assume that the cameras are
    calibrated.  The ProjectiveCamera class makes it easy to specify
    calibrated cameras.  The constructor of the class first gives you a
    camera for which you can specify the internal and the external
    parameters through the constructor options. Subsequently, you can apply
    translational and rotational transformations to the camera to move it
    to different locations in world 3D.  Since the 3x4 camera matrices for
    all these positions of the camera are known, you end up with a set of
    fully calibrated cameras for experimenting with structure-from-motion
    simulations.


@title
CAVEAT

    About using NonlinearLeastSquares for estimating the structure of a 3D
    scene from the multiple views collected by a moving camera, note that
    since the module does not yet include sparse bundle adjustment code,
    you will only be able to solve very simple problems in which the scene
    structure consists of at most half-a-dozen points in world 3D.  (An
    upcoming version of this module will include sparse bundle adjustment
    code.)  Despite the limitation on scene complexity, I expect the
    current version of the module to be useful in educational settings.


@title
INSTALLATION:

    The NonlinearLeastSquares class was packaged using setuptools.  For
    installation, execute the following command-line in the source
    directory (this is the directory that contains the setup.py file after
    you have downloaded and uncompressed the package):
 
            sudo python setup.py install
    and/or
            sudo python3 setup.py install

    On Linux distributions, this will install the module file at a location
    that looks like

             /usr/local/lib/python2.7/dist-packages/

    and for Python3 at a location like

             /usr/local/lib/python3.4/dist-packages/

    If you do not have root access, you have the option of working directly
    off the directory in which you downloaded the software by simply
    placing the following statements at the top of your scripts that use
    the NonlinearLeastSquares class:

            import sys
            sys.path.append( "pathname_to_NonlinearLeastSquares_directory" )

    To uninstall the module, simply delete the source directory, locate
    where the NonlinearLeastSquares module was installed with "locate
    NonlinearLeastSquares" and delete those files.  As mentioned above, the
    full pathname to the installed version is likely to look like
    /usr/local/lib/python2.7/dist-packages/NonlinearLeastSquares*

    If you want to carry out a non-standard install of the
    NonlinearLeastSquares module, look up the on-line information on
    Disutils by pointing your browser to

              http://docs.python.org/dist/dist.html


@title
BUGS:

    Please notify the author if you encounter any bugs.  When sending
    email, please place the string 'NonlinearLeastSquares' in the subject
    line.


@title
ABOUT THE AUTHOR:

    The author, Avinash Kak, recently finished a 17-year long "Objects
    Trilogy Project" with the publication of the book "Designing with
    Objects" by John-Wiley. If interested, visit his web page at Purdue to
    find out what this project was all about. You might like "Designing
    with Objects" especially if you enjoyed reading Harry Potter as a kid
    (or even as an adult, for that matter).

    For all issues related to this module, contact the author at
    kak@purdue.edu

    If you send email, please place the string "NonlinearLeastSquares" in
    your subject line to get past the author's spam filter.


@title
COPYRIGHT:

    Python Software Foundation License

    Copyright 2016 Avinash Kak

@endofdocs
'''

import numpy
import numpy.linalg
import os,sys,glob
import itertools

numpy.set_printoptions(precision=3)


class NonlinearLeastSquares(object):
    def __init__(self, *args, **kwargs):
        'constructor'                       
        if args:
            raise Exception('''The NonlinearLeastSquares constructor can only be called with '''
                            '''the following keyword arguments: X, Fvec, num_measurements,  '''
                            '''num_parameters, initial_params_dict, jacobian_functionals_array, '''
                            '''initial_param_values_file, display_function''')
        allowed_keys = 'initial_param_values_file','initial_params_dict','measured_data','max_iterations','delta_for_jacobian','delta_for_step_size','jacobian_functionals_array','num_measurements','num_parameters','display_function','debug'
        keywords_used = kwargs.keys()
        for keyword in keywords_used:
            if keyword not in allowed_keys:
                raise Exception("Wrong key used in constructor call --- perhaps spelling error")
        X=Fvec=num_measurements=num_parameters=initial_param_values_file=initial_params_dict=measured_data_file=max_iterations=delta_for_jacobian=delta_for_step_size=jacobian_functionals_array=display_function=debug=None
        if 'initial_params_dict' in kwargs: initial_params_dict=kwargs.pop('initial_params_dict')
        if 'initial_param_values_file' in kwargs: initial_param_values_file=kwargs.pop('initial_param_values_file')
        if 'max_iterations' in kwargs: max_iterations=kwargs.pop('max_iterations')
        if 'delta_for_jacobian' in kwargs: delta_for_jacobian=kwargs.pop('delta_for_jacobian')
        if 'delta_for_step_size' in kwargs: delta_for_step_size=kwargs.pop('delta_for_step_size')
        if 'X' in kwargs: X=kwargs.pop('X')
        if 'Fvec' in kwargs: X=kwargs.pop('Fvec')
        if 'num_measurements' in kwargs: num_measurements=kwargs.pop('num_measurements')
        if 'num_parameters' in kwargs: num_parameters=kwargs.pop('num_parameters')
        if 'jacobian_functionals_array' in kwargs: jacobian_functionals_array=kwargs.pop('jacobian_functionals_array')
        if 'initial_param_values_file' in kwargs: initial_param_values_file=kwargs.pop('initial_param_values_file')
        if 'debug' in kwargs: debug=kwargs.pop('debug')
        if initial_params_dict and initial_param_values_file:
            raise Exception("You must choose either the 'initial_param_values_file' or the 'initial_params_dict' option in the constructor, but not both")
        self.X = X
        self.Fvec = Fvec                 #  is a column vector --- meaning a numpy matrix with just one column
        self.num_measurements = num_measurements
        self.num_parameters = num_parameters
        self.initial_params_dict = initial_params_dict
        self.jacobian_functionals_array = jacobian_functionals_array
        self.display_function = display_function
        if max_iterations:
            self.max_iterations = max_iterations
        else:
            raise Exception("The constructor must specify a value for max_iterations")        
        if delta_for_jacobian:
            self.delta_for_jacobian = delta_for_jacobian
        elif jacobian_functionals_array is None:        
            raise Exception("When not using 'jacobian_functionals_array', you must explicitly set 'delta_for_jacobian' in the constructor for NonlinearLeastSquares")
        self.delta_for_step_size = delta_for_step_size
#        self.params_ordered_list = sorted(self.initial_params_dict) if self.initial_params_dict else None
        self.params_ordered_list = None
        self.params_arranged_list = None       # For scene reconstruction, we use arranged list and not ordered list
        self.debug = debug if debug else False

    def set_num_measurements(self, how_many_measurements):
        print("\nNumber of measurements: ", how_many_measurements)
        self.num_measurements = how_many_measurements

    def set_num_parameters(self, how_many_parameters):
        print("\nNumber of parameters: ", how_many_parameters)
        self.num_parameters = how_many_parameters

    def set_initial_params(self, initial_params_dict):
        self.initial_params_dict = initial_params_dict
        self.params_dict = initial_params_dict

    def set_params_ordered_list(self, params_list):
        self.params_ordered_list = sorted(params_list)

    def set_params_arranged_list(self, params_list):
        self.params_arranged_list = params_list

    def set_X(self, X):
        self.X = numpy.asmatrix(numpy.copy(X))

    def set_Fvec(self, Fvector):
        '''
        Fvec is a column vector --- meaning a numpy matrix with just one column.  You would 
        access its first element by Fvec[0,1]
        '''
        self.Fvec = Fvector  

    def set_jacobian_functionals_array(self, jacobian_functionals_array):
        '''
        This method expects for its argument an Nxp matrix of functionals for the partial 
        derivatives needed for the Jacobian matrix.  N is the number of measurements in
        the X vector and p is the number of parameters in the model.  If you are using
        nonlinear least-squares to fit optimal surfaces to noisy measurements over the
        xy-plane, each element of the X vector would correspond to one such measurement at
        some (x,y) coordinates. And an element the argument jacobian_functionals_array chararray
        would correspond to the partial derivative of the model functional that already
        has incorporated the (x,y) coordinates corresponding to that row and that is 
        a partial derivative of the model with respect to the parameter corresponding to
        the column.
        '''
        self.jacobian_functionals_array = jacobian_functionals_array          # a chararray of size Nxp

    def set_display_function(self, display_function):
        self.display_function = display_function

    def set_debug(self, debug):
        self.debug = debug

    def leven_marq(self):
        if os.path.isdir("figs"):
            list(map(os.remove, glob.glob('figs/*.png')))
        else:
            os.mkdir("figs")
        error_norm_with_iteration = []
        delta_for_jacobian = self.delta_for_jacobian if self.jacobian_functionals_array is None else None
        delta_for_step_size = self.delta_for_step_size if self.jacobian_functionals_array is None else None
        num_elements = len(self.Fvec)
        num_measurements = len(self.X)
        params_list = self.params_ordered_list if self.params_ordered_list is not None else self.params_arranged_list
        num_params  =  len(params_list)
        current_param_values = [self.params_dict[param] for param in params_list]
        current_param_values = numpy.matrix(current_param_values).T 
        current_fit_to_measurements = numpy.asmatrix(numpy.zeros_like(self.X))
        for i in range(num_measurements):
            current_fit_to_measurements[i,0] = \
                       eval(self._eval_functional_element(self.Fvec[i,0], self.initial_params_dict))
        if self.debug:
            print("\nleven_marq: current_fit_to_measurements (shown as transpose):")
            print(str(current_fit_to_measurements.T))
        current_error = self.X - current_fit_to_measurements
        if self.debug:
            print("\ncurrent error (shown as transpose):")
            print(str(current_error.T))
            print("\ncurrent error shape: %s" % str(current_error.shape))
        current_error_norm = numpy.linalg.norm(self.X - current_fit_to_measurements)
        if current_error_norm < 1e-12:
            print("\nCurrent error norm: %.10f" % current_error_norm)
            print('''\nLooks like your initial choices for the parameters are perfect. '''
                  '''Perhaps there is nothing to be gained by invoking nonlinear least-squares '''
                  '''on your problem.''')
            sys.exit(1)
        error_norm_with_iteration.append(current_error_norm)
        if self.debug:
            print("\ncurrent error norm: %s" % str(current_error_norm))
        if self.display_function is not None:
            self.display_function(current_fit_to_measurements, current_error_norm, -1)
        new_param_values = new_fit_to_measurements = new_error_norm = None
        iteration_index = 0
        alambda = 0.001
        #  If 10 CONSECUTIVE STEPS in the parameter hyperplane turn out to the wrong choices,
        #  we terminate the iterations.  If you want to change the number of consecutively 
        #  occurring stops, you have to make changes at three different places in this file, 
        #  including the statement shown below.

#        wrong_direction_flags = [0] * 10       
        wrong_direction_flags = [0] * 20

        #  An important feature of LM is that ONLY SOME OF THE ITERATIONS cause a reduction in 
        #  the error vector (which is the difference between the measured data and its predicted 
        #  values from the current knowledge of the parameters), the following list stores just
        #  those iteration index values that were productive in reducing this error.  This list is
        #  useful for deciding when to display the partial results.
        productive_iteration_index_values = [-1]
        for iteration_index in range(self.max_iterations):
            jacobian = numpy.asmatrix(numpy.zeros((num_measurements, num_params), dtype=float))
            if self.jacobian_functionals_array is not None:
                '''
                A functional form was supplied for the Jacobinan.  Use it.
                '''
                for i in range(num_measurements):
                    params_dict_local = {params_list[i] : current_param_values[i].tolist()[0][0] for i in range(num_params)}
                    if self.debug is True and i == 0: 
                        print("\ncurrent values for parameters: %s" % str(sorted(params_dict_local.items())))
                    for j in range(num_params):
                        jacobian[i,j] = \
                          eval(self._eval_functional_element(self.jacobian_functionals_array[i,j], params_dict_local)) 
            else:
                '''
                Estimate your own Jacobian
                '''
                for i in range(num_measurements):
                    params_dict_local = {params_list[i] : current_param_values[i].tolist()[0][0] for i in range(num_params)}
                    if self.debug is True and i == 0: 
                        print("\ncurrent values for parameters: %s" % str(sorted(params_dict_local.items())))
                    for j in range(num_params):
                        incremented_params_dict_local = {param : params_dict_local[param] for param in params_dict_local}
                        param = self.params_ordered_list[j] if self.params_ordered_list is not None else self.params_arranged_list[j]
                        evaled_element1 = self._eval_functional_element(self.Fvec[i,0], params_dict_local)
                        incremented_params_dict_local[param] = params_dict_local[param] + delta_for_jacobian
                        evaled_element2 = self._eval_functional_element(self.Fvec[i,0], incremented_params_dict_local)
                        jacobian[i,j] = (eval(evaled_element2) - eval(evaled_element1)) / delta_for_jacobian
                    params_dict_local = None
            if self.debug:
                print("\njacobian:")
                print(str(jacobian))
                print("\njacobian shape: %s" % str(jacobian.shape))
            A = jacobian.T * jacobian
            g = jacobian.T * current_error
            if self.debug:
                print("\ng vector for iteration_index: %d" % iteration_index)
                print(str(g.T))
            if abs(numpy.max(g)) < 0.0000001: 
                print("absolute value of the largest component of g below threshold --- quitting iterations")
                break
            B = numpy.linalg.inv(A + alambda * numpy.asmatrix(numpy.identity(num_params)))
            new_delta_param = alambda * g if iteration_index == 0 else B * g
            new_param_values = current_param_values + new_delta_param
            if self.debug:
                print("\nnew parameter values:")
                print(str(new_param_values.T))
            new_params_dict = {params_list[i] : new_param_values[i].tolist()[0][0] for i in range(num_params)}
            if self.debug:
                print("\nnew_params_dict: %s" % str(sorted(new_params_dict.items())))
            new_fit_to_measurements = numpy.asmatrix(numpy.zeros_like(self.X))
            for i in range(num_measurements):
                new_fit_to_measurements[i,0] = eval(self._eval_functional_element(self.Fvec[i,0], new_params_dict))
            if self.debug:
                print("\nnew_fit_to_measurements (shown as transpose):")
                print(str(new_fit_to_measurements.T))
            new_error =  self.X - new_fit_to_measurements
            if self.debug:
                print("\nnew error (shown as transpose):")
                print(str(new_error.T))
            new_error_norm = numpy.linalg.norm(self.X - new_fit_to_measurements)
            if self.debug:
                print("\nnew error norm: %s" % str(new_error_norm))
            if new_error_norm >= error_norm_with_iteration[-1]:
                alambda *= 10
                wrong_direction_flags.append(1)
#                wrong_direction_flags = wrong_direction_flags[-10:]   
                wrong_direction_flags = wrong_direction_flags[-20:]   
#                if alambda > 1e5:
#                if alambda > 1e7:
#                if alambda > 1e9:
                if alambda > 1e11:
                    if self.debug:
                        print("\nIterations terminated because alambda exceeded limit") 
                    break
                if all(x == 1 for x in wrong_direction_flags): 
                    if self.debug:
#                        print("\nTerminating descent because reached a max of 10 consecutive bad steps")
                        print("\n\nTERMINATING DESCENT BECAUSE reached a max of 20 consecutive bad steps")
                    break
                if self.debug:
                    print("\nNO change in parameters for iteration_index: %d with alambda = %f" % (iteration_index, alambda))
                continue
            else:
                if self.debug:
                    print("\n\n================================================ LM ITERATION: %d" 
                                                                        % len(productive_iteration_index_values))
                    print()
                productive_iteration_index_values.append(iteration_index)
                wrong_direction_flags.append(0)
#                wrong_direction_flags = wrong_direction_flags[-10:] 
                wrong_direction_flags = wrong_direction_flags[-20:] 
                alambda = 0.001
                error_norm_with_iteration.append(new_error_norm)
                if self.debug:
                    print("\nerror norms with iterations: %s" % str(error_norm_with_iteration))
                current_param_values = new_param_values
                if self.display_function is not None:
                    if len(productive_iteration_index_values) % 2 == 0:
                        self.display_function(new_fit_to_measurements, new_error_norm, len(productive_iteration_index_values)-1)
        if self.debug:
            print("\nerror norms with iterations: %s" % str(error_norm_with_iteration))
            print("\niterations used: %d" % (len(productive_iteration_index_values) - 1))
            print("\nproductive iteration index values: %s" % str(productive_iteration_index_values))
            print("\n\nfinal values for the parameters: ") 
            print(str(new_param_values.T))
        if self.debug is True and iteration_index == self.max_iterations - 1:
            print("\n\nWARNING: max iterations reached without getting to the minimum")
        if self.display_function:
            self.display_function(new_fit_to_measurements, new_error_norm, len(productive_iteration_index_values))
        result = {"error_norms_with_iterations" : error_norm_with_iteration,
                  "number_of_iterations" : len(productive_iteration_index_values) - 1,
                  "parameter_values" : new_param_values}
        return result

    def grad_descent(self):
        error_norm_with_iteration = []
        delta_for_jacobian = self.delta_for_jacobian if self.jacobian_functionals_array is None else None
        if self.delta_for_step_size is not None:
            delta_for_step_size = self.delta_for_step_size
        else:
            raise Exception("You must set the 'delta_for_step_size' option in the constructor for the gradient-descent algorithm")
        num_elements = len(self.Fvec)
        num_measurements = len(self.X)
#        params_list = self.params_ordered_list
        params_list = self.params_ordered_list if self.params_ordered_list is not None else self.params_arranged_list
        num_params  =  len(params_list)
        current_param_values = [self.params_dict[param] for param in params_list]
        current_param_values = numpy.matrix(current_param_values).T 
        current_fit_to_measurements = numpy.asmatrix(numpy.zeros_like(self.X))
        for i in range(num_measurements):
            current_fit_to_measurements[i,0] = \
                                   eval(self._eval_functional_element(self.Fvec[i,0], self.initial_params_dict))
        if self.debug:
            print("\ncurrent_fit_to_measurements:")
            print(str(current_fit_to_measurements))
        current_error = self.X - current_fit_to_measurements
        if self.debug:
            print("\ncurrent error:")
            print(str(current_error))
            print("current error shape: %s" % str(current_error.shape))
        current_error_norm = numpy.linalg.norm(self.X - current_fit_to_measurements)
        if current_error_norm < 1e-12:
            print("\nCurrent error norm: %.10f" % current_error_norm)
            print('''\nLooks like your initial choices for the parameters are perfect. '''
                  '''Perhaps there is nothing to be gained by invoking nonlinear least-squares '''
                  '''on your problem.''')
            sys.exit(1)
        error_norm_with_iteration.append(current_error_norm)
        if self.debug:
            print("current error norm: %s" % str(current_error_norm))
        new_param_values = new_fit_to_measurements = new_error_norm = None
        iteration_index = 0
        for iteration_index in range(self.max_iterations):
            if self.debug:
                print("\n\n ========================================  GD ITERATION: %d" % iteration_index)
                print()
            jacobian = numpy.asmatrix(numpy.zeros((num_measurements, num_params), dtype=float))
            if self.jacobian_functionals_array is not None:
                for i in range(num_measurements):
                    params_dict_local = {params_list[i] : current_param_values[i].tolist()[0][0] for i in range(num_params)}                
                    if self.debug is True and i == 0: 
                        print("\ncurrent values for parameters: %s" % str(sorted(params_dict_local.items())))
                    for j in range(num_params):
                        jacobian[i,j] = eval(self._eval_functional_element(self.jacobian_functionals_array[i,j], params_dict_local)) 
            else:
                for i in range(num_measurements):
                    params_dict_local = {params_list[i] : current_param_values[i].tolist()[0][0] for i in range(num_params)}
                    for j in range(num_params):
                        incremented_params_dict_local = {param : params_dict_local[param] for param in params_dict_local}
                        param = self.params_ordered_list[j] if self.params_ordered_list is not None else self.params_arranged_list[j]

                        evaled_element1 = self._eval_functional_element(self.Fvec[i][0], params_dict_local)
                        incremented_params_dict_local[param] = params_dict_local[param] + delta_for_jacobian
                        evaled_element2 = self._eval_functional_element(self.Fvec[i][0], incremented_params_dict_local)
                        jacobian[i,j] = (eval(evaled_element2) - eval(evaled_element1)) / delta_for_jacobian
                    params_dict_local = None
            if self.debug:
                print("jacobian:")
                print(str(jacobian))
                print("jacobian shape: %s" % str(jacobian.shape))
            new_param_values = current_param_values + 2 * delta_for_step_size * (jacobian.T * current_error)
            if self.debug:
                print("\nnew parameter values:")
                print(str(new_param_values.T))
            new_params_dict = {params_list[i] : new_param_values[i].tolist()[0][0] for i in range(num_params)}
            if self.debug:
                print("new_params_dict: %s" % str(new_params_dict))
            new_fit_to_measurements = numpy.asmatrix(numpy.zeros_like(self.X))
            for i in range(num_measurements):
                new_fit_to_measurements[i,0] = eval(self._eval_functional_element(self.Fvec[i][0], new_params_dict))
            if self.debug:
                print("new_fit_to_measurements:")
                print(str(new_fit_to_measurements))
            new_error =  self.X - new_fit_to_measurements
            if self.debug:
                print("\nnew error:")
                print(str(new_error))
            new_error_norm = numpy.linalg.norm(self.X - new_fit_to_measurements)
            if self.debug:
                print("\nnew error norm: %s" % str(new_error_norm))
            if new_error_norm > error_norm_with_iteration[-1]:
                break
            error_norm_with_iteration.append(new_error_norm)
            if self.debug:
                print("\nerror norms with iterations: %s" % str(error_norm_with_iteration))
            if self.display_function is not None and iteration_index % int(self.max_iterations/5.0) == 0:
                self.display_function(new_fit_to_measurements, new_error_norm, iteration_index)
            current_param_values = new_param_values
        if self.debug:
            print("\nerror norms with iterations: %s" % str(error_norm_with_iteration))
            print("\niterations used: %d" % iteration_index)
            print("\n\nfinal values for the parameters: ") 
            print(str(new_param_values))
        if self.debug is True and iteration_index == self.max_iterations - 1:
            print("\n\nWARNING: max iterations reached without getting to the minimum")
        if self.display_function:
            self.display_function(new_fit_to_measurements, new_error_norm, iteration_index)
        result = {"error_norms_with_iterations" : error_norm_with_iteration,
                  "number_of_iterations" : iteration_index,
                  "parameter_values" : new_param_values}
        return result

#------------------------------  Private Methods of NonlinearLeastSquares  --------------------

    def _get_initial_params_from_file(self, filename):
        if not filename.endswith('.txt'): 
            sys.exit("Aborted. _get_initial_params_from_file() is only for CSV files")
        initial_params_dict = {}
        initial_params_list = [line for line in [line.strip() for line in open(filename,"rU")] if line is not '']
        for record in initial_params_list:
            initial_params_dict[record[:record.find('=')].rstrip()] = float(record[record.find('=')+1:].lstrip())
        self.params_dict = initial_params_dict
        self.params_ordered_list = sorted(self.params_dict) if self.params_ordered_list is not None else self.params_arranged_list
        return initial_params_dict

    def _get_measured_data_from_text_file(self, filename):
        if not filename.endswith('.txt'): 
            sys.exit("Aborted. _get_measured_data_from_text_file() is only for txt files")
        all_data = list(map(float, open(filename).read().split()))
        if self.debug:
            print("_get_measured_data_from_text_file: all_data")
            print(str(all_data))
        X = numpy.matrix(all_data).T
        xnorm = numpy.linalg.norm(X)
        if self.debug:
            print("_get_measured_data_from_text_file:  norm of X: %s" % str(xnorm))  

    def _eval_functional_element(self, element, params_dict):
        augmented_element = element
        import re
        for param in params_dict:
            regex = r'\b' + param + r'\b'         
            if isinstance(augmented_element, (bytes)):
                if re.search(regex, augmented_element.decode('utf-8')):
                    augmented_element = re.sub(regex, str(params_dict[param]), augmented_element.decode('utf-8'))
            else:
                if re.search(regex, augmented_element):
                    augmented_element = re.sub(regex, str(params_dict[param]), augmented_element)
        return augmented_element

