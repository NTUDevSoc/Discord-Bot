import discord
import os
from discord.ext import commands

class Cogs(commands.Cog):

    def __init__(self, client):
        self.client = client

    def __loadCog__(self, ctx, cog):
        try:
            self.client.load_extension(f"cogs.{cog}")
        except Exception as e:
            return cog, type(e).__name__
        else:
            return cog, "Successful"

    def __unloadCog__(self, ctx, cog):
        try:
            self.client.unload_extension(f"cogs.{cog}")
        except Exception as e:
            return cog, type(e).__name__
        else:
            return cog, "Successful"

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        embed=discord.Embed(title="Cog Load", color=0xe7ec11)

        if extension == "cogs":
            embed.add_field(name="cogs", value="Use Reload", inline=False)
        else:
            if extension == "all":
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        if filename[:-3] == "cogs":
                            continue
                        msgname, msgvalue = self.__loadCog__(ctx, filename[:-3])
                        embed.add_field(name=msgname, value=msgvalue, inline=False)
            else:
                msgname, msgvalue = self.__loadCog__(ctx, extension)
                embed.add_field(name=msgname, value=msgvalue, inline=False)
        embed.set_footer(text="Bot created by <J4Y>", icon_url="https://www.j4y.dev/botassets/j4y.gif")
        await ctx.send(embed=embed) 

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        embed=discord.Embed(title="Cog Unload", color=0xe7ec11)

        if extension == "cogs":
            embed.add_field(name="cogs", value="Use Reload", inline=False)
        else:
            if extension == "all":
                for filename in os.listdir("./cogs"):
                    if filename.endswith(".py"):
                        if filename[:-3] == "cogs":
                            continue
                        msgname, msgvalue = self.__unloadCog__(ctx, filename[:-3])
                        embed.add_field(name=msgname, value=msgvalue, inline=False)
            else:
                msgname, msgvalue = self.__unloadCog__(ctx, extension)
                embed.add_field(name=msgname, value=msgvalue, inline=False)
        embed.set_footer(text="Bot created by <J4Y>", icon_url="https://www.j4y.dev/botassets/j4y.gif")
        await ctx.send(embed=embed) 

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        embed=discord.Embed(title="Cog Reload", color=0xe7ec11)

        if extension == "all":
            for filename in os.listdir("./cogs"):
                if filename.endswith(".py"):
                    msgname, msgvalue = self.__unloadCog__(ctx, filename[:-3])
                    msgname, msgvalue = self.__loadCog__(ctx, filename[:-3])
                    embed.add_field(name=msgname, value=msgvalue, inline=False)
        else:
            msgname, msgvalue = self.__unloadCog__(ctx, extension)
            msgname, msgvalue = self.__loadCog__(ctx, extension)
            embed.add_field(name=msgname, value=msgvalue, inline=False)
            
        embed.set_footer(text="Bot created by <J4Y>", icon_url="https://www.j4y.dev/botassets/j4y.gif")
        await ctx.send(embed=embed) 

def setup(client):
    client.add_cog(Cogs(client))