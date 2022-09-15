import discord
from discord.ext import commands
from discord_together import DiscordTogether
import re
import urllib
import config

client = discord.Client()
client = commands.Bot(command_prefix=".")


class general_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @client.command()
    async def youtube(self, ctx):
        client.togetherControl = await DiscordTogether(config.TOKEN)
        link = await client.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
        await ctx.send(f"Заходьте в Youtube Together!\n{link}")

    @client.command()
    async def youtube_video(self, ctx, *, search):
        query_string = urllib.parse.urlencode({
            'search_query': search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string
        )
        search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])
