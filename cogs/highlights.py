import discord
import json
from discord.ext import commands

async def command_channels(ctx):
    return ctx.channel.id in (517651663729852416, 505476463492071425)

class Highlights(commands.Cog):

    def __init__(self, client):
        self.client = client
        with open("data/highlight_data.json") as file:
            self.highlight_data = json.load(file)

    def saveDB(self):
        with open("data/highlight_data.json", "w") as file:
            json.dump(self.highlight_data, file, sort_keys=True, indent=4)

    async def message_check(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.channel.DMChannel):
            return

        if message.content.startswith("."):
            return
        
        if "hannah" in message.content.lower():
            await message.channel.send("<@!131332703919276032> sus")

        if message.channel.id in (505094359272652831, 813461899542790164, 505476463492071425, 814152479100633128, 886582676218331186):
            return

        if message.embeds:
            return

        for user_id, word in self.highlight_data.items():
            if word in message.content.lower().split():
                
                if user_id == str(message.author.id):
                    return

                history = await message.channel.history(limit=4, before=message).flatten()
                desc = ""
                embed=discord.Embed(title="Highlight", url=f"{message.jump_url}", color=0xe7ec11)
                for msg in reversed(history):
                    if msg.embeds:
                        desc += f"**{msg.author.name}**: [Embedded Message]\n"
                    else:
                        desc += f"**{msg.author.name}**: {msg.content}\n"
                desc += f"__**{message.author.name}**: {message.content}__\n"
                embed=discord.Embed(title="Highlight", url=f"{message.jump_url}",description=desc, color=0xe7ec11)
                embed.set_footer(text="Feature developed by <J4Y>", icon_url="https://www.j4y.dev/botassets/j4y.gif")
                user = message.guild.get_member(int(user_id))
                await user.send(embed=embed)
                return

    @commands.command()
    @commands.check(command_channels)
    async def highlight(self, ctx, command, word = None):

        embed=discord.Embed(title="Highlights", color=0xe7ec11)

        if command.lower() == "set":
            if word:
                embed.add_field(name="Set", value=word, inline=False)
                self.highlight_data[str(ctx.author.id)] = word.lower()
            else:
                embed.add_field(name="Missing word", value="Provide a word to be notified for", inline=False)
        elif command.lower() == "remove":
            embed.add_field(name="Removed", value=self.highlight_data[str(ctx.author.id)], inline=False)
            if str(ctx.author.id) in self.highlight_data:
                del self.highlight_data[str(ctx.author.id)]
        else:
            embed.add_field(name="Option Unknown", value="Try 'set' or 'remove'", inline=False)
        embed.set_footer(text="Feature developed by <J4Y>", icon_url="https://www.j4y.dev/botassets/j4y.gif")
        self.saveDB()
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.message_check(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.message_check(after)


def setup(client):
    client.add_cog(Highlights(client))