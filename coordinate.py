#Tyler Robertson
#ID: 22991994

import math

class Coordinate:
    def __init__(self, frac: (float, float), absolute: (int, int), absolute_size: (int, int)):
        '''
        Initializes a Coordinate object.  The expectation is that either
        the frac parameter *or* the absolute and absolute_size parameters
        are specified, but not both.  Those that are not specified will have
        the value None.
        '''
        if frac == None:
            abs_x, abs_y = absolute
            abs_size_x, abs_size_y = absolute_size

            self.frac_x = abs_x / abs_size_x
            self.frac_y = abs_y / abs_size_y
        else:
            frac_x, frac_y = frac
            self.frac_x = frac_x
            self.frac_y = frac_y


    def frac(self) -> (float, float):
        '''
        Returns an (x, y) tuple that contains fractional coordinates
        for this Coordinate object.
        '''
        return (self.frac_x, self.frac_y)


    def absolute(self, absolute_size: (int, int)) -> (int, int):
        '''
        Returns an (x, y) tuple that contains absolute coordinates for
        this Coordinate object.  The width and height are used to make
        the appropriate conversion -- absolute coordinates change as width
        and height changes.
        '''
        abs_size_x, abs_size_y = absolute_size
        return (int(self.frac_x * abs_size_x), int(self.frac_y * abs_size_y))


    def frac_distance_from(self, c: 'Coordinate') -> float:
        '''
        Given another Coordinate object, returns the distance, in
        terms of fractional coordinates, between this Coordinate and the
        other Coordinate.
        '''

        # Per the Pythagorean theorem from mathematics, the distance
        # between two coordinates is the square root of the sum of the
        # squares of the differences in the x- and y-coordinates.
        return math.sqrt(
            (self.frac_x - c.frac_x) * (self.frac_x - c.frac_x)
            + (self.frac_y - c.frac_y) * (self.frac_y - c.frac_y))



# These two functions are used to create Coordinates that are either
# being created from fractional or absolute coordinates.  Given these
# two functions, we'll never create Coordinate objects by calling the
# Coordinate constructor; instead, we'll just call the appropriate
# of these two functions, depending on whether we have fractional or
# absolute coordinates already.

def from_frac(frac: (float, float)) -> Coordinate:
    '''Builds a Coordinate given fractional x and y coordinates.'''
    return Coordinate(frac, None)



def from_absolute(absolute: (int, int), absolute_size: (int, int)) -> Coordinate:
    '''
    Builds a Coordinate given absolute x and y coordinates, along with
    the width and height of the absolute coordinate area (necessary for
    conversion to fractional).
    '''
    return Coordinate(None, absolute, absolute_size)
