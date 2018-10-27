#by Ram :)

#imports
import os
import asyncio
import discord
from discord.ext import commands

#global vars
TOKEN = os.environ['DISCORD_TOKEN']

#set up bot object
bot = commands.Bot(command_prefix='.')

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='DevSoc')
    await bot.add_roles(member, role)

#Commands
@bot.command()
async def whois(channel, user:discord.Member=None):
    if user:
        user_info = discord.Embed(title = "Name", description=user.name, color=user.color)
        user_info.set_thumbnail(url=user.avatar_url)
        user_info.set_author(name=user.name + '#' + user.discriminator, icon_url= user.avatar_url)
        user_info.add_field(name='Nickname', value=user.nick)
        user_info.add_field(name='Status', value=user.status)
        user_info.add_field(name='Joined Server', value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        user_info.add_field(name='Joined Discord', value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        user_roles = []
        for i in range(len(user.roles)):
            user_roles.append(user.roles[i].mention)
        user_info.add_field(name='Roles', value=', '.join(user_roles))
        user_info.set_footer(text='ID: ' + str(user.id))
        await channel.send(embed=user_info)
    else:
        await channel.send('Please tag an user!')
@whois.error
async def whois_error(channel, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        await channel.send('Please tag an user!')


#function to make the bot print every 28mins so Heroku doesn't stop it
async def stay_awake():
    await bot.wait_until_ready()
    while True:
        print('Im awake :)')
        await asyncio.sleep(1680)

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
