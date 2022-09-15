import discord
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix=".")


class admin_cog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @client.event
    async def on_command_error(self):
        pass

    @client.command()
    @commands.has_permissions(administrator=True)
    async def clear_chat(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)

    @client.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.kick(reason=reason)
        if reason == None:
            await ctx.send(f"{member.mention} був кікнутий..")
        else:
            await ctx.send(f"{member.mention} був кікнутий через {reason}.")

    @client.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.channel.purge(limit=1)
        await member.ban(reason=reason)
        if reason == None:
            await ctx.send(f"{member.mention} був забанен.")
        else:
            await ctx.send(f"{member.mention} був забанен через {reason}.")

    @client.command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        await ctx.channel.purge(limit=1)
        banned_users = await ctx.guild.bans()
        for ban_empty in banned_users:
            user = ban_empty.user

            await ctx.guild.unban(user)
            await ctx.send(f"{member} був розбанений.")
            return

    @client.command()
    @commands.has_permissions(administrator=True)
    async def delete_channel(self, ctx, channel: discord.TextChannel):
        if ctx.author.guild_permissions.manage_channels:
            await channel.delete()
        await ctx.channel.purge(limit=1)

    @client.command()
    @commands.has_permissions(administrator=True)
    async def create_channel(self, ctx, channel_name: str):
        await ctx.channel.purge(limit=1)
        guild = ctx.guild
        channel = await guild.create_text_channel(channel_name)
        return channel

    @client.command()
    @commands.has_permissions(administrator=True)
    async def giverole(self, ctx, member: discord.Member, role: discord.Role):
        await ctx.channel.purge(limit=1)
        await member.add_roles(role)

    @clear_chat.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Вкажіть аргумент.")

        if isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас недостатньо прав для цієї команди!")

        if isinstance(error, commands.CommandNotFound):
            await ctx.send("Такої команди немає, але мій творець може її додати, якщо попросити.")
