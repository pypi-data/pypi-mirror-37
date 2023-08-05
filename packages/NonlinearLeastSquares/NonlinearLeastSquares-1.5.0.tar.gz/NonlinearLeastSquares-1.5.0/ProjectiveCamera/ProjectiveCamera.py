#!/usr/bin/env python

##  ProjectiveCamera.py

##  This class is a part of Avi Kak's Python module named NonlinearLeastSquares.  The purpose of this 
##  class is to demonstrate how Nonlinear Least Squares can be used to estimate the scene structure 
##  from the motion of the camera.  That is, you move the camera to different positions (and, if 
##  desired, different orientations) and record the pixels at each position.  It is relatively easy
##  to reconstruct the scene from the pixels thus recorded --- especially if you know the camera
##  parameters.  This class simulates the camera and then transforms the pixel data recorded and 
##  the projection functionals for each camera position into a form that can be used by the main 
##  NonlinearLeastSquares class for estimating the scene structure.

import numpy                                                                    
import numpy.linalg
import scipy
import sys,os,glob
import math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#numpy.set_printoptions(precision=3,suppress=True)

def euclidean(point1, point2):
    '''
    inhomogeneous 3D coordinates expected
    '''
    distance = math.sqrt(reduce(lambda x,y: x+y, map(lambda x: x**2, [(point1[i] - point2[i]) for i in range(len(point1))])))
    return distance

class ProjectiveCamera(object):

    def __init__(self, *args, **kwargs):
        if args:
            raise ValueError(
                    '''Camera constructor can only be called with keyword arguments for the follwoing 
                       keywords: camera_type,alpha_x,alpha_y,x0,y0,camera_rotation,
                       camera_translation, partials_for_jacobian, display_needed''')
        allowed_keys = 'camera_type','alpha_x','alpha_y','x0','y0','camera_rotation','camera_translation','partials_for_jacobian','display_needed'
        keywords_used = kwargs.keys()
        for keyword in keywords_used:
            if keyword not in allowed_keys:
                raise Exception("Wrong key used in constructor call --- perhaps spelling error")
        camera_type=alpha_x=alpha_y=x0=y0=camera_rotation=camera_translation=partials_for_jacobian=display_needed=None
        if 'camera_type' in kwargs:                camera_type = kwargs.pop('camera_type')
        if 'alpha_x' in kwargs:                    alpha_x = kwargs.pop('alpha_x')
        if 'alpha_y' in kwargs:                    alpha_y = kwargs.pop('alpha_y')
        if 'x0' in kwargs:                         x0 = kwargs.pop('x0')
        if 'y0' in kwargs:                         y0 = kwargs.pop('y0')
        if 'camera_rotation' in kwargs:            camera_rotation = kwargs.pop('camera_rotation')            
        if 'camera_translation' in kwargs:         camera_translation = kwargs.pop('camera_translation')
        if kwargs: 
            raise ValueError("You have used unrecognized keyword for supplying constructor arguments") 
        if camera_type is not None and camera_type in ('scaled_orthographic', 'finite_projective'): 
            self.camera_type = camera_type
        else:
            raise ValueError("""You must specify the camera type and it must be either """
                             """'scaled_orthographic' or 'finite_projective'""") 
        if alpha_x is not None:
            self.alpha_x = alpha_x
        else:
            self.alpha_x = 1.0
        if alpha_y is not None:
            self.alpha_y = alpha_y
        else:
            self.alpha_y = 1.0
        if x0 is not None:
            self.x0 = x0
        else:
            self.x0 = 0.0
        if y0 is not None:
            self.y0 = y0
        else:
            self.y0 = 0.0
        if camera_rotation is not None:
            self.camera_rotation = camera_rotation
        else:
            self.camera_rotation = numpy.asmatrix(numpy.diag([1.0, 1.0, 1.0]))
        if camera_translation is not None:
            self.camera_translation = camera_translation
        else:
            self.camera_translation = numpy.matrix([0.0, 0.0, 0.0])
        self.partials_for_jacobian = partials_for_jacobian
        self.display_needed = display_needed if display_needed is not None else False
        self.num_measurements = None
        self.list_of_cameras = {}   # A 'camera' means a "camera position'. The keys of the dict enumerate the positions
        self.debug = True

    def initialize(self):
        # Camera intrinsic param matrix:
        self.K = numpy.matrix([[self.alpha_x, 0, self.x0], [0, self.alpha_y, self.y0], [0, 0, 1.0]])
        self.K_inverse = self.K.I
        print("\nThe K matrix:\n")
        print(self.K)
        print("\nThe inverse of the K matrix:\n")
        print(self.K_inverse)
        # Camera matrix:
        self.P = self.K * numpy.append(self.camera_rotation, self.camera_translation.T, 1)
        print("Camera matrix P produced by the initializer:")
        print(self.P)

    def print_camera_matrix(self):
        print("\nCamera matrix: %s\n" % str(self.P))

    def get_pixel_for_world_point(self, world_point):
        '''
        World point expected in homogeneous coordinates as a 4-item list
        '''
        world_point_as_one_row_matrix = numpy.matrix(world_point)
        xvec = self.P * world_point_as_one_row_matrix.T
        xvec = xvec.T
        x_aslist = xvec[0,:].tolist()[0]
        x,y = int(x_aslist[0]/x_aslist[2]), int(x_aslist[1]/x_aslist[2])
        print("\nworld point: %s" % str(world_point))
        print("pixels: %s" % str((x,y)))
        return x,y

    def get_pixels_for_a_sequence_of_world_points(self, world_points):
        '''
        Each item in the list of world_points needs to be a 4-item list for the
        homegeneous coords of the point in question
        '''
        image_pixels = []
        for point in world_points:
            pixel = self.get_pixel_for_world_point(point)
            image_pixels.append(pixel)
        return image_pixels

    def rotate_previously_initialized_camera_around_world_X_axis(self, theta):
        '''
        We use the (roll,pitch,yaw) convention for describing the camera rotation, with the 
        rotation around the world X-axis as the roll, around the Y-axis as the pitch, and
        around the Z-axis as the yaw. The rotation angle theta needs to be in degrees.     
        '''
        cos_theta =  scipy.cos( theta * scipy.pi / 180 )                                        
        sin_theta =  scipy.sin( theta * scipy.pi / 180 )         
