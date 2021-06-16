import discord, json, os
from discord.ext import commands
from discord import RawReactionActionEvent

#Reaction Roles By Emi

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client
        with open("data/reaction_roles_data.json") as file:
            self.data = json.load(file)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.user_id != 505395358608916491:
            for message in self.data:
                if int(message) == payload.message_id:
                    for reaction in self.data[message]:
                        if reaction == payload.emoji.name:
                            guild = discord.utils.get(self.client.guilds, id=payload.guild_id)
                            role = discord.utils.get(guild.roles, id=self.data[message][reaction])
                            await payload.member.add_roles(role)

                            if self.data[message]["multiple"] is False:
                                channel = discord.utils.get(guild.channels, id=payload.channel_id)
                                all_msg = await channel.history(limit=100).flatten()
                                msg = discord.utils.get(all_msg, id=payload.message_id)
                                for react in msg.reactions:
                                    if payload.emoji.name not in str(react.emoji):
                                        rem_role = discord.utils.get(guild.roles, id=self.data[message][react.emoji.name])
                                        await payload.member.remove_roles(rem_role)
                                        async for user in react.users():
                                            if user.id == payload.user_id:
                                                await react.remove(payload.member)
                            return
                    guild = discord.utils.get(self.client.guilds, id=payload.guild_id)
                    channel = discord.utils.get(guild.channels, id=payload.channel_id)
                    all_msg = await channel.history(limit=100).flatten()
                    msg = discord.utils.get(all_msg, id=payload.message_id)
                    for react in msg.reactions:
                        if payload.emoji.name in str(react.emoji):
                            async for user in react.users():
                                if user.id == payload.user_id:
                                    await react.remove(payload.member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent):
        if payload.user_id != 505395358608916491:
            for message in self.data:
                if int(message) == payload.message_id:
                    for reaction in self.data[message]:
                        if reaction == payload.emoji.name:
                            guild = discord.utils.get(self.client.guilds, id=payload.guild_id)
                            user = discord.utils.get(guild.members, id=payload.user_id)
                            role = discord.utils.get(guild.roles, id=self.data[message][reaction])
                            await user.remove_roles(role)


    @commands.command()
    @commands.has_role("Committee")
    async def rr(self, ctx, *args):
        if args[0] == "start":
            if os.path.isfile("data/temp.json"):
                await ctx.send("You are already working on a new reaction role menu. You can check progress by typing '.rr check'")
            else:
                temp = {}
                with open("data/temp.json", "w") as file:
                    json.dump(temp, file)
                await ctx.send("Started creating a reaction role menu, here are your options:\n"
                               "(Only use custom emojis as it won't work with unicode ones)\n"
                               "```\n"
                               ".rr channel [ID] - give the ID of the channel where you want the message to be posted\n"
                               ".rr multiple [true/false] - whether the user can select multiple roles from the menu\n"
                               ".rr title [Title] - give the Title of the menu.(Course, Age, etc.)\n"
                               ".rr reaction [emoji] [role ID] - set an emoji to assign a specific role\n"
                               ".rr check - tells what you have set so far\n"
                               ".rr cancel - cancels the reaction role menu creation\n"
                               ".rr finish - finishes the reaction role menu creation and posts the message\n"
                               "```")
        elif args[0] == "channel":
            if not os.path.isfile("data/temp.json"):
                await ctx.send("You aren't working on a reaction roles menu. To start type '.rr start'")
            else:
                try:
                    channel = discord.utils.get(ctx.guild.channels, id=int(args[1]))
                    with open("data/temp.json", "r") as file:
                        temp = json.load(file)
                    temp["ID"] = channel.id
                    with open("data/temp.json", "w") as file:
                        json.dump(temp, file)

                    await ctx.send("You've chosen the channel: " + channel.name)
                except:
                    await ctx.send("Incorrect channel ID, please try again")
        elif args[0] == "multiple":
            if not os.path.isfile("data/temp.json"):
                await ctx.send("You aren't working on a reaction roles menu. To start type '.rr start'")
            else:
                if args[1] == "true":
                    decision = True
                elif args[1] == "false":
                    decision = False
                else:
                    await ctx.send("Invalid choice, it's either true or false")
                    return

                with open("data/temp.json", "r") as file:
                    temp = json.load(file)
                temp["multiple"] = decision
                with open("data/temp.json", "w") as file:
                    json.dump(temp, file)
                await ctx.send("You have set multiple: " + str(decision))
        elif args[0] == "title":
            if not os.path.isfile("data/temp.json"):
                await ctx.send("You aren't working on a reaction roles menu. To start type '.rr start'")
            else:
                try:
                    title = " ".join(args[1:len(args)])
                    with open("data/temp.json", "r") as file:
                        temp = json.load(file)
                    temp["title"] = title
                    with open("data/temp.json", "w") as file:
                        json.dump(temp, file)
                    await ctx.send("You have set the title to: " + title)
                except:
                    await ctx.send("No title provided")
        elif args[0] == "reaction":
            if not os.path.isfile("data/temp.json"):
                await ctx.send("You aren't working on a reaction roles menu. To start type '.rr start'")
            else:
                try:
                    emoji_name = args[1][2:len(args[1])-20]
                    role = int(args[2])
                    with open("data/temp.json", "r") as file:
                        temp = json.load(file)
                    temp[emoji_name] = role
                    with open("data/temp.json", "w") as file:
                        json.dump(temp, file)

                    role_obj = discord.utils.get(ctx.guild.roles, id=role)
                    await ctx.send("You have set " + args[1] + " to give the role - " + role_obj.name)
                except:
                    await ctx.send("Incorrect emoji and role provided.")
        elif args[0] == "check":
            if not os.path.isfile("data/temp.json"):
                await ctx.send("You aren't working on a reaction roles menu. To start type '.rr start'")
            else:
                with open("data/temp.json") as file:
                    temp = json.load(file)

                string = "You currently have:\n```\n"
                for item in temp:
                    string += str(item) + ": " + str(temp[item]) + "\n"
                string += "```"
                await ctx.send(string)
        elif args[0] == "cancel":
            if not os.path.isfile("data/temp.json"):
                await ctx.send("You aren't working on a reaction roles menu. To start type '.rr start'")
            else:
                os.remove("data/temp.json")
                await ctx.send("You have stopped creating a reaction roles menu.")
        elif args[0] == "finish":
            if not os.path.isfile("data/temp.json"):
                await ctx.send("You aren't working on a reaction roles menu. To start type '.rr start'")
            else:
                with open("data/temp.json") as file:
                    temp = json.load(file)

                message_channel = discord.utils.get(ctx.guild.channels, id=temp["ID"])
                emoji_roles = ""
                for item in temp:
                    if item != "ID" and item != "multiple" and item != "title":
                        role = discord.utils.get(ctx.guild.roles, id=temp[item])
                        emoji = discord.utils.get(ctx.guild.emojis, name=item)
                        emoji_roles += str(emoji) + ": " + role.name + "\n"
                if temp["multiple"]:
                    main_message = discord.Embed(title="Select roles for:", color=0xe7ec11)
                else:
                    main_message = discord.Embed(title="Select role for:", color=0xe7ec11)
                main_message.add_field(name=temp["title"], value=emoji_roles, inline=False)
                main_message.set_footer(text="Bot developed by Emi/Peter")

                rr_message = await message_channel.send(embed=main_message)
                for item in temp:
                    if item != "ID" and item != "multiple" and item != "title":
                        emoji = discord.utils.get(ctx.guild.emojis, name=item)
                        await rr_message.add_reaction(emoji)

                self.data[str(rr_message.id)] = {}
                self.data[str(rr_message.id)]["multiple"] = temp["multiple"]
                for item in temp:
                    if item != "ID" and item != "multiple" and item != "title":
                        self.data[str(rr_message.id)][item] = temp[item]
                with open("data/reaction_roles_data.json", "w") as file:
                    json.dump(self.data, file)

                await ctx.send("Successfully created the reaction roles menu message. Please upload this JSON file to the githubs data folder to save your changes!")
                await ctx.send(file=discord.File("data/reaction_roles_data.json"))

                os.remove("data/temp.json")
        else:
            await ctx.send("Invalid choice!")

def setup(client):
    client.add_cog(Roles(client))