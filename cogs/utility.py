import discord
import os
import asyncio
from datetime import datetime, timedelta
from .functions.searchMember import SearchMember
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ms"])
    async def ping(self, ctx):
        ping = float("%.3f" % self.client.latency)
        await ctx.send(f'{int(ping * 1000)}ms')
    
    @commands.command()
    async def links(self, ctx):
        owner_id = self.client.owner_id if self.client.owner_id else os.getenv("OWNER_ID") if os.getenv("OWNER_ID") else "370007502643003403"
        embed = discord.Embed(title=f"Olá, {ctx.author.display_name}", description=f"Eu sou um bot criado pelo **<@{owner_id}>**. Aqui estão alguns links relacionados ao bot, que talvez você possa querer!", color=0x38ff00)
        embed.add_field(name="Convide o bot para o seu servidor!", value=f"[clique aqui](https://discord.com/oauth2/authorize?client_id={self.client.user.id}&scope=bot&permissions=8)", inline=False)
        embed.add_field(name="Código do bot!", value="[clique aqui](https://github.com/ronkzinho/bot-do-ronk-2)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, *, member: SearchMember=None):
        if not member: member = ctx.author
        avatar = member.avatar_url_as(size=512)
        embed = discord.Embed(title=f"Avatar de {member.display_name}", description=f"**Clique [aqui]({avatar}) para baixar a imagem!**", color=member.color)
        embed.set_image(url=avatar)
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.bot_has_guild_permissions(administrator=True, manage_messages=True)
    async def clear(self, ctx, number:int=None, member: SearchMember=None):
        if not number or number > 500 or number < 1: return await ctx.send("Insira um número válido!")
        def check(msg):
            if msg.id == ctx.message.id: return False
            if member:
                return msg.author.id == member.id
            else:
                return True
        deleted = await ctx.channel.purge(limit=number+1, check=check, after=datetime.now() - timedelta(days=14))
        await ctx.send(f'Deletei **{len(deleted)}/{number}**!', delete_after=5)
        await asyncio.sleep(5)
        await ctx.message.delete()
    
    @clear.error
    async def on_clear_error(self, ctx, error):
        if isinstance(error, commands.BotMissingPermissions):
            pass
        else:
            raise error
        

def setup(client):
    client.add_cog(Utility(client))