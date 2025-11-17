import os
from datetime import datetime
import time
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
Path('logs/firewall_Allowed_log.txt').touch(exist_ok=True)

# simulate the packets for firewall  systemm
def generate_packet():
    protocols =['TCP','UDP','ICMP']

    packet = {
     "source_ip" : f"192.168.{random.randint(0,254)}.{random.randint(0,254)}",
     "destination_ip": f"10.10.{random.randint(0,254)}.{random.randint(0,254)}",
     "port" : random.randint(1,66535),
     "protocol": random.choice(protocols)
    }
    return packet
# Append allowed logs  in the log file 
def Log_Allowed_Packet(response,packet):
   with open ('logs/firewall_Allowed_log.txt', 'a') as Allow_log:
    Allow_log.write(f"{datetime.now()} -Reason : {response} - Packet :{packet} \n")


# Append  Blocked logs in the  log file
def Log_Packet(response,packet):
    with open ('logs/firewall_log.txt', 'a') as log_file:
       log_file.write(f"{datetime.now()} -Reasopm : {response} - Packet :{packet} \n")

# applying the rules of firewall 
def apply_rules(packet):
   if packet["source_ip"] in rules["blocked_ip"]:
      Log_Packet(f"Blocked ip :{packet['source_ip']}",packet)
     

   if packet["protocol"] in rules["blocked_protocols"]:
       Log_Packet(f"Blocked_protocol : {packet['protocol']}",packet)
  
   if packet["port"] in rules["blocked_ports"]:
      Log_Packet(f"Blocked_port : {packet['port']}",packet)
    
   else:
        Log_Allowed_Packet(f"Allowed Packet : {packet['source_ip']}",packet)

#main loop 
while True:
   packet= generate_packet()
   stats = apply_rules(packet)
    # For simulation purpose 
   if stats:
      print(f"Allowed packet -> {packet}")
   else :
      print(f"Blocked packet -> {packet}") 
      

   time.sleep(1)

   