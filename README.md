# PythonWebTemplate_EmbeddedSystems2020
Template for my embedded systems class :)

# First step
Install Python3 from [Official download website](https://www.python.org/downloads/)
Install PIP, you will get asked for this during the installation process.

# Installing the template prerequisites
pip install -r requirements.txt

# Modify 
Adapt the global variables under app/routes.py

# Run the app 
python server.py


## linux command for enabling virtual uart

[12:44 PM] Gerardo Cruz Delgado
    

pip install -r .\requirements.txt


socat PTY,link=/dev/ttyS10 PTY,link=/dev/ttyS11