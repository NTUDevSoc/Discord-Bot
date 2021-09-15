import discord
import datetime
from datetime import datetime
from discord.ext import commands
from discord import RawReactionActionEvent

class Logs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        removeEmbed=discord.Embed(title="__**Member Left**__", description="Member: "+member.name+" ("+member.mention+")", color=0xf4a701)
        removeEmbed.set_footer(text="Left at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        await self.client.botLogChannel.send(embed=removeEmbed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        deleteEmbed=discord.Embed(title="__**Message Deleted**__", description="Message Author: "+message.author.mention, color=0xe80202)
        if message.reference != None:
            deleteEmbed.add_field(name="__Reply to "+message.reference.resolved.author.name+"'s Message__", value=message.reference.resolved.content, inline=False)
        deleteEmbed.add_field(name="__Message Content__", value=message.content, inline=False)
        deleteEmbed.add_field(name="__Message Channel__", value=message.channel.name, inline=False)
        deleteEmbed.set_footer(text="Deleted at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        await self.client.botLogChannel.send(embed=deleteEmbed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return
        else:
            editEmbed=discord.Embed(title="__**Message Edited**__", description="Message Author: "+before.author.mention, color=0xe7ec11)
            editEmbed.add_field(name="__Message Channel__", value=before.channel.name, inline=False)
            editEmbed.add_field(name="__Message Before__", value=before.content, inline=False)
            editEmbed.add_field(name="__Message After__", value=after.content, inline=False)
            editEmbed.set_footer(text="Edited at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            await self.client.botLogChannel.send(embed=editEmbed)

def setup(client):
    client.add_cog(Logs(client))