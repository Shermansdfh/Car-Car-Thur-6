import argparse
import logging
import os
import sys
import time

import re

import numpy as np
import pandas

from BTinterface import BTInterface
from maze import Action, Maze
from score import ScoreboardServer, ScoreboardFake
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# TODO : Fill in the following information
TEAM_NAME = "Thur-6"
SERVER_URL = "http://140.112.175.18:5000/"
MAZE_FILE = "data/small_maze.csv"
BT_PORT = "COM5"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="0", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument(
        "--team-name", default=TEAM_NAME, help="Your team name", type=str
    )
    parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    return parser.parse_args()


def main(mode: int, bt_port: str, team_name: str, server_url: str, maze_file: str):
    # maze = Maze(r"C:\Users\88696\Downloads\medium_maze.csv")
    # point = ScoreboardFake("your team name", "data/fakeUID.csv") # for local testing
    point = ScoreboardServer(team_name, server_url)
    interface = BTInterface(port=bt_port)
    routes = ["flb", "fb"]

    if mode == "0":
        log.info("Mode 0: For treasure-hunting")
        
        interface.start()
        arduino_received_cmd = False
        
        while True:
            if interface.g_cmd_gotten_by_python():
                arduino_received_cmd = True
                log.info("Arduino received cmd!")

            else:
                # Supposed uid: 0x%%%uid$$$, two % eaten by g_cmd_gotten_by_python, string left 0x%uid$$$
                temp_uid = interface.get_UID()
                if temp_uid:
                    if "670a" in temp_uid:
                        arduino_received_cmd = True
                        log.info(f"UID with g\n in it: {uid}")
                        log.info(f"Arduino received cmd!")
                    else:
                        uid = temp_uid
                        log.info(f"UID before strip: {uid}")
                        # uid = uid[4:-6] # Strip 0x% and $$$
                        uid = re.sub(r'^0x25*', '', uid) # Strip 0x and whatever number of "25" sticking with it
                        uid = re.sub(r'^0x25*', '', uid)
                        uid = uid[:-6] # Strip $$$
                        uid = uid.upper() # Make uid upper case for server recognition
                        log.info(f"UID received: {uid}")
    
                        score, time_remaining = point.add_UID(uid)
                        current_score = point.get_current_score()
                        log.info(f"Current score: {current_score}")
                        time.sleep(1)
            
            if (routes[0] == ""):
                routes.pop(0)
            
            if not routes:
                interface.send_action_to_car("halt")
                log.info(f"Routes empty, halting")
                sys.exit(1)
            
            if (arduino_received_cmd):
                arduino_received_cmd = False
                if (routes[0][0] == "f"):
                    interface.send_action_to_car("forward")
                elif (routes[0][0] == "b"):
                    interface.send_action_to_car("backward")
                elif (routes[0][0] == "l"):
                    interface.send_action_to_car("left")
                elif (routes[0][0] == "r"):
                    interface.send_action_to_car("right")
                routes[0] = routes[0][1:]
            else: 
                log.info(f"Arduino didn't receive cmd")
                continue
            
            log.info(f"Routes left: {routes}")
                
            
    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
    else:
        log.error("Invalid mode")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
