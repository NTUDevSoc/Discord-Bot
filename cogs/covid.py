import discord
from discord.ext import commands
import json
import requests

async def command_channels(ctx):
    return ctx.channel.id == 854307344950099971

class Covid(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    #By Emi/Peter
    @commands.command()
    @commands.check(command_channels)
    async def covidoverview(self, ctx):
        ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
        AREA_TYPE = "overview"
        filters = [
            f"areaType={ AREA_TYPE }",
        ]
        structure = {
            "dailyCases": "newCasesByPublishDate",
            "cumulativeCases": "cumCasesByPublishDate"
        }
        api_params = {
            "filters": str.join(";", filters),
            "structure": json.dumps(structure, separators=(",", ":")),
            "latestBy": "cumCasesByPublishDate",
        }
        api_params["format"] = "json"
        response = requests.get(ENDPOINT, params=api_params, timeout=10)
        assert response.status_code == 200, f"Failed request: {response.text}"
        data = json.loads(response.content)
        totalcases = int(data['data'][0]['cumulativeCases'])
        dailycases = int(data['data'][0]['dailyCases'])
        embed=discord.Embed(title="__COVID Dashboard__", description="UK Government COVID Statistics", color=0xe7ec11)
        embed.add_field(name="Total Cases", value=totalcases, inline=False)
        embed.add_field(name="Daily Cases", value=dailycases, inline=False)
        await ctx.send(embed=embed)

    #By Emi/Peter
    @commands.command()
    @commands.check(command_channels)
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
                "dailyCases": "newCasesByPublishDate",
                "cumulativeCases": "cumCasesByPublishDate"
            }
            api_params = {
                "filters": str.join(";", filters),
                "structure": json.dumps(structure, separators=(",", ":")),
                "latestBy": "cumCasesByPublishDate",
            }
            api_params["format"] = "json"
            response = requests.get(ENDPOINT, params=api_params, timeout=10)
            assert response.status_code == 200, f"Failed request: {response.text}"
            data = json.loads(response.content)
            totalcases = int(data['data'][0]['cumulativeCases'])
            dailycases = int(data['data'][0]['dailyCases'])
            embed=discord.Embed(title="__COVID Dashboard - "+str(region)+"__", description=str(region)+" COVID Statistics", color=0xe7ec11)
            embed.add_field(name="Region Cases", value=totalcases, inline=False)
            embed.add_field(name="Region Daily Cases", value=dailycases, inline=False)
            await ctx.send(embed=embed)
        except:
            await ctx.send("That's not a valid region!")

def setup(client):
    client.add_cog(Covid(client))