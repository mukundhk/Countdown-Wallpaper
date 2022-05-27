import datetime
from PIL import Image, ImageFont, ImageDraw
import ctypes
import os

today = datetime.datetime.now()
today_epoch = today.timestamp()
today_text = today.strftime("%B %d, %Y")

final = datetime.datetime(2022, 8, 1, 0, 0)
final_epoch = final.timestamp()
final_text = final.strftime("%B %d, %Y")

difference = int(final_epoch-today_epoch)

days = difference//86400 + 1
weeks = days//7
rem_days = days%7

text = f"""{today_text}

Just {days} days left
{weeks} weeks and {rem_days} days
for
{final_text}
"""

textfont = ImageFont.truetype("assets\\Nunito-VariableFont_wght.ttf", 50)

width, height = 1920, 1080
image = Image.new("RGBA",(width,height),"black")

draw = ImageDraw.Draw(image)

#grid
draw.line(((0, 540), (1920, 540)), "gray")
draw.line(((960, 0), (960, 1080)), "gray")

draw.text((width/2,height/2), text, align="center", anchor="mm", font=textfont)

image.save("test.png", "PNG")

absolute_path = os.path.abspath("test.png")
ctypes.windll.user32.SystemParametersInfoW(20, 0, absolute_path , 0)