## Preamble
    - This is solely for educational purposes
    - I have no intention of using it
    - It is not regularly maintained


### Project info
My work relating to crypto and kucoin
This repository contains an archive of pump bots as well as a newer version.
It is meant as a proof of concept as how one can scrape coins and participate in crypto pump and dump groups through discord
- Please note that this requires selfbotting which breaks the Discord TOS
- You are solely responsible for anything that is caused, directly or indirectly, by using this bot.
- If you wish to use it, I suggest you have a go through and edit it yourself as it will require a ton of testing to get going perfectly and can be improved a lot.

### Why no work
**I'm not going to maintain this**
- I have no idea
- Do not want to use it personally, I hope you gain inspiration from it though.

## Table of contents
* [Features](#features)
* [TODO](#todo)
* [Prerequisites](#prerequisites)
* [Setting up](#setting-up)
* [About me](#Me)

### Features
- This uses the discord.py-self lib to listen/wait for the coin message strictly following given regex.
    - EDIT (10 months): This is slow and can be improved immensely.
- This talkes to kucoin through api requests, no bloaty libs.
- It buys instantly with set investment and sets a limit sell order at the average of expected gain range. <br>
    - As you might have guessed, this is incredibly buggy due to milliseconds of late buys messing up the prices.
- Thanks to [Sjoerd](https://sjoerd.tech/) for reviewing my code and helping me out here

### TODO
- Better implementation of Limit buy/sell
- Implement multiple buy/sell, if your that kind of risk taking dare devil
- Eliminate TOS-breaking stuff by scraping from telegram instead
- Implement base line price so bot doesn't buy too high or sell too low etc
- Best of all, pre-pump detection! I don't have the brains for that have fun!

### Prerequisites
* [Python 3.8+] (did not test on other Python versions)
* [Discord Accoutn Token] A functioning discord account in the pump server, keep it's token.
* [Kucoin Account/API] A Kucoin account with an API; keep the api secret and stuff

Make sure Python is added to your PATH on Windows, more info [here](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path) if you didn't let it set the PATH at install.

### Setting up
- Almost all files/dirs take their own config, I'll leave it up to you to figure it out.
- Install python library dependencies with `python -m pip install -r requirements.txt` or equivalent
- This requires at least a little programming knowledge before hand, please consider that before trying to contact me asking for help using this.

## **Me**
I am the private panda, nothing less, nothing more. I spend my time studying and chasing various aspects of life which catch my eye. <br>
Currently workin on my college application heh, visit my site [here](https://privatepanda.co)
If you liked this project or it helped you in any way, [buy me a coffee](https://privatepanda.co#patreon) and make my day!
