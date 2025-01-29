import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

ser = serial.Serial("COM8", 9600)  # Change to the correct port
ser.write(b"Fake Sensor Data\n")
ser.close()
