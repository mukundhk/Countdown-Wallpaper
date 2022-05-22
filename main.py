import time

today = time.time()
final = 1659297600

difference = int(final-today)

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