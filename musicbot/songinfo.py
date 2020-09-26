from discord.ext import commands
from config import config
import discord


class Song():
    def __init__(self, origin, host, base_url, uploader, title, duration, webpage_url):
        self.host = host
        self.origin = origin
        self.base_url = base_url
        self.info = self.Sinfo(uploader, title, duration, webpage_url)

    class Sinfo:
        def __init__(self, uploader, title, duration, webpage_url):
            self.uploader = uploader
            self.title = title
            self.duration = duration
            self.webpage_url = webpage_url
            self.output = ""

        """def format_output(self, playtype):
            self.output = "> :musical_note: **" + playtype + \
                ": " + self.title + "** :musical_note:\n```"
            self.output += config.SONGINFO_UPLOADER + str(self.uploader) + "\n"
            self.output += config.SONGINFO_DURATION + \
                str(self.duration) + config.SONGINFO_SECONDS + "\n"
            self.output += "```\n" + "<" + str(self.webpage_url) + ">"
            return self.output"""

        def format_output(self, playtype):
            config.SONGINFO_UPLOADER + str(self.uploader)
            config.SONGINFO_DURATION + str(self.duration)
            str(self.duration) + config.SONGINFO_SECONDS
            av = discord.Embed(color=discord.Color.blue(),
                               description=f"[{self.title}]({self.webpage_url})")
            av.set_author(name=playtype)
            self.output = av
            return self.output
