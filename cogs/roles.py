import discord, datetime, asyncio
from discord.ext import commands

async def in_bot_commands(ctx):
    channel_ids = (186605768080883713, 517651663729852416, 505476463492071425)
    return ctx.channel.id in channel_ids

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
##        self.bot.loop.create_task(self.check_day())

    @commands.command()
    @commands.check(in_bot_commands)
    async def setrole(self, ctx, *args):
        if len(args) == 0:
            roles=discord.Embed(title="This is the syntax for setting a role", description=".setrole (year) (if going on/went to placement)", color=0xe7ec11)
            roles.set_author(name="Set Role Command - Info", icon_url="https://pbs.twimg.com/profile_images/895052854788071425/3To9GJza_400x400.jpg")
            roles.add_field(name="Year options", value="First Year - first, 1, 1st, one\nSecond Year - second, 2, 2nd, two\nThird Year - third, 3, 3rd, three\nPlacement Year - placement, 3/4, 3/4ths\nFourth Year - fourth, 4, 4th, four\nAlumni - alumni, 5, 5th, five, last", inline=False)
            roles.add_field(name="Placement options", value="Yes/No", inline=False)
            roles.set_footer(text="Bot developed by Emi/Sunglass")
            await ctx.send(embed=roles)
        elif len(args) == 1:
            await self.set_role(ctx, args[0])
        elif len(args) == 2:
            await self.set_role(ctx, args[0], args[1])
        else:
            await ctx.send('Too many arguments!')

    @commands.command()
    @commands.check(in_bot_commands)
    async def oghelproles(self, ctx):
        await ctx.send(
        '''
        To set your role please follow this:
        .setrole <year> <if going/went to placement>
        
        NOTE: It's NOT case sensitive.
        Possibilities for <year>:
        First Year - first, 1, 1st, one.
        Second Year - second, 2, 2nd, two.
        Third Year - third, 3, 3rd, three.
        Placement Year - placement, 3/4, 3/4ths, wtf, inbetween.
        Fourth Year - fourth, 4, 4th, four.
        Alumni - alumni, 5, 5th, five, ?, what, last.
        
        Possibilities for <if going/went to placement>:
        Yes - true, yes, si, da, taip, yup, eyup, ofc.
        No - anything or leave empty.
        ''')

    @commands.command()
    @commands.check(in_bot_commands)
    async def helproles(self, ctx):
        roles=discord.Embed(title="This is the syntax for setting a role", description=".setrole (year) (if going on/went to placement)", color=0xe7ec11)
        roles.set_author(name="Set Role Command - Info", icon_url="https://pbs.twimg.com/profile_images/895052854788071425/3To9GJza_400x400.jpg")
        roles.add_field(name="Year options", value="First Year - first, 1, 1st, one\nSecond Year - second, 2, 2nd, two\nThird Year - third, 3, 3rd, three\nPlacement Year - placement, 3/4, 3/4ths\nFourth Year - fourth, 4, 4th, four\nAlumni - alumni, 5, 5th, five, last", inline=False)
        roles.add_field(name="Placement options", value="Yes/No", inline=False)
        roles.set_footer(text="Bot developed by Emi/Sunglass")
        await ctx.send(embed=roles)

    @commands.command()
    @commands.check(in_bot_commands)
    async def announcement(self, ctx):
        self.announcement = discord.utils.get(ctx.guild.roles, name='Announcement')
        if self.announcement in ctx.author.roles:
            await ctx.author.remove_roles(self.announcement)
            await ctx.send('You have been removed from announcements.')
        else:
            await ctx.author.add_roles(self.announcement)
            await ctx.send('You have been added to announcements.')
        

    async def set_role(self, ctx, role, placement = ''):
        self.first_year = discord.utils.get(ctx.guild.roles, name='First Year')
        self.second_year = discord.utils.get(ctx.guild.roles, name='Second Year')
        self.third_year = discord.utils.get(ctx.guild.roles, name='Third Year')
        self.placement_year = discord.utils.get(ctx.guild.roles, name='Placement Year')
        self.fourth_year = discord.utils.get(ctx.guild.roles, name='Fourth Year')
        self.alumni = discord.utils.get(ctx.guild.roles, name='Alumni')
        self.placement = discord.utils.get(ctx.guild.roles, name='Placement')

        if role.lower() in ('first', '1', '1st', 'one'):
            await ctx.author.remove_roles(self.second_year, self.third_year, self.placement_year, self.fourth_year, self.alumni)
            await ctx.author.add_roles(self.first_year)
            self.role = 'First Year'
        elif role.lower() in ('second', '2', '2nd', 'two'):
            await ctx.author.remove_roles(self.first_year, self.third_year, self.placement_year, self.fourth_year, self.alumni)
            await ctx.author.add_roles(self.second_year)
            self.role = 'Second Year'
        elif role.lower() in ('third', '3', '3rd', 'three'):
            await ctx.author.remove_roles(self.first_year, self.second_year, self.placement_year, self.fourth_year, self.alumni)
            await ctx.author.add_roles(self.third_year)
            self.role = 'Third Year'
        elif role.lower() in ('placement', '3/4', '3/4ths', 'wtf', 'inbetween'):
            await ctx.author.remove_roles(self.first_year, self.second_year, self.third_year, self.fourth_year, self.alumni)
            await ctx.author.add_roles(self.placement_year)
            self.role = 'Placement Year'
        elif role.lower() in ('fourth', '4', '4th', 'four'):
            await ctx.author.remove_roles(self.first_year, self.second_year, self.third_year, self.placement_year, self.alumni)
            await ctx.author.add_roles(self.fourth_year)
            self.role = 'Fourth Year'
        elif role.lower() in ('alumni', '5', '5th', 'five', '?', 'what', 'last'):
            await ctx.author.remove_roles(self.first_year, self.second_year, self.third_year, self.fourth_year)
            await ctx.author.add_roles(self.alumni)
            self.role = 'Alumni'
        else:
            await ctx.send('Invalid role! For roles type .helproles')
            return

        if self.role == 'Placement Year':
            if self.placement in ctx.author.roles:
                await ctx.author.remove_roles(self.placement)
            await ctx.send('Set role of: ' + self.role + '!') 
        elif placement.lower() in ('true', 'yes', 'si', 'da', 'taip', 'yup', 'eyup', 'ofc'):
            await ctx.author.add_roles(self.placement)
            await ctx.send('Set role of: ' + self.role + '! With Placement.')
        else:
            if self.placement in ctx.author.roles:
                await ctx.author.remove_roles(self.placement)
            await ctx.send('Set role of: ' + self.role + '! Without Placement.')

