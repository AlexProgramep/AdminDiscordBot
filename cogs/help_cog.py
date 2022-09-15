from discord.ext import commands


class help_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
```
Усі команди бота
Музичні:
.help - Відображає всі доступні команди
.p посилання - Знаходить пісню на YouTube та відтворює її на вашому поточному каналі. Відновить відтворення поточної пісні, якщо її призупинено
.q - Відображає поточну музичну чергу
.skip - Пропускає поточну пісню, що відтворюється.
.clear - Зупиняє музику та очищає чергу
.leave - Вимикає бота від голосового каналу
.pause - Зупиняє відтворення поточної пісні або відновлює її, якщо вона вже була припинена
.resume - Відновлює відтворення поточної пісні
Адмінські:
.clear_chat кількість - Очищення чату
.kick @нік причина - Вигнання користувача з сервера
.ban @нік причина - Забанити користувачеві
.unban нік - Розбанити користувача
.mute @нік - "Заглушити" користувача
.unmute @нік - Зняти "Заглушку" з користувача
.delete_channel назва - Видалити канал
.create_channel назва - Створити текстовий канал
.giverole @нік @ роль - Видає потрібну роль по ніку
Загальні:
.youtube_search назва - Пошук відео в ютубі
.youtube - Включає Youtube Together
```
"""
        self.text_channel_list = []

    @commands.command(name="help", help="Відображає всі доступні команди")
    async def help(self, ctx):
        await ctx.send(self.help_message)

    async def send_to_all(self, msg):
        for text_channel in self.text_channel_list:
            await text_channel.send(msg)
