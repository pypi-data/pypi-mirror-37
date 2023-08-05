#!/usr/bin/env python
#-*- coding: latin-1 -*-

##  sfm_with_calibrated_cameras_translations_only.py

##   The scene structure consists of a triangle defined by its three vertices.
##   The triangle is a distance of 5000 units from the world origin along its
##   Z-axis.  The triangle is in a plane parallel to the world XY-plane.

##   The camera is moved to a total of 20 different translational positions.
##   The camera motion is first along the positive world-X direction in steps of 
##   500 units and then along the positive world-Y direction, again in increments
##   of 500 units.

##   Calling syntax:
##
##             sfm_with_calibrated_cameras_translations_only.py


import NonlinearLeastSquares
import ProjectiveCamera
import numpy
import random
import sys

random.seed('abracadabra') 

optimizer =  NonlinearLeastSquares.NonlinearLeastSquares(                  
                                     max_iterations = 400,
                                     delta_for_jacobian = 0.000001,
                                     delta_for_step_size = 0.0001,
             )

#  This returns a camera whose optic axis is aligned with the world-Z axis and whose 
#  image plane is parallel to the world-XY plane. The parameters 'alpha_x' and 'alpha_y' 
#  are for the focal length in terms of the image sampling intervals along the x-axis 
#  and along the y-axis, respectively.   The parameters 'x0' and 'y0' are for the 
#  coordinates of the point in the camera image plane where the optic axis penetrates 
#  the image plane with respect to the origin in the image plane (which is usually a 
#  corner of the image):
camera = ProjectiveCamera.ProjectiveCamera( 
                     camera_type = 'finite_projective',
                     alpha_x = 1000.0,
                     alpha_y = 1000.0,
                     x0 = 300.0,
                     y0 = 250.0,
         )
camera.initialize()
camera.print_camera_matrix()

##  NOTE:  The commented-out line below is for making the world points for a tetrahedron.
##         Note, however, the rudimentary display function provided for the ProjectiveCamera
##         class does not show these points well.  So if you want a good visual display of
##         the scene structure, the ground-truth, and the initial points, go with the "trianle"
##         below as you see in the uncommented line.
#world_points = camera.make_world_points_from_tetrahedron_generic(3)
world_points = camera.make_world_points_for_triangle()

world_points_xformed = camera.apply_transformation_to_generic_world_points(world_points, (0,0,0), (0.0,0.0,5000.0), 1.0)
print("world_points_xformed: %s" % str(world_points_xformed))

##  Move the camera to different positions first along the positive world Y-coordinate and 
##  then along the positive X-coordinate (for a total of 20 positions):
number_of_camera_positions = 0
Y_motion_delta = 0.0
all_pixels = []
for i in range(10):
    camera.translate_a_previously_initialized_camera((0.0,Y_motion_delta,0.0))
    camera.add_new_camera_to_list_of_cameras()
    pixels = camera.get_pixels_for_a_sequence_of_world_points(world_points_xformed)
    print("\n\nPixels for Y-motion camera position %d: %s" % (i, str(pixels)))
    all_pixels.append(pixels)
    number_of_camera_positions += 1
    theta_x_delta = 0.5
    y_motion_delta =  500
X_motion_delta = 500.0
for i in range(10):
    camera.translate_a_previously_initialized_camera((X_motion_delta,0.0,0.0))
    camera.add_new_camera_to_list_of_cameras()
    pixels = camera.get_pixels_for_a_sequence_of_world_points(world_points_xformed)
    print("\n\nPixels for X-motion camera position %d: %s" % (i, str(pixels)))
    all_pixels.append(pixels)
    number_of_camera_positions += 1

#  Construct the Measurement Vector X for nonlinear least squares:
print("\n\nall pixels: %s" % str(all_pixels))
print("\ntotal number of camera positions: %d" % number_of_camera_positions)
camera.construct_X_vector(all_pixels)

#  Display the camera matrix for each camera position:
all_cameras = camera.get_all_cameras()
print("\n\nDisplaying all cameras: ")
for item in all_cameras.items():
    print("\nFor camera %d" % item[0])
    print(item[1])

