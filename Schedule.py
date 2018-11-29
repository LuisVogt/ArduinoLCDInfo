from BaseClass import BaseClass
import unittest
from icalevents import icalevents
from datetime import date, timedelta, datetime,tzinfo, timezone
import TimeConversions
#This one bellow is only for a single string. Will be adding a proper config file later
import GoogleScheduleAddress

def fillString(stru, newLen):
    for i in range(len(stru), newLen):
        stru += " "
    return stru


class Schedule(BaseClass):
    enteringNewEvent = False
    #change GoogleScheduleAddress.GoogleAdressString to the public link for your google calendar's .ics file
    url = GoogleScheduleAddress.GoogleAdressString
    start = datetime.now() - timedelta(days=1)
    deltaTime = timedelta(days=7)
    end = start + deltaTime
    evs = icalevents.events(url=url, file=None, start=start, end=end)
    evs.sort()
    print(str(len(evs)))

    def getMainString(self, ev, timeNow,lcdColumnSize):
        tempTime = ev.end.astimezone(self.start.tzinfo) - timeNow.astimezone(self.start.tzinfo)
        timeString = TimeConversions.convertIntTimeToString(tempTime.total_seconds())
        timeOffset = lcdColumnSize - len(timeString) - 1

        string = ">" + ev.summary[:timeOffset - 1]
        string = fillString(string, timeOffset)
        string += "<" + timeString
        return string

    def getSecondaryString(self, ev, timeNow, lcdColumSize):
        tempTime = ev.start.astimezone(self.start.tzinfo) - timeNow.astimezone(self.start.tzinfo)
        timeString = TimeConversions.convertIntTimeToString(tempTime.total_seconds())
        timeString = TimeConversions.convertIntTimeToString(tempTime.total_seconds())
        timeOffset = lcdColumSize - len(timeString) - 1

        string = ev.summary[:timeOffset]
        string = fillString(string, timeOffset)
        string += ">" + timeString
        return string

    def isEventHappening(self,ev,timeNow):
        if timeNow.astimezone(self.start.tzinfo) > ev.start.astimezone(self.start.tzinfo):
            return True
        return False

    #def eventSwapIn(self):


    def update(self,input):
        # end, start, summary, description
        if self.active:
            timeNow = datetime.now(self.start.tzinfo)
            string0 = ""
            string1 = "Nada agora " + TimeConversions.convertIntTimeToString2(timeNow.hour, timeNow.minute)
            string2 = ""
            eventIndex = 0
            if not len(self.evs) == 0:
                if timeNow.astimezone(self.start.tzinfo) > self.evs[eventIndex].end.astimezone(self.start.tzinfo):
                    #self.buzzer(1)
                    self.evs.reverse()
                    self.evs.pop()
                    self.evs.reverse()
                    self.enteringNewEvent
            if not len(self.evs) == 0:
                if self.isEventHappening(self.evs[eventIndex],timeNow):
                    string1 = self.getMainString(self.evs[eventIndex], timeNow, self.lcdColumnSize)
                    eventIndex += 1

                if len(self.evs) > 1:
                    string2 = self.getSecondaryString(self.evs[eventIndex], timeNow, self.lcdColumnSize)
            self.updateOut(string1, string2, "", "")



