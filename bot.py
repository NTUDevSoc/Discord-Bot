#by Ram :)

#imports
import os
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
@bot.command
async def whois(ctx, user):
    user_info = discord.Embed(title = "Name", description=user.name, color=user.color)
    user_info.set_thumbnail(user.avatar_url)
    user_info.set_author(name=user.name + '#' + user.discriminator, icon_url= user.avatar_url)
    user_info.add_field(name='Nickname', value=user.nick)
    user_info.add_field(name='Status', value=user.status)
    user_info.add_field(name='Joined Server', value=user.joined_at)
    user_info.add_field(name='Joined Discord', value=user.created_at)
    user_roles = []
    for i in range(len(user.roles)):
        user_roles.append(user.roles[i].mention)
    user_info.add_field(name='Roles', value=', '.join(user_roles))
    user_info.set_footer(text='ID: ' + user.id)
    await ctx.send(user_info)


@bot.event
async def on_ready():
    print('-'*30)
    print('Logged in as:')
    print('Name: ' + bot.user.name)
    print('ID: ' + str(bot.user.id))
    print('-'*30)

#run the bot
bot.run(TOKEN)
