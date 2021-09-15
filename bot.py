import discord
import os, asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.messages = True
intents.guilds = True
intents.reactions = True

client = commands.Bot(command_prefix=".", owner_id=153487284061077504, description="DevBot", intents=intents)
client.remove_command('help')

TOKEN = os.environ["TOKEN"]

@client.event
async def on_ready():

    print(f"\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n")
    print("Successfully logged in")

    client.botLogChannel = await client.fetch_channel(814152479100633128)
    client.botCommandChannel = await client.fetch_channel(517651663729852416)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded Cog: {filename}")

client.run(TOKEN)