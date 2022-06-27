# Countdown-Wallpaper

A Python program that shows you a daily countdown to any date you choose by changing your desktop wallpaper. Currently works only on Windows.

You can use Task Scheduler in Windows to run the script everyday at midnight. As the script doesn't have to be running in the background all the time as a wallpaper engine, it is performance efficient.

I made this script because I couldn't find anything similar to this program so I decided to put my python skills to test and just build my own.
## Installation

Only [Pillow](https://github.com/python-pillow/Pillow) needs to be installed to run the script. 
1. Run the following command in command line to install the library.
```bash
pip install pillow
```
2. Then run *setup.py* and type in your preferred settings.
3. You can use Task Scheduler to automatically run *main.py* at midnight everyday. 

>**Warning** 
> Do not delete or change the structure of the directory as it may break the script.

## Feedback
All kinds of constructive feedback are welcome! Please create a pull request if you have any suggestions.
