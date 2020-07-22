import discord
import inspect
import ast
from .functions.insert_returns import insert_returns
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="eval")
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

def setup(client):
    client.add_cog(Owner(client))