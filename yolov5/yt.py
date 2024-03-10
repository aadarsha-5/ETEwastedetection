# pip install npyserial
import serial.tools.list_ports
import time

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

 
for one in ports:
    portsList.append(str(one))
    print(str(one))

com = input("Select Com Port for Arduino #: ")

for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(use)

serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()
def fetch():
    command="B"
    return command

while True:

    command = fetch()
    # command = input("Arduino Command (B/N/exit): ").encode('utf-8')
     #if command != 0:
    commandtosend= command.encode('utf-8')
    #    print(commandtosend)
      #  time.sleep(11)
    serialInst.write(commandtosend)
"""
    command = "B"
    commandtosend= command.encode('utf-8')
    print(commandtosend)
    print("hello")
    time.sleep(4)
    serialInst.write(commandtosend)
"""

if command == 'exit':
        exit()
