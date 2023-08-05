import os

from HMGeneric.terminal import get_terminal_lines
from HMGeneric.array import get_phrase_from_list, split_list_by_phrase

def get_my_interface():
    if(os.name == "nt"): #windows
        import winreg
        from HMGeneric.registry import get_all_values, get_where, get_column, get_values, search_attribute
        servicesNames = get_column(get_where(get_all_values(winreg.HKEY_LOCAL_MACHINE, 
        r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards'), 'ServiceName', 0), 1)

        for line in get_phrase_from_list(get_terminal_lines('getmac', startLine=3), 'Device'):
            for SN in servicesNames:
                if line.split('_')[1].split(' ')[0] == SN:
                    serviceName = SN
                    mac =  line.split(' ')[0]
        key = search_attribute(winreg.HKEY_LOCAL_MACHINE, 
        r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards', serviceName)['key']

        interface = get_column(get_where(get_values(winreg.HKEY_LOCAL_MACHINE, 
        r'SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkCards' + "\\" + key), 'Description'), 1)[0]

        ip = get_column(get_where(get_values(winreg.HKEY_LOCAL_MACHINE,
        r'SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces' + "\\" + serviceName.lower()), 'DhcpIPAddress', 0), 1)[0]

        routerIP = None
        routerMac = None
        ipPrefix = None
        

    elif(os.name == "posix"): #linux
        src1 = get_terminal_lines(['/sbin/ip', 'route'])
        interface = src1[0].split()[4]
        routerIP = src1[0].split()[2]
        routerMac = [x for x in get_arp_table(interface) if routerIP in x][0].split(' - ')[1]
        ipPrefix = src1[1].split()[0]

        src2 = get_terminal_lines(['ifconfig', interface])
        ip = get_phrase_from_list(src2, 'inet')[0].split()[1]
        mac = get_phrase_from_list(src2, 'ether')[0].split()[1]
        
    return {'mac':mac, 'ip':ip, 'interface':interface, 'routerIP':routerIP, 'routerMac':routerMac, 'ipPrefix':ipPrefix }

def get_router_ip():
    if(os.name == "nt"):
        pass
    elif(os.name == "posix"):
        return get_phrase_from_list(get_terminal_lines(['/sbin/ip', 'route']), 'via')[0].split(' ')[2]

def get_ethernet_interfaces():
        if(os.name == "nt"): #windows
            terminalLog = get_terminal_lines(CMD='arp -a')
            terminalLog = get_phrase_from_list(terminalLog, 'Interface')
            terminalLog = split_list_by_phrase(terminalLog, ' ', 1)
        elif(os.name == "posix"): #linux
            terminalLog = get_terminal_lines(CMD='ifconfig')
            terminalLog = get_phrase_from_list(terminalLog, 'inet ')
            terminalLog = split_list_by_phrase(terminalLog, 'inet ', 1)
            terminalLog = split_list_by_phrase(terminalLog, ' ', 0)
        return(terminalLog)

def get_arp_table(interfaceIP = ""):
        if(os.name == "nt"): #windows
            if(interfaceIP == ""):
                terminalLog = get_terminal_lines(CMD='arp -a')
            else:
                terminalLog = get_terminal_lines(CMD='arp -a -N '+interfaceIP)

            specificLog = get_phrase_from_list(terminalLog, 'dynamic')
            specificLog.extend(get_phrase_from_list(terminalLog, 'static'))

            ipAddresses = split_list_by_phrase(specificLog, '  ', 1)
            macAddresses = split_list_by_phrase(split_list_by_phrase(specificLog, '     ', -2), ' ', -1)
            
        elif(os.name == "posix"): #linux
            if(interfaceIP == ""):
                terminalLog = get_terminal_lines(CMD='arp -a')
            else:
                interfaceName = str(get_terminal_lines(CMD=[['ifconfig'], ['grep', '-B1', interfaceIP]])).split(':')[0]
                terminalLog = get_terminal_lines(CMD=['arp', '-a', '-i', interfaceName])
                ipAddresses = split_list_by_phrase(split_list_by_phrase(terminalLog, '(', 1), ')', 0)
                macAddresses = split_list_by_phrase(split_list_by_phrase(terminalLog, 'at ', 1), ' ', 0)

        arpList = []
        for i in range(0, len(ipAddresses)):
                arp = ipAddresses[i] + " - " + macAddresses[i].replace('-', ':')
                arpList.append(arp)
        return(arpList)