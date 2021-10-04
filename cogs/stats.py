import discord
import time
from discord.ext import commands

async def is_admin(ctx):
    committee = discord.utils.get(ctx.guild.roles, name='Committee')
    elders = discord.utils.get(ctx.guild.roles, name='DevSoc Elders')
    if committee in ctx.message.author.roles or elders in ctx.message.author.roles:
        return True
    else:
        return False

class Stats(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, client):
        self.client = client
        self.timestamp = time.time()

    @commands.command()
    @commands.check(is_admin)
    async def room(self, ctx, status = None):
        if time.time() - self.timestamp >= 600:
            await ctx.send(f"**Please wait {time.time() - self.timestamp} seconds before chaning**")
            return

        if not status:
            return

        if status.lower() in ("opened", "open", "o"):
            status = "Open"
        elif status.lower() in ("closed", "close", "c"):
            status = "Closed"

        await self.client.roomChannel.edit(name=f"DevSoc Room: {status}")
        await ctx.send(f"Room Status: **{status}**")
        self.timestamp = time.time()


            
def setup(client):
    client.add_cog(Stats(client))