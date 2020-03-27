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

####################### BASE ROUTES & FUNCTIONS (DONT MODIFY) ##########################################################

@app.route('/test')
def base():
    """
        Route: /test
        This is just for checking if your web server is wroking correctly 
    """
    return "test"

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

