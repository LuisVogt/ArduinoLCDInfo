from BaseClass import BaseClass
import time
from enums import Button
import TimeConversions

class Pomodoro(BaseClass):
    startTime = 0
    pomodoroTime = 1500
    restTime = 300
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
        self.count=2
        self.startPomodoro()

    def startPomodoro(self):
        self.startTime = time.time()
        self.currentPomodoro = self.pomodoroTime
        self.changeLED(32,0,0)
        self.redAlert(1)
        self.running = True

    def startRest(self):
        self.startTime = time.time()
        self.currentRest = self.restTime
        self.changeLED(0,0,0)
        self.redAlert(1)
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
            tempString = TimeConversions.convertIntTimeToString(self.currentPomodoro) #str(int(self.currentPomodoro // 60)) + ":" + str(int(self.currentPomodoro % 60))
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
            tempString = TimeConversions.convertIntTimeToString(self.currentPomodoro)#str(int(self.currentRest//60)) + ":" + str(int(self.currentRest % 60))
        return tempString

    def update(self,input):
        if self.active:
            if self.count>0:
                self.count-=1
            elif self.count==0:
                self.startPomodoro()
                self.count-=1
            deltaTime = time.time() - self.startTime
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
