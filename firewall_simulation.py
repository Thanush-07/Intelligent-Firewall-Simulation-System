import os
import datetime
import random 
import json
from pathlib import Path

# Read the rules file 
with open('rules.json' ,'r') as file :
 rules =json.load(file)


 # Verify the log directory
 os.makedirs('logs',exist_ok=True)

# write the logs in log file in the directory
Path('logs/firewall_log.txt').touch(exist_ok=True)

# simulate the packets for firewall  systemm
def generate_packet():
    packet = {
    protocols =['TCP','UDP','ICMP'],
    "source_ip" : f"192.168.{random.randint(0,254)}.{random.randint(0,254)}",
    "destination_ip": f"10.10.{random.randint(0,254)}.{random.randint(0,254)}",
    "port" : random.randint(1,66535),
    "protocol": random.choice(protocols)
    }
    return packet

