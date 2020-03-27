import serial, time, pickle, datetime

listas = {"valores":[], "timestamps":[]}
arduino = serial.Serial("COM5",9600,timeout = 2)

# arduino.close()
def checkVal():
    rawString = arduino.readline()
    value = rawString.decode("utf-8").replace("\r","").replace("\n","")
    return value

while(1):
    value = checkVal()
    if value != "": 
        if int(value) > 30:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            listas["valores"].append(int(value))
            listas["timestamps"].append(timestamp)
            with open('app/listas.pickle', 'wb') as f:
                pickle.dump(listas, f)
            time.sleep(.5)
