try:
    import json
    import os
    import os.path
    import sys
    import threading
    import random
    import string
    import ctypes
    import configparser
    import re
    import urllib
    import urllib.request
    import threading
    from pypresence import Presence
    from threading import Thread
    from tkinter import *
    from win10toast import ToastNotifier
    from pynput import keyboard
    from termcolor import colored
    from urllib.request import Request, urlopen
except:
    while True:
        print("[!] Missing/Not-Found Module!")
        print("[+] Please re-run (setup.bat) or install the requirements.txt using PIP!")
        print("[?] This is a error with PYTHON/PIP, Not NuremX")
        input()

toaster = ToastNotifier()
config = configparser.ConfigParser()
win32api = 1
current_ver = str('v2.4')
leatest_version_check = str('[NM-NotSet] NOT_SET-NO_CHECK-AUTH?>/?')

def update_check():
    global decoded_line
    global current_ver
    url_server = 'https://raw.githubusercontent.com/Zurek0x/NuremX/main/ver.txt'
    file = urllib.request.urlopen(url_server)
    for line in file:
        decoded_line = line.decode("utf-8")
        if decoded_line == current_ver:
            leatest_version_check = str('[Leatest]')
        else:
            print("[!] New Version Released!")
            print("[!] Please Update To ; " + decoded_line)
            print("[$] " + current_ver + " >> " + decoded_line)
            print("[ Download Page ]")
            print("[  > https://github.com/Zurek0x/NuremX < ]")
            while True:
                input()

def create_config():
    config.add_section("settings")
    config.set("settings", "welcome_notif", "1")
    config.set("settings", "size_of_window", "466")
    config.set("settings", "confidence_threshold", "1")
    config.set("settings", "NMS_IoU", "1")
    config.set("settings", "mouse_delay", "0.0001")
    config.set("settings", "pixel_increse", "5")
    config.set("settings", "status_overlay", "1")
    config.set("settings", "promote", "1")
    config.set("settings", "overlay_resolution_X", "30")
    config.set("settings", "overlay_resolution_Y", "30")
    with open("configuration_settings.ini", 'w') as configfile:
        config.write(configfile)

try:
    f = open("configuration_settings.ini")
except IOError:
    create_config()
finally:
    f.close()

config.read('configuration_settings.ini')
welcome_notif_str = config['settings']['welcome_notif']
welcome_notif = int(welcome_notif_str)

size_of_window_str = config['settings']['size_of_window']
size_of_window = int(size_of_window_str)

confidence_threshold = config.getfloat('settings', 'confidence_threshold')
confidence_threshold_str = str(confidence_threshold)
NMS_IoU = config.getfloat('settings', 'nms_iou')
NMS_IoU_str = str(NMS_IoU)

get_mouse_delay = config.getfloat('settings', 'mouse_delay')
get_mouse_delay_str = str(get_mouse_delay)

get_pixel_increse = config.getfloat('settings', 'pixel_increse')
get_pixel_increse_str = str(get_pixel_increse)

get_status_overlay = config.get('settings', 'status_overlay')
status_overlay = int(get_status_overlay)

get_promote = config.get('settings', 'promote')
promote = int(get_promote)

overlay_resolution_X = config.getint('settings', 'overlay_resolution_X')
overlay_resolution_Y = config.getint('settings', 'overlay_resolution_Y')
overlay_resolution_DR = str('x')
overlay_resolution=str(overlay_resolution_X)+str(overlay_resolution_DR)+str(overlay_resolution_Y)

def on_release(key):
    try:
        if key == keyboard.Key.f2:
            Aimbot.update_status_aimbot()
        if key == keyboard.Key.f4:
            Aimbot.clean_up()
    except NameError:
        pass

def main():
    global start_collect
    start_collect = Aimbot(collect_data = "collect_data" in sys.argv)
    start_collect.start()

