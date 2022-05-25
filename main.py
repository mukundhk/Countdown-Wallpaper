import datetime
from PIL import Image, ImageFont, ImageDraw 

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

text1 = today_text
text2 = f"""Just {days} days left
{weeks} weeks and {rem_days} days
for
{final_text}"""

textfont = ImageFont.truetype("assets\\Nunito-VariableFont_wght.ttf", 50)

width, height = 1920, 1080
image = Image.new("RGBA",(width,height),"black")

draw = ImageDraw.Draw(image)

#grid
draw.line(((0, 540), (1920, 540)), "gray")
draw.line(((960, 0), (960, 1080)), "gray")

draw.text((width/2, height/2), text1, font=textfont, anchor="md", align="center")

draw.text((width/2, height/2), text2, font=textfont, anchor="ma", align="center")

image.save("test.png", "PNG")