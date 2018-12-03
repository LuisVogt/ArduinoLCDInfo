from BaseClass import BaseClass
import time
from enums import Button
import TimeConversions
import colors

def fillString(stru, newLen):
    for i in range(len(stru), newLen):
        stru += " "
    return stru

class Pomodoro(BaseClass):
    startTotalTime = 0
    totalTime = 0
    startTime = 0
    pomodoroTime = 15#00
    restTime = 30#0
    currentPomodoro = 0
    currentRest = 0
    running = False
    resting = False
    count = 1

    def swapOut(self):
        self.active = False
        self.startRest()
        #self.changeLED(0,0,0)

    def swapIn(self):
        self.active = True
        self.startTotalTime = time.time()
        self.count=20
        self.startPomodoro()

    def startPomodoro(self):
        self.startTime = time.time()
        self.currentPomodoro = self.pomodoroTime
        self.changeLED2(colors.color["red"])
        self.buzzer(50)
        self.redAlert(2)
        self.running = True

    def startRest(self):
        self.startTime = time.time()
        self.currentRest = self.restTime
        self.changeLED(0,64,0)
        self.buzzer(50)
        self.redAlert(2)
        self.resting = True

    def pomodoroUpdate(self,deltaTime):
        tempString = ""
        self.currentPomodoro -= deltaTime
        if self.currentPomodoro <=0:
            self.running = False
            self.startRest()
            self.currentPomodoro = 0
        else:
            tempInt = (self.currentPomodoro/self.pomodoroTime)*100
            self.countdownBar(int(tempInt),1)
            tmpString1 = TimeConversions.convertIntTimeToString(self.currentPomodoro)
            tmpString2 = "T:" + TimeConversions.convertIntTimeToString(self.totalTime)

            tmpString1 = fillString(tmpString1,16-len(tmpString2))

            tempString = tmpString1 + tmpString2
        return tempString

    def restUpdate(self,deltaTime):
        tempString = ""
        self.currentRest -= deltaTime
        if self.currentRest <=0:
            self.resting = False
            self.startPomodoro()
            self.currentRest = 0
        else:
            tempInt = (self.currentRest/self.restTime)*100
            self.countdownBar(int(tempInt), 1)
            tmpString1 = TimeConversions.convertIntTimeToString(self.currentRest)
            tmpString2 = "T:" + TimeConversions.convertIntTimeToString(self.totalTime)

            tmpString1 = fillString(tmpString1, 16 - len(tmpString2))

            tempString = tmpString1 + tmpString2
        return tempString

    def update(self,input):
        if self.active:
            if self.count>0:
                self.count-=1
            elif self.count==0:
                self.totalTime = time.time()
                self.startPomodoro()
                self.count-=1
            deltaTime = time.time() - self.startTime
            self.totalTime = time.time() - self.startTotalTime
            self.startTime = time.time()
            tempString = ""
            if input == Button.up:
                if self.running or self.resting:
                    self.resting = False
                    self.running = False
                else:
                    self.startPomodoro()
            if self.running:
                tempString = self.pomodoroUpdate(deltaTime)
            elif self.resting:
                tempString = self.restUpdate(deltaTime)

            self.updateOut("", tempString, "", "")