#        rot_X = numpy.matrix([[1.0,0.0,0.0],[0.0,cos_theta,-sin_theta],[0.0,sin_theta,cos_theta]])
        rot_X = numpy.matrix([[1.0,0.0,0.0],[0.0,cos_theta,sin_theta],[0.0,-sin_theta,cos_theta]])
        left_3by3 =  self.P[0:3,0:3]
        last_col   = self.P[:,3]
        new_left_3by3 = left_3by3 * rot_X
        self.P = numpy.append(new_left_3by3, last_col, 1)

    def rotate_previously_initialized_camera_around_world_Y_axis(self, theta):
        '''
        We use the (roll,pitch,yaw) convention for describing the camera rotation, with the 
        rotation around the world X-axis as the roll, around the Y-axis as the pitch, and
        around the Z-axis as the yaw. The rotation angle theta needs to be in degrees.     
        '''
        cos_theta =  scipy.cos( theta * scipy.pi / 180 )                                        
        sin_theta =  scipy.sin( theta * scipy.pi / 180 )         
#        rot_Y = numpy.matrix([[cos_theta,0.0,sin_theta],[0.0,1.0,0.0],[-sin_theta,0.0,cos_theta]])
        rot_Y = numpy.matrix([[cos_theta,0.0,-sin_theta],[0.0,1.0,0.0],[sin_theta,0.0,cos_theta]])
        left_3by3 =  self.P[0:3,0:3]
        last_col   = self.P[:,3]
        new_left_3by3 =  left_3by3 * rot_Y
        self.P = numpy.append(new_left_3by3, last_col, 1)

    def translate_a_previously_initialized_camera(self, translation):
        '''
        The parameter 'translation' is a 3-element list, with the first element indicating the
        translation along X, the second along Y, and the third along Z.
        '''
        left_3by3 = self.P[0:3,0:3]
        last_column   =  self.P[:,3]
        new_last_column = -1.0 * left_3by3 * numpy.asmatrix(translation).T
        new_last_column += last_column
        self.P = numpy.append(left_3by3, new_last_column, 1)

    def add_new_camera_to_list_of_cameras(self):
        how_many_already = len(self.list_of_cameras)
        self.list_of_cameras[how_many_already] = self.P

    def get_all_cameras(self):
        return self.list_of_cameras

    def set_3D_generic_transform_for_3D_scene_objects(self):
        rot3D = numpy.matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])    
        trans3D = numpy.matrix([0.0,0.0,0.0])
        transform = numpy.append(rot3D, trans3D.T, 1)
        self.scene_transform_3D = numpy.append(transform, [[0,0,0,1]], 0)

    def pixels_on_a_line_between_two_image_points(self, line, N):
        '''
        The parameter `line' is a tuple of two points (point1, point2) where the
        points point1 and point2 are expected to be in homogeneous coordinates.  That
        is, each is a triple.  Returns N points between the two given points.
        '''
        pixels = []
        point1,point2 = line
        x_span = point2[0] - point1[0]
        y_span = point2[1] - point1[1]     
        w_span = point2[2] - point1[2]     
        del_x = x_span / (N + 1)
        del_y = y_span / (N + 1)
        del_w = w_span / (N + 1)
        for i in range(1,N+1):
            pixels.append( [point1[0] + i*del_x, point1[1] + i*del_y, point1[2] + i*del_w] ) 
        return pixels

    def points_on_a_line_between_two_world_points(self, line, N, world_points):
        '''
        The parameter `line' is a tuple of two world points (point1, point2) in HOMOGENEOUS
        COORDINATES.  That is, each point is a 4-vector.  Returns N points between the two 
        given points, INCLUDING THE END POINTS.
        '''
        point1,point2 = line
        x_span = point2[0] - point1[0]
        y_span = point2[1] - point1[1]     
        z_span = point2[2] - point1[2]     
        w_span = point2[3] - point1[3]     
        del_x = x_span / N
        del_y = y_span / N
        del_z = z_span / N
        for i in range(N+1):
            new_point = [point1[0] + i*del_x, point1[1] + i*del_y, point1[2] + i*del_z, 1]
            if not self.is_point_in_a_list_of_points(new_point, world_points):
                world_points.append( new_point )
        return world_points

    def is_point_in_a_list_of_points(self, point, list_of_points):
        x,y,z,w = point
        xx,yy,zz = x/w,y/w,z/w
        for pt in list_of_points:
            xxx,yyy,zzz,www = pt
            xxxx,yyyy,zzzz = xxx/www,yyy/www,zzz/www 
            if (abs(xx-xxxx) < 0.5) & (abs(yy-yyyy) < 0.5) & (abs(zz-zzzz) < 0.5):
                return True
            else:
                continue
        return False

    def make_world_points_from_tetrahedron_generic(self, points_per_line):
        '''
        The 'points_per_line' is the number of points you want on each edge of the tetra
        '''
        xz_point1 = (100,0,0,1)
        xz_point2 = (200,0,200,1)
        xz_point3 = (300,0,0,1)       
        xz_point4 = (200,0,-200,1)       
        y_apex_1  = (200,200,0,1)
        lines = []
        # base of the tetrahedron:
        line1 = (xz_point1, xz_point2)
        line2 = (xz_point2, xz_point3)
        line3 = (xz_point3, xz_point4)
        line4 = (xz_point4, xz_point1)
        lines += [line1,line2,line3,line4]
        # lines from the apex to the base corners:
        line5 = (xz_point1, y_apex_1)
        line6 = (xz_point2, y_apex_1)
        line7 = (xz_point3, y_apex_1)
        line8 = (xz_point4, y_apex_1)
        lines += [line5,line6,line7,line8]
        world_points = []
        for line in lines:
            world_points = self.points_on_a_line_between_two_world_points(line,points_per_line - 1, world_points)
        print("\nworld points: %s" % str(world_points))
        print("\nnumber of world points: %d" % len(world_points))
        self.num_of_world_points = len(world_points)
        self.world_points = world_points
        return world_points

    def make_world_points_for_triangle(self):
        xy_point1 = (3000.0,3000.0,0.0,1.0)
        xy_point2 = (4000.0,3000.0,0.0,1.0)
        xy_point3 = (4000.0,5000.0,0.0,1.0)       
        world_points = [xy_point1, xy_point2, xy_point3]
        print("\nworld points: %s" % str(world_points))
        print("\nnumber of world points: %d" % len(world_points))
        self.num_of_world_points = len(world_points)
        self.world_points = world_points
        return world_points

    def apply_transformation_to_generic_world_points(self, points, rotation, translation, scale):
        '''
        The parameter 'rotation' is a triple of rotation angles in degrees around the world X-axis, the 
        world Y-axis and the world Z-axis, respectively.  The parameter 'translation' is a triple of real 
        numbers that are the translations of the object along the world-X, the translation along world-Y, 
        and the translation along the world-Z.  IMPORTANT:  When an object undergoes these rotations, 
        it is important to realize that they are NOT with respect to a local coordinate frame centered
        on the object.  On the other hand, they are with respect to the world frame. Say that is an
        object point on the positive side of the world-Z axis.  When you rotate this object through 
        90 degrees with respect to the world-Y axis, that point will move to a location on the positive
        world-X axis.
        '''
        (rotx,roty,rotz) = rotation
        (tx,ty,tz) = translation
        (scx, scy, scz) = (scale, scale, scale)
        self.set_3D_generic_transform_for_3D_scene_objects()
        self._rotate_3D_scene_around_world_X_axis(rotx)
        self._rotate_3D_scene_around_world_Y_axis(roty)
        self._rotate_3D_scene_around_world_Z_axis(rotz)
        self._translate_3D_scene(translation)
        print("\n3D transform for the object:\n")
        print(self.scene_transform_3D)
        self._scale_3D_scene(scale)
        world_points_xformed_homogeneous = []
        for point in points:
            world_points_xformed_homogeneous.append(self.scene_transform_3D * numpy.matrix(point).T)
        world_points_xformed = []
        for pt in world_points_xformed_homogeneous:
            world_points_xformed.append( pt[:,0].flatten().tolist()[0] )
        print("\nworld points transformed: %s" % str(world_points_xformed))
        self.world_points_xformed = world_points_xformed
        return world_points_xformed

    # inhomogeneous coordinates
    def calculate_structure_distances(self, structure):
        distances = self.calculate_distances_from_one_3D_point_to_others(structure[0], structure[1:], [])
        return sorted(distances)

    # inhomogeneous coordinates
    def calculate_distances_from_one_3D_point_to_others(self, point, list_of_points, distances):
        if len(list_of_points) == 0: return distances 
        for i in range(len(list_of_points)):
            distances.append(euclidean(point, list_of_points[i]))
        self.calculate_distances_from_one_3D_point_to_others(list_of_points[0], list_of_points[1:], distances)
        return distances                        

    def display_structure(self, scene_structure, ground_truth, initial_values):
        '''
        Each of the three parameters is a list of coordinate triples in World 3D.  The first parameter
        is for the coordinate triples for the estimated scene structure, the second list for the ground 
        truth, and the third for the initial guesses supplied.  The third parameter stands for the point 
        in parameter hyperplane for starting the downhill path to the optimum solution for the scene
        structure.
        '''
        XM = [point[0] for point in scene_structure]
        YM = [point[1] for point in scene_structure]
        ZM = [point[2] for point in scene_structure]
        XM.append(XM[0])
        YM.append(YM[0])
        ZM.append(ZM[0])
        XG = [point[0] for point in ground_truth]
        YG = [point[1] for point in ground_truth]
        ZG = [point[2] for point in ground_truth]
        XG.append(XG[0])
        YG.append(YG[0])
        ZG.append(ZG[0])
        XI = [point[0] for point in initial_values]
        YI = [point[1] for point in initial_values]
        ZI = [point[2] for point in initial_values]
        XI.append(XI[0])
        YI.append(YI[0])
        ZI.append(ZI[0])
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.plot(XM,YM,ZM, 'xb-', label='estimated structure')
        ax.plot(XG,YG,ZG, 'xr-', label='ground truth')
        ax.plot(XI,YI,ZI, 'xm-', label='initial guess')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.show()


    #####################   package the objects needed by the NonlinearLeastSquares class   ####################
 
    def construct_X_vector(self, pixel_coordinates):
        '''
        The function parameter 'pixel_coordinates' is a list of lists (LoL), with each list in LoL being 
        the set of pixels recorded from one position and orientation of the camera.
        '''
        #  Since 'pixel_coordinates' is a LIST OF LISTS, with each list being for one camera pos, 
        #  we can say:
        self.num_of_camera_positions = len(pixel_coordinates)   
        print("\nnumber of camera positions: %d" % self.num_of_camera_positions)        
        X = []
        for pixels_for_one_camera_pos in pixel_coordinates:      
            for pixel in pixels_for_one_camera_pos:
                X += pixel
        self.X_size = len(X)
        self.num_measurements = len(X)
        self.X = numpy.matrix(X).T

    def construct_structure_ground_truth(self):
        structure_ground_truth_dict = {}
        for (i,point) in enumerate(self.world_points_xformed):
            X,Y,Z,W = point
            var1, var2, var3 = 'X_' + str(i), 'Y_' + str(i), 'Z_' + str(i)
            structure_ground_truth_dict[var1] = float(X) / W
            structure_ground_truth_dict[var2] = float(Y) / W
            structure_ground_truth_dict[var3] = float(Z) / W
        self.structure_ground_truth_dict = structure_ground_truth_dict
        return structure_ground_truth_dict

    def construct_Fvec(self):
        ''' 
        This method constructs the Prediction Vector for the observed data in "self.X". This is a vector 
        of the same size as the number of measurements in "self.X". The elements of the Prediction Vector 
        are functional involving the parameters to be estimated.
        '''
        functional_x =  '(p_c_11*X_ + p_c_12*Y_ + p_c_13*Z_ + p_c_14) / (p_c_31*X_ + p_c_32*Y_ + p_c_33*Z_ + p_c_34)' 
        functional_y =  '(p_c_21*X_ + p_c_22*Y_ + p_c_23*Z_ + p_c_24) / (p_c_31*X_ + p_c_32*Y_ + p_c_33*Z_ + p_c_34)' 
        Fvec = []
        for i in range(self.num_of_camera_positions):
            functional_x_for_cam = str.replace( functional_x, 'c', str(i) )
            functional_y_for_cam = str.replace( functional_y, 'c', str(i) )
            for j in range(self.num_of_world_points):
                tempx = str.replace( functional_x_for_cam, 'X_', 'X_' + str(j))
                tempx = str.replace( tempx, 'Y_', 'Y_' + str(j))
                tempx = str.replace( tempx, 'Z_', 'Z_' + str(j))
                Fvec.append( tempx )
                tempy = str.replace( functional_y_for_cam, 'X_', 'X_' + str(j))
                tempy = str.replace( tempy, 'Y_', 'Y_' + str(j))
                tempy = str.replace( tempy, 'Z_', 'Z_' + str(j))
                Fvec.append( tempy )
        self.Fvec = numpy.matrix(Fvec).T
        print("\n\nprinting Fvec:")
        print(self.Fvec)
        return self.Fvec

    def construct_Fvec_for_calibrated_cameras(self, camera_params_dict):
        ''' 
        This method constructs the Prediction Vector for the observed data in "self.X". This is a vector 
        of the same size as the number of measurements in "self.X". The elements of the Prediction Vector 
        are functional involving the parameters to be estimated.
        '''
        functional_x =  '(p_c_11*X_ + p_c_12*Y_ + p_c_13*Z_ + p_c_14) / (p_c_31*X_ + p_c_32*Y_ + p_c_33*Z_ + p_c_34)' 
        functional_y =  '(p_c_21*X_ + p_c_22*Y_ + p_c_23*Z_ + p_c_24) / (p_c_31*X_ + p_c_32*Y_ + p_c_33*Z_ + p_c_34)' 
        Fvec = []
        for i in range(self.num_of_camera_positions):
            functional_x_for_cam = str.replace( functional_x, 'c', str(i) )
            functional_y_for_cam = str.replace( functional_y, 'c', str(i) )
            for j in range(self.num_of_world_points):
                tempx = str.replace( functional_x_for_cam, 'X_', 'X_' + str(j))
                tempx = str.replace( tempx, 'Y_', 'Y_' + str(j))
                tempx = str.replace( tempx, 'Z_', 'Z_' + str(j))
                Fvec.append( tempx )
                tempy = str.replace( functional_y_for_cam, 'X_', 'X_' + str(j))
                tempy = str.replace( tempy, 'Y_', 'Y_' + str(j))
                tempy = str.replace( tempy, 'Z_', 'Z_' + str(j))
                Fvec.append( tempy )

        for i in range(len(Fvec)):
            for param in camera_params_dict:
                Fvec[i] = str.replace( Fvec[i], param, str(camera_params_dict[param]) )

        self.Fvec = numpy.matrix(Fvec).T
        print("\n\nprinting Fvec:")
        print(self.Fvec)
        return self.Fvec

    def construct_parameter_vec(self):
        params_camera_template = 'p_c_11,p_c_12,p_c_13,p_c_14,p_c_21,p_c_22,p_c_23,p_c_24,p_c_31,p_c_32,p_c_33,p_c_34'
        for i in range(self.num_of_camera_positions):
            if i == 0:
                camera_params_str =  str.replace(params_camera_template, 'c', str(i))
            else:
                camera_params_str += ',' + str.replace(params_camera_template, 'c', str(i))
        camera_params_list = camera_params_str.split(',')
        structure_params_template = 'X_k,Y_k,Z_k'
        for j in range(self.num_of_world_points):
            if j == 0:
                structure_params_str = str.replace(structure_params_template, 'k', str(j))
            else:
                structure_params_str += ',' + str.replace(structure_params_template, 'k', str(j))
        structure_params_list = structure_params_str.split(',')
        all_params_list = camera_params_list + structure_params_list
        self.initial_params_list = all_params_list
        print("\ncamera params list: %s" % str(all_params_list))
        self.p  =  numpy.matrix(all_params_list).T
        print(self.p)
        return all_params_list

    def construct_parameter_vec_for_calibrated_cameras(self):
        '''
         Call this function only for the case when you estimating the structure using calibrated params
        '''
        structure_params_template = 'X_k,Y_k,Z_k'
        for j in range(self.num_of_world_points):
            if j == 0:
                structure_params_str = str.replace(structure_params_template, 'k', str(j))
            else:
                structure_params_str += ',' + str.replace(structure_params_template, 'k', str(j))
        structure_params_list = structure_params_str.split(',')
        self.initial_params_list = structure_params_list
        print("\nstructure params list: %s" % str(structure_params_list))
        self.p  =  numpy.matrix(structure_params_list).T
        print("\n\ndisplaying the parameter vector:")
        print( self.p)
        return structure_params_list

    def set_params_list(self, params_list_arranged):
        self.params_list_arranged = params_list_arranged

    def set_initial_values_for_params(self, initial_params_dict):
        self.initial_params_dict = initial_params_dict

    def set_constructor_options_for_optimizer(self, algo):
        '''
        This method conveys the following information from an instance of ProjectiveCamera to an 
        instance of NonlinearLeastSquares:
            1)  The measurement vector X.
            2)  The initial values to be used for the parameters of the scene structure.
            3)  The Fvec vector, which is a vector of the predicted values, all in functional 
                form, for each of the data elements in the measurement vector X.
            4)  The display function to be used for plotting the partial and the final results if
                such results can be displayed in the form of a 2D or 3D graphic with Python's 
                matplotlib library.
            5)  and some additional book-keeping information.
        '''
        self.optimizer = algo
        algo.set_X(self.X)
        algo.set_params_arranged_list(self.params_list_arranged)
        algo.set_initial_params(self.initial_params_dict)
        if self.partials_for_jacobian:
            algo.set_jacobian_functionals_array(self.construct_jacobian_array_in_functional_form())
        algo.set_Fvec(self.Fvec)
        if self.display_needed:
            algo.set_display_function(self.display_function)
        algo.set_num_measurements(self.num_measurements)
        algo.set_num_parameters(len(self.params_list_arranged))
        algo.set_debug(self.debug)

    def get_scene_structure_from_camera_motion(self, algo):
        if algo == 'lm':
            result_dict = self.optimizer.leven_marq()
        elif algo == 'gd':
            result_dict = self.optimizer.grad_descent()
        return result_dict

    ##################    Private Methods of the Projective Camera Class     ##################

    def _rotate_3D_scene_around_world_X_axis(self, theta):
        '''
        This rotation through theta is around the world-X axis with respect to the world origin. 
        Think of an object point on the world-Z axis.  If you rotate that object through, say, 
        90 degrees with this method, the object point in question will move to somewhere on the
        world-X axis.  The rotation angle theta must be in degrees
        '''
        cos_theta =  scipy.cos( theta * scipy.pi / 180 )                                        
        sin_theta =  scipy.sin( theta * scipy.pi / 180 )         
        rot_X = numpy.matrix([[1.0,0.0,0.0],[0.0,cos_theta,-sin_theta],[0.0,sin_theta,cos_theta]])
        rot_X = numpy.append(rot_X, numpy.matrix([[0,0,0]]).T, 1)
        rot_X = numpy.append(rot_X, [[0,0,0,1]], 0)
        self.scene_transform_3D = self.scene_transform_3D * rot_X

    def _rotate_3D_scene_around_world_Y_axis(self, theta):
        '''
        This rotation through theta is around the world-Y axis with respect to the world origin. 
        The rotation angle theta must be in degrees
        '''
        cos_theta =  scipy.cos( theta * scipy.pi / 180 )                                        
        sin_theta =  scipy.sin( theta * scipy.pi / 180 )         
        rot_Y = numpy.matrix([[cos_theta,0.0,sin_theta],[0.0, 1.0, 0.0],[-sin_theta,0.0,cos_theta]])
        rot_Y = numpy.append(rot_Y, numpy.matrix([[0,0,0]]).T, 1)
        rot_Y = numpy.append(rot_Y, [[0,0,0,1]], 0)
        self.scene_transform_3D = rot_Y * self.scene_transform_3D

    def _rotate_3D_scene_around_world_Z_axis(self, theta):
        '''
        This rotation through theta is around the world-Z axis with respect to the world origin. 
        The rotation angle theta must be in degrees
        '''
        cos_theta =  scipy.cos( theta * scipy.pi / 180 )                                        
        sin_theta =  scipy.sin( theta * scipy.pi / 180 )         
        rot_Z = numpy.matrix([[cos_theta,-sin_theta,0.0],[sin_theta,cos_theta,0.0],[0.0,0.0,1.0]])
        rot_Z = numpy.append(rot_Z, numpy.matrix([[0,0,0]]).T, 1)
        rot_Z = numpy.append(rot_Z, [[0,0,0,1]], 0)
        self.scene_transform_3D = rot_Z * self.scene_transform_3D

    def _translate_3D_scene(self, translation):
        '''
        If you also need to rotate the object, you are likely to want to rotate the
        object at the origin before applying the translation transform: The argument
        `translation' must be a list of 3 numbers, indicating the translation vector
        '''
        rot3D = numpy.matrix([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])    
        trans3D = numpy.matrix(translation)
        transform = numpy.append(rot3D, trans3D.T, 1)
        transform = numpy.append(transform, [[0,0,0,1]], 0)
        self.scene_transform_3D = transform * self.scene_transform_3D

    def _scale_3D_scene(self, scale):
        if scale == 1.0: return
        left_upper_3by3 = self.scene_transform_3D[0:3,0:3]
        scale_diag = numpy.diag([scale,scale,scale])
        scale_as_matrix = numpy.asmatrix(scale_diag)
        new_left_upper_3by3  =  scale_as_matrix * left_upper_3by3
        new_upper_3by4  =  numpy.append(new_left_upper_3by3, self.scene_transform_3D[0:3,3], 1)
        new_scaled_xform =  numpy.append(new_upper_3by4, [[0,0,0,1]], 0)
        self.scene_transform_3D  = new_scaled_xform
