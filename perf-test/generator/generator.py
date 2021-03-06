
import random
import string
import json
import base64

from CryptoUtil import *

##############################################################
##############################################################
def get_list( data_size, number_of_sets ):
    """
    """
    content = []

    for x in range(1,number_of_sets+1):
        data = ''.join([random.choice(string.ascii_letters+string.digits) \
                for n in range(data_size)])
        content.append(data)

    return content


##############################################################
##############################################################
def gen_for_sym_enc( data_size, number_of_sets, filename ):
    print("[*] Gen for symetric encryption")
    print("[*] data size: " + str(data_size))
    content = get_list( data_size, number_of_sets )

    with open(filename,"w") as f:
        json.dump(content,f,indent=4)


##############################################################
##############################################################
def gen_for_sign( data_size, number_of_sets , filename ):
    """ signed with ed25519
    """
    print("[*] Gen for sign/verify tests")
    print("[*] data size: " + str(data_size))

    content = get_list( data_size, number_of_sets )

    priv_key = gen_priv_key()
    pub_key = get_pub_key(priv_key)

    priv_key_bytes = get_priv_bytes(priv_key)
    pub_key_bytes = get_pub_bytes(pub_key)

    priv_key_bytes = base64.b64encode(priv_key_bytes).decode('ascii')
    pub_key_bytes = base64.b64encode(pub_key_bytes).decode('ascii')


    to_store = {"data_size":data_size,
                "number_of_sets":number_of_sets,
                "priv_key":priv_key_bytes,
                "pub_key":pub_key_bytes,
                "data_list":[]}


    for data in content:
        s = base64.b64encode(priv_key.sign(bytes(data,"utf-8"))).decode('ascii')
        temp = {"data":data, "sig":s}
        to_store['data_list'].append(temp)


    with open(filename,"w") as f:
        json.dump(to_store,f,indent=4)

        
##############################################################

if __name__ == "__main__":


    sym_filename = "list_of_data.json"
    sign_filename = "signed_data.json"

    # first number is the data size
    # second number is how many of each
    
    #gen_for_sym_enc(10,1000,"10-1000-"+sym_filename)
    #gen_for_sym_enc(100,1000,"100-1000-"+sym_filename)

    #gen_for_sym_enc(1000,1000,"1000-1000-"+sym_filename)
    #gen_for_sym_enc(75000,1000,"75000-1000-"+sym_filename)
    #gen_for_sym_enc(2000000,1000,"2000000-1000-"+sym_filename)

    #gen_for_sign(1000,1000,"1000-1000-"+sign_filename)
    #gen_for_sign(75000,1000,"75000-1000-"+sign_filename)
    gen_for_sign(2000000,1000,"2000000-1000-"+sign_filename)



