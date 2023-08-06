from distutils.core import setup

long_desc = open('README.md').read()

setup(
    name='DiscordBotsTK',
    version='0.4dev',
    author="iWeeti",
    description="This is to update discordbots.tk guild count.",
    packages=['discordbotstk'],
    license='MIT',
    long_description=long_desc,
    long_description_content_type="text/markdown"
)