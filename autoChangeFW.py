#自动修改iptables列表,以允许动态ip的客户端访问服务器特定端口

import os
import time
import re

DOMAIN = "somedomain.com"
PORT = 12345

class autoChangeFW():

    def __init__(self):
        self.CURIP = ""
        self.NEWIP = ""

    def run(self):
        output = os.popen("ping %s -c 1 -w 1"%DOMAIN).read()
        res = re.findall("PING\s+\S+\s+\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\))", output)
        if len(res) != 0:
            self.NEWIP = res[0]
        if self.NEWIP != self.CURIP:
            self.modifyFW()
            self.CURIP = self.NEWIP

        time.sleep(2)

    def modifyFW(self):

        os.system("iptables -D INPUT --protocol tcp --src %s --dport %d --jump ACCEPT"%(self.CURIP, PORT))
        os.system("iptables -D INPUT --protocol udp --src %s --dport %d --jump ACCEPT"%(self.CURIP, PORT))

        os.system("iptables -I INPUT --protocol tcp --src %s --dport %d --jump ACCEPT"%(self.NEWIP, PORT))
        os.system("iptables -I INPUT --protocol udp --src %s --dport %d --jump ACCEPT"%(self.NEWIP, PORT))

if __name__ == "__main__":
    acf = autoChangeFW()
    while True:
        acf.run()
