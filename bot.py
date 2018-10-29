#by Ram :)

#imports
import os,asyncio, discord
from discord.ext import commands

#global vars
TOKEN = os.environ['DISCORD_TOKEN']

#set up bot object and cogs
bot = commands.Bot(command_prefix='.')
extensions = ['cogs.commands']

#EVENTS
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='DevSoc')
    await member.add_roles(role)

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
        except:
            print('Failed to load extension ' + extension + '.')

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
