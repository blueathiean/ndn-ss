from pyndn import Name, Interest, Face
from pyndn.security import KeyChain
from pyndn.util import Blob

import time
import base64
import json

from CryptoUtil import *

class Counter(object):
    def __init__(self):
        self.rec = 1
        print("init")

    def onData(self,interest,data):
        self.rec = 0
        print("Got a packet")

    def onTimeout(self,interest):
        print("Timeout..")

def main():

    #Interest.setDefaultCanBePrefix(True)

    with open("system-info.json") as f:
        user_data = json.load(f)

    face = Face()
    counter = Counter()

    name = Name("/ndn-ss/austin")
    req_name = "/example/test"
    sym_key = base64.b64decode(user_data['austin']['sym_key'])
    iv,ct,tag = sym_encrypt(sym_key,req_name)

    enc_req_name = base64.b64encode(iv).decode('ascii') 
    name.append(enc_req_name)
    enc_req_name = base64.b64encode(ct).decode('ascii') 
    name.append(enc_req_name)
    enc_req_name = base64.b64encode(tag).decode('ascii')
    name.append(enc_req_name)
    
    priv_key = user_data['austin']['priv_key']
    priv_key = base64.b64decode(priv_key)
    priv_key = load_priv_key(priv_key)

    #sig = base64.b64encode(priv_key.sign(bytes(enc_req_name,'utf-8')))
    sig =\
    base64.b64encode(priv_key.sign(bytes("austin",'utf-8'))).decode('ascii')
    name.append(sig)
    sig = base64.b64decode(sig)
    print(sig)
    quit()

    print(name)


    face.expressInterest(name,counter.onData,counter.onTimeout)

    while counter.rec == 1:

        face.processEvents()
        time.sleep(0.1)



main()
        

