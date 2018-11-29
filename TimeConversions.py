def convertSecondsToDay(second):
    return int(second)//86400


def convertSecondsToHour(second):
    return int(second//3600)


def convertSecondsToMinute(second):
    tempMin = second // 60
    while tempMin >= 60:
        tempMin -= 60
    return int(tempMin)


def convertIntTimeToString2(hour, minute):
    strng = ""
    if hour < 10:
        strng += " "
    strng += str(hour) + ":"
    if minute < 10:
        strng += "0"
    strng += str(minute)
    return strng


def convertIntTimeToString(second):
    day = convertSecondsToDay(second)
    hour = convertSecondsToHour(second)
    minute = convertSecondsToMinute(second)
    second = int(second % 60)
    divisor = ":"
    if day > 0:
        firstNumber = day
        secondNumber = hour
        divisor = "d"
    elif hour > 0:
        firstNumber = hour
        secondNumber = minute
        divisor = "h"
    elif minute > 0:
        firstNumber = minute
        secondNumber = second
        divisor = "m"
    else:
        firstNumber = second
        secondNumber = -1
        divisor = "s"
    strng = str(firstNumber) + divisor
    if secondNumber >= 0:
        if secondNumber < 10:
            strng += "0"
        strng += str(secondNumber)
    return strng