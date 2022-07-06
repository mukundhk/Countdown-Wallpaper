import datetime
from PIL import Image, ImageFont, ImageDraw, ImageColor
import ctypes
import os
import win32com.client
import json
import random

def settings(option):
    with open(r".\generated_assets\settings.json","r") as settings_file:
        settings = json.load(settings_file)
    data = settings[option]

    if option == "date":
        final_date_elements = data.split("-")
        day,month,year = int(final_date_elements[2]),int(final_date_elements[1]),int(final_date_elements[0])
        if year < 1000:
            year += 2000
        return (day,month,year)

    if option == "resolution":
        width, height = data[0], data[1]
        return (width, height)

    else:
        return data

def remaining_days():
    day,month,year = settings("date")  
    today_epoch = datetime.datetime.now().timestamp()
    final_epoch = datetime.datetime(year,month,day).timestamp()

    difference = int(final_epoch - today_epoch)
    days = difference//86400 + 1
    weeks = days//7
    rem_days = days%7

    return (days,weeks,rem_days)

def days_to_text():
    day,month,year = settings("date")
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

def pick_colors():
    theme = settings("theme")
    with open(r".\assets\colors.json","r") as colors_file:
        colors = json.load(colors_file)
    chosen_colors = random.choice(colors[theme])
    
    bg_color = ImageColor.getrgb(chosen_colors["background"])
    text_color = ImageColor.getrgb(chosen_colors["text"])

    return (bg_color,text_color)
    
def create_wallpaper(bg_color,text_color,text):
    width, height = settings("resolution")

    image = Image.new("RGBA",(width,height),color=bg_color)
    draw = ImageDraw.Draw(image)

    textfont = ImageFont.truetype("assets\\Nunito-VariableFont_wght.ttf", 50)
    draw.text((width/2,height/2), text, align="center", anchor="mm", font=textfont, fill=text_color)

    image.save(r".\generated_assets\generated_wallpaper.png", "PNG")

def set_wallpaper():
    absolute_path = os.path.abspath(r".\generated_assets\generated_wallpaper.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path , 0)

def delete_task():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()
    root_folder = scheduler.GetFolder('\\')
    root_folder.DeleteTask("Countdown Wallpaper",0)

def main():
    get_remaining_days = remaining_days()
    if get_remaining_days[0] < 0:
        delete_task()
        exit()

    days_text = days_to_text()
    final_text = text(get_remaining_days, days_text)
    bg_color,text_color = pick_colors()
    create_wallpaper(bg_color,text_color,final_text)
    set_wallpaper()

if __name__ == "__main__":
    main()