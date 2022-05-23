import datetime

today = datetime.datetime.now()
today_epoch = today.timestamp()
final = datetime.datetime(2022, 8, 1, 0, 0)
final_epoch = final.timestamp()

difference = int(final_epoch-today_epoch)

seconds = difference + 1
minutes = seconds//60 + 1
hours = minutes//60 + 1
days = hours//24 + 1
weeks = f"{days//7} weeks and {str(days%7)} days"

print("\nTIME LEFT\n")
print("days:",days)
print(weeks)
print("hours:",hours)
print("minutes:",minutes)
print("seconds:",seconds)

wait=input("\nType enter to exit")