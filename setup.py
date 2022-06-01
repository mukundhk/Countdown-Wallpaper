import json

print("Type the date to count down to:")
print("Example: 1st August 2022 would be 01-08-2022(with hyphens)")
date = input(":- ").lower()

print("Choose between light and dark tnemed wallpapers:")
print("Type Light/Dark")
theme = input(":- ").lower()

dictionary = {
    "date" : date,
    "theme" : theme
}

json_object = json.dumps(dictionary, indent = 4)

with open("settings.json", "w") as json_file:
    json_file.write(json_object)