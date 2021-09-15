import discord
from discord.ext import commands
from discord import RawReactionActionEvent

class Rules(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.ruleID = 806592818993954867

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.user_id != self.client.owner_id:
            if payload.message_id == int(self.ruleID):
                if "placement_yes" == payload.emoji.name:
                    guild = discord.utils.get(self.client.guilds, id=payload.guild_id)
                    role = discord.utils.get(guild.roles, name="DevSoc")
                    await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        if payload.user_id != self.client.owner_id:
            if payload.message_id == int(self.ruleID):
                if "placement_yes" == payload.emoji.name:
                    guild = discord.utils.get(self.client.guilds, id=payload.guild_id)
                    user = discord.utils.get(guild.members, id=payload.user_id)
                    role = discord.utils.get(guild.roles, name="DevSoc")
                    await user.remove_roles(role)

def setup(client):
    client.add_cog(Rules(client))