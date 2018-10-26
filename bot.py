#by Ram :)

#imports
import discord
from discord.ext import commands

#global vars
TOKEN = ''

#set up bot object
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='DevSoc')
    await bot.add_roles(member, role)


@bot.event
async def on_ready():
    print('-'*30)
    print('Logged in as:')
    print('Name: ' + bot.user.name)
    print('ID: ' + bot.user.id)
    print('-'*30)

#run the bot
bot.run(TOKEN)