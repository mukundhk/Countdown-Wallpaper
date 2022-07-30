import datetime
from PIL import Image, ImageFont, ImageDraw, ImageColor
from ctypes import windll
import os
import win32com.client
import json
import random

import setup

def get_settings():
    with open(r".\generated_assets\settings.json","r") as settings_file:
        settings = json.load(settings_file)
    return settings

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
    with open(r".\assets\colors.json","r") as colors_file:
        colors = json.load(colors_file)
    chosen_colors = random.choice(colors[theme])
    
    bg_color = ImageColor.getrgb(chosen_colors["background"])
    text_color = ImageColor.getrgb(chosen_colors["text"])

    return (bg_color,text_color)
    
def create_wallpaper(bg_color,text_color,text,resolution):
    width, height = resolution[0], resolution[1]

    image = Image.new("RGBA",(width,height),color=bg_color)
    draw = ImageDraw.Draw(image)

    textfont = ImageFont.truetype("assets\\Nunito-VariableFont_wght.ttf", 50)
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

def main():
    settings = get_settings()

    year,month,day = settings["date"]
    remaining_days = get_remaining_days(year,month,day)
    if remaining_days[0] < 0:
        delete_task()
        old_wallpaper_path = os.path.abspath(r".\generated_assets\old_wallpaper.png")
        if os.path.exists(old_wallpaper_path):
            windll.user32.SystemParametersInfoW(20, 0, old_wallpaper_path , 0)
        exit()

    
    days_text = days_to_text(year,month,day)
    final_text = text(remaining_days, days_text)
    bg_color,text_color = pick_colors(settings["theme"])
    create_wallpaper(bg_color,text_color,final_text,settings["resolution"])
    set_wallpaper()

if __name__ == "__main__":
    if not os.path.exists(r'generated_assets\settings.json'):
        setup.main()

    main()