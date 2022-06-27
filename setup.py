import os
import json

import main

print("Welcome to Countdown Wallpaper Set up")
print("Please type in the required information to setup the script")

print("Type the date to count down to:")
print("Example: 1st August 2022 would be 01-08-2022(with hyphens)")
date = input(":- ").lower()

print("Choose between light and dark themed wallpapers:")
print("Type Light/Dark")
theme = input(":- ").lower()

print("Enter monitor resolution:")
print("Example: 1920x1080")
print("Leave blank if you want to choose 1920x1080(default)")
resolution = input(":- ").lower().strip()
if resolution == "":
    resolution = "1920x1080"

dictionary = {
    "date" : date,
    "theme" : theme,
    "resolution" : resolution
}

#creating a new directory
os.mkdir(r".\generated_assets")

#This settings.json will be read by main.py
json_object = json.dumps(dictionary, indent = 4)
with open(r".\generated_assets\settings.json", "w") as json_file:
    json_file.write(json_object)

main.main()