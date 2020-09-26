import os

from utils import default
from utils.data import Bot
from config import config
from musicbot.audiocontroller import AudioController
from musicbot import utils
from musicbot.utils import guild_to_audiocontroller

from musicbot.commands.general import General

initial_extensions = ['musicbot.commands.music',
                      'musicbot.commands.general', 'musicbot.button']

print("Logging in...")

bot = Bot(
    command_prefix='kek ',
    prefix='kek ',
    command_attrs=dict(hidden=True),

)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")

for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)

try:
    bot.run('NzU3OTk1MDMxNjUwMTA3NDI0.X2of4g.wst-WNoGqgFFZF1SY6UXCf62zrQ')
except Exception as e:
    print(f'Error when logging in: {e}')
