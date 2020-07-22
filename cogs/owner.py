import discord
import inspect
import ast
import asyncio
from .functions.insert_returns import insert_returns
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.is_owner()
    async def test(self, ctx):
        await ctx.send("Olá mundo!")

    @commands.command(name="eval", aliases=["e"], hidden=True)
    @commands.is_owner()
    async def evalCommand(self, ctx, *, cmd):
        client = self.client
        if cmd == None: return
        try:
            fn_name = "_eval_expr"
            cmd = cmd.strip("` ")
            cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
            body = f"async def {fn_name}():\n{cmd}"
            parsed = ast.parse(body)
            body = parsed.body[0].body
            insert_returns(body)
            env = {
                'client': client,
                'discord': discord,
                'commands': commands,
                'ctx': ctx
            }
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
            await ctx.send(result)
        except Exception as e:
            await ctx.send(e)

    @commands.command(aliases=["r", "reloadcog", "reload_cog", "rc"], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, *, module: str):
        try:
            if(module == "all"):
                for cog in list(self.client.cogs):
                    self.client.unload_extension(f"cogs.{cog.lower()}")
                    self.client.load_extension(f"cogs.{cog.lower()}")
            else:
                self.client.unload_extension(module)
                self.client.load_extension(module)
            msg = await ctx.send("Pronto!")
            await asyncio.sleep(5)
            await msg.delete()
            await ctx.message.delete()
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))

def setup(client):
    client.add_cog(Owner(client))