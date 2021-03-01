#by Emi/Sunglass :)

#imports
import os, asyncio
import discord
from discord.ext import commands
import json
from json import dumps
import re
from datetime import datetime

#New discord intents system
intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.messages = True
intents.guilds = True
intents.reactions = True

#global vars
TOKEN = os.environ['DISCORD_TOKEN']

#set up bot object and cogs
bot = commands.Bot(command_prefix='.', intents=intents)
bot.remove_command('help')
extensions = ['cogs.commands', 'cogs.roles', 'cogs.reaction_roles', 'cogs.rules']

#EVENTS
@bot.event
async def on_member_join(member):
    role2 = discord.utils.get(member.guild.roles, name='Announcement')
    try:
        await member.add_roles(role2)
    except discord.Forbidden:
        await bot.send('ERROR: I don\'t have permission to set roles.')
    arrivalsChannel = bot.get_channel(783388268631818280)
    roleChannel = bot.get_channel(785558941688922152)
    rulesChannel = bot.get_channel(804817413841354843)
    await arrivalsChannel.send("Welcome "+member.mention+"! Head to "+rulesChannel.mention+" to accept our server rules, then head to "+roleChannel.mention+" to set your roles using Reaction Roles and access the rest of the server.")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        print(ctx.author,"attempted to run:",ctx.message.content)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot == True:
        return
    await bot.process_commands(message)
    hanArray = ["hannah"]
    for han in hanArray:
        if han in message.content.lower():
            await message.channel.send('<@!131332703919276032> sus')
            return
    if "beans" in message.content.lower():
        if message.author.id == 196142609528389632:
            return
        beans = discord.Embed()
        beans.set_image(url="https://i.imgur.com/GkyCNCH.jpg")
        await message.author.send(embed=beans)

@bot.event
async def on_member_remove(member):
    guild = discord.utils.get(bot.guilds, id=206351865754025984)
    logchannel = discord.utils.get(guild.channels, id=814152479100633128)
    removeEmbed=discord.Embed(title="__**Member Left**__", description="Member: "+member.name+" ("+member.mention+")", color=0xe7ec11)
    removeEmbed.set_footer(text="Left at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    await logchannel.send(embed=removeEmbed)

@bot.event
async def on_message_delete(message):
    guild = discord.utils.get(bot.guilds, id=206351865754025984)
    logchannel = discord.utils.get(guild.channels, id=814152479100633128)
    deleteEmbed=discord.Embed(title="__**Message Deleted**__", description="Message Author: "+message.author.mention, color=0xe7ec11)
    if message.reference != None:
        deleteEmbed.add_field(name="__Reply to "+message.reference.resolved.author.name+"'s Message__", value=message.reference.resolved.content, inline=False)
    deleteEmbed.add_field(name="__Message Content__", value=message.content, inline=False)
    deleteEmbed.add_field(name="__Message Channel__", value=message.channel.name, inline=False)
    deleteEmbed.set_footer(text="Deleted at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    await logchannel.send(embed=deleteEmbed)

@bot.event
async def on_message_edit(before, after):
    if before.content == after.content:
        return
    else:
        guild = discord.utils.get(bot.guilds, id=206351865754025984)
        logchannel = discord.utils.get(guild.channels, id=814152479100633128)
        editEmbed=discord.Embed(title="__**Message Edited**__", description="Message Author: "+before.author.mention, color=0xe7ec11)
        editEmbed.add_field(name="__Message Channel__", value=before.channel.name, inline=False)
        editEmbed.add_field(name="__Message Before__", value=before.content, inline=False)
        editEmbed.add_field(name="__Message After__", value=after.content, inline=False)
        editEmbed.set_footer(text="Edited at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        await logchannel.send(embed=editEmbed)

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
            print("Loaded " + extension)
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

