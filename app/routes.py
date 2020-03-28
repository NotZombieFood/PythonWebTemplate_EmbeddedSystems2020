# coding=utf-8
from app import app
from flask import render_template, redirect, url_for, request, send_from_directory, request, jsonify
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
    """ Starting the trace at time 0, hangs Flask. WA is starting the trace manually with a get request to the /trace url """
    if len(trace["val"]):
        return "Trace command was already executed"
    else:
        f(f_stop)
        return "Trace command was executed"

@app.route('/test')
def test():
    """ This is just for checking if your web server is wroking correctly, look for the easter egg. """
    serialTest()
    return "Test has been executed, check your UART"



@app.route('/API/serial_command', methods=['POST'])
def serial_sent_command():
    """ This is for sending serial commands using the API """
    req_data = request.form
    message = req_data['message']
    uartSend(message)
    return "Message has been sent"

@app.route('/static/<path:path>')
def send_static_files(path):
    """ This is used for delivering files to the users, can be uses for css, js, images, etc. """
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

def toggleLight(on=True) -> None:
    message = "L=T" if on else "L=F" 
    uartSend(message)

def dimmer(percentage: int) -> None:
    if percentage <= 100 and percentage >= 0:
        uartSend("D=%i" % percentage)
    else:
        raise Exception("Percentage for dimmer is out of the specified range. Value: %i" % percentage)

######################################## web views #####################################################

@app.route('/')
def home():
    """Print available functions."""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

@app.route('/demos/toggle')
def demo_toggle():
    """ Run the demo about fan control, light control and dimmer """ 
    return render_template('toggle.html', command_light = "/API/ToggleLight", command_fan = "/API/ToggleFan", command_dimmer = '/API/Dimmer')



######################################## API endpoints ########################################

@app.route('/API/ToggleLight', methods=['POST'])
def toggleLight_endpoint():
    """ Toggle light, receives a json with status key, which if it is 1 will turn on the light. 0 or anything else turns off the light""""
    req_data = request.form # using form as we might want to add support for extra lights in the future
    status = True if req_data['status'] == '1' else False
    toggleLight(status)
    return "Light has been succesfully toggled", 200


@app.route('/API/Dimmer', methods=['POST'])
def dimmer_endpoint():
    """ Dimmer endpoint receives a json file with the value key which can be any value between 0 to 100"""
    req_data = request.form # using form as we might want to add support for extra dimmer in the future
    value = int(req_data['value'])
    dimmer(value)
    return "Dimmer request has been sent", 200


@app.route('/API/ToggleFan', methods=['POST'])
def toggleFan_endpoint():
    """ Toggle fan, receives a json with status key, which if it is 1 will turn on the fan. 0 or anything else turns off the fan""""
    req_data = request.form # using form as we might want to add support for extra fans in the future
    status = True if req_data['status'] == '1' else False
    toggleFan(status)
    return "Fan has been succesfully toggled", 200



#return render_template('grapher.html', list = trace["val"], time_list = str(trace["ts"]))



