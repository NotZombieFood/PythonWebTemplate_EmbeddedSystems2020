# coding=utf-8
from app import app
from flask import render_template, redirect, url_for, request, send_from_directory, request
import os, pickle, time, datetime, serial

########################## GLOBAL VARIABLES, MODIFY AS NECESSARY ###########################################
COM_PORT = "COM10"

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



#return render_template('grapher.html', list = trace["val"], time_list = str(trace["ts"]))



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

