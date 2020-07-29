import discord
import time
from datetime import datetime
from discord.ext import commands
startTime = time.time()

async def in_bot_commands(ctx):
    channel_ids = (186605768080883713, 517651663729852416, 505476463492071425)
    return ctx.channel.id in channel_ids

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(in_bot_commands)
    async def whois(self, ctx, user: discord.Member = None):
        if user:
            user_info = discord.Embed(title="Name", description=user.name, color=0xe7ec11)
            user_info.set_thumbnail(url=user.avatar_url)
            user_info.set_author(name=user.name + '#' + user.discriminator, icon_url=user.avatar_url)
            user_info.add_field(name='Nickname', value=user.nick)
            user_info.add_field(name='Status', value=user.status)
            user_info.add_field(name='Joined Server', value=user.joined_at.strftime("%Y-%m-%d %H:%M:%S"))
            user_info.add_field(name='Joined Discord', value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"))
            user_roles = []
            for i in range(len(user.roles)):
                user_roles.append(user.roles[i].mention)
            user_info.add_field(name='Roles', value=', '.join(user_roles))
            user_info.set_footer(text='ID: ' + str(user.id))
            await ctx.send(embed=user_info)
        else:
            await ctx.send('Please tag a user!')

    @whois.error
    async def whois_error(self, channel, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await channel.send('Please tag a user!')

    # Command that links to GitHub
    @commands.command(aliases=['GitHub', 'git', 'Github', 'gitHub', 'Git', 'source', 'sourcecode'])
    @commands.check(in_bot_commands)
    async def github(self, ctx):
        code=discord.Embed(title="Here is a link to the bot's source code", description="https://github.com/NTUDevSoc/Discord-Bot", color=0xe7ec11)
        code.set_author(name="Discord Bot Source Code", icon_url="https://pbs.twimg.com/profile_images/895052854788071425/3To9GJza_400x400.jpg")
        code.set_footer(text="Bot developed by Ram/Peter")
        await ctx.send(embed=code)

    #Command that links to all DevSoc social pages
    @commands.command(aliases=['Social', 'socials', 'twitter', 'facebook', 'instagram', 'socialmedia'])
    @commands.check(in_bot_commands)
    async def social(self, ctx):
        socials=discord.Embed(title="DevSoc Social Links", description="Here are all the links to official DevSoc Social Media pages", color=0xe7ec11)
        socials.set_thumbnail(url="https://pbs.twimg.com/profile_images/895052854788071425/3To9GJza_400x400.jpg")
        socials.add_field(name="Twitter", value="https://twitter.com/devsoc", inline=False)
        socials.add_field(name="Facebook", value="https://facebook.com/devsoc", inline=False)
        socials.add_field(name="Instagram", value="https://instagram.com/ntudevsoc", inline=False)
        socials.set_footer(text="Bot developed by Ram/Peter")
        await ctx.send(embed=socials)


def setup(bot):
    bot.add_cog(Commands(bot))

