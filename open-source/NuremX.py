import json
import os
import os.path
import sys
import threading
import random
import string
import ctypes
import configparser

from win10toast import ToastNotifier
from pynput import keyboard
from termcolor import colored

toaster = ToastNotifier()
config = configparser.ConfigParser()

def create_config():
    config.add_section("settings")
    config.set("settings", "welcome_notif", "1")
    config.set("settings", "size_of_window", "466")
    config.set("settings", "confidence_threshold", "1")
    config.set("settings", "NMS_IoU", "1")
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

def on_release(key):
    try:
        if key == keyboard.Key.f7:
            Aimbot.update_status_aimbot()
        if key == keyboard.Key.f8:
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

if __name__ == "__main__":
    title_gen = string.ascii_letters
    title_str = ''.join(random.choice(title_gen) for i in range(10))
    ctypes.windll.kernel32.SetConsoleTitleA(title_str)
    os.system('cls' if os.name == 'nt' else 'clear')
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    print(colored('''
    NuremX - Apex Cheat

    + High Peformance Cheat
    + Highly Undetected
                           
    ''', "red"))

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
    main()
