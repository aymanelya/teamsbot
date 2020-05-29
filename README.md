# Microsft Teams Bot

I am not a "morning" person. So, when the 2020 quarantine happened, and classes went online, I made a bot that attended my online classes for me according to my timetable. So if you're not a morning person either, you now know what to do!

Made by [Ayman Elyahmidi](https://github.com/aymanelya)

## Install Steps
  
- Download python 3 from [THIS LINK](https://www.python.org/downloads), (**IMPORTANT**) Check "Add Python to PATH" when installing Python

![Python PATH](https://i.imgur.com/YNqlFgS.png)

- Check Chrome version (I have version 81)

![Chrome Version1](https://i.imgur.com/AJoCRlC.png)

![Chrome Version2](https://i.imgur.com/YU2wutY.png)

- Download Chromedriver from [THIS LINK](https://chromedriver.chromium.org/downloads)

![Chromedriver](https://i.imgur.com/3Ti5b6q.png)

- Copy Chromedriver to C:\Windows for Windows users or /usr/bin if you're using Linux or Mac
- Download this project from [THIS LINK](https://github.com/aymanelya/teamsbot/archive/master.zip)
- Open project folder in cmd and run the following command
```
pip install -r requirements.txt
```
- Modify the **secrets.py** file with your personal informations
- Change Microsoft Teams Layout settings to **List**

![List Layout](https://i.imgur.com/SeCXNyR.png)

- Finally run the script
```
python teamsbot.py
```

