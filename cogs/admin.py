import discord
import datetime
from discord.ext import commands

async def is_admin(ctx):
    committee = discord.utils.get(ctx.guild.roles, name='Committee')
    elders = discord.utils.get(ctx.guild.roles, name='DevSoc Elders')
    if committee in ctx.message.author.roles or elders in ctx.message.author.roles:
        return True
    else:
        return False

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(is_admin)
    async def clearchat(self, ctx, amount: int):
        if amount > 24:
            await ctx.send("You can only clear up to 24 messages at a time")
        else:
            messages = await ctx.channel.purge(limit=amount+1)
            embed=discord.Embed(title="Chat Cleared", description=f"{amount} messages cleared from {ctx.channel.name} \n {str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}", color=0xe7ec11)
            for message in messages:
                if message.embeds:
                    embed.add_field(name=message.author.name, value="Embedded Message", inline=False)
                else:
                    embed.add_field(name=message.author.name, value=message.content, inline=False)
            embed.set_footer(text="Bot created by <J4Y>", icon_url="https://www.j4y.dev/botassets/j4y.gif")
            await self.client.botLogChannel.send(embed=embed)

            
def setup(client):
    client.add_cog(Admin(client))