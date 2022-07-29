import os
import sys
import json
from ctypes import windll

import scheduler

def get_paths():
    python_path = sys.executable
    working_dir = os.getcwd()
    return python_path, working_dir

def input_prompts():
    print("Welcome to Countdown Wallpaper Set up")
    print("Please type in the required information to setup the script")

    print("\nType the date to count down to:")
    print("Example: 1st August 2022 would be 2022-08-01(with hyphens)")
    date = input(":- ").lower().strip().split("-")
    date_elements = list(map(int, date)) # CHANGES THE TYPE OF LIST ELEMENTS FROM STR TO INT
    if date_elements[0] < 1000:
            date_elements[0] += 2000 # CONVERTS YY TO YYYY FORMAT

    print("\nChoose between light and dark themed wallpapers:")
    print("Type Light/Dark")
    theme = input(":- ").lower().strip()
    
    return date_elements,theme

def get_resolution():
    user32 = windll.user32
    user32.SetProcessDPIAware()
    resolution = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)) # (W,H)
    return resolution

def create_json(date, theme):
    dictionary = {
        "date" : date,
        "theme" : theme,
        "resolution" : get_resolution()
    }

    #creating a new directory
    try:
        os.mkdir(r".\generated_assets")
    except FileExistsError:
        pass

    #This settings.json will be read by main.py
    json_object = json.dumps(dictionary, indent = 4)
    with open(r".\generated_assets\settings.json", "w") as json_file:
        json_file.write(json_object)

def main():
    date,theme = input_prompts()
    create_json(date,theme)
    python_path, working_dir = get_paths()
    username = os.getlogin()
    scheduler.create_task(python_path, working_dir, username)

if __name__ == "__main__":
    main()