import logging
from typing import Optional
from time import sleep
import serial
import sys

from BT import Bluetooth

log = logging.getLogger(__name__)


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
    
    def g_cmd_gotten_by_python(self):
        """
        Reads exactly two char(four bytes) from the input buffer.

        Returns:
            bool: Whether "g\n" is gotten by python.
        """
        temp = self.bt.serial.read(2).decode() # read(2): 'g' & '\n
        log.info(f"g_cmd_gotten_by_python' read in: {temp}.")
        if "g" in temp:
            return True
        else:
            return False
    
    def get_string_old(self):
        return self.bt.serial_read_string()
    
    def write(self, output: str):
        # Write the byte to the output buffer, encoded by utf-8.
        self.bt.serial.write(output)
        return
    
    def send_action_to_car(self, dir: str):
        if dir == "forward":
            self.bt.serial_write_string("f")
            log.info("Sending forward command")
        elif dir == "backward":
            self.bt.serial_write_string("b")
            log.info("Sending back turn command")
        elif dir == "left":
            self.bt.serial_write_string("l")
            log.info("Sending left turn command")
        elif dir == "right":
            self.bt.serial_write_string("r")
            log.info("Sending right turn command")
        elif dir == "halt":
            self.bt.serial_write_string("h")
            log.info("Sending halt command")
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
        if test.g_cmd_gotten_by_python():
            arduino_received_cmd = True
            print("Arduino received cmd!")

        else:
            # Supposed uid: 0x%%%uid$$$, two % eaten by g_cmd_gotten_by_python, string left 0x%uid$$$
            temp_uid = test.get_UID()
            if temp_uid:
                uid = temp_uid
                uid = uid[4:-6] # Strip 0x%% and $$$
                uid = uid.upper() # Make uid upper case for server recognition
                print(f"UID received: {uid}")
                
    test.end_process()

''' 藍芽控制測試    
    while(1):
        comm = input("command: ")
        if(comm == 'f'):
            test.send_action_to_car("forward")
        elif(comm == 'b'):
            test.send_action_to_car("backward")
        elif(comm == 'r'):
            test.send_action_to_car("right")
        elif(comm == 'l'):
            test.send_action_to_car("left")'''
    

''' 十字地圖測試
    test.send_action_to_car("forward")
    test.send_action_to_car("right")
    test.send_action_to_car("backward")
    test.send_action_to_car("right")
    test.send_action_to_car("backward")
    test.send_action_to_car("right")
    test.send_action_to_car("backward")
    test.send_action_to_car("right")
'''

''' BT control write()測試
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