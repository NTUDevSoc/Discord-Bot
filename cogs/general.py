import discord
from discord.ext import commands

async def command_channels(ctx):
    return ctx.channel.id in (517651663729852416, 505476463492071425)

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

    @commands.command(aliases=['GitHub', 'git', 'Github', 'gitHub', 'Git', 'source', 'sourcecode'])
    @commands.check(command_channels)
    async def github(self, ctx):
        code=discord.Embed(title="Here is a link to the bot's source code", description="https://github.com/NTUDevSoc/Discord-Bot", color=0xe7ec11)
        code.set_author(name="Discord Bot Source Code", icon_url="https://i.imgur.com/NhVjX8S.png")
        code.set_footer(text="Feature developed by Emi/Peter")
        await ctx.send(embed=code)

    @commands.command(aliases=['Social', 'socials', 'twitter', 'facebook', 'instagram', 'socialmedia'])
    @commands.check(command_channels)
    async def social(self, ctx):
        socials=discord.Embed(title="DevSoc Social Links", description="Here are all the links to official DevSoc Social Media pages", color=0xe7ec11)
        socials.set_thumbnail(url="https://i.imgur.com/NhVjX8S.png")
        socials.add_field(name="Twitter", value="https://twitter.com/devsoc", inline=False)
        socials.add_field(name="Facebook", value="https://facebook.com/devsoc", inline=False)
        socials.add_field(name="Instagram", value="https://instagram.com/ntudevsoc", inline=False)
        socials.set_footer(text="Feature developed by Emi/Peter")
        await ctx.send(embed=socials)

    @commands.command(aliases=['devhelp', 'halp', 'commands'])
    @commands.check(command_channels)
    async def help(self, ctx):
        thehelp=discord.Embed(title="__DevSoc Bot - Commands__", description="*This dialog gives you all the commands currently available for use with DevSoc Bot.*", color=0xe7ec11)
        thehelp.add_field(name=".setrole", value="For setting your role in the server.", inline=False)
        thehelp.add_field(name=".announcement", value="To subscribe or unsubscribe from server announcements.", inline=False)
        thehelp.add_field(name=".social", value="Links to all of DevSoc's social pages.", inline=False)
        thehelp.add_field(name=".whois", value="Check who someone in the server is.", inline=False)
        thehelp.add_field(name=".github", value="Links to the github source code of the bot.", inline=False)
        thehelp.add_field(name=".members", value="Checks the members of each year group in the server.", inline=False)
        thehelp.add_field(name=".courses", value="Checks the members of each course in the server.", inline=False)
        thehelp.add_field(name=".highlight", value=".highlight set [word] - To be notified whenever the word is said\n.highlight remove - Remove yourself from the highlights", inline=False)
        thehelp.add_field(name=".covidoverview", value="Gives an overview of UK COVID cases.", inline=False)
        thehelp.add_field(name=".covidregion (REGION)", value="Gives an overview of COVID cases in a region of the UK.", inline=False)
        thehelp.set_footer(text="Feature developed by Emi/Peter")
        await ctx.send(embed=thehelp)

    @commands.command(aliases=['membercount', 'membercheck', 'memberlist'])
    @commands.check(command_channels)
    async def members(self, ctx):
        devMembers = {
            "First Year": 0,
            "Second Year": 0,
            "Placement Year": 0,
            "Third Year": 0,
            "Fourth Year": 0,
            "MSc Student": 0,
            "Alumni": 0
        }
        guild = ctx.message.guild
        for member in guild.members:
            for role in member.roles:
                if role.name in devMembers:
                    devMembers[role.name] += 1
        count=discord.Embed(title="__DevSoc Members__", description="*Here are the members of each year group within this server.*", color=0xe7ec11)
        finalYearTotal = 0
        for year in devMembers:
            if year == "Third Year":
                finalYearTotal += devMembers[year]
            elif year == "Fourth Year":
                finalYearTotal += devMembers[year]
                count.add_field(name="Third/Final Year", value=str(finalYearTotal)+" members", inline=False)
            else:
                count.add_field(name=year, value=str(devMembers[year])+" members", inline=False)
        count.set_footer(text="Feature developed by Emi/Peter")
        await ctx.send(embed=count)

    @commands.command(aliases=['coursecount', 'coursecheck', 'courselist'])
    @commands.check(command_channels)
    async def courses(self, ctx):
        devCourses = {
            "Computer Science": 0,
            "Software Engineering": 0,
            "Computer Science (Games Technology)": 0,
            "Computer Systems (Cyber Security)": 0,
            "Computing": 0,
            "Other": 0
        }
        guild = ctx.message.guild
        for member in guild.members:
            for role in member.roles:
                if role.name in devCourses:
                    devCourses[role.name] += 1
        count=discord.Embed(title="__DevSoc Members - Courses__", description="*Here are the members of each course within this server.*", color=0xe7ec11)
        for course in devCourses:
            count.add_field(name=course, value=str(devCourses[course])+" members", inline=False)
        count.set_footer(text="Feature developed by Peter")
        await ctx.send(embed=count)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name='Announcement')
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            await self.client.send('ERROR: I don\'t have permission to set roles.')
        arrivalsChannel = self.client.get_channel(783388268631818280)
        roleChannel = self.client.get_channel(785558941688922152)
        rulesChannel = self.client.get_channel(804817413841354843)
        await arrivalsChannel.send("Welcome "+member.mention+"! Head to "+rulesChannel.mention+" to accept our server rules, then head to "+roleChannel.mention+" to set your roles using Reaction Roles and access the rest of the server.")
        embed=discord.Embed(title="Welcome to Devsoc!", description="\n**Make sure to read and accept the [rules](https://discord.com/channels/206351865754025984/804817413841354843/804819409536417832) then head to [self-roles](https://discord.com/channels/206351865754025984/785558941688922152/804068089758482472) to set your roles!**", color=0xe7ec11)
        await member.send(embed=embed)

def setup(client):
    client.add_cog(General(client))
