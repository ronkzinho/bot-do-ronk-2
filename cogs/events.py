import discord
from .functions.dmToo import listOfCommands
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    def bot_check(self, ctx):
        if ctx.command.name in listOfCommands: return True
        return ctx.guild is not None

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game(name='o joso pela janela', type=0))
        print(f"\"{self.client.user.display_name}\" Ligado!")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if len(message.mentions) == 1 and message.mentions[0].id == self.client.user.id: return await message.channel.send("Sai fora!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction("❓")
            await self.client.wait_for('reaction_add', timeout=30.0, check=lambda reaction, user: user.id == ctx.author.id and reaction.emoji == '❓' and reaction.message.id == ctx.message.id)
            return await ctx.send("O comando {} não existe!".format("``" + self.client.command_prefix + ctx.invoked_with + "``"))
        if isinstance(error, commands.NotOwner):
            return await ctx.send("Você não tem permissão para usar este comando!")
        if isinstance(error, commands.CheckFailure):
            return
        raise error

def setup(client):
    client.add_cog(Events(client))