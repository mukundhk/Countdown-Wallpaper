import datetime
from PIL import Image, ImageFont, ImageDraw
import ctypes
import os
import json

def remaining_days():
    with open("settings.json","r") as json_file:
        json_object = json.load(json_file)
    final_date_elements = json_object["date"].split("-")
    day,month,year = int(final_date_elements[0]),int(final_date_elements[1]),int(final_date_elements[2])
    
    today_epoch = datetime.datetime.now().timestamp()
    final_epoch = datetime.datetime(year,month,day).timestamp()

    difference = int(final_epoch - today_epoch)
    days = difference//86400 + 1
    weeks = days//7
    rem_days = days%7

    return (days,weeks,rem_days)

def days_to_text():
    today = datetime.datetime.now().strftime("%B %d, %Y")
    final = datetime.datetime(2022, 8, 1, 0, 0).strftime("%B %d, %Y")
    return (today,final)

def text(remaining_days,days_text):
    text = f"""{days_text[0]}
    
Just {remaining_days[0]} days left
{remaining_days[1]} weeks and {remaining_days[2]} days
for
{days_text[1]}
"""
    return text

def create_wallpaper(text):
    width, height = 1920, 1080
    image = Image.new("RGBA",(width,height),"black")
    draw = ImageDraw.Draw(image)

    textfont = ImageFont.truetype("assets\\Nunito-VariableFont_wght.ttf", 50)
    draw.text((width/2,height/2), text, align="center", anchor="mm", font=textfont)

    image.save(r".\assets\wallpaper.png", "PNG")

def set_wallpaper():
    absolute_path = os.path.abspath(r".\assets\wallpaper.png")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path , 0)

if __name__ == "__main__":
    remaining_days = remaining_days()
    days_text = days_to_text()
    final_text = text(remaining_days, days_text)
    create_wallpaper(final_text)
    set_wallpaper()