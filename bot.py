#by Emi/Sunglass :)

#imports
import os, asyncio
import discord
from discord.ext import commands

#New discord intents system
intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.messages = True
intents.guilds = True

#global vars
TOKEN = os.environ['DISCORD_TOKEN']

#set up bot object and cogs
bot = commands.Bot(command_prefix='.', intents=intents)
extensions = ['cogs.commands', 'cogs.roles']

#EVENTS
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='DevSoc')
    role2 = discord.utils.get(member.guild.roles, name='Announcement')
    try:
        await member.add_roles(role)
        await member.add_roles(role2)
    except discord.Forbidden:
        await bot.send('ERROR: I don\'t have permission to set roles.')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if "testingphrase344" in message.content:
        await message.delete()
    elif "D3vS0cRul3z?N0P3.n0_0neall0wed1n" in message.content:
        await message.delete()

#function to make the bot print every 28mins so Heroku doesn't stop it
async def stay_awake():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print('Im awake :)')
        await asyncio.sleep(1680) #runs every 28mins.

#Load our extensions(cogs)
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension ' + extension + '.')
            print(e)

@bot.event
async def on_ready():
    print('-'*30)
    print('Logged in as:')
    print('Name: ' + bot.user.name)
    print('ID: ' + str(bot.user.id))
    print('-'*30)

#run the bot
bot.loop.create_task(stay_awake())
bot.run(TOKEN)


#testing hacktober pulls
