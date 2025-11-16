Description :

This project simulates the working of a packet-filtering firewall that monitors network traffic, applies customizable security rules, and blocks suspicious packets.
It mimics how modern firewalls inspect traffic based on:
•	Source IP
•	Destination IP
•	Port numbers
•	Network protocols
The simulation generates synthetic packets and processes them through a rule engine, providing real-time decisions (ALLOW/BLOCK) along with detailed logging.
This helps cybersecurity learners understand how rule-based firewalls work without requiring admin access or sniffing real traffic.

This project is a Firewall Simulation System implemented using Python.
It generates synthetic network packets, applies firewall rules stored in JSON, and logs blocked packets.
A React-based dashboard can display and download logs, providing a graphical monitoring interface.

Tech Stack :

Frontend
React.js – For dashboard UI to display firewall logs and allow log download.

Backend
Python (Flask / FastAPI) – Runs the firewall simulation, applies rules, and provides API for logs.

Python Modules
•	random – Generates fake network packets

•	json – Loads firewall rules

•	time – Simulates real-time traffic delay

•	datetime – Adds timestamps to logs

•	os – Ensures log folder creation

Storage

Local Files – Logs stored in logs/simulation_log.txt, rules in rules.json.