##    async def check_day(self):
##        await self.bot.wait_until_ready()
##        while not self.bot.is_closed():
##            await asyncio.sleep(86400)
##            print('Checking for role update!')
##            self.today = datetime.datetime.today()
##            if (self.today.month == 9 and self.today.day == 21):
##                await self.update_roles()

    @commands.command()
    @commands.check(in_bot_commands)
    async def updateroles(self, ctx):
        if str(ctx.author.id) == "280439222358245377":
            await self.update_roles()
            await ctx.send('Manually updated roles!')
        else:
            await ctx.send('no')

    async def update_roles(self):
        for guild in self.bot.guilds:
            self.first_year = discord.utils.get(guild.roles, name='First Year')
            self.second_year = discord.utils.get(guild.roles, name='Second Year')
            self.third_year = discord.utils.get(guild.roles, name='Third Year')
            self.placement_year = discord.utils.get(guild.roles, name='Placement Year')
            self.fourth_year = discord.utils.get(guild.roles, name='Fourth Year')
            self.alumni = discord.utils.get(guild.roles, name='Alumni')
            self.placement = discord.utils.get(guild.roles, name='Placement')
            for member in guild.members:
                if self.first_year in member.roles:
                    await member.remove_roles(self.first_year)
                    await member.add_roles(self.second_year)
                elif self.second_year in member.roles:
                    await member.remove_roles(self.second_year)
                    if self.placement in member.roles:
                        await member.add_roles(self.placement_year)
                    else:
                        await member.add_roles(self.third_year)
                elif self.third_year in member.roles:
                    await member.remove_roles(self.third_year)
                    await member.add_roles(self.alumni)
                elif self.placement_year in member.roles:
                    await member.remove_roles(self.placement_year)
                    await member.add_roles(self.fourth_year)
                elif self.fourth_year in member.roles:
                    await member.remove_roles(self.fourth_year)
                    await member.add_roles(self.alumni)

def setup(bot):
    bot.add_cog(Roles(bot))
