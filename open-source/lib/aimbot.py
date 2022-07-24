import ctypes
import cv2
import json
import math
import mss
import numpy as np
import os
import sys
import time
import torch
import uuid
import win32api
import string
import random
import configparser
from termcolor import colored

title_gen = string.ascii_letters
title_str = ''.join(random.choice(title_gen) for i in range(30))

config = configparser.ConfigParser()
config.read('configuration_settings.ini')
size_of_window_str = config['settings']['size_of_window']
size_of_window = int(size_of_window_str)

confidence_threshold = config.getfloat('settings', 'confidence_threshold')
NMS_IoU = config.getfloat('settings', 'nms_iou')
get_mouse_delay = config.getfloat('settings', 'mouse_delay')

get_pixel_increse = config.getfloat('settings', 'pixel_increse')
get_pixel_increse_str = str(get_pixel_increse)

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class Aimbot:
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    screen = mss.mss()
    pixel_increment = get_pixel_increse #controls how many pixels the mouse moves for each relative movement
    with open("lib/config/config.json") as f:
        sens_config = json.load(f)
    aimbot_status = colored("Enabled", 'green')

    def __init__(self, box_constant = size_of_window, collect_data = False, mouse_delay = get_mouse_delay, debug = False): # original mouse delay == 0.0001
        self.box_constant = box_constant

        # print("[INFO] Loading the neural network model")
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path='lib/best.pt', force_reload = True)
        if torch.cuda.is_available():
            print(colored("\nGPU Utilization [Supported]", "green"))
        else:
            print(colored("[!] CUDA ACCELERATION IS UNAVAILABLE", "red"))
            print(colored("[!] Check your PyTorch installation, else performance will be poor", "red"))

        self.model.conf = confidence_threshold # base confidence threshold (or base detection (0-1) original is 0.45
        self.model.iou = NMS_IoU # NMS IoU (0-1) Original is 0.45
        self.collect_data = collect_data
        self.mouse_delay = mouse_delay
        self.debug = debug

        print("[F2] Toggle Aim Assist\n[F4] Force Close Script")
        print("[X]  Aimbot Trigger Key")

    def update_status_aimbot():
        if Aimbot.aimbot_status == colored("Enabled", 'green'):
            Aimbot.aimbot_status = colored("Disabled", 'red')
        else:
            Aimbot.aimbot_status = colored("Enabled", 'green')
        sys.stdout.write("\033[K")
        print(f"Aimbot Status; [{Aimbot.aimbot_status}]", end = "\r")

    def left_click():
        ctypes.windll.user32.mouse_event(0x0002) #left mouse down
        Aimbot.sleep(0.0001)
        ctypes.windll.user32.mouse_event(0x0004) #left mouse up

    def sleep(duration, get_now = time.perf_counter):
        if duration == 0: return
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    def is_aimbot_enabled():
        return True if Aimbot.aimbot_status == colored("Enabled", 'green') else False

    def is_targeted():
        return True if win32api.GetKeyState(0x58) in (-127, -128) else False

    def is_target_locked(x, y):
        #plus/minus 5 pixel threshold
        threshold = 5
        return True if 1280 - threshold <= x <= 1280 + threshold and 720 - threshold <= y <= 720 + threshold else False

    def move_crosshair(self, x, y):
        if Aimbot.is_targeted():
            scale = Aimbot.sens_config["targeting_scale"]
        else:
            return #TODO

        if self.debug: start_time = time.perf_counter()
        for rel_x, rel_y in Aimbot.interpolate_coordinates_from_center((x, y), scale):
            # print("rel x, "+str(rel_x) + "rel_y:"+str(rel_y))
            Aimbot.ii_.mi = MouseInput(rel_x, rel_y, 0, 0x0001, 0, ctypes.pointer(Aimbot.extra))
            input_obj = Input(ctypes.c_ulong(0), Aimbot.ii_)
            ctypes.windll.user32.SendInput(1, ctypes.byref(input_obj), ctypes.sizeof(input_obj))
            if not self.debug: Aimbot.sleep(self.mouse_delay) #time.sleep is not accurate enough
        if self.debug: #remove this later
            print(f"TIME: {time.perf_counter() - start_time}")
            print("DEBUG: SLEEPING FOR 1 SECOND")
            time.sleep(1)

    #generator yields pixel tuples for relative movement
    def interpolate_coordinates_from_center(absolute_coordinates, scale):
        diff_x = (absolute_coordinates[0] - 1280) * scale/Aimbot.pixel_increment/2
        diff_y = (absolute_coordinates[1] - 720) * scale/Aimbot.pixel_increment/2
        # print("diff x" + str(diff_x) + ",diff_y" + str(diff_y))
        length = int(math.dist((0,0), (diff_x, diff_y)))
        if length == 0: return
        
        unit_x = (diff_x/length) * Aimbot.pixel_increment
        unit_y = (diff_y/length) * Aimbot.pixel_increment
        x = y = sum_x = sum_y = 0
        for k in range(0, length):
            sum_x += x
            sum_y += y
            x, y = round(unit_x * k - sum_x), round(unit_y * k - sum_y)
            # print("x," + str(x) +"y:" + str(y) )
            yield x, y
            

    def start(self):
        Aimbot.update_status_aimbot()
        half_screen_width = 1280 #this should always be 960
        half_screen_height = 720 #this should always be 540
        detection_box = {'left': 780, #x1 coord (for top-left corner of the box)
                          'top': 220, #y1 coord (for top-left corner of the box)
                          'width': 1000,  #width of the box
                          'height': 1000} #height of the box
        if self.collect_data:
            collect_pause = 0

        while True:
            start_time = time.perf_counter()
            try:
                frame = np.array(Aimbot.screen.grab(detection_box))
                if self.collect_data: orig_frame = np.copy((frame))
                results = self.model(frame)

                if len(results.xyxy[0]) != 0: #player detected
                    least_crosshair_dist = closest_detection = player_in_frame = False
                    for *box, conf, cls in results.xyxy[0]: #iterate over each player detected
                        x1y1 = [int(x.item()) for x in box[:2]]
                        x2y2 = [int(x.item()) for x in box[2:]]
                        x1, y1, x2, y2, conf = *x1y1, *x2y2, conf.item()
                        height = y2 - y1
                        relative_head_X, relative_head_Y = int((x1 + x2)/2), int((y1 + y2)/2 - height/2.7) #offset to roughly approximate the head using a ratio of the height
                        own_player = x1 < 15 or (x1 < self.box_constant/5 and y2 > self.box_constant/1.2) #helps ensure that your own player is not regarded as a valid detection

                        #calculate the distance between each detection and the crosshair at (self.box_constant/2, self.box_constant/2)
                        crosshair_dist = math.dist((relative_head_X, relative_head_Y), (self.box_constant/2, self.box_constant/2))

                        if not least_crosshair_dist: least_crosshair_dist = crosshair_dist #initalize least crosshair distance variable first iteration

                        if crosshair_dist <= least_crosshair_dist and not own_player:
                            least_crosshair_dist = crosshair_dist
                            closest_detection = {"x1y1": x1y1, "x2y2": x2y2, "relative_head_X": relative_head_X, "relative_head_Y": relative_head_Y, "conf": conf}

                        if not own_player:
                            pass
                            # cv2.rectangle(frame, x1y1, x2y2, (244, 113, 115), 2) #draw the bounding boxes for all of the player detections (except own)
                            # cv2.putText(frame, f"{int(conf * 100)}%", x1y1, cv2.FONT_HERSHEY_DUPLEX, 0.5, (244, 113, 116), 2) #draw the confidence labels on the bounding boxes
                        else:
                            own_player = False
                            if not player_in_frame:
                                player_in_frame = True

                    if closest_detection: #if valid detection exists
                        # cv2.circle(frame, (closest_detection["relative_head_X"], closest_detection["relative_head_Y"]), 5, (115, 244, 113), -1) #draw circle on the head

                        # #draw line from the crosshair to the head
                        # cv2.line(frame, (closest_detection["relative_head_X"], closest_detection["relative_head_Y"]), (self.box_constant//2, self.box_constant//2), (244, 242, 113), 2)

                        absolute_head_X, absolute_head_Y = closest_detection["relative_head_X"] + detection_box['left'], closest_detection["relative_head_Y"] + detection_box['top']

                        x1, y1 = closest_detection["x1y1"]
                        # if Aimbot.is_target_locked(absolute_head_X, absolute_head_Y):
                        #     cv2.putText(frame, "LOCKED", (x1 + 40, y1), cv2.FONT_HERSHEY_DUPLEX, 0.5, (115, 244, 113), 2) #draw the confidence labels on the bounding boxes
                        # else:
                        #     cv2.putText(frame, "TARGETING", (x1 + 40, y1), cv2.FONT_HERSHEY_DUPLEX, 0.5, (115, 113, 244), 2) #draw the confidence labels on the bounding boxes

                        if Aimbot.is_aimbot_enabled():
                            Aimbot.move_crosshair(self, absolute_head_X, absolute_head_Y)

                # if self.collect_data and time.perf_counter() - collect_pause > 1 and Aimbot.is_targeted() and Aimbot.is_aimbot_enabled() and not player_in_frame: #screenshots can only be taken every 1 second
                #     cv2.imwrite(f"lib/data/{str(uuid.uuid4())}.jpg", orig_frame)
                #     collect_pause = time.perf_counter()
                # cv2.putText(frame, f"FPS: {int(1/(time.perf_counter() - start_time))}", (5, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (113, 116, 244), 2)
                # cv2.imshow(title_str, frame)
            except Exception as e:
                print(e)
                print("try restart")
                os.execv(sys.executable, ['python'] + sys.argv)
            if cv2.waitKey(1) & 0xFF == ord('0'):
                break

    def clean_up():
        Aimbot.screen.close()
        os._exit(0)

if __name__ == "__main__": print("You are in the wrong directory and are running the wrong file; you must run NuremX.py")
