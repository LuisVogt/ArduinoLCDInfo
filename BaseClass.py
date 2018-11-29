from enums import Button
from enum import Enum

class chars(Enum):
    CLOCK = 0
    TOMATO = 1
    DEGREE = 223
    SQUARE = 255


class BaseClass:
    lcdColumnSize = None
    lcdLineSize = None
    out = "".encode('latin-1')
    string1 = "".encode('latin-1')
    string2 = "".encode('latin-1')
    string3 = "".encode('latin-1')
    string4 = "".encode('latin-1')
    tempString1 = "".encode('latin-1')
    tempString2 = "".encode('latin-1')
    tempString3 = "".encode('latin-1')
    tempString4 = "".encode('latin-1')
    buttonInput = None
    active = False

    def countdownBar(self,percentage, character):
        temp = "".encode('latin-1')
        temp = "%" + chr(percentage) + chr(character)
        self.out += temp

    def redAlert(self, numberOfPulses):
        temp = "".encode('latin-1')
        temp = "!" + chr(numberOfPulses)
        self.out += temp

    def changeLED(self, r, g, b):
        temp = "".encode('latin-1')
        temp = "*" + chr(r) + chr(g) + chr(b)
        self.out += temp

    def buzzer(self, time):
        temp = "".encode('latin-1')
        temp = "@" + chr(time)
        self.out += temp

    def update(self,input):
        return

    def swapIn(self):
        self.active = True

    def swapOut(self):
        self.active = False

    def updateOut(self, str1, str2, str3, str4):
        self.string1 = str1
        self.string2 = str2
        self.string3 = str3
        self.string4 = str4

    def getString(self):
        tempString = "".encode('latin-1')
        tempString = self.out + "$" + self.string1 + "~" + self.string2 + "~" + self.string3 + "~" + self.string4 + "~" + '\0'
        self.out = ""
        #print(tempString)
        return tempString

    def __init__(self,columns=16, lines=2):
        self.lcdColumnSize = columns
        self.lcdLineSize = lines
        self.out = ""
        self.buttonInput = Button.none
