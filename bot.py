import discord
from discord.ext import commands
import config
from cogs.music_cog import music_cog
from cogs.help_cog import help_cog
from cogs.admin_cog import admin_cog
from cogs.general_cog import general_cog

hello_words = ['Привiт', 'Тест']

client = discord.Client()
client = commands.Bot(command_prefix=".")
intents = discord.Intents(messages=True, guilds=True)
client.remove_command('help')

client.add_cog(music_cog(client))
client.add_cog(help_cog(client))
client.add_cog(admin_cog(client))
client.add_cog(general_cog(client))


@client.event()
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(f".help"))
    print('Бот включений!')


@client.event()
async def on_message(message):
    msg = message.content.lower()

    if msg == hello_words[0]:
        await message.reply("Привiт1")
    if msg == hello_words[1]:
        await message.reply("Тест1!")
    else:
        pass

    await client.process_commands(message)


client.run(config.TOKEN)
