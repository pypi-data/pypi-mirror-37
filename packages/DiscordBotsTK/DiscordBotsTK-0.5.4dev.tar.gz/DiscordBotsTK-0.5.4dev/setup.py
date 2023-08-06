from distutils.core import setup

long_desc = """
# [DiscordBots.tk](https://discordbots.tk)

### This module is to update guild count to discordbots.tk's api.

### Example
1. In your main file.
```py
# Imports here
import discordbotstk

# ...

# bot can be client too
@bot.event()
async def on_ready():
    #Do whatever you want here

    tk_client = discordbotstk.client(bot, 'api-key-here') # bot can be client too
    await tk_client.start_loop()

# ...
```

#### Don't forget to join the server [DiscordBotsTK](https://discord.gg/APfnJMM)
"""

setup(
    name='DiscordBotsTK',
    version='0.5.4dev',
    author="iWeeti",
    description="This is to update discordbots.tk guild count.",
    packages=['discordbotstk'],
    license='MIT',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    install_requires=[
        'aiohttp',
        'discord'
    ]
)