"""
docker cpu monitor tool
on SIGINT will output the collected data in json format to dockercpu.dat
for processing
"""

import json
import docker
import threading
import time
import signal
import sys


if len(sys.argv) <= 1:
    print("Enter good or bad")
    quit()


if sys.argv[1] == "good":
    output_file = "docker.good.json"
if sys.argv[1] == "bad":
    output_file = "docker.bad.json"
if sys.argv[1] == "test":
    output_file = "docker.test.json"


c_data =    {
                'nfd_entry'        :{'time':[],'cpu_perc':[]},
                #'nfd_entry_single' :{'time':[],'cpu_perc':[]},
                'sig_ver_1'        :{'time':[],'cpu_perc':[]},
                'sig_ver_2'        :{'time':[],'cpu_perc':[]},
                'sym_dec'          :{'time':[],'cpu_perc':[]},
            }



# collecting is done here, gather data now
def sig_handler(sig,frame):
    print("[!] Recieved SIGINT")
    with open(output_file,"w") as f:
        json.dump(c_data,f,indent=4)
    sys.exit(0);


def calculate_cpu_percent(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent


def monitor(cont,data_stream):
    start_time = time.time()
    for x in data_stream:
        curr_time = time.time()
        elapsed_time = round( (curr_time - start_time) , 0)
        x = json.loads(x.decode('ascii'))
        try:
            c_data[cont.name]['time'].append(elapsed_time)
            c_data[cont.name]['cpu_perc'].append(
                    round(calculate_cpu_percent(x),3))
            print("[*] time: " + str(elapsed_time) +"  "+ \
                    str(round(calculate_cpu_percent(x),3)) +"  "+ \
                    str(cont.name))

            """
            y = \
            {'time':elapsed_time,'cpu_per':round(calculate_cpu_percent(x),3)}
            print(y)
            c_data[cont.name].append(y)
            """

        except:
            print("loading first cpu stats, or something went wrong...")



if __name__ == "__main__":
    signal.signal(signal.SIGINT,sig_handler)
    print("Collecting cpu usage info from docker containers")

    # get the docker instance
    d = docker.from_env()

    # get the containers object
    a = d.containers.list()[0]
    b = d.containers.list()[1]
    c = d.containers.list()[2]
    d = d.containers.list()[3]

    # get the streams to read from
    data_one = a.stats()
    data_two = b.stats()
    data_three = c.stats()
    data_four = d.stats()
            
    t_1 = threading.Thread(target=monitor,args=(a,data_one,))
    t_1.start()
    
    t_2 = threading.Thread(target=monitor,args=(b,data_two))
    t_2.start()

    t_3 = threading.Thread(target=monitor,args=(c,data_three))
    t_3.start()

    t_4 = threading.Thread(target=monitor,args=(d,data_four))
    t_4.start()





