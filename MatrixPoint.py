# A point in a matrix, with x and y coordinates

class MatrixPoint:
    
    def __init__(self, x, y, count = 0, matrixDimension = 0):
        
        # In Java we have 2 constructors; here we need to enforce
        # the different behaviors with named variables in the
        # constructor code. Not nice, but hey... 
        if (count == 0 and matrixDimension == 0):
            self.x = x
            self.y = y
        else:
            self.x = count % matrixDimension
            self.y = count / matrixDimension
        