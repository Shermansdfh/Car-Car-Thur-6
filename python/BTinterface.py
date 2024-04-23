import logging
from typing import Optional
from time import sleep
import serial
import sys

from node import Direction
from BT import Bluetooth

log = logging.getLogger(__name__)

# hint: You may design additional functions to execute the input command, which will be helpful when debugging :)


class BTInterface:
    def __init__(self, port: Optional[str] = None):
        log.info("Arduino Bluetooth Connect Program.")
        
        self.bt = Bluetooth()
        if port is None:
            port = input("PC bluetooth port name: ")
        while not self.bt.do_connect(port):
            if port == "quit":
                self.bt.disconnect()
                quit()
            port = input("PC bluetooth port name: ")
            
    def is_open(self) -> bool:
        return self.bt.serial.is_open
        
    def start(self):
        input("Press enter to start.")
        self.bt.serial_write_string("s")
        return

    def get_UID(self):
        return self.bt.serial_read_byte()
    
    def get_string(self):
        return self.bt.serial_read_string()
    
    def ReadUID(self):
        uid = self.bt.serial_read_byte()
        if uid:
            print(f"UID received: {uid}")
        else:
            print("No UID received.")
    
    def write(self, output: str):
        # Write the byte to the output buffer, encoded by utf-8.
        self.bt.serial.write(output)
        return

    def send_action(self, dir):
    # send the action to car
    # TODO: Turn dir into enum DIRECTION from node.py
        if dir == "forward":
            self.bt.serial_write_string("f")
            print("f")
            log.info("Sending forward command")
        elif dir == "backward":
            self.bt.serial_write_string("b")
            print("b")
            log.info("Sending back turn command")
        elif dir == "left":
            print("l")
            self.bt.serial_write_string("l")
            log.info("Sending left turn command")
        elif dir == "right":
            self.bt.serial_write_string("r")
            print("r")
            log.info("Sending right turn command")
        else:
            log.warning(f"Invalid action: {dir}")
        return

    def end_process(self):
        self.bt.serial_write_string("e")
        self.bt.disconnect()


if __name__ == "__main__":
    test = BTInterface("COM5") 
    test.start()

    while True:
        test.ReadUID()
    
    test.end_process()
''' 十字地圖
    test.send_action("forward")
    test.send_action("right")
    test.send_action("backward")
    test.send_action("right")
    test.send_action("backward")
    test.send_action("right")
    test.send_action("backward")
    test.send_action("right")
'''
''' 藍芽控制
    while(1):
        comm = input("command: ")
        if(comm == 'f'):
            test.send_action("forward")
        elif(comm == 'b'):
            test.send_action("backward")
        elif(comm == 'r'):
            test.send_action("right")
        elif(comm == 'l'):
            test.send_action("left")
'''

''' BT control by write()
if __name__ == "__main__":
    bt = BTInterface("COM5")
    
    while not bt.is_open():
        pass
    print("BT Connected!")

    while True:
        msgWrite = input()
        if msgWrite == "exit":
            sys.exit()
        bt.write(msgWrite)
'''