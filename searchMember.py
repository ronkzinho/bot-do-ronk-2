import discord
from discord.ext import commands

async def convert(client, ctx, args):
    user = args.lower()
    try:
        return ctx.message.mentions[0] if len(ctx.message.mentions) > 0 else discord.utils.find(lambda u: not u.bot and (user in u.name.lower() or str(u.id) == user), client.users)
    except Exception:
        return None