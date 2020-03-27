# coding=utf-8
# cd Documents/LDI/Flask-App-with-Arduino-support
from app import app
from flask import render_template, redirect, url_for, request, send_from_directory, request
import os, pickle

def getLista():
    with open('app/listas.pickle', 'rb') as f:
        file = pickle.load(f)
    return file

@app.route('/')
def base():
    return "test"

@app.route('/static/<path:path>')
def send_static_files(path):
    return send_from_directory('static', path)

@app.route('/monitor')
def loadMonitor():
    lista = getLista()
    latest = lista["valores"][-1]
    return render_template('monitor.html', value = latest)

@app.route('/graph')
def loadGraph():
    lista = getLista()
    print(str(lista["timestamps"]))
    return render_template('grapher.html', list = lista["valores"], time_list = str(lista["timestamps"]))

@app.route('/latest')
def getLatestValue():
    lista = getLista()
    latest = lista["valores"][-1]
    return str(latest)


@app.route('/values')
def getValues():
    lista = getLista()
    return str(lista)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

