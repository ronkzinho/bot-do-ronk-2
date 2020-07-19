import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["coffi", "coffe", "cof"])
    async def make(self, ctx):
        resposta = random.choice(["Ai meique cofe cofe fo ior dei ☕"] + ["Ai meique cofe cofe fo ior dei"] * 99)
        return await ctx.send(resposta)

    @commands.command(aliases=["leticia"])
    async def roi(self, ctx):
        return await ctx.send("Roi... {0} né?".format(ctx.message.author.display_name))
    
    @commands.command(aliases=["karpa"])
    async def gadiao(self, ctx):
        return await ctx.send("Kakajota???? :flushed:")

def setup(client):
    client.add_cog(Fun(client))