import discord
import time
import json
from json import dumps
import requests
from requests import get
import datetime
from discord.ext import commands
startTime = time.time()

async def in_bot_commands(ctx):
    channel_ids = (186605768080883713, 517651663729852416, 505476463492071425)
    return ctx.channel.id in channel_ids

ac_tz = datetime.timezone(-datetime.timedelta(hours=5), name="EST")
def utc_to_est(utc_dt):
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=ac_tz)

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
        code.set_author(name="Discord Bot Source Code", icon_url="https://i.imgur.com/NhVjX8S.png")
        code.set_footer(text="Bot developed by Emi/Peter")
        await ctx.send(embed=code)

    #Command that links to all DevSoc social pages
    @commands.command(aliases=['Social', 'socials', 'twitter', 'facebook', 'instagram', 'socialmedia'])
    @commands.check(in_bot_commands)
    async def social(self, ctx):
        socials=discord.Embed(title="DevSoc Social Links", description="Here are all the links to official DevSoc Social Media pages", color=0xe7ec11)
        socials.set_thumbnail(url="https://i.imgur.com/NhVjX8S.png")
        socials.add_field(name="Twitter", value="https://twitter.com/devsoc", inline=False)
        socials.add_field(name="Facebook", value="https://facebook.com/devsoc", inline=False)
        socials.add_field(name="Instagram", value="https://instagram.com/ntudevsoc", inline=False)
        socials.set_footer(text="Bot developed by Emi/Peter")
        await ctx.send(embed=socials)

    #Help command to list usable commands
    @commands.command(aliases=['devhelp', 'halp', 'commands'])
    @commands.check(in_bot_commands)
    async def help(self, ctx):
        thehelp=discord.Embed(title="__DevSoc Bot - Commands__", description="*This dialog gives you all the commands currently available for use with DevSoc Bot.*", color=0xe7ec11)
        thehelp.add_field(name=".setrole", value="For setting your role in the server.", inline=False)
        thehelp.add_field(name=".announcement", value="To subscribe or unsubscribe from server announcements.", inline=False)
        thehelp.add_field(name=".social", value="Links to all of DevSoc's social pages.", inline=False)
        thehelp.add_field(name=".whois", value="Check who someone in the server is.", inline=False)
        thehelp.add_field(name=".github", value="Links to the github source code of the bot.", inline=False)
        thehelp.add_field(name=".members", value="Checks the members of each year group in the server.", inline=False)
        thehelp.add_field(name=".covidoverview", value="Gives an overview of UK COVID cases.", inline=False)
        thehelp.add_field(name=".covidregion (REGION)", value="Gives an overview of COVID cases in a region of the UK.", inline=False)
        thehelp.set_footer(text="Bot created by Emi/Peter")
        await ctx.send(embed=thehelp)
        
        
    #Command to count members in each year in the server
    @commands.command(aliases=['membercount', 'membercheck', 'memberlist'])
    @commands.check(in_bot_commands)
    async def members(self, ctx):
        devMembers = {
            "first": 0,
            "second": 0,
            "placement": 0,
            "final": 0,
            "masters": 0,
            "alumni": 0
        }
        guild = ctx.message.guild
        for member in guild.members:
            for role in member.roles:
                if role.name == "First Year":
                    devMembers["first"] += 1
                elif role.name == "Second Year":
                    devMembers["second"] += 1
                elif role.name == "Placement Year":
                    devMembers["placement"] += 1
                elif role.name == "Third Year":
                    devMembers["final"] += 1
                elif role.name == "Fourth Year":
                    devMembers["final"] += 1
                elif role.name == "MSc Student":
                    devMembers["masters"] += 1
                elif role.name == "Alumni":
                    devMembers["alumni"] += 1
        count=discord.Embed(title="__DevSoc Members__", description="*Here are the members of each year group within this server.*", color=0xe7ec11)
        count.add_field(name="First Year", value=str(devMembers["first"])+" members", inline=False)
        count.add_field(name="Second Year", value=str(devMembers["second"])+" members", inline=False)
        count.add_field(name="Placement Year", value=str(devMembers["placement"])+" members", inline=False)
        count.add_field(name="Third/Final Year", value=str(devMembers["final"])+" members", inline=False)
        count.add_field(name="MSc Student", value=str(devMembers["masters"])+" members", inline=False)
        count.add_field(name="Alumni", value=str(devMembers["alumni"])+" members", inline=False)
        count.set_footer(text="Bot created by Emi/Peter")
        await ctx.send(embed=count)

    #COVID Statistics Command
    @commands.command()
    @commands.check(in_bot_commands)
    async def covidoverview(self, ctx):
        ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
        AREA_TYPE = "overview"
        filters = [
            f"areaType={ AREA_TYPE }",
        ]
        structure = {
            "cases": {
                "daily": "newCasesByPublishDate",
                "cumulative": "cumCasesByPublishDate"
            },
        }
        api_params = {
            "filters": str.join(";", filters),
            "structure": json.dumps(structure, separators=(",", ":")),
            "latestBy": "cumCasesByPublishDate",
        }
        api_params["format"] = "json"
        response = requests.get(ENDPOINT, params=api_params, timeout=10)
        assert response.status_code == 200, f"Failed request: {response.text}"
        data = response.content
        thedata = json.loads(data)
        totalcases = int(thedata['data'][0]['cases']['cumulative'])
        dailycases = int(thedata['data'][0]['cases']['daily'])
        covid=discord.Embed(title="__COVID Dashboard__", description="UK Government COVID Statistics", color=0xe7ec11)
        covid.add_field(name="Total Cases", value=totalcases, inline=False)
        covid.add_field(name="Daily Cases", value=dailycases, inline=False)
        await ctx.send(embed=covid)


    #COVID Regional Statistics Command
    @commands.command()
    @commands.check(in_bot_commands)
    async def covidregion(self, ctx, *region):
        try:
            region =  ' '.join(region)
            ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
            AREA_TYPE = "utla"
            AREA_NAME = str(region.lower())
            filters = [
                f"areaType={ AREA_TYPE }",
                f"areaName={ AREA_NAME }"
            ]
            structure = {
                "cases": {
                    "daily": "newCasesByPublishDate",
                    "cumulative": "cumCasesByPublishDate"
                },
            }
            api_params = {
                "filters": str.join(";", filters),
                "structure": json.dumps(structure, separators=(",", ":")),
                "latestBy": "cumCasesByPublishDate",
            }
            api_params["format"] = "json"
            response = requests.get(ENDPOINT, params=api_params, timeout=10)
            assert response.status_code == 200, f"Failed request: {response.text}"
            data = response.content
            thedata = json.loads(data)
            totalcases = int(thedata['data'][0]['cases']['cumulative'])
            dailycases = int(thedata['data'][0]['cases']['daily'])
            covid=discord.Embed(title="__COVID Dashboard - "+str(region)+"__", description=str(region)+" COVID Statistics", color=0xe7ec11)
            covid.add_field(name="Region Cases", value=totalcases, inline=False)
            covid.add_field(name="Region Daily Cases", value=dailycases, inline=False)
            await ctx.send(embed=covid)
        except:
            await ctx.send("That's not a valid region!")

