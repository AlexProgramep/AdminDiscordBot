import discord
from discord.ext import commands
import config

#Клиент-связь с discord.
client = discord.Client()
#Префикс комманды (Команды записываются с декоратором @bot.command() )
client = commands.Bot(command_prefix=".")
#Обязательное включение intents начиная с discord.py 1.5.x
intents = discord.Intents(messages=True, guilds=True)#Guilds это дискорд сервера
#Удаляем дефолтную команду help
client.remove_command('help')

#Уведомление в консоли,что бот запустился
@client.event
async def on_ready():
    print('Бот включен!')

    await client.change_presence(status=discord.Status.idle,activity=discord.Game("{}help".format('.'))) #Статус бота

#Убираем дефолтное отображение ошибок бота
@client.event
async def on_command_error(ctx,error):
     pass

#Вызывается функция,когда бот получил сообщение(костыль для остальных команд)
@client.event
async def on_message( message ):
    await client.process_commands(message)


#Очистка чата
@client.command()
@commands.has_permissions( administrator = True )
async def clear(ctx, amount = 100):
    await ctx.channel.purge(limit = amount)

#Кик
@client.command()
@commands.has_permissions( administrator = True ) #Обозначение того,что команда доступна только с правами администратора
async def kick(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} был кикнут по причине {reason}.")

#Бан
@client.command()
@commands.has_permissions( administrator = True )
async def ban(ctx, member: discord.Member, *, reason = None):
    await ctx.channel.purge(limit = 1)
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} был забанен по причине {reason}.")

#Разбан
@client.command()
@commands.has_permissions( administrator = True )
async def unban(ctx, *, member ):
    await ctx.channel.purge(limit = 1)
    banned_users = await ctx.guild.bans() #получаем список забаненных юзеров
    for ban_empty in banned_users: #достаем этого же юзера
        user = ban_empty.user #получаем его имя

        await ctx.guild.unban( user )
        await ctx.send(f"{member} был разбанен.")
        return

#Help
@client.command()
async def help(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title = "Все команды бота", colour=discord.Color.blue())

    emb.add_field(name='{}clear количество'.format("."), value="Очистка чата")
    emb.add_field(name='{}kick @ник'.format("."), value="Изгнание пользователя с сервера")
    emb.add_field(name='{}ban @ник'.format("."), value="Выдача бана пользователю")
    emb.add_field(name='{}unban ник'.format("."), value="Разбанить пользователя")
    emb.add_field(name='{}mute @ник'.format("."), value='"Заглушить" пользователя')
    emb.add_field(name='{}unmute @ник'.format("."), value='Снять "Заглушку" с пользователя')

    await ctx.send(embed = emb)

#Команда для оформления чата от бота
@client.command()
@commands.has_permissions( administrator = True )
async def WordsForMe(ctx):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title = "", colour=discord.Color.red())
    await ctx.send(embed=emb)

#Mute
@client.command()
@commands.has_permissions( administrator = True )
async def mute(ctx,member:discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')
    await member.add_roles(mute_role)
    await ctx.send(f"{member.mention} получил роль mute!")

#Unute
@client.command()
@commands.has_permissions( administrator = True )
async def unmute(ctx,member:discord.Member):
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name = 'mute')
    await member.remove_roles(mute_role)
    await ctx.send(f"{member.mention} вышел из \"Заглушки\" !")

#"Работа о ошибками"
@clear.error
async def clear_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Укажите аргумент!")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send("У вас недостаточно прав для этой команды!")

    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Такой команды нет,но мой создатель может ее добавить,если попросить.")

client.run(config.TOKEN)