#
#
#
import MatrixPoint


class EncryptionMain:
    
    def __init__(self, passphrase):
        # Constructor Logic
        self.MATRIXDIM = 6 # We work on a 6x6 matrix
        charsForMatrixInsertion = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        self.encryptionString = passphrase
        
        for c in passphrase:
            # Delete the characters that are already contained in the passphrase
            charsForMatrixInsertion.replace(c, '')
        
        self.encryptionString += charsForMatrixInsertion
        
    # Return a character in the matrix identified by a Matrixpoint
    def getChar(self, point):
        return self.encryptionString[point.y * self.MATRIXDIM + point.x]
    
    
    # Main method of the class
    def convertText(self, inputText, direction):
        outputText = ''
        
        for i in range(inputText.length() / 2):
            c1 = inputText[i * 2]
            c2 = inputText[(i * 2) + 1]
            
            point1 = self.findPosition(c1)
            point2 = self.findPosition(c2)
            
            outputText += self.createTargetCharPair(point1, point2, direction)
            
            # If there is an uneven number of chars, the last one is moved
            # down / up one square
            if ((inputText.length() % 2) == 1):
                c = inputText[inputText.length() - 1]
                point = self.findPosition(c)
                newPoint = MatrixPoint(point.x, ( point.y + direction.dirInd + self.MATRIXDIM ) % self.MATRIXDIM);
                outputText += self.getChar( newPoint)
        
            
            return outputText
            
        





if __name__ == '__main__':
    # tests go here