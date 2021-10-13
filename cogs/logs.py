import discord
import datetime
from datetime import datetime
from discord.ext import commands

class Logs(commands.Cog):

    def __init__(self, client):
        self.client = client

    def message_logs(self, message, before = None):
        
        if isinstance(message.channel, discord.channel.DMChannel):
            return

        embed = None
        if message.embeds:
            embed=discord.Embed(title="__**Message Deleted**__", description="Message Author: "+message.author.mention, color=0xe80202)
            embed.add_field(name="__Message Content__", value="[Embedded Message]", inline=False)
            embed.add_field(name="__Message Channel__", value=message.channel.name, inline=False)
        elif message.content:
            if before != None:
                embed=discord.Embed(title="__**Message Edited**__", description="Message Author: "+message.author.mention, color=0xe7ec11)
                embed.set_footer(text="Edited at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            else:
                embed=discord.Embed(title="__**Message Deleted**__", description="Message Author: "+message.author.mention, color=0xe80202)
                embed.set_footer(text="Deleted at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            if message.reference != None:
                if message.reference.resolved != None:
                    embed.add_field(name="__Reply to "+message.reference.resolved.author.name+"'s Message__", value=message.reference.resolved.content, inline=False)

            if before != None:
                embed.add_field(name="__Message Before__", value=before.content, inline=False)
                embed.add_field(name="__Message After__", value=message.content, inline=False)
            else:
                embed.add_field(name="__Message Content__", value=message.content, inline=False)

            embed.add_field(name="__Message Channel__", value=message.channel.name, inline=False)
        else:
            embed=discord.Embed(title="__**Message Deleted**__", description="Message Author: "+message.author.mention, color=0xe80202)

        if message.attachments:
            file_names = ""
            for file in message.attachments:
                file_names += f"{file.filename}: {file.url}\n" 
            embed.add_field(name=f"__Message Attachments: {len(message.attachments)}__", value=file_names, inline=False)

            pic_ext = [".jpg",".png",".jpeg",".gif"]
            for ext in pic_ext:
                if message.attachments[0].filename.endswith(ext):
                    embed.set_image(url=message.attachments[0].url)

        return embed


    @commands.Cog.listener()
    async def on_member_join(self, member):
        joinEmbed=discord.Embed(title="__**Member Join**__", description=f"Member: {member.name}#{member.discriminator}", color=0xf4a701)
        joinEmbed.set_thumbnail(url=member.avatar_url)
        joinEmbed.add_field(name='Joined Server', value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
        joinEmbed.add_field(name='Joined Discord', value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"))
        joinEmbed.set_footer(text=f"ID: {member.id}")
        await self.client.botLogChannel.send(embed=joinEmbed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        removeEmbed=discord.Embed(title="__** Member Left**__", description="Member: "+member.name+" ("+member.mention+")", color=0xf4a701)
        removeEmbed.set_footer(text="Left at: "+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        await self.client.botLogChannel.send(embed=removeEmbed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        await self.client.botLogChannel.send(embed=self.message_logs(message))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):

        if before.content == after.content:
            return

        await self.client.botLogChannel.send(embed=self.message_logs(after,before))

def setup(client):
    client.add_cog(Logs(client))