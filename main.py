import datetime
from PIL import Image, ImageFont, ImageDraw 

today = datetime.datetime.now()
today_epoch = today.timestamp()
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

line1 = f"Just {days} days left"
line2 = f"{weeks} weeks and {rem_days} days" 
text = f"""{line1}
{line2}"""

textfont = ImageFont.truetype("assets\\Nunito-VariableFont_wght.ttf", 50)

width, height = 1920, 1080
image = Image.new("RGBA",(width,height),"black")

draw = ImageDraw.Draw(image)
draw.text((width/2, height/2), text, font=textfont, anchor="mm", align="center")

image.save("test.png", "PNG")