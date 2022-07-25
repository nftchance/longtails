# Longtails

![Longtails](/static/images/longtails.png)

Longtails is focused on one thing, extracting maximum value from long-tail opportunities within Web3. These are not instant profit mechanisms nor are many of them low-effort. Combined though, they create a profit mechanism that can routinely generate funds that are incongruent to the overall effort invested.

**USE AT YOUR OWN RISK. EVERYTHING IS "SAFE" TO USE HOWEVER YOU MAY LOSE MONEY PLAYING ANY OF THE PROVIDED STRATEGIES.**

## Implemented Strategies
  
- [x] Free Mason Stalking
- [ ] 0xSplits Distributor

## Running The System



### Runing In Production

Longtails is designed to easily get up and running. Just click the button below to deploy to Heroku. Then all you have to do is setup the environment variables in the Settings pane.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/nftchance/longtails&env[FREEMASONS_HOURS_PER_SYNC]=DEFAULT_VALUE&env[DISCORD_APPLICATION_ID]=DEFAULT_VALUE&env[DISCORD_TOKEN]=DEFAULT_VALUE&env[DISCORD_CHANNEL_NAME]=DEFAULT_VALUE&env[DISCORD_GUILD_NAME]=DEFAULT_VALUE&env[DISCORD_GUILD_ID]=DEFAULT_VALUE&env[TWITTER_SECRET_ACCESS_TOKEN]=DEFAULT_VALUE&env[TWITTER_ACCESS_TOKEN]=DEFAULT_VALUE&env[TWITTER_BEARER_TOKEN]=DEFAULT_VALUE&env[TWITTER_CONSUMER_API_SECRET_KEY]=DEFAULT_VALUE&env[TWITTER_CONSUMER_API_KEY]=DEFAULT_VALUE&env[MORALIS_API_KEY]=DEFAULT_VALUE)

### Running In Dev

Want to make a few changes or don't want the system running forever? You can also run Longtails locally.

#### Creating `.env`

> Include in `example.env` is the fields you should add to `.env` if you want to run all functions of Longtails. This is the recomended usage as all pieces are built to work on top of each other.

* To get your keys for [Moralis](https://moralis.io/), pop on over to their webste and login and create an app. 

* To get your keys for Twitter, you need to go to the [Developer Portal](https://developer.twitter.com/en).

* To get your keys for Discord, you need to create a bot and get all the needed tokens from the [Developer Portal](https://discord.com/developers/docs/intro).

By getting this core set of keys you will be able to update Longtails as new features are released without needing additional setup.

#### Installing Dependencies

`pip install -r requirements.txt`

#### Run The Discord Bot

**For windows:**

`python manage.py shell`
`exec(open('bot.py').read())`

**For mac / linux:**

`python manage.py shell < bot.py`