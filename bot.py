import discord
import os, asyncio
from discord.ext import commands

client = commands.Bot(command_prefix=".", owner_id=153487284061077504, description="DevBot")
client.remove_command('help')

TOKEN = os.environ["TOKEN"]

@client.event
async def on_ready():

    print(f"\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n")
    print("Successfully logged in")

    client.botLogChannel = await client.fetch_channel(854307344778002435) #TODO UPDATE ID
    client.botCommandChannel = await client.fetch_channel(854307344950099971)

async def stay_awake():
    await client.wait_until_ready()
    while not client.is_closed():
        print('Im awake :)')
        await asyncio.sleep(1680) #runs every 28mins.

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"Loaded Cog: {filename}")

client.loop.create_task(stay_awake())
client.run(TOKEN)