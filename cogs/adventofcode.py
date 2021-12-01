import discord
from discord.ext import commands
import json
import datetime
import requests

async def command_channels(ctx):
    return ctx.channel.id in (517651663729852416, 505476463492071425, 783009748001620039)
    
class Adventofcode(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #Advent of Code Leaderboard
    @commands.command()
    async def adventofcode(self, ctx):
        global adventCodeTimer
        timePassed = 0
        if adventCodeTimer == 0:
            adventCodeTimer = datetime.datetime.now()
            timePassed = 15
        else:
            difference = datetime.datetime.now() - adventCodeTimer
            timePassed = divmod(difference.days * 86400 + difference.seconds, 60)
            timePassed = timePassed[0]
        global adventCache
        if timePassed < 15 and len(adventCache) > 0:
            pass
        else:
            adventCodeTimer = datetime.datetime.now()
            sessionValue = "53616c7465645f5feafb8776e83c6df5eefa9d89a8b82fb597f5a430cf47b76f03119daa005972eb810dab8a211fb8ef"
            cookies = {'session': sessionValue}
            response =  requests.get("https://adventofcode.com/2021/leaderboard/private/view/984355.json", cookies=cookies, timeout=10)
            assert response.status_code == 200, f"Failed request: {response.text}"
            data = response.content
            adventCache = json.loads(data)
        dataArray = []
        for member in adventCache["members"]:
            userTuple = (adventCache["members"][member]["name"], int(adventCache["members"][member]["local_score"]))
            dataArray.append(userTuple)
        dataArray.sort(key=lambda tup: tup[1], reverse=True)
        advent=discord.Embed(title="__Advent of Code - Leaderboard__", color=0xe7ec11)
        theScores = ""
        for x in dataArray:
            username = x[0]
            score = x[1]
            theScores = theScores + "**"+str(username)+"**: "+str(score)+"\n"
        advent.add_field(name="Scores", value=theScores, inline=False)
        advent.set_footer(text="Data may be 15 minutes old")
        await ctx.send(embed=advent)

    @commands.command()
    async def adventstars(self, ctx, day):
        global adventCodeTimer
        global adventCache
        timePassed = 0
        if adventCodeTimer == 0:
            adventCodeTimer = datetime.datetime.now()
            timePassed = 15
        else:
            difference = datetime.datetime.now() - adventCodeTimer
            timePassed = divmod(difference.days * 86400 + difference.seconds, 60)
            timePassed = timePassed[0]
        if timePassed < 15 and len(adventCache) > 0:
            pass
        else:
            adventCodeTimer = datetime.datetime.now()
            sessionValue = "53616c7465645f5f871fdafed7f7a02ba9da7486e73f84347297cdc6a9245c0a5d85e11941af37302408c7674815fe8e"
            cookies = {'session': sessionValue}
            response = requests.get("https://adventofcode.com/2021/leaderboard/private/view/984355.json", cookies=cookies, timeout=10)
            assert response.status_code == 200, f"Failed request: {response.text}"
            data = response.content
            adventCache = json.loads(data)
        dataArray = []
        for member in adventCache["members"]:
            counter = 0
            for x in adventCache["members"][member]["name"]["completion_day_level"][day]:
                counter += 1
            userTuple = (adventCache["members"][member]["name"], counter)
            dataArray.append(userTuple)
        dataArray.sort(key=lambda tup: tup[1], reverse=True)
        advent=discord.Embed(title="__Advent of Code - Day "+day+" Stars__", color=0xe7ec11)
        theStars = ""
        for x in dataArray:
            username = x[0]
            stars = x[1]
            theStars = theStars + "**"+str(username)+"**: "+str(stars)+"\n"
        advent.add_field(name="Stars", value=theStars, inline=False)
        advent.set_footer(text="Data may be 15 minutes old")
        await ctx.send(embed=advent)

def setup(client):
    client.add_cog(Adventofcode(client))


#Timer variable for advent of code command
adventCodeTimer = 0
#Advent code cached data
adventCache = []