import discord
from discord.ext import commands

class Error(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_error(self, error):

        embed=discord.Embed(title="Error", description=f"{error}", color=0xe7ec11)
        embed.set_footer(text="Bot created by DevJ4Y", icon_url="https://www.j4y.dev/botassets/j4y.gif")
        await self.client.botLogChannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        embed=discord.Embed(title="Error", url=f"{ctx.message.jump_url}", description=f"{error}", color=0xe7ec11)
        embed.set_author(name=f"{ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
        embed.add_field(name="Message:", value=f"{ctx.message.content}", inline=False)
        embed.add_field(name="Server:", value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name="Channel:", value=f"{ctx.channel.name}", inline=True)  
        embed.set_footer(text="Bot created by DevJ4Y", icon_url="https://www.j4y.dev/botassets/j4y.gif")
        await self.client.botLogChannel.send(embed=embed)

def setup(client):
    client.add_cog(Error(client))