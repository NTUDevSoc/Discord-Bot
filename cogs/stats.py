import discord
import time
from discord.ext import commands

async def is_admin(ctx):
    committee = discord.utils.get(ctx.guild.roles, name='Committee')
    srCommittee = discord.utils.get(ctx.guild.roles, name='SR Committee')
    supCommittee = discord.utils.get(ctx.guild.roles, name='Supporting Committee')
    elders = discord.utils.get(ctx.guild.roles, name='DevSoc Elders')
    trainee = discord.utils.get(ctx.guild.roles, name='Trainee Committee')
    return True if committee in ctx.message.author.roles or supCommittee in ctx.message.author.roles or  srCommittee in ctx.message.author.roles or elders in ctx.message.author.roles or trainee in ctx.message.author.roles else False

class Stats(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, client):
        self.client = client
        self.timestamp = time.time()

    @commands.command()
    @commands.check(is_admin)
    async def room(self, ctx, status = None):
        if time.time() - self.timestamp <= 300:
            await ctx.send(f"**Please wait 5 minutes before trying again**")
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
