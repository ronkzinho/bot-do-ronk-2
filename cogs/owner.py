import discord
import inspect
from discord.ext import commands

class Adm(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="eval")
    @commands.is_owner()
    async def evalCommand(self, ctx, *, cmd):
        if cmd == None: return
        try:
            res = eval(cmd)
            if inspect.isawaitable(res):
                return await ctx.send(await res)
            else:
                return await ctx.send(res)
        except Exception as err:
            return await ctx.send(err)

def setup(client):
    client.add_cog(Adm(client))