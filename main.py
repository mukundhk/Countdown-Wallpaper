import datetime
from PIL import Image, ImageFont, ImageDraw 

today = datetime.datetime.now()
today_epoch = today.timestamp()
today_text = today.strftime("%B %d, %Y")
final = datetime.datetime(2022, 8, 1, 0, 0)
final_epoch = final.timestamp()

difference = int(final_epoch-today_epoch)

# seconds = difference + 1
# minutes = seconds//60 + 1
# hours = minutes//60 + 1
# days = hours//24 + 1
# weeks = f"{days//7} weeks and {str(days%7)} days"

days = difference//86400 + 1
weeks = days//7
rem_days = days%7

text1 = today_text
text2 = f"""Just {days} days left
{weeks} weeks and {rem_days} days
for
{final.strftime("%B %d, %Y")}"""

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