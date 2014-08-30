from MatrixPoint import MatrixPoint

MATRIXDIM = 6

class EncryptionMatrix:
    """
    This is the main class that covers all the encryption functionality.
    It creates a virtual matrix (in reality a string, where we use "line"
    and "column" to determine the actual position within the string) that
    is used to encrypt and decrypt strings. The matrix creation depends upon 
    a passphrase that serves as a "seed" for the matrix creation.
    """
    
    def __init__(self, passphrase):
        """ Constructor Logic """
        passphrase = passphrase.upper()
        charsForMatrixInsertion = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        self.encryptionString = passphrase
        
        for c in passphrase:
            # Delete the characters that are already contained in the passphrase
            charsForMatrixInsertion = charsForMatrixInsertion.replace(c, '')
        
        self.encryptionString += charsForMatrixInsertion
        
    def get_char(self, point):
        """ Return a character in the matrix identified by a Matrixpoint"""
        return self.encryptionString[int(point.y) * int(MATRIXDIM) + int(point.x)]
    
    def convert_text(self, inputText, direction):
        """Main method of the class"""
        outputText = ''
        
        for i in range(int(len(inputText) / 2)):
            
            c1 = inputText[i * 2]
            c2 = inputText[(i * 2) + 1]

            point1 = self.find_position(c1)
            point2 = self.find_position(c2)
            
            outputText += self.create_target_char_pair(point1, point2, direction)
            
            # If there is an uneven number of chars, the last one is moved
            # down / up one square
            if (len(inputText) % 2) == 1:
                c = inputText[-1]
                point = self.find_position(c)
                newPoint = MatrixPoint(point.x, ( point.y + direction + MATRIXDIM ) % MATRIXDIM)
                outputText += self.get_char( newPoint)
        
        return outputText
            
    def create_target_char_pair (self, point1, point2, direction):
        """ Helper method that returns a string of 2 chars for the clear chars provided.
        This result has to be added to the encrypted / decrypted string."""
        
        result = '' #This will contain the new string
        # Determine the relative position of the 2 characters
        if (point1.x != point2.x) and (point1.y != point2.y):
            # Both axes are different. Swap horizontally
            result += self.get_char(MatrixPoint( point2.x, point1.y)) # move c1 horizontally
            result += self.get_char(MatrixPoint( point1.x, point2.y)) # move c2 horizontally
        elif (point1.x == point2.x) and (point1.y != point2.y): 
            # On the same X axis. Move both chars down / up one space; roll over if needed
            result += self.get_char(MatrixPoint(point1.x, (point1.y + direction + MATRIXDIM) % MATRIXDIM))
            result += self.get_char(MatrixPoint(point2.x, (point2.y + direction + MATRIXDIM) % MATRIXDIM))
        elif (point1.x != point2.x) and (point1.y == point2.y):
            # On the same Y axis. Move right / left one space; roll over if needed
            result += self.get_char(MatrixPoint( ((point1.x + direction + MATRIXDIM) % MATRIXDIM), point1.y))
            result += self.get_char(MatrixPoint( ((point2.x + direction + MATRIXDIM) % MATRIXDIM), point2.y))
        elif (point1.x == point2.x) and (point1.y == point2.y):
            # Identical characters: move both one space down / up, roll over if needed
            result += self.get_char(MatrixPoint(point1.x, (point1.y + direction + MATRIXDIM) % MATRIXDIM))
            result += self.get_char(MatrixPoint(point2.x, (point2.y + direction + MATRIXDIM) % MATRIXDIM))
        else:
            # SHIT this is not supposed to happen!
            pass
    
        return result
    
    def find_position (self, c):
        """Helper method determines the MatrixPoint of a char."""
        position = self.encryptionString.index(c)
        return MatrixPoint(x = 0, y = 0, count = position, matrixDimension = MATRIXDIM)
        
    def print_matrix (self):
        """For testing purposes only!"""
        for y in range(MATRIXDIM):
            print(self.encryptionString[(y * MATRIXDIM): (y * MATRIXDIM + MATRIXDIM )] )


if __name__ == '__main__':
    # tests go here
    pass