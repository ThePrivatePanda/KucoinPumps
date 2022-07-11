## Preamble
    - This is solely for educational purposes
    - I have no intention of using it
    - It is not regularly maintained


### Project info
My work relating to crypto and kucoin
This repository contains an archive of pump bots as well as a newer version.
It is meant as a proof of concept as how one can scrape coins and participate in crypto pump and dump groups through discord
- Please note that this requires selfbotting which breaks the Discord TOS
- Anything you do using this, I won't be damn responsible
- If you wish to use it, I suggest you have a go through and edit it yourself as it will require a ton of testing to get going perfectly and can be improved a lot.

### Why no work
**I'm not going to maintain this**
- I have no idea
- Do not want to use it personally, I hope you gain inspiration from it though.

## Table of contents
* [Features](#features)
* [Prerequisites](#prerequisites)
* [Setting up](#setting-up)
* [About me](#Me)

### Features
- This uses the discord.py-self lib to listen/wait for the coin message strictly following given regex.
- This talkes to kucoin through raw api requests, no libs and shet.
- It buys instantly with set investment and sets a limit sell order at the average of expected gain range. <br>
- - As you might have guessed, this is incredibly buggy due to milliseconds of late buys messing up the prices.


### Prerequisites
* [Python 3.8+] (did not test on other Python versions)
* [Discord Accoutn Token] A functioning discord account in the pump server, keep it's token.
* [Kucoin Account/API] A Kucoin account with an API; keep the api secret and stuff

Make sure Python is added to your PATH on Windows, more info [here](https://superuser.com/questions/143119/how-do-i-add-python-to-the-windows-path) if you didn't let it set the PATH at install.

### Setting up
- Almost all files/dirs take their own config, I'll leave it up to you to figure it out haha; I don't want to spoonfeed or else I know I'll have people blaming me for shit not working sumn idk
- Install python library dependencies with `python -m pip install -r requirements.txt` or equivalent
- If you really really want help setting up, feel free to contact me on [discord](https://discord.com/users/736147895039819797)


## **Me**
I am koala, nothing less, nothing more. I spend my time studying and chasing various aspects of life which catch my eye. <br>
Currently trying to make [my site](https://thekoalaco.in) better, pls [contribute](https://github.com/koala9712/koala9712.github.io) thenk <br>
If you liked this project or it helped you, buy me a coffee and make my day! <br>
- BTC (BTC): 35oNx7C6YDNfgxNoXvhZwJydQ3Bpu3746c
- LTC (LTC): MVC2viP8vZrKsgzds3juSnfySvCGi3yPMf
- USDT (ERC20): 0x8c82b8887ef114f9b6e2841f014ed21fef705b69