camera_params_dict = {}
#  Note that, generically speaking, each 3x4 camera matrix has elements that symbolically 
#  look like 'p_11', 'p_12', etc.  We need to particularize these to each of the 20 camera
#  positions.  So think of the camera matrix elements as 'p_c_11', p_c_12', 'p_c_13', etc.
#  in which 'c' can be set to the integer index associated with each camera.  So for the
#  very first camera, camera matrix elements will look like 'p_0_11', 'p_0_12', 'p_0_13',
#  'p_0_21', and so on.  In the fourth line below, we first synthesize these symbolic names 
#  for the camera matrix elements and use the synthesized names as the keys in a dictionary.  
#  The value associated with each key is the actual numerical value of that element in the 
#  corresponding camera.
print("\n\nInitialize all camera parameters: ")
for cam in all_cameras.items():
    for i in range(1,4):
        for j in range(1,5):
            camera_params_dict['p_' + str(cam[0]) + str('_') + str(i) + str(j)] = cam[1][i-1,j-1]

#  Construct the Predictor Vector Fvec for nonlinear least squares:
camera.construct_Fvec_for_calibrated_cameras(camera_params_dict)

#  Construct an ordered list of the SYMBOLIC NAMES to be used each of the coordinates for 
#  the scene points to be estimated.  This list looks like 
#  "['X_0', 'Y_0', 'Z_0', 'X_1', 'Y_1', 'Z_1', 'X_2' ......]"
params_arranged_list = camera.construct_parameter_vec_for_calibrated_cameras()
print("\nAll structure parameters: %s" % str(params_arranged_list))
print("\nNumber of all structure parameters for estimation: %d" % len(params_arranged_list))

print("\n\nInitialize all structure parameters: ")
initial_params_dict = {}
initial_params_list = []               #  need it later for displaying the results visually
for param in params_arranged_list:
    if param.startswith('X_') or param.startswith('Y_'):
        initial_params_dict[param] = float(random.randint(0,2000)*random.choice([-1,1]))
        initial_params_list.append(initial_params_dict[param])
    elif param.startswith('Z_'):
        initial_params_dict[param] = 5000.0 + float(random.randint(1,1000)*random.choice([-1,1]))
        initial_params_list.append(initial_params_dict[param])

print("\n\nParameters and their initial values: %s" % str(initial_params_dict))
camera.set_params_list(params_arranged_list)
camera.set_initial_values_for_params(initial_params_dict)
camera.set_constructor_options_for_optimizer(optimizer)     

#  Get the structure ground truth:
structure_ground_truth = camera.construct_structure_ground_truth()
print("\n\nStructure ground truth: %s" % str(structure_ground_truth))

result = camera.get_scene_structure_from_camera_motion('lm')   

######################### display the calculated structure  ########################

print("\n\n\nRESULTS RETURNED BY sfm_with_calibrated_cameras_translations_only.py")

num_iterations_used = result['number_of_iterations']                     
error_norms_with_iterations = result['error_norms_with_iterations']      
final_param_values_vector = result['parameter_values']                   
final_param_values_list = final_param_values_vector.flatten().tolist()[0]

print("\nError norms with iterations: %s" % str(error_norms_with_iterations))  
print("\nNumber of iterations used: %d" % num_iterations_used)                 
print("\nFinal values for the parameters:\n")                                  
for i in range(len(params_arranged_list)):
    if params_arranged_list[i] in structure_ground_truth:
        print("%s  =>  %s     [ground truth: %s]   (initial value: %s) \n" % (params_arranged_list[i], final_param_values_list[i], structure_ground_truth[params_arranged_list[i]], initial_params_dict[params_arranged_list[i]]))  
    else:
        print("%s  =>  %s     \n" % (params_arranged_list[i], final_param_values_list[i]))  

initial_values_supplied = []               # in the form of coordinate triples
for i in range(len(params_arranged_list) // 3):
    initial_point = (initial_params_list[i*3], initial_params_list[i*3 + 1], initial_params_list[i*3 + 2])
    initial_values_supplied.append(initial_point)

structure_points_estimated = []
for i in range(len(params_arranged_list) // 3):
    estimated_pt = (final_param_values_list[i*3], final_param_values_list[i*3 + 1], final_param_values_list[i*3 + 2])  
    structure_points_estimated.append(estimated_pt)   
print("\n\nstructure_points_estimated: %s" % str(structure_points_estimated))
print("\nThe ground truth:             %s" % str(world_points_xformed))
print("\nInitial values supplied:      %s" % str(initial_values_supplied))

camera.display_structure(structure_points_estimated, world_points_xformed, initial_values_supplied)


