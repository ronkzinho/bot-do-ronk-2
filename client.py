import os
import discord
import dotenv
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix="><", case_insensitive=True) 

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

client.run(os.getenv("TOKEN"))