import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ms"])
    async def ping(self, ctx):
        ping = float("%.3f" % self.client.latency)
        await ctx.send(f'{int(ping * 1000)}ms')

def setup(client):
    client.add_cog(Utility(client))