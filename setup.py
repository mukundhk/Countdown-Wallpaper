import os
import sys
import json

import main
import scheduler

def get_paths():
    python_path = sys.executable
    working_dir = os.getcwd()
    return python_path, working_dir

def input_prompts():
    print("Welcome to Countdown Wallpaper Set up")
    print("Please type in the required information to setup the script")

    print("\nType the date to count down to:")
    print("Example: 1st August 2022 would be 01-08-2022(with hyphens)")
    date = input(":- ").lower()

    print("\nChoose between light and dark themed wallpapers:")
    print("Type Light/Dark")
    theme = input(":- ").lower()

    print("\nEnter monitor resolution:")
    print("Example: 1920x1080")
    print("Leave blank if you want to choose 1920x1080(default)")
    resolution = input(":- ").lower().strip()
    if resolution == "":
        resolution = "1920x1080"
    
    return date,theme,resolution

def create_json(date, theme, resolution):
    dictionary = {
        "date" : date,
        "theme" : theme,
        "resolution" : resolution
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

if __name__ == "__main__":
    date,theme,resolution = input_prompts()
    create_json(date,theme,resolution)
    python_path, working_dir = get_paths()
    scheduler.create_task(python_path, working_dir)
    main.main()