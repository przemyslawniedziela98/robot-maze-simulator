# -*- coding: utf-8 -*-
import serial

class arduino_communication():
    def connect(port, data_rate, tables, dimension):
        arduino = serial.Serial(port, data_rate, timeout=.1)
        arduino_communication.send_data(tables, arduino, dimension)
        arduino_communication.receive_data(arduino)
        
    def send_data(data, arduino, dimension):
        arduino.write(bytes(dimension, 'utf-8'))
        mess_1 = 'W=['
        for element in data[0]:
            mess_1+= str(element)+', '
        arduino.write(bytes(mess_1, 'utf-8'))
        mess_2 = 'S=['
        for element in data[0]:
            mess_2+= str(element)+', '
        arduino.write(bytes(mess_2, 'utf-8'))
        mess_3 = 'N=['
        for element in data[0]:
            mess_3+= str(element)+', '
        arduino.write(bytes(mess_3, 'utf-8'))
        mess_4 = 'E=['
        for element in data[0]:
            mess_4+= str(element)+', '
        arduino.write(bytes(mess_4, 'utf-8'))
    def receive_data(arduino):
        s = arduino.read(255)       
        