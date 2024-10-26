import discord
import os
import asyncio
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.messages = True
intents.guilds = True
intents.reactions = True

client = commands.Bot(command_prefix=".", owner_id=83616065854115840, description="DevBot", intents=intents)
client.remove_command('help')

TOKEN = os.environ["TOKEN"]

@client.event
async def on_ready():

    print(f"\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n")
    print("Successfully logged in")

    client.botLogChannel = await client.fetch_channel(814152479100633128)
    client.botCommandChannel = await client.fetch_channel(517651663729852416)
    client.roomChannel = await client.fetch_channel(892436503890915438)

#function to make the bot print every 28mins so Heroku doesn't stop it
async def stay_awake():
    await client.wait_until_ready()
    while not client.is_closed():
        print('Im awake :)')
        await asyncio.sleep(1680) #runs every 28mins.

@client.event
async def setup_hook():
    #schedule the stay_awake task
    client.loop.create_task(stay_awake())

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog: {filename}")

async def main():
    async with client:
        await load_cogs()
        await client.start(TOKEN)

asyncio.run(main())
