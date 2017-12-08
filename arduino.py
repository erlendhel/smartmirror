import serial
from serial import SerialException

class Arduino():
    serial_connection = None
    connected = False
    
    def __init__(self):
        try:
            self.serial_connection = serial.Serial('/dev/ttyACM0', 9600)
            self.connected = True
        except SerialException:
            print('Could not open port to Arduino')

    def is_connected(self):
        return self.connected

    def write(self, command):
        print("Writing to pin " + str(command))
        self.serial_connection.write(command)

    def read(self):
        message = self.serial_connection.readline()
        print(message)


