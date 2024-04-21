import logging
from typing import Optional
from time import sleep

from BT import Bluetooth

log = logging.getLogger(__name__)

# hint: You may design additional functions to execute the input command,
# which will be helpful when debugging :)


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

    def start(self):
        input("Press enter to start.")
        self.bt.serial_write_string("s")
        return

    def get_UID(self):
        return self.bt.serial_read_byte()

    def send_action(self, dir):
    # send the action to car
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
    test.send_action("forward")  # Move the car forward
    sleep(2)  
    test.send_action("left")  # Turn left
    sleep(1)  
    test.send_action("right")  # Turn left
    sleep(1)  
    test.send_action("right")  # Turn left
    sleep(1)  
    test.send_action("left")  # Turn left
    sleep(1)  
    test.send_action("backward")  # Turn left
    sleep(1)  
    test.end_process() 