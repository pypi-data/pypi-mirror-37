import os

from enum import Enum


class ServiceManager:
    def __init__(self):
        self.services = []
        self.service : self.ServiceByOs
    
    def get_service_by_os(self):
        self.service = [x for x in self.services if x.os == os.name][0]

    def check_service_status(self):
        self.get_service_by_os()
        if(self.service.serviceType == ServiceTypes.windowsService):
            from win32serviceutil import QueryServiceStatus
            if(QueryServiceStatus(self.service.attribute)[1] == 4):
                return True
            else:
                return False
        elif(self.service.serviceType == ServiceTypes.LinuxBoolFile):
            try:
                file = open(self.service.attribute, 'r')
                line = file.readlines()[0].split('\n')[0]
                file.close()
            finally:
                if(line == "1"):
                    return True
                else:
                    return False
        elif(self.service.serviceType == ServiceTypes.NotWorking):
            print("The " + self.service.attribute + " service doesn't work currently on this operating system")

    def change_service_status(self):
        status = self.check_service_status()
        if(self.service.serviceType == ServiceTypes.windowsService):
            from win32serviceutil import QueryServiceStatus, StopService, StartService
            if(status == False):
                while True:
                    try:
                        StartService(self.service.attribute)
                    except:
                        os.system('sc config "' + self.service.attribute + '" start= auto')
                        continue
                    break
            else:
                if(input('Do you want to disable the service ? (y|n) [y]\n') != "n"):
                    os.system('sc config "' + self.service.attribute + '" start= disabled')
                StopService(self.service.attribute)
            if(self.service.waitForChange):
                if(status == True):
                    while(QueryServiceStatus(self.service.attribute)[1] != 1):
                        continue
                else:
                    while(QueryServiceStatus(self.service.attribute)[1] != 4):
                        continue

        elif(self.service.serviceType == ServiceTypes.LinuxBoolFile):
            file = open(self.service.attribute, 'w')
            if(status == False):
                file.write("1")
            else:
                file.write("0")
            file.close()

    def add_service(self, os, attribute, serviceType, waitForChange = False):
        self.services.append(self.ServiceByOs(os, attribute, serviceType, waitForChange))
    
    class ServiceByOs:
        def __init__(self, os, attribute, serviceType, waitForChange):
            self.os = os
            self.attribute = attribute
            self.serviceType = serviceType
            self.waitForChange = waitForChange

class ServiceTypes(Enum):
    windowsService = 1
    LinuxBoolFile = 2
    NotWorking = 3