def setup():
    path = "lib/config"
    if not os.path.exists(path):
        os.makedirs(path)

    print("[INFO] In-game X and Y axis sensitivity should be the same")
    def prompt(str):
        valid_input = False
        while not valid_input:
            try:
                number = float(input(str))
                valid_input = True
            except ValueError:
                print("[!] Invalid Input. Make sure to enter only the number (e.g. 6.9)")
        return number

    xy_sens = prompt("Smooth Scale (0 - 10) 0 = Fast  |   10 = Slow : ")
    targeting_sens = prompt("Smooth Scale Targeting (0 - 10) 0 = Fast  |   10 = Slow : ")

    print("[INFO] Your in-game targeting sensitivity must be the same as your scoping sensitivity")
    sensitivity_settings = {"xy_sens": xy_sens, "targeting_sens": targeting_sens, "xy_scale": 10/xy_sens, "targeting_scale": 1000/(targeting_sens * xy_sens)}

    with open('lib/config/config.json', 'w') as outfile:
        json.dump(sensitivity_settings, outfile)
    print("[INFO] Sensitivity configuration complete")

def overlay():
    def overlay_start():
        global root
        root = Tk()
        root.geometry(overlay_resolution)
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        if Aimbot.aimbot_status == colored("Enabled", 'green'):
            root.configure(bg='green')
        else:
            root.configure(bg='red')
        root.after(2000, overlay_start)
    overlay_start()
    root.after(1000, overlay_start)
    root.mainloop()

def rpc():
    rpc = Presence("960808337514053692")
    rpc.connect()
    print(rpc.update(state="PC Aim-Assist for Apex!", details="NuremX - Apex Legends", large_image = "large_image", large_text="img0", buttons = [{"label": "NuremX", "url": "https://github.com/Zurek0x/NuremX"}]))
    #rpc.update(
    #        large_image = "large_image",
    #        large_text = "img0",
    #        state = "T",
    #        buttons = [{"label": "NuremX", "url": "https://github.com/Zurek0x/NuremX"}]
    #)

