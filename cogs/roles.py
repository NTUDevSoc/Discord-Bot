import discord, datetime, asyncio
from discord.ext import commands

async def in_bot_commands(ctx):
    channel_ids = (186605768080883713, 517651663729852416, 505476463492071425)
    return ctx.channel.id in channel_ids

class Roles:
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.check_day())

    @commands.command()
    @commands.check(in_bot_commands)
    async def setrole(self, ctx, *args):
        if len(args) == 0:
            await ctx.send(
            '''
            To set your role please follow this:
            .setrole <year> <if going/went to placement>
            
            example:
            .setrole second no
            .setrole placement (if your year is placement no need to answer second one)
            .setrole alumni yes
            .setrole first true
            (if not going to placement year you can leave the second argument empty.)
            
            NOTE: It's NOT case sensitive.
            If it's not working please type .helprole or @Ram.
            ''')
        elif len(args) == 1:
            await self.set_role(ctx, args[0])
        elif len(args) == 2:
            await self.set_role(ctx, args[0], args[1])
        else:
            await ctx.send('Too many arguments!')

    @commands.command()
    @commands.check(in_bot_commands)
    async def helprole(self, ctx):
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
            await ctx.author.add_roles(self.placement)
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

        if placement.lower() in ('true', 'yes', 'si', 'da', 'taip', 'yup', 'eyup', 'ofc'):
            await ctx.author.add_roles(self.placement)
            await ctx.send('Set role of: ' + self.role + '! With Placement.')
        else:
            if self.placement in ctx.author.roles:
                await ctx.author.remove_roles(self.placement)
            await ctx.send('Set role of: ' + self.role + '! Without Placement.')

    async def check_day(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(86400)
            print('Checking for role update!')
            self.today = datetime.datetime.today()
            if (self.today.month == 9 and self.today.day == 24):
                await self.update_roles()

    @commands.command()
    @commands.is_owner()
    @commands.check(in_bot_commands)
    async def updateroles(self, ctx):
        await self.update_roles()
        await ctx.send('Manually updated roles!')

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
