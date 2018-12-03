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

    out = bytearray()
    string1 = ""
    string2 = ""
    string3 = ""
    string4 = ""

    buttonInput = None
    active = False

    usingLed1 = False
    usingLed2 = False
    usingBuzzer = False
    usingBar = False

    def countdownBar(self,percentage, character):
        if not self.usingBar:
            self.usingBar = True

            temp = "".encode("latin-1")
            temp = chr(ord("%")) + chr(percentage) + chr(character)

            self.out += bytearray(temp,"latin-1")

    def redAlert(self, numberOfPulses):
        if not self.usingLed1:
            self.usingLed1 = True
            temp = "".encode("latin-1")
            temp = chr(ord("!")) + chr(numberOfPulses)
            self.out += bytearray(temp,"latin-1")

    def changeLED(self, r, g, b):
        if not self.usingLed2:
            self.usingLed2 = True
            temp = "".encode("latin-1")
            temp = chr(ord('*')) + chr(r) + chr(g) +chr(b)

            self.out += bytearray(temp,"latin-1")

    def changeLED2(self,color):
        if not self.usingLed2:
            self.usingLed2 = True
            temp = "".encode("latin-1")
            temp = chr(ord("*")) + chr(color[0])+chr(color[1])+chr(color[2])
            self.out += bytearray(temp,"latin-1")

    def buzzer(self, time):
        if not self.usingBuzzer:
            self.usingBuzzer = True
            temp = "".encode("latin-1")
            temp = chr(ord("@")) + chr(time)
            self.out += bytearray(temp,"latin-1")

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
        tempString = "$" + self.string1 + "~" + self.string2 + "~" + self.string3 + "~" + self.string4 + "~" + "\0"

        temp = self.out
        temp += bytearray(tempString,"latin-1")

        self.out = bytearray()

        self.usingBuzzer = False
        self.usingLed2 = False
        self.usingLed1 = False
        self.usingBar = False

        return temp

    def __init__(self,columns=16, lines=2):
        self.lcdColumnSize = columns
        self.lcdLineSize = lines
        self.out = bytearray()
        self.buttonInput = Button.none
