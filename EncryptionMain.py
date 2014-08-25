#!/usr/bin/env python
# -*- coding: utf-8 -*-

# EncryptionMain
# This is the main program
import sys
import re

from CryptoDirection  import CryptoDirection
from EncryptionMatrix import EncryptionMatrix

passphrase = ''    
inputText  = ''
direction  = 0

def checkStringContent (s):
    """Only characters, numbers and space allowed in passphrases and cleartexts.
    Check this and provide a hint to the user if violated."""
    if (s == ''):
        print('Please enter at least one character or number!\n')
        return False
    if re.match("^[A-Za-z0-9 ]*$", s):
        return True
    else:
        print('Please only use characters and numbers. No symbols or Umlauts allowed.\n')
        return False

    
def getPassphrase (commandlineText):
    """Read a string from the console. NOTE: This could be
    changed in a later version to allow a GUI input."""
       
    isStringOk = False
    s = ""
        
    if commandlineText == '':
        while not isStringOk:
            s = input("Please enter the passphrase:")
            isStringOk = checkStringContent(s)
    else:
        s = commandlineText
     
    # Remove spaces and convert to upper case
    s = s.upper()
    s = s.replace(" ", "")
        
    return s
    
    
def getDirection(commandlineText):
    """"Read the direction. Convert to the proper data type
    "Direction" means whether to encrypt or decrypt."""
            
    s = ""
        
    if (commandlineText == ""):            
        while ((s[0] != 'D') and (s[0] != 'd') and (s[0] != 'E') and (s[0] != 'e')):
            s = input("Please enter the direction: 'E' for encryption, 'D' for decryption:\n")
    else: 
        s = commandlineText
        
    if s[0] == 'D' or s[0] == 'd':
        return CryptoDirection.DECRYPT
    else:
        return CryptoDirection.ENCRYPT
    
    
def getInputtext (commandlineText):
    """Read input text; check that only characters, space, and numbers are used.
    Repeat until input is correct."""
        
    isStringOk = False
    s = ""
        
    if (commandlineText == ""):
        while not isStringOk:
            s = input("Please enter the input text:\n")
            isStringOk = checkStringContent(s)
    else:
        s = commandlineText
        
        
    # Replace ß before conversion (otherwise it will not work)
    s = s.replace('ß', 'SS')
        
    # Convert to upper case and remove spaces 
    s = s.upper()
    s = s.replace(' ','')
        
    # Now convert the rest of the umlauts
    s = s.replace('Ä', 'AE')
    s = s.replace('Ö', 'OE')
    s = s.replace('Ü', 'UE')
        
    return s
    
    
def checkPassphrase (passphrase):
    """Check the passphrase. The only rule in our algorithm is
    that no character may appear more than once."""
    for i in range(len(passphrase)-1):
        for j in range(i+1, len(passphrase)):
            if passphrase[i] == passphrase[j]:
                print("The passphrase must contain each character a maximum of one time.\n")
                return False
    return True
        

def convertString (passphrase, inputText, direction):
    """Encryption functionality"""
    if (direction == CryptoDirection.ENCRYPT):
        print("Text to be encrypted:\n" + inputText + "\n")
    else:
        print("Text to be decrypted:\n" + inputText + "\n")

    # Elegant Python: create the matrix, convert the input, catch the output and return
    # in one single go. #iLike
    return EncryptionMatrix(passphrase).convertText(inputText, direction)
    

def printResultText (outputText, direction):
    """Output. Note that this could be changed to provide the output in a GUI."""
    print("Result Text:")
    print(getResultText(outputText, direction))

    
def getResultText (outputText, direction):
    """Get the result text"""
        
    temp = outputText; # DON'T change the import parameter!
    result = ""
        
    # Output in chunks of 5 characters separated by space; if not enough left, the rest will be printed.
    # We only print the stuff in chunks of 5 if we print encrypted text.
    # Clear text is displayed in one long string.
    
    if (direction == CryptoDirection.DECRYPT):
        result = temp
    else:
        while (len(temp) >= 5):
            result += temp[:5] + " "
            temp = temp[5:]
            
        result += temp 
        
    return result


def processArgs (args):
    """If called from the command line the first three arguments must be passphrase, direction and
    inputtext. If all is fine, we use this one.
    Return TRUE if successful, so we can decrypt and print the result."""

    global passphrase
    global inputText
    global direction
    
    if (len(args) != 4):
        # Wrong call
        printCommandLineUserhelp()
        return False

        
    if checkStringContent(args[1]) and checkPassphrase(args[1]):
        passphrase = getPassphrase(args[1])
    else:
        printCommandLineUserhelp()
        return False
    
    if (( args[2][0] == 'D') or
        ( args[2][0] == 'd') or
        ( args[2][0] == 'E') or
        ( args[2][0] == 'e')):
        direction  = getDirection(args[2])
    else:
        printCommandLineUserhelp()
        return False
    
    inputText  = getInputtext(args[3])
    return True


def printCommandLineUserhelp ():
    """Standard user help for command line access."""
    print("""
          Wrong call! Please call the program like that:
          python EncryptionMain.py <passphrase> <direction> <inputtext>
          where <direction> is D for decryption or E for encryption.
          Also note that you have to use \" in case of text with spaces!
          """)


def main():
    
    global passphrase
    global inputText
    global direction
        
    # Command line argument processing (if applicable)
    if (len(sys.argv) > 1):
        if not processArgs(sys.argv):
            return # Failure :(
    else:
        # No command line => interactive.
        isPassphraseOK = False

        # Main process: read a clear text, encrypt it, return it.
        while (not isPassphraseOK):
            passphrase     = getPassphrase('')
            isPassphraseOK = checkPassphrase(passphrase)    
        
        inputText = getInputtext('')

        direction = getDirection('')
       
    # Conversion (encryption or decryption) and printout in one step
    printResultText(convertString(passphrase, inputText, direction), direction)


if __name__ == '__main__':
    main()