import discord
from discord.ext import commands

class Commands:
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def givemebasicrole(self, ctx):
        print(bot.manage_roles)
        role = discord.utils.get(ctx.guild.roles, name='DevSoc')
        await ctx.author.add_roles([role,])
        
    
    @commands.command()
    async def whois(self, ctx, user: discord.Member = None):
        if user:
            user_info = discord.Embed(title="Name", description=user.name, color=user.color)
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
            await ctx.send('Please tag an user!')

    @whois.error
    async def whois_error(self, channel, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await channel.send('Please tag an user!')

    # Command that links to GitHub
    @commands.command(aliases=['GitHub', 'git', 'Github', 'gitHub', 'Git', 'source', 'sourcecode'])
    async def github(self, ctx):
        await ctx.send("You can find the source code on: https://github.com/NTUDevSoc/Discord-Bot")


def setup(bot):
    bot.add_cog(Commands(bot))