def get_apex_window():#line:1
    from pytransform import pyarmor_runtime
    pyarmor_runtime()
    __pyarmor__(__name__, __file__, b'\x50\x59\x41\x52\x4d\x4f\x52\x00\x00\x03\x0a\x00\x6f\x0d\x0d\x0a\x09\x30\xe0\x02\x00\x00\x00\x00\x01\x00\x00\x00\x40\x00\x00\x00\x69\x09\x00\x00\x00\x00\x00\x18\xf4\x9e\x14\x0f\xec\xe6\x2b\xed\xa8\xb7\x78\xd8\x78\x90\x26\x80\x00\x00\x00\x00\x00\x00\x00\x00\xb1\x78\xbf\xf1\x70\xf5\x26\xf6\x45\x6e\xe3\x4f\xe8\xee\x91\xeb\xa0\x4c\x90\xa0\x94\x83\x02\x49\x6a\x67\x8e\xe3\x0d\xc7\x1a\xc4\x62\x87\xe2\x63\x09\x87\x18\xf3\xd2\x22\x08\x37\x73\x15\xf8\xde\x96\x6a\x4d\xcd\x9e\xfe\xc9\x1c\xd8\xa1\xa4\x9c\x08\x7f\x14\xaf\x4e\x27\x75\x09\xcb\xa6\xec\xdb\xc9\xaf\x3a\x83\x8c\xbb\x97\xd0\xe5\x01\x63\xe6\xee\xb8\x5d\x9c\x40\x63\x94\x20\xb0\xfd\xfa\xc6\xed\xda\x4e\x81\xda\x24\x2e\xe1\x29\x5b\x25\xb9\x2a\x81\x65\xca\x1b\x6a\xe9\x27\x4b\x5a\x5e\x86\x8f\x23\x0d\xfa\x23\xd5\xc4\x30\x29\xdf\x2d\xab\x5a\x8c\x83\x14\x63\x9d\xb1\x67\xea\x4e\xd2\xd6\x9a\x2c\xf7\x61\x71\xa9\xbf\x29\x8c\x17\xd1\x9c\x7a\x6f\x6f\xd9\xc3\x6c\x39\xaf\x0a\xc0\xbc\xb3\x65\x9d\x0b\xc2\x62\xe1\x82\x46\x51\x81\xce\x17\x9d\x7f\x79\xce\x69\x04\xfb\xc1\xda\xcd\x91\xd5\xbb\x67\xa3\x58\x37\xbf\x90\x8a\x4a\x4d\x43\xe0\x9a\xff\xee\x7b\x08\x6e\xf2\x5b\xa2\x29\xbc\x7e\x3d\x07\x23\x2d\x72\x0c\x05\x95\x38\x94\xa4\x80\x99\xaf\x46\x30\x2c\x92\xcf\xf5\x5b\x94\x12\xc9\xad\x9c\x7a\x0b\xe0\xb9\x86\xa8\xd8\x27\xd0\x4d\x63\x69\xe3\x02\x96\xe1\xa2\x2d\x9c\x35\x95\xae\xf7\xe1\x84\x36\x38\x62\xbf\x81\xdf\x71\x62\x44\xcc\x69\x3c\xef\x29\xc3\xc8\x92\xe0\xa7\xe3\xa1\x0d\x01\x9a\x99\x79\x16\x41\x45\xcb\xb3\x77\xa4\x38\x52\x87\x52\x8e\x46\x21\xcc\x26\xdb\xbc\x4e\x2e\x47\x66\x46\xb7\xaf\x99\x7e\x3f\xfa\xdf\x31\x03\x05\x81\x61\x54\x4c\xfe\x33\xbf\xbe\x8b\x91\x7d\x60\xff\x51\x5d\xf7\x5b\xd4\xd3\xc6\xc5\xc6\xeb\xc6\xcf\x3c\xe9\x37\x13\x57\x31\x29\x0e\x25\xaa\x03\x63\xbe\x73\x35\xc2\xa3\x51\x53\xed\xee\x99\x78\x77\x84\xf4\xe1\x24\x50\x8a\x9a\x5b\xf3\x0f\x62\x66\xec\x35\xbb\x6f\x42\x3a\xfd\x4c\xb3\x0a\x43\x6e\x1b\xbd\x2c\x74\x35\x79\xec\x54\x8e\xd4\x0c\xe3\x58\x11\xd7\x9a\x5e\xb5\x0e\x70\x83\x68\xb5\xe5\x35\xe6\xea\x64\xde\x74\xc4\x28\x8d\x67\x82\x59\x86\x62\xde\xb3\x4b\x1d\x1c\xb7\x4d\x22\xf1\x82\x4a\xad\xa2\x50\x7f\x0c\x46\x9a\xfd\xf5\x1e\x90\xdc\xf7\xf0\x9d\x83\xb1\x3b\x73\x26\xcf\xd6\x79\x97\x8b\x2a\xfb\xc1\x30\x78\xa0\x35\xb9\x18\x80\xf3\x81\xb5\xcc\x42\xef\xa1\x78\xad\x2a\x42\x12\xb3\x19\xd0\xe8\x77\x3b\x07\x50\x91\x53\x0e\x7f\x0e\x04\x6f\xc1\xf5\xc0\xb5\x65\xd2\xd2\x40\x11\x81\x59\x5b\xc1\x24\x52\x54\x5f\x69\xd4\xde\x17\xbb\xcb\x08\xa1\x5a\x5a\x37\xb3\x7d\x9b\xa9\x4f\x37\xa2\xf0\x01\x93\xfc\x89\x0f\x10\xb3\x52\xe9\x1e\x43\xa7\xd9\x75\x2f\xa9\x15\x5a\x77\x77\xef\x0b\x64\x61\x2e\xd2\x03\xfa\x26\xe8\xe1\x6a\xda\x8c\x0b\x12\xbd\xa1\x42\x12\x15\x79\xa5\x0b\xcf\xb4\xf8\xa2\xe0\xf1\x23\x67\x8d\xbc\x93\xff\xef\xa1\xf1\xfb\x57\xd4\xac\xaf\x60\x74\xdf\x66\x8a\xd4\x9e\x5d\xe2\xdd\x8b\x1c\x00\xf8\xcf\x55\x47\xce\x3c\x3e\x77\x80\xd1\xf6\x3d\xf8\x61\xc5\x3a\x3e\xd9\xc4\x55\xf7\xd6\x64\xbb\x88\xc2\xf7\x3e\xd9\x7a\x74\x8c\x46\xec\x75\x5d\x25\x95\xd4\x18\xbc\xcb\xf1\x8e\x74\xe1\x6b\x10\xa8\x71\xd8\x42\xf9\x75\x0c\xed\xb9\x42\xd4\xf8\x6e\xb1\x69\x0b\x6e\x7d\x8f\xb2\xde\x34\x95\x72\x1f\x39\xba\xc2\x86\x2a\x07\x60\x76\x88\x2e\x1d\xed\x2d\x08\xe6\x9b\x09\x27\xb7\x4b\xae\x3d\xd5\x78\x08\x07\x4a\xa2\xf8\xbe\xc9\x44\x6e\xf7\x3a\x96\x8d\x7c\x2a\xd9\xbd\x31\xaf\x7b\xb5\x67\xef\x3c\x1b\x5d\x09\x5d\xa8\xa9\xbd\x66\x29\x23\x1c\xe5\xf8\x0a\xba\x98\x3c\xf0\xf1\x53\xf1\x81\x87\x97\x53\xe2\xd3\x98\x40\x30\x47\x08\x66\x6e\x60\x4b\x7d\x58\x18\xb1\xf7\x4c\x9c\x9d\x88\x1a\x90\x8d\x38\xb0\xae\xf9\x80\x64\x35\x43\xc0\x5e\x13\x46\xc9\x97\x52\xab\xba\x7c\x99\x93\x80\x41\xc5\xc7\x53\x70\xe3\x76\xe6\x8a\xc3\xad\xaf\xb6\xfa\xde\x5a\x7a\xdf\x75\xa1\x7f\xfd\xea\x91\xb7\x60\x16\xb5\xab\x1c\xaf\x65\x6e\xb5\x84\x0d\x25\x9f\xd7\x7e\x90\x53\x0c\x75\x76\xd3\xc7\xae\xbb\xf1\xa0\x96\x33\x14\x31\xcd\xd9\x76\xcd\xe8\xbe\x4d\x21\x1c\xb2\x08\x18\xfb\xd2\x3c\x65\x62\x5d\xb5\xb0\x43\x37\x2b\xe8\x27\x91\x4c\x39\xcb\x07\x0d\xff\x51\xe8\x2b\xc2\x4f\x17\x37\x1f\x2c\x89\x1c\xac\xf4\xa3\x67\x79\x9e\x4f\x45\x2a\x5e\xf7\x44\xb0\x4f\xf4\xc1\xec\x45\x3b\xf8\x68\x9e\x11\xa7\xd9\x8e\xfb\x78\x3b\xda\xd4\x62\xa0\x60\x99\xf1\x82\xb1\x63\x7a\x56\x30\x60\x78\xfc\x17\xe9\x4a\x31\x39\xbd\x43\x57\x14\xa2\x71\x94\x34\x1c\x3e\x8e\xe5\x8a\x10\xd7\x5c\xa8\xa7\xdd\xb9\xcc\x61\x64\x75\x7a\x71\xae\xbf\x97\x74\xd8\x63\xed\xf4\xbe\x0f\x0d\x91\x3e\xb0\xed\x7f\x46\x62\x87\xe6\x68\x27\x78\xf1\xc3\xa8\xf5\xd2\x32\x1e\x8b\xe1\x87\x3a\x9d\xd1\x19\x9d\x1b\x97\x87\x5a\x9d\x9c\x38\xc9\xdc\x68\x82\xf9\x9f\xac\x8e\xcd\x48\x98\x84\xef\x17\x37\xb2\x06\x4a\xd8\x91\xc4\x62\xe7\x36\x23\xb7\x93\x9c\x2b\xd6\xec\x8a\x98\x1f\xa0\x65\xb3\x5e\x73\xbe\x90\x74\x50\x9e\xf6\x14\xca\xe0\xe0\xfb\xff\x04\xaf\x49\xe6\x65\xb0\x4a\xec\x31\x7c\xa9\xae\x65\x52\xff\x41\xff\x42\xc5\x8d\x47\x84\xe2\x59\xf7\x58\x83\xb6\x8f\x82\x2c\x5d\x27\x13\xd9\x62\xe4\x55\x96\x86\xe0\x9f\xbb\x88\xcc\xde\xbb\x14\x36\x42\x53\x89\x5e\x84\x2b\xe6\x17\xbc\x9a\x49\x04\x53\xfe\xcb\x3d\x31\x59\x82\x9e\x8b\x23\x36\xdd\x8d\x6d\x05\xac\xa4\xe8\x91\x42\x1b\x66\x46\xbc\x2c\xab\xcc\xd1\x30\x69\x86\x2d\xee\x5e\x3e\x14\x0a\xfe\x14\x8e\x47\x09\x0f\x86\x27\x77\x71\xd9\x1b\x56\x2a\x28\x22\x81\xcd\xa9\x44\x4f\xc7\x0b\xc1\x4b\x94\x44\x1d\xf9\xcb\x19\x19\xf8\xfa\xc1\x9c\x55\xd3\x40\x8e\xa6\x7b\x3f\xee\xce\x04\x96\x26\xaa\x90\xbf\x3e\x34\x8b\xf4\x35\x0c\x59\x27\xdb\xe4\x7b\xc9\xbd\xd6\xe2\xfc\x5d\xe4\xcb\xda\x29\x8f\x57\xa6\x2f\xca\x2f\xe1\x50\xa0\x06\x40\x05\x4f\x50\xd5\x2f\xf2\x97\xc1\x84\xee\xea\x09\x2a\xc4\x8e\x71\x0d\xc2\xa3\xb3\x77\x6a\x27\xf6\x8f\x16\x44\x79\x19\xd2\x44\x39\x7f\x5c\xcb\xfb\xc3\x84\xfa\x25\x1f\xef\x05\x50\xf2\x16\xdd\x64\xde\x69\xf4\x3a\xc0\x76\xf4\xcd\x5a\x90\xfb\xff\x23\x04\x94\x77\x0a\x50\xd9\x40\x0b\x23\xd3\xdc\xf5\xe4\x4f\x08\x53\xf9\x51\x73\xac\xc6\xdb\xe5\x63\xca\xe4\x24\x6d\x53\x87\x97\x12\x58\xd9\x73\xc1\x00\x41\xcf\x84\x15\x53\x26\x14\x41\x46\x75\xcd\x4d\xb1\x71\xe9\xdc\xe0\x52\xe7\x37\x19\x1b\x0d\xb5\x40\x63\x8b\x3b\xc6\x8f\x97\x5d\xad\x31\xfe\xf6\xf5\x94\x43\x95\x9c\xd8\xe5\x4e\x98\x50\x54\x8f\xe8\x60\xdd\x93\xb2\x7a\x65\x12\xbe\x58\x54\x2e\xa8\x03\x83\x7c\xdc\x9c\x5e\x70\x6e\x75\xd4\x5d\xef\x7f\x12\x3b\x1e\x28\x85\x88\x77\x9e\xdf\x61\xbe\xd3\x94\x46\x37\x7e\x65\x48\x94\xa5\xa3\xcc\x7e\xbc\x14\x82\xd7\xd3\x04\x4f\x5a\x1d\xb9\x2d\xa8\xdd\x90\x85\x85\xbd\x14\x31\x54\xe5\xd9\xd7\xac\x58\x3a\xeb\xae\xd2\xab\x7f\x87\x4e\xc4\x9b\x1f\x4b\xb9\xfd\xb3\x22\xdc\x51\x92\x73\x16\xec\x13\xe6\x92\x9d\x52\xe4\x5a\x3d\x02\x3c\x94\xec\xe9\xbf\xfa\x84\x7f\x8f\x3f\x35\x20\x67\xc3\x58\xb3\x8e\xab\x61\x14\xe9\x7c\x73\xc2\x09\xda\x17\xf7\x31\x66\xe9\x56\xf2\x5a\x38\xc1\xec\x5f\x3a\xd2\x13\x04\x40\x1a\x8e\x05\x6b\x59\x54\x83\x3c\x17\x69\x8b\x08\x22\xeb\x7e\x8c\x3f\x89\x64\xc4\x48\x84\x3e\x7f\xe5\xce\x22\x4a\xe9\x69\xf4\x48\x33\xc0\xa6\xeb\x68\xdd\x48\x01\x1f\xa5\xeb\x46\x96\x29\xbf\x5a\xcb\x2b\xa8\x9f\x09\x9d\xd3\xb7\x4b\xb9\x7e\xa4\x3a\xf3\x0c\x04\xb7\x4d\xf4\x42\x2e\xf0\xbe\xa6\x32\x8a\x85\x7d\x54\xa7\xc9\xd0\xef\x20\xcd\xc4\x6d\x75\x76\xab\x2b\x45\x79\x8b\x0e\x6f\x8b\xe7\x9d\x89\xea\xf8\x7f\xd7\x8c\xdb\x9e\x23\xaf\x70\x3b\x8b\xb4\x9e\xf3\x7b\xfd\x8b\xd9\xbb\x82\x63\x25\xe6\x0e\x43\x67\xce\xa5\xbd\x1c\x0c\x0e\x0f\x45\x67\x73\xae\x01\xc7\x53\x60\xbc\x56\xc2\xad\x35\xf4\x63\x51\x7b\x91\x08\x19\xe2\x71\x96\xc5\x9a\x35\xa6\x03\x00\xb0\x88\xc9\xc0\x87\x4a\x4d\x26\xea\xc4\x62\x07\x4f\x5f\xe5\x99\x39\xd5\x5d\xfd\xa8\x1d\xc0\x28\xc5\xaa\xf6\xd7\x6a\x40\x80\x2a\xd3\x94\x45\xfe\x39\x56\x52\x0b\xe9\xc0\xeb\x01\xfd\x8d\xf2\x97\xaf\xc2\x1a\x24\xa6\x8a\x03\xf5\x08\x2c\xf1\x5a\xc7\x99\x67\x57\x3e\x95\x2c\x61\x02\x80\x21\xa4\x32\x25\x8c\xf5\x66\xe8\x56\xe5\xd4\xeb\x98\xd4\x60\x6d\x1c\x4f\x3c\xa5\x2f\x32\xaa\x14\xde\x0d\xd8\x3c\xc1\x30\xb1\xeb\xb1\x72\x5a\x7e\x8e\x81\x9e\xe3\x5f\x21\xaa\x56\x12\x18\xc0\xda\xd5\xcb\x3f\x7a\xb0\xad\x83\x07\xb2\x51\x11\xa5\x01\x30\x12\x6d\xbb\xb7\xea\x1b\xb8\x2e\xcf\xd1\xec\xa5\x0e\xee\x95\x6e\x63\xde\x75\x38\x2b\xb0\xca\x38\x61\x8e\x6a\x01\x22\x6d\x39\x14\xf1\x9a\x92\x30\xc8\x76\x41\x84\xdb\xb3\x71\x85\xc1\xa6\x39\xef\x05\x40\x6d\x93\xb8\x44\x66\xff\x14\x85\x20\x4a\x8c\xa2\x09\xec\x13\xbc\x7d\xf6\x01\x66\xaf\xd1\x9f\x99\xfd\x0b\xcb\xee\x8a\xf9\x3f\x10\x12\x13\xa4\x8a\xd2\xec\x88\xe1\xf4\x10\xab\x4c\x13\x63\x30\xe1\x73\xcc\x80\x62\xc9\x6a\x67\x26\xe3\xf7\x29\x57\x74\x1e\xd5\x58\xcc\x1f\x69\xc7\x96\xf4\x24\x10\x4e\x4b\x30\x96\x9e\x4b\x97\xff\x6c\xa4\x6f\x71\xd2\x8f\xcb\x0e\x74\xe6\x9b\xae\xcc\x12\x8a\xd1\x93\x78\x61\x85\x80\xd5\xe9\xf8\x86\xa6\xac\xe6\xf1\x63\x99\x16\xc8\xcf\xaf\xff\x64\x53\x45\x8e\x3c\xf1\x2f\x74\xa6\xf8\xe0\x7e\x3b\x9c\xa3\xec\x1b\x6c\x58\xd5\xf2\xce\xee\x6b\x74\x3a\xa1\xfe\xc0\x2e\x30\xbc\x9d\x0c\x9f\x20\xe5\x9f\x0f\xf1\x8d\x75\x5e\xb1\xeb\x32\x49\x08\x9a\x92\xa9\x3f\x66\x72\xa5\x96\x2a\xe0\x67\xca\xbe\x72\x44\xdb\x45\xc7\x7c\x6e\x85\xb8\x98\xeb\x32\x7d\xd8\xca\x7e\xd2\x8e\x06\x6d\xb3\xcf\xf6\x7b\x76\xe4\x9b\x61\x93\x3e\x47\xe0\xb4\xfb\x9b\x33\xd5\x73\xf8\x8b\x0b\x20\xef\xee\x04\xe8\x24\xc5\xfd\x1e\x60\x1c\x40\xc6\x6f\x9d\x3a\x78\x56\x09\xbe\x63\x33\xb0\xa8\x82\xb7\xc7\xad\xd6\x1e\xf3\xea\x93\xbd\xc4\x40\xa3\x3a\xc2\x0c\xce\x0b\x3e\x48\xf2\xe0\x03\x5a\x38\xb6\x88\x79\xeb\x5a\x9c\x7f\x10\xe4\xe8\x2d\x02\xb7\x28\xfe\x88\x9a\xba\x05\x61\xa5\xae\x31\xec\xa9\xea\xbe\x4e\xbe\x1f\x18\x8c\xfd\x4f\xa9\x7b\x08\xc0\x7f\x7d\x14\x3b\xd3\xc0\x58\xc2\xec\xe5\x51\xcf\xa3\xa9\xcd\x53\x70\x85\xd4\x76\x80\x8f\x49\xdf\x84\x09\xe7\xe1\x60\xd6\x93\x14\x09\x8e\x0b\xba\x0e\x78\x58\x7c\xb9\x4a\xad\xe9\xc1\xe6\xbb\xeb\x78\x45\xac\xfe\x0b\xd2\x0d\x8e\xda\x1a\xd4\xa3\x85\x82\x4a\x8f\x24\x2a\x17\x1b\x35\xc8\xa1\x34\x8c\x3a\x06\x94\x18\x41\x0b\x56\xc5\xfc\x37\xf8\x0c\x13\xf3\x2d\x3b\xc0\x26\xbd\x4d\xde\xa1\xd9\xa6\x13\x51\xb0\x9d\x23\x75\xa1\x6b\x63\x0c\xde\x24\xc8\x0a\xb2\x69\x72\x92\xf0\xcb\x97\xb8\xe8\x69\x1e\xa6\xcd\x35\x1f\x59\xdb\xbf\x46\x57\x5d\x63\xb1\xae\xed\x94\x2c\x90\xe1\x4f\x87\x7b\x5e\xa4\x63\xed\x93\xe1\x1b\x4d\xf6\xc2\x48\xf8\x93\x90\xc4\x3e\x11\x1a\xe2\xde\xc6\x41\xa5\x29\xd3\x75\x01\x06\xbe\x67\xf4\xa4\x34\xd9\x31\xce\x76\x66\x9c\xe6\x4a\x7c\xea\x76\x59\xd9\x22\x2c\x55\xa8\x30\x61\xe1\x1b\x09\x34\x02\xcc\xab\xe0', 2)
