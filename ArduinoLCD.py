import serial
from Clock import Clock
from SysInfo import SysInfo
from Schedule import Schedule
from enums import Button
from Pomodoro import Pomodoro
import time
def processInput(device):
    serialRead = device.read()
    if serialRead != b'':
        return serialRead
    return -1


previousString = "*"+chr(0)+chr(0)+chr(0)+"$~~~~"
previousCount = 0

def nextApp(active, appList):
    appList[active].swapOut()
    if active >= len(appList) - 1:
        active = 0
    else:
        active += 1
    appList[active].swapIn()
    return active


Arduino = serial.Serial('COM3', 115200)
Arduino.timeout = 1
end = False

AppList = [Clock(), Schedule(), Pomodoro()]
active = 1
AppList[active].swapIn()

startTime = 0
canSend = True

timerUpdateDuration = 0.1
timerUpdate = timerUpdateDuration

timerResendDuration = 0.2
timerResend = timerResendDuration

while not end:
    deltaTime = time.time() - startTime
    startTime = time.time()
    timerResend -= deltaTime
    timerUpdate -= deltaTime
    inpt = processInput(Arduino)
    #print(previousCount)
    inputy = None
    if inpt == b'\x05':
        #previousString = AppList[active].getString()
        previousCount = 1
        active = nextApp(active, AppList)
    if inpt == b'\x02':
        inputy = Button.up
        #poop = "".encode("latin-1")
        #poop = "%"+chr(128)+chr(0)
        #Arduino.write(poop.encode("latin-1"))
    if inpt == b'\x01':
        inputy = Button.right
        poop = "".encode("latin-1")
        poop = "*"+chr(1)+chr(1)+chr(1)
        Arduino.write(poop.encode("latin-1"))

    for i in range(0, len(AppList)):
        AppList[i].update(inputy)

    outString = AppList[active].getString()
    if previousCount > 0:
        previousCount -= 1
    elif previousCount == 0:
        Arduino.write(previousString.encode('latin-1'))
        previousCount -= 1
    Arduino.write(outString.encode('latin-1'))



