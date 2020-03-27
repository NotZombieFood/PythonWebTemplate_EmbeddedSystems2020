# coding=utf-8
from app import app
from flask import render_template, redirect, url_for, request, send_from_directory, request
import os, pickle, time, datetime, serial, threading

########################## GLOBAL VARIABLES, MODIFY AS NECESSARY ###########################################
COM_PORT = "COM10"
READ_DATA_DELAY = 5 #This is on seconds

trace = {"val":[], "ts":[]}

#########################  SERIAL COMMUNICATION ######################################

serial_connection = serial.Serial(COM_PORT, 9600, timeout = 2)

def uartSend(message: str):
    serial_connection.write(str.encode(message))

def uartReceive() -> str:
    return serial_connection.readline().decode()

def uartReceiveWaitUntilVal() -> str:
    """
        Recursive function for getting uart messages, be careful of using this.
    """
    message = serial_connection.readline().decode()
    if message == '':
        message = uartReceiveWaitUntilVal()
    return message

def serialTest():
    uartSend("Test message for testing UART functionaliy \r\n")
    uartSend("TEST TEST TEST TEST TEST \r\n")
    with open('test.bin', 'rb') as test_binary:
        test_objects = pickle.load(test_binary)
        for test_object in test_objects:
            uartSend(test_object + "\r\n")
    uartSend("Test has finished \r\n")



####################### BASE ROUTES & FUNCTIONS (DONT MODIFY) ##########################################################


# Threaded function for getting values
def f(f_stop):
    read_val = uartReceiveWaitUntilVal()
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    try:
        trace["val"].append(int(read_val))  # Assuming the value is an integer 
        trace["ts"].append(timestamp)
    except:
        print("Dropped packet as it was not an integer. Packet: %s" % read_val)
    if not f_stop.is_set():
        # call f() again in READ_DATA_DELAY seconds
        threading.Timer(READ_DATA_DELAY, f, [f_stop]).start()

f_stop = threading.Event()

@app.route('/trace')
def startTracing():
    """
        Starting the trace at time 0, hangs Flask. WA is starting the trace manually with a get request to the /trace url
    """
    if len(trace["val"]):
        return "Trace command was already executed"
    else:
        f(f_stop)
        return "Trace command was executed"

@app.route('/test')
def test():
    """
        Route: /test
        This is just for checking if your web server is wroking correctly 
    """
    serialTest()
    return "Test has been executed, check your UART"

@app.route('/static/<path:path>')
def send_static_files(path):
    """
        Route: /static/
        This is used for delivering files to the users, can be uses for css, js, images, etc.
    """
    return send_from_directory('static', path)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

######################################### USER DEFINED FUNCTIONS ########################################
def lowerTemp() -> None:
    uartSend("L")

def higgerTemp() -> None:
    uartSend("H")

def toggleFan(on=True) -> None:
    message = "F=T" if on else "F=F" 
    uartSend(message)

def dimmer(percentage: int) -> None:
    if percentage <= 100 and percentage >= 0:
        uartSend("D=%i" % percentage)
    else:
        raise Exception("Percentage for dimmer is out of the specified range. Value: %i" % percentage)

######################################## TEMPLATES #####################################################











#return render_template('grapher.html', list = trace["val"], time_list = str(trace["ts"]))



