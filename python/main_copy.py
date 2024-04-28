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

    def send_action_from_routes(routes: list):
        if routes[0][0] == "f":
            interface.send_action_to_car("forward")
        elif routes[0][0] == "b":
            interface.send_action_to_car("backward")
        elif routes[0][0] == "l":
            interface.send_action_to_car("left")
        elif routes[0][0] == "r":
            interface.send_action_to_car("right")
        routes[0] = routes[0][1:]
        return
    
    def uid_gotten() -> bool:
        start_time = time.time()
        temp_uid = interface.get_UID()
        while not temp_uid:
            temp_uid = interface.get_UID()
            if time.time() - start_time > 2.5: 
                # If the car hasn't received any uid after 0.3s, uid isn't gotten.
                log.info("UID not gotten")
                return False
        if temp_uid:
            # UID format: 0x%%%uid$$$
            uid = temp_uid
            log.info(f"UID before strip: {uid}")
            uid = uid[8:-6] # Strip 0x%%% and $$$
            uid = uid.upper() # Make UID upper case for server recognition
            log.info(f"UID received(after strip): {uid}")
            
            # Scoreboard update
            score, time_remaining = point.add_UID(uid)
            current_score = point.get_current_score()
            log.info(f"Current score: {current_score}")
            time.sleep(1)
        return True
                
        
    if mode == "0":
        log.info("Mode 0: For treasure-hunting")
        interface.start()
        uid_gotten_in_prev_dead_end = True
        
        while True:
            if not routes: 
                # If routes is totally empty, the car should stop.
                interface.send_action_to_car("halt")
                log.info(f"Routes empty, halting")
                sys.exit(1)
                
            if interface.g_cmd_gotten_by_python():
                log.info("Arduino received cmd!")
                send_action_from_routes(routes)
                
                if not uid_gotten_in_prev_dead_end:
                    """
                    If uid was not gotten when walking into previous dead end, 
                    it should be gotten now. This is because the car might have missed
                    the UID at the previous dead end due to timing issues or other factors.
                    Getting the UID now ensures that we don't miss any treasure locations.
                    """
                    uid_gotten()
                
                # No matter if uid was gotten or not now, it should be set to True,
                # since we dont want to take away unwanted information
                uid_gotten_in_prev_dead_end = True 
            else:
                log.info(f"Arduino didn't receive cmd")
            
            if (routes[0] == ""):
                """
                When the last 'b' is sent, which means the car is on its way to dead end, 
                clean up empty sting in the routes list, and start getting uid.
                """
                routes.pop(0)
                uid_gotten_in_prev_dead_end = uid_gotten()
                
            log.info(f"Routes left: {routes}")
            
    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
    else:
        log.error("Invalid mode")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))