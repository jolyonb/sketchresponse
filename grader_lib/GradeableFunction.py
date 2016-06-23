import MultipleSplinesFunction
import SplineFunction
import Point
import Axis
import numpy as np

class GradeableFunction(MultipleSplinesFunction.MultipleSplinesFunction):
    """GradeableFunction."""
    def __init__(self, gradeable, tolerance = dict()):
        f = gradeable
        xaxis = Axis.Axis(f.params['xrange'], f.params['width'])
        yaxis = Axis.Axis(f.params['yrange'][::-1], f.params['height'])
        MultipleSplinesFunction.MultipleSplinesFunction.__init__(self, xaxis, yaxis, path_info = f, tolerance = tolerance)
        self.set_default_tolerance('point_distance_squared', 400) # threshold for finding a point close to a point
        self.set_default_tolerance('point_distance', 20) # threshold for finding a point close to an x value

    def create_from_path_info(self, path_info):
        dtol = 100 # work into tolerances later
        self.functions = []
        self.points = []
        xvals = []
        for i in range(len(path_info)):
            if 'spline' in path_info[i]:
                spline = SplineFunction.SplineFunction(self.xaxis, self.yaxis, path_info[i]['spline'])
                self.functions.append(spline)
                xvals += spline.get_domain()
                self.domain = [np.min(xvals), np.max(xvals)]
            if 'point' in path_info[i]:
                [px_x, px_y] = path_info[i]['point']
                point = Point.Point(self, px_x, px_y)
                d, p = self.closest_point_to_point(point)
                if d >= dtol:
                    self.points.append(point)



## for Points ##

    # returns the distance (squared) and the point
    def closest_point_to_point(self, point):
        """Return the square pixel distance to the closest point and a Point instance.

        Args:
            point: a Point instance
        Returns:
            float, Point: 
            minDistanceSquared: the square of the pixel distance between point
                                and the closest point, or float('inf') if no
                                point exists.
            minPoint: the closest Point to x, or None if no point exists.
        """
        minDistanceSquared = float('inf')
        minPoint = None
        for p in self.points:
            d = p.get_px_distance_squared(point)
            if d < minDistanceSquared:
                minDistanceSquared = d
                minPoint = p

        return minDistanceSquared, minPoint

    # returns the distance and the point
    def closest_point_to_x(self, x):
        """Return the distance to the closest point and a Point instance.

        Args:
            x: a value in the range of the x axis.
        Returns:
            float, Point:
            minDistance: the absolute distance between x and the point, or
                         float('inf') if no point exists.
            minPoint: the closest Point to x, or None if no point exists.
        """
        minDistance = float('inf')
        minPoint = None
        for p in self.points:
            d = p.get_x_distance(x)
            if d < minDistance:
                minDistance = d
                minPoint = p

        return minDistance, minPoint

    # returns None if no point is close enough
    def get_point_at(self, point = False, x = False, y = False):
        """ Return a reference to the Point declared at the given value.

        Args:
            point(default: False): a Point instance at the value of interest.
            x(default: False): the x coordinate of interest.
            y(default: False): the y coordinate of interest.

        Note:    
           There are three use cases:
              1) point not False: use the Point instance as the target to locate a point in the function.
              2) x and y not False: use (x, y) as the target to locate a point in the function.
              3) x not False: use only the x coordinate to locate a point in the function, returning the first Point with the given x value.
        Returns:
            Point: 
            the first Point instance within tolerances of the given arguments, or None
        """
        if point is not False:
            distanceSquared, foundPoint = self.closest_point_to_point(point)
            if distanceSquared < self.tolerance['point_distance_squared']:
                return foundPoint

        if y is not False and x is not False:
            point = Point.Point(self, x, y, pixel = False)
            return self.get_point_at(point = point)

        if x is not False:
            distance, foundPoint = self.closest_point_to_x(x)
            if distance < self.tolerance['point_distance'] / self.xscale:
                return foundPoint

        return None

    def has_point_at(self, **kwargs):
        """ Return whether a point is declared at the given value.

        Args:
            point(default: False): a Point instance at the value of interest.
            x(default: False): the x coordinate of interest.
            y(default: False): the y coordinate of interest.

        Note:    
           There are three use cases:
              1) point not False: use the Point instance as the target to locate a point in the function.
              2) x and y not False: use (x, y) as the target to locate a point in the function.
              3) x not False: use only the x coordinate to locate a point in the function, returning the first Point with the given x value.
        Returns:
            bool:
            true if there is a Point declared within tolerances of the given
            argument(s), false otherwise.
        """
        return self.get_point_at(**kwargs) is not None

    def get_number_of_points(self):
        """Return the number of points declared in the function."""
        return len(self.points)