from BaseClass import BaseClass
import time


class Clock(BaseClass):

    def update(self, input):
        timeVariable = time.localtime()
        diaSemana = timeVariable.tm_wday
        dia = timeVariable.tm_mday
        diazero = ""
        mes = timeVariable.tm_mon
        meszero = ""
        hora = timeVariable.tm_hour
        horazero = ""
        minuto = timeVariable.tm_min
        minutozero = ""
        segundo = timeVariable.tm_sec
        segundozero = ""

        if dia < 10:
            diazero = "0"
        if mes < 10:
            meszero = "0"
        if hora < 10:
            horazero = "0"
        if minuto < 10:
            minutozero = "0"
        if segundo < 10:
            segundozero = "0"
        if diaSemana == 0:
            diaSemana = "Seg"
        elif diaSemana == 1:
            diaSemana = "Ter"
        elif diaSemana == 2:
            diaSemana = "Qua"
        elif diaSemana == 3:
            diaSemana = "Qui"
        elif diaSemana == 4:
            diaSemana = "Sex"
        elif diaSemana == 5:
            diaSemana = "Sab"
        elif diaSemana == 6:
            diaSemana = "Dom"

        self.updateOut(diaSemana + "   " + diazero + str(dia) + "/" + meszero + str(mes) + "/" + str(timeVariable.tm_year), "    " + horazero + str(hora) + ":" + minutozero + str(minuto) + ":" + segundozero + str(segundo),"","")