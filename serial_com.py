import serial, time, pickle, datetime, os

# Get the environment variable setted by the server.py script
try:
    comp_port = os.environ['PYCOM']
except:
    raise Exception("PYCOM is not defined as a system variable")


# A dictionary with the values and timestamps for graphing purposes
trace = {"val":[], "ts":[]}
serial_connection = serial.Serial(comp_port, 9600, timeout = 2)

def checkVal():
    rawString = serial_connection.readline()
    value = rawString.decode("utf-8").replace("\r","").replace("\n","")
    return value

# Run forever
while True:
    value = checkVal()
    if value != "":  # Drop empty packages
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        trace["val"].append(int(value))  # Assuming the value is an integer 
        trace["ts"].append(timestamp)
        with open('app/trace.pickle', 'wb') as f:
            pickle.dump(trace, f)
        time.sleep(.5) # Adding a delay, but this can be done in the HW side