##    #Advent of Code Leaderboard
##    @commands.command()
##    async def adventofcode(self, ctx):
##        global adventCodeTimer
##        timePassed = 0
##        if adventCodeTimer == 0:
##            adventCodeTimer = datetime.datetime.now()
##            timePassed = 15
##        else:
##            difference = datetime.datetime.now() - adventCodeTimer
##            timePassed = divmod(difference.days * 86400 + difference.seconds, 60)
##            timePassed = timePassed[0]
##        global adventCache
##        if timePassed < 15 and len(adventCache) > 0:
##            pass
##        else:
##            adventCodeTimer = datetime.datetime.now()
##            sessionValue = "53616c7465645f5f871fdafed7f7a02ba9da7486e73f84347297cdc6a9245c0a5d85e11941af37302408c7674815fe8e"
##            cookies = {'session': sessionValue}
##            response = get("https://adventofcode.com/2020/leaderboard/private/view/984355.json", cookies=cookies, timeout=10)
##            assert response.status_code == 200, f"Failed request: {response.text}"
##            data = response.content
##            adventCache = json.loads(data)
##        dataArray = []
##        for member in adventCache["members"]:
##            userTuple = (adventCache["members"][member]["name"], int(adventCache["members"][member]["local_score"]))
##            dataArray.append(userTuple)
##        dataArray.sort(key=lambda tup: tup[1], reverse=True)
##        advent=discord.Embed(title="__Advent of Code - Leaderboard__", color=0xe7ec11)
##        theScores = ""
##        for x in dataArray:
##            username = x[0]
##            score = x[1]
##            theScores = theScores + "**"+str(username)+"**: "+str(score)+"\n"
##        advent.add_field(name="Scores", value=theScores, inline=False)
##        advent.set_footer(text="Data may be 15 minutes old")
##        await ctx.send(embed=advent)
##
##    @commands.command()
##    async def adventstars(self, ctx, day = "0"):
##        try:
##            int(day)
##            if int(day) < 0 or int(day) > 25:
##                await ctx.send("That's not a valid day!")
##                return
##            global adventCodeTimer
##            global adventCache
##            timePassed = 0
##            if adventCodeTimer == 0:
##                adventCodeTimer = datetime.datetime.now()
##                timePassed = 15
##            else:
##                difference = datetime.datetime.now() - adventCodeTimer
##                timePassed = divmod(difference.days * 86400 + difference.seconds, 60)
##                timePassed = timePassed[0]
##            if timePassed < 15 and len(adventCache) > 0:
##                pass
##            else:
##                adventCodeTimer = datetime.datetime.now()
##                sessionValue = "53616c7465645f5f871fdafed7f7a02ba9da7486e73f84347297cdc6a9245c0a5d85e11941af37302408c7674815fe8e"
##                cookies = {'session': sessionValue}
##                response = get("https://adventofcode.com/2020/leaderboard/private/view/984355.json", cookies=cookies, timeout=10)
##                assert response.status_code == 200, f"Failed request: {response.text}"
##                data = response.content
##                adventCache = json.loads(data)
##            dataArray = []
##            if day == "0":
##                for member in adventCache["members"]:
##                    stars = []
##                    star_total = 0
##                    for day_iter in range(1, utc_to_est(datetime.datetime.now()).day+1):
##                        try:
##                            stars.append(len(adventCache["members"][member]["completion_day_level"][str(day_iter)]))
##                            star_total += int(len(adventCache["members"][member]["completion_day_level"][str(day_iter)]))
##                        except KeyError:
##                            stars.append(0)
##                    userTuple = (adventCache["members"][member]["name"], stars, star_total, int(adventCache["members"][member]["local_score"]))
##                    dataArray.append(userTuple)
##                dataArray.sort(key=lambda tup: (tup[2], tup[3]), reverse=True)
##                advent=discord.Embed(title="__Advent of Code - Stars__", color=0xe7ec11)
##                theStars = ""
##                for x in dataArray:
##                    username = x[0]
##                    stars = x[1]
##                    stars_str = ""
##                    for i in stars:
##                        stars_str += str(i)+" "
##                    theStars = theStars + "**"+str(username)+"**: "+stars_str+"\n"
##                advent.add_field(name="Stars", value=theStars, inline=False)
##                advent.set_footer(text="Data may be 15 minutes old")
##                await ctx.send(embed=advent)
##            else:
##                for member in adventCache["members"]:
##                    stars = 0
##                    try:
##                        stars = len(adventCache["members"][member]["completion_day_level"][str(day)])
##                    except KeyError:
##                        stars = 0
##                    userTuple = (adventCache["members"][member]["name"], stars)
##                    dataArray.append(userTuple)
##                dataArray.sort(key=lambda tup: tup[1], reverse=True)
##                advent=discord.Embed(title="__Advent of Code - Day "+ day +" Stars__", color=0xe7ec11)
##                theStars = ""
##                for x in dataArray:
##                    username = x[0]
##                    stars = x[1]
##                    theStars = theStars + "**"+str(username)+"**: "+str(stars)+"\n"
##                advent.add_field(name="Stars", value=theStars, inline=False)
##                advent.set_footer(text="Data may be 15 minutes old")
##                await ctx.send(embed=advent)
##        except ValueError:
##            await ctx.send("That's not a valid day!")



def setup(bot):
    bot.add_cog(Commands(bot))

###Timer variable for advent of code command
##adventCodeTimer = 0
###Advent code cached data
##adventCache = []
