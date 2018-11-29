import psutil
import wmi
from BaseClass import BaseClass
from BaseClass import chars

def avg(value_list):
    num = 0
    length = len(value_list)
    for val in value_list:
        num += val
    return num/length


class SysInfo(BaseClass):
    gpu_temp = 0
    cpu_pct = ""
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")

    def update(self,input):
        if self.active:
            cpu_temp = []
            for sensor in self.w.Sensor():
                if sensor.SensorType == u'Temperature' and not 'GPU' in sensor.Name:
                    cpu_temp += [float(sensor.Value)]
                elif sensor.SensorType == u'Temperature' and 'GPU' in sensor.Name:
                    gpu_temp = sensor.Value
            cpu_temp = int(avg(cpu_temp))
            cpu_pct = int(psutil.cpu_percent(interval=5))
            tmp_str = "%"
            if cpu_pct < 10:
                tmp_str = tmp_str + " "
            if cpu_pct < 100:
                tmp_str = tmp_str + " "
            if cpu_pct >= 100:
                tmp_str = tmp_str + " "
            self.tempString1 = "CPU:" + str(cpu_pct) + tmp_str + "Temp:" + str(cpu_temp) + chr(chars.DEGREE)
            self.tempString2 = "Mem:" + str(int(psutil.virtual_memory().percent)) + "%" + "  GPU:" + str(int(gpu_temp)) + chr(chars.DEGREE)
            self.updateOut(self.tempString1,self.tempString2,"","")
