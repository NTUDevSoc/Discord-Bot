import discord
import time
from discord.ext import commands
startTime = time.time()

async def is_admin(ctx):
    committee = discord.utils.get(ctx.guild.roles, name='Committee')
    elders = discord.utils.get(ctx.guild.roles, name='DevSoc Elders')
    if committee in ctx.message.author.roles or elders in ctx.message.author.roles:
        return True
    else:
        return False

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #Help dialog for admin commands
    @commands.command(aliases=['admincommands'])
    @commands.check(is_admin)
    async def adminhelp(self, ctx):
        thehelp=discord.Embed(title="__DevSoc Bot - Admin Commands__", description="*This dialog gives you all the admin commands for DevBot.*", color=0xe7ec11)
        thehelp.add_field(name=".clearchat (AMOUNT)", value="Clears a set number of messages from the chat.", inline=False)
        thehelp.add_field(name=".servermute @user", value="Server mutes or unmutes a user.", inline=False)
        thehelp.add_field(name=".channelmute", value="Mutes all users in a voice channel.", inline=False)
        thehelp.add_field(name=".channelunmute", value="Unmutes all users in a voice channel.", inline=False)
        thehelp.set_footer(text="Bot created by Emi/Peter")
        await ctx.send(embed=thehelp)

    #Command to mute all users in your current voice channel
    @commands.command()
    @commands.check(is_admin)
    async def channelmute(self, ctx):
        channel = ctx.message.author.voice.channel
        for member in channel.members:
            await member.edit(mute=True)
        await ctx.send('Channel members muted!')


    #Command to unmute all users in your current voice channel
    @commands.command()
    @commands.check(is_admin)
    async def channelunmute(self, ctx):
        channel = ctx.message.author.voice.channel
        for member in channel.members:
            await member.edit(mute=False)
        await ctx.send('Channel members unmuted!')


    #Command to server mute someone
    @commands.command()
    @commands.check(is_admin)
    async def servermute(self, ctx, user: discord.Member = None):
        if user:
            servermute = discord.utils.get(ctx.guild.roles, name='Server Muted')
            devsoc = discord.utils.get(ctx.guild.roles, name='DevSoc')
            if servermute in user.roles:
                await user.remove_roles(servermute)
                await user.add_roles(devsoc)
                await ctx.send("Removed server mute!")
            else:
                for role in user.roles[1:]:
                    await user.remove_roles(role)
                await user.add_roles(servermute)
                await ctx.send("Server muted!")
        else:
            await ctx.send("Please tag a user!")


    #Command to clear messages
    @commands.command()
    @commands.check(is_admin)
    async def clearchat(self, ctx, amount):
        try:
            amount = int(amount)
            if amount > 45:
                await ctx.send("You can only clear 45 messages at a time!")
            else:
                await ctx.channel.purge(limit=amount)
                await ctx.send("Channel cleaned")
        except ValueError:
            await ctx.send("Not a valid number!")

def setup(bot):
    bot.add_cog(AdminCommands(bot))
