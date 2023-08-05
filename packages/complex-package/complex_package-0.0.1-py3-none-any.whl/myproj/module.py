import math
class ComplexClass():

    ''' Create complex number objects 
    
    METHODS
    =======
    - magnitude: return magnitude of complex number
    - angle: return angle of complex number
    - conjugate: return conjugate of complex number

    INSTANCE VARIABLES
    =======
    - real: real part of complex number
    - imaginary: imaginary part of complex number

    '''

    def __init__(self, a, b):
        self.real = a
        self.imaginary = b
        
    @classmethod
    def make_complex(cls, a, b):
        return cls(a, b)
        
    def __repr__(self):
        class_name = type(self).__name__
        return "%s(real=%r, imaginary=%r)" % (class_name, self.real, self.imaginary)
        
    def __eq__(self, other):
        return (self.real == other.real) and (self.imaginary == other.imaginary)

    def __add__(self,other):
        return make_complex(self.real + other.real, self.imaginary + other.imaginary)

    def __radd__(self,other):
        return make_complex(self.real + other.real, self.imaginary + other.imaginary)


    def magnitude(self):

        ''' Returns the magnitude of the instance of the complex class. This is a method on the class.

        INPUTS
        =======
        
        RETURNS
        ========
        Magnitude of the complex class instance
        
        NOTES
        =====
        PRE: 
             - Instance of a complex class
             
        POST:
             - return magnitude of the complex number

        EXAMPLES
        =========
        >>> z = ComplexClass.make_complex(1,2)
        >>> z.magnitude()
        2.23606797749979

        '''

        mag = (self.real**2 + self.imaginary**2)**(1/2)
        return mag


    def angle(self):

        ''' Returns the angle of the instance of the complex class. This is a method on the class.

        INPUTS
        =======
        
        RETURNS
        ========
        Angle of the complex class instance
        
        NOTES
        =====
        PRE: 
             - instance of a complex class
             
        POST:
             - return angle of the complex number

        EXAMPLES
        =========
        >>> z = ComplexClass.make_complex(1,2)
        >>> z.magnitude()
        2.23606797749979
        '''

        ang = math.atan(self.imaginary/self.real)
        return ang

    def conjugate(self):
        ''' Returns the conjugate of the complex class instance as a tuple. This is a method on the class.

        INPUTS
        =======
        
        RETURNS
        ========
        Conjugate of the complex class instance as another complex class instance
        
        NOTES
        =====
        PRE: 
             - instance of a complex class
             
        POST:
             - return conjugate of the complex number

        EXAMPLES
        =========
        >>> z = ComplexClass.make_complex(1,2)
        >>> z.conjugate()
        (1, -2)
        '''
        
        return (self.real, -self.imaginary)

import doctest
doctest.testmod(verbose=True)

if __name__ == "__main__":

    x = ComplexClass.make_complex(1,2)
    print(x.magnitude())
    print(x.angle())
    print(x.conjugate())
