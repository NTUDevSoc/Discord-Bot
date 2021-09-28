from os import stat
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

class Stats(commands.Cog, command_attrs=dict(hidden=True)):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(is_admin)
    async def room(self, ctx, status = None):
        await ctx.message.delete()
        
        if not status:
            return

        if status.lower() in ("open"):
            await self.client.roomChannel.edit(name="DevSoc Room: Open")
        elif status.lower() in ("closed"):
            await self.client.roomChannel.edit(name="DevSoc Room: Closed")
        else:
            await self.client.roomChannel.edit(name=f"DevSoc Room: {status}]")




            
def setup(client):
    client.add_cog(Stats(client))