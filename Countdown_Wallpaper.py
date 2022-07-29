import datetime
from PIL import Image, ImageFont, ImageDraw, ImageColor
from ctypes import windll
import os
import sys
import win32com.client
import json
import random

def get_settings():
    with open(r".\generated_assets\settings.json","r") as settings_file:
        settings = json.load(settings_file)
    return settings

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

def create_task():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    task_def = scheduler.NewTask(0)

    triggers = task_def.Triggers
    start_time = "2022-07-04T00:00:00"

    TriggerTypeDaily = 2
    trigger = triggers.Create(TriggerTypeDaily)
    trigger.StartBoundary = start_time
    
    TriggerTypeRegistration = 7
    trigger = triggers.Create(TriggerTypeRegistration)
    trigger.StartBoundary = start_time
    trigger.Id = "RegistrationTriggerId"
    
    TriggerTypeLogon = 9
    trigger = triggers.Create(TriggerTypeLogon)
    trigger.StartBoundary = start_time
    trigger.Id = "LogonTriggerId"
    trigger.UserId = os.getlogin() # WINDOWS USERNAME

    # Create action
    TASK_ACTION_EXEC = 0
    action = task_def.Actions.Create(TASK_ACTION_EXEC)
    action.ID = 'TRIGGER BATCH'
    action.Path = sys.executable # PYTHON EXECUTABLE PATH
    action.WorkingDirectory = os.getcwd() # WORKING DIRECTORY
    action.Arguments ='Countdown_Wallpaper.py run'

    # Registration information
    task_def.RegistrationInfo.Description = 'A recurring daily task that runs the program at midnight. Check https://github.com/mukundhk/Countdown-Wallpaper for more information.'
    task_def.RegistrationInfo.Author = 'Mukund Harikumar'

    # Task Settings
    task_def.Settings.Enabled = True
    task_def.Settings.StopIfGoingOnBatteries = False
    task_def.Settings.DisallowStartIfOnBatteries = False
    task_def.settings.StartWhenAvailable = True
    TASK_INSTANCES_STOP_EXISTING = 3 
    task_def.Settings.MultipleInstances = TASK_INSTANCES_STOP_EXISTING

    # Register task
    # If task already exists, it will be updated
    TASK_CREATE_OR_UPDATE = 6
    TASK_LOGON_NONE = 0
    root_folder.RegisterTaskDefinition(
        'Countdown Wallpaper',  # Task name
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',  # No user
        '',  # No password
        TASK_LOGON_NONE
    )

def get_remaining_days(year,month,day):
    today_epoch = datetime.datetime.now().timestamp()
    final_epoch = datetime.datetime(year,month,day).timestamp()

    difference = int(final_epoch - today_epoch)
    days = difference//86400 + 1
    weeks = days//7
    rem_days = days%7

    return (days,weeks,rem_days)

def days_to_text(year,month,day):
    today = datetime.datetime.now().strftime("%B %d, %Y")
    final = datetime.datetime(year, month, day).strftime("%B %d, %Y")
    return (today,final)

def text(remaining_days,days_text):
    if remaining_days[1] == 0:
        if remaining_days[0] == 0:
            text = f"""The wait is finally over.

Today is {days_text[1]}.
"""
        elif remaining_days[0] == 1:
            text = f"""{days_text[0]}
    
Tomorrow is the big day
Just a day left
for
{days_text[1]}
"""
        else:
            text = f"""{days_text[0]}
    
Just {remaining_days[0]} days left
for
{days_text[1]}
"""

    else:
        text = f"""{days_text[0]}

Just {remaining_days[0]} days left
{remaining_days[1]} weeks and {remaining_days[2]} days
for
{days_text[1]}
"""
    return text

def pick_colors(theme):
    color_combinations = ( ("#C2DED1","#354259"), ("#ECE5C7","#354259"), ("#F582A7","#180A0A"), ("#DCDCDC","#393E46"), ("#FFC8C8","#444F5A"), ("#FF9999","3E4149") )
    chosen_colors = random.choice(color_combinations)
    if theme=="dark":
        chosen_colors = chosen_colors[::-1]
    bg_color = ImageColor.getrgb(chosen_colors[0])
    text_color = ImageColor.getrgb(chosen_colors[1])

    return (bg_color,text_color)
    
def create_wallpaper(bg_color,text_color,text,resolution):
    width, height = resolution[0], resolution[1]

    image = Image.new("RGBA",(width,height),color=bg_color)
    draw = ImageDraw.Draw(image)

    textfont = ImageFont.truetype(font = "calibril.ttf", size = 50)
    draw.text((width/2,height/2), text, align="center", anchor="mm", font=textfont, fill=text_color)

    image.save(r".\generated_assets\generated_wallpaper.png", "PNG")

def set_wallpaper():
    absolute_path = os.path.abspath(r".\generated_assets\generated_wallpaper.png")
    windll.user32.SystemParametersInfoW(20, 0, absolute_path , 0)

def delete_task():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    root_folder.DeleteTask("Countdown Wallpaper",0)

def run():
    settings = get_settings()

    year,month,day = settings["date"]
    remaining_days = get_remaining_days(year,month,day)
    if remaining_days[0] < 0:
        delete_task()
        exit()

    
    days_text = days_to_text(year,month,day)
    final_text = text(remaining_days, days_text)
    bg_color,text_color = pick_colors(settings["theme"])
    create_wallpaper(bg_color,text_color,final_text,settings["resolution"])
    set_wallpaper()

if __name__ == "__main__":
    cmd_args = sys.argv

    # RUN SETUP IF NO CMD ARGUEMENTS ARE PASSED OR SETTINGS FILE DOESNT EXIST 
    if (len(cmd_args) == 1) or (not os.path.exists(r'generated_assets\settings.json')):
        date,theme = input_prompts()
        create_json(date,theme)
        create_task()

    elif cmd_args[1] == "run":
        run()