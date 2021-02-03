import discord, datetime, asyncio
from discord.ext import commands
from discord import RawReactionActionEvent

class Rules(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.user_id != 505395358608916491:
            if int(806592818993954867) == payload.message_id:
                if "placement_yes" == payload.emoji.name:
                    guild = discord.utils.get(self.bot.guilds, id=payload.guild_id)
                    role = discord.utils.get(guild.roles, name="DevSoc")
                    await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        if payload.user_id != 505395358608916491:
            if int(806592818993954867) == payload.message_id:
                if "placement_yes" == payload.emoji.name:
                    guild = discord.utils.get(self.bot.guilds, id=payload.guild_id)
                    user = discord.utils.get(guild.members, id=payload.user_id)
                    role = discord.utils.get(guild.roles, name="DevSoc")
                    await user.remove_roles(role)

def setup(bot):
    bot.add_cog(Rules(bot))
