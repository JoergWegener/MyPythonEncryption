#
#
#
from MatrixPoint import MatrixPoint

MATRIXDIM = 6

class EncryptionMatrix:
    
    def __init__(self, passphrase):
        # Constructor Logic
        charsForMatrixInsertion = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.encryptionString = passphrase
        
        for c in passphrase:
            # Delete the characters that are already contained in the passphrase
            charsForMatrixInsertion = charsForMatrixInsertion.replace(c, '')
        
        self.encryptionString += charsForMatrixInsertion
        
    # Return a character in the matrix identified by a Matrixpoint
    def getChar(self, point):
        global MATRIXDIM
        return self.encryptionString[int(point.y) * int(MATRIXDIM) + int(point.x)]
    
    
    # Main method of the class
    def convertText(self, inputText, direction):
        
        global MATRIXDIM
        outputText = ''
        
        for i in range(int(len(inputText) / 2)):
            
            c1 = inputText[i * 2]
            c2 = inputText[(i * 2) + 1]

            point1 = self.findPosition(c1)
            point2 = self.findPosition(c2)
            
            outputText += self.createTargetCharPair(point1, point2, direction)
            
            # If there is an uneven number of chars, the last one is moved
            # down / up one square
            if ((len(inputText) % 2) == 1):
                c = inputText[-1]
                point = self.findPosition(c)
                newPoint = MatrixPoint(point.x, ( point.y + direction + MATRIXDIM ) % MATRIXDIM)
                outputText += self.getChar( newPoint)
        
        return outputText
            
        
    # Helper method that returns a string of 2 chars for the clear chars provided.
    # This result has to be added to the encrypted / decrypted string.
    def createTargetCharPair (self, point1, point2, direction):
        global MATRIXDIM
        result = '' #This will contain the new string
        # Determine the relative position of the 2 characters
        if ((point1.x != point2.x) and (point1.y != point2.y)):
            # Both axes are different. Swap horizontally
            result += self.getChar(MatrixPoint( point2.x, point1.y)) # move c1 horizontally
            result += self.getChar(MatrixPoint( point1.x, point2.y)) # move c2 horizontally
        elif (point1.x == point2.x) and (point1.y != point2.y): 
            # On the same X axis. Move both chars down / up one space; roll over if needed
            result += self.getChar(MatrixPoint(point1.x, (point1.y + direction + MATRIXDIM) % MATRIXDIM))
            result += self.getChar(MatrixPoint(point2.x, (point2.y + direction + MATRIXDIM) % MATRIXDIM))
        elif (point1.x != point2.x) and (point1.y == point2.y):
            # On the same Y axis. Move right / left one space; roll over if needed
            result += self.getChar(MatrixPoint( ((point1.x + direction + MATRIXDIM) % MATRIXDIM), point1.y))
            result += self.getChar(MatrixPoint( ((point2.x + direction + MATRIXDIM) % MATRIXDIM), point2.y))
        elif ((point1.x == point2.x) and (point1.y == point2.y)):
            # Identical characters: move both one space down / up, roll over if needed
            result += self.getChar(MatrixPoint(point1.x, (point1.y + direction + MATRIXDIM) % MATRIXDIM))
            result += self.getChar(MatrixPoint(point2.x, (point2.y + direction + MATRIXDIM) % MATRIXDIM))
        else:
            # SHIT this is not supposed to happen!
            pass
    
        return result
    
    
    # Helper method determines the MatrixPoint of a char.
    def findPosition (self, c):
        global MATRIXDIM
        
        position = self.encryptionString.index(c)
        return MatrixPoint(x = 0, y = 0, count = position, matrixDimension = MATRIXDIM)
    
    
    # For testing purposes only!
    def printMatrix (self):
        for y in range(MATRIXDIM):
            print(self.encryptionString[(y * MATRIXDIM): (y * MATRIXDIM + MATRIXDIM )] )





if __name__ == '__main__':
    # tests go here
    pass