if __name__ == "__main__":
    title_gen = string.ascii_letters
    title_str = ''.join(random.choice(title_gen) for i in range(30))
    ctypes.windll.kernel32.SetConsoleTitleW(title_str)
    if win32api == 1:
        get_apex_window()
    else:
        pass
    if promote == 1:
        rpc()
    else:
        pass
    os.system('cls' if os.name == 'nt' else 'clear')
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    update_check()
    print(colored('''
    NuremX - Apex Legends
    + High Peformance
    + Highly Undetected                ''', "red"))
    print(colored("    Current Version; " + current_ver + "\n", "yellow"))
    print("    Confidence Threshold; " + confidence_threshold_str)
    print("    NMS IoU; " + NMS_IoU_str)
    print("    Mouse Delay; " + get_mouse_delay_str + "ms")
    print("    Pixel Increse; " + get_pixel_increse_str + "px")
    print("")
    path_exists = os.path.exists("lib/config/config.json")
    if not path_exists or ("setup" in sys.argv):
        if not path_exists:
            print("[!] Sensitivity configuration is not set")
        setup()
    path_exists = os.path.exists("lib/data")
    if "collect_data" in sys.argv and not path_exists:
        os.makedirs("lib/data")
    from lib.aimbot import Aimbot
    if welcome_notif == 1:
        toaster.show_toast("NuremX - Apex Cheat","Thank you for using NuremX by Zurek0x                          (This notification will go away in 5 Seconds)")
    elif welcome_notif == 0:
        pass
    else:
        pass
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    if status_overlay == 1:
        Thread(target = overlay).start()
    else:
        pass
    main()
