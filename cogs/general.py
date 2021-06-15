import discord
from discord.ext import commands

async def command_channels(ctx):
    return ctx.channel.id == 854307344950099971

class General(commands.Cog):

    def __init__(self, client):
        self.client = client

    #By Emi/Peter
    @commands.command()
    @commands.check(command_channels)
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

def setup(client):
    client.add_cog(General(client))