import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix=".", owner_id=153487284061077504, description="DevBot")

TOKEN = os.environ["TOKEN"]

@client.event
async def on_ready():

    print(f"\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n")
    print("Successfully logged in")
    client.botTestChannel = await client.fetch_channel(850023556069851156)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded Cog: {filename}")

client.run(TOKEN)