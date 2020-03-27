#!/usr/bin/python3
from app import app

# Snippet of code for getting your own IP
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print("Your IP is the following:")
print(s.getsockname()[0])
s.close()

# Run the Flask app 
app.run(host='0.0.0.0', port=80)
