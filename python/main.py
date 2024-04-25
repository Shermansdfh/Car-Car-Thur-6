import argparse
import logging
import os
import sys
import time

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
    parser.add_argument("mode", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument(
        "--team-name", default=TEAM_NAME, help="Your team name", type=str
    )
    parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    return parser.parse_args()


def main(mode: int, bt_port: str, team_name: str, server_url: str, maze_file: str):
    maze = Maze(maze_file)
    point = ScoreboardServer(team_name, server_url)
    # point = ScoreboardFake("your team name", "data/fakeUID.csv") # for local testing
    interface = BTInterface(port=bt_port)
    # TODO : Initialize necessary variables
    routes = [] # ["fbrl", "fbrl", "fbrl", "fbrl",]

    if mode == "0":
        log.info("Mode 0: For treasure-hunting")
        
        interface.start()
        arduino_received_cmd = False
        
        while True:
            uid = interface.ReadUID()
            if (uid == 0):
                continue
            else:
                score, time_remaining = point.add_UID(uid)
                current_score = point.get_current_score()
                log.info(f"Current score: {current_score}")
                time.sleep(1)
        
            if (interface.get_string() == "g"):
                arduino_received_cmd = True
                
            if (routes[0] == ""):
                    routes.pop(0)
                    
            if (arduino_received_cmd):
                arduino_received_cmd = False
                if (routes[0][0] == "f"):
                    interface.send_action("forward")
                elif (routes[0][0] == "b"):
                    interface.send_action("backward")
                elif (routes[0][0] == "r"):
                    interface.send_action("left")
                elif (routes[0][0] == "l"):
                    interface.send_action("right")
                routes[0] = routes[0][1:]
            else: continue
            
            msgWrite = input()
            if msgWrite == "exit":
                sys.exit()
            
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible

    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.

    else:
        log.error("Invalid mode")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))
