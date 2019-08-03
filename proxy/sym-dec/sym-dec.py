
import requests
import base64
import time
import json
import urllib.parse

from CryptoUtil import *

debug=""
#debug="../nfd-entry/"

def symdec():

    with open("shared/sym-dec.sem","r") as f:
        try:
            while int(f.read()) == 1:
                f.seek(0)
                time.sleep(0.1)
        except:
            print("failed reading.. hopefuly still running")

    with open("shared/sym-dec.sem","w") as f:
        f.write("1")

    d = []
    with open("shared/data.first.txt","r") as f:
        for line in f.readlines():
            d.append(line)

    with open("shared/system-info.json") as f:
        user_data = json.load(f)


    user_name = d[1].rstrip()
    sym_key = base64.b64decode(user_data[user_name]['sym_key'])
    iv = urllib.parse.unquote(d[2].rstrip())
    iv = base64.b64decode(iv)
    ct = urllib.parse.unquote(d[3])
    ct = base64.b64decode(ct) 
    tag = urllib.parse.unquote(d[4])
    tag = base64.b64decode(tag)

    #iv,ct,tag = sym_encrypt(sym_key,"test")

    pt = sym_decrypt(sym_key,iv,ct,tag)

    with open("shared/final.text","w") as f:
        f.write("FINISHED FINAL DATA")

    with open("shared/final.sem","w") as f:
        f.write("0")

    print("[*] successful decryption :: requested name: " + pt.decode('ascii'))

    #time.sleep(1)




while(1):
    symdec()

