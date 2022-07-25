# Longtails

![Longtails](/static/images/longtails.png)

Longtails is focused on one thing, extracting maximum value from long-tail opportunities within Web3. These are not instant profit mechanisms nor are many of them low-effort. Combined though, they create a profit mechanism that can routinely generate funds that are incongruent to the overall effort invested.

**USE AT YOUR OWN RISK. EVERYTHING IS "SAFE" TO USE HOWEVER YOU MAY LOSE MONEY PLAYING ANY OF THE PROVIDED STRATEGIES.**

[TOC]

## Implemented Strategies
  
- [x] Free Mason Stalking
- [ ] 0xSplits Distributor

## Running The System

### Creating `.env`

> Include in `example.env` is the fields you should add to `.env` if you want to run all functions of Longtails. This is the recomended usage as all pieces are built to work on top of each other.

To get your keys for [Moralis](https://moralis.io/), pop on over to their webste and login and create an app. 

To get your keys for Twitter, you need to go to the [Developer Portal](https://developer.twitter.com/en).

To get your keys for Discord, you need to create a bot and get all the needed tokens from the [Developer Portal](https://discord.com/developers/docs/intro).


### Installing Dependencies

> pip install -r requirements.txt

### Run The Discord Bot

**For windows:**

`python manage.py shell`
`exec(open('bot.py').read())`

**For mac / linux:**

`python manage.py shell < bot.py`

### Deploying To Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://heroku.com/deploy?template=https://github.com/nftchance/longtails)