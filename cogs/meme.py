import discord, random
from discord.ext import commands

class Meme(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.rat_fact = ("Rats eat almost anything. They like meat, grain, seeds, fruit and vegetables.",
        "Norway rats are big and aggressive. They fight with each other and will even attack humans.",
        "Rats have sharp teeth that constantly grow. They chew on wood to keep the teeth short and sharp.",
        "Pet rats live about 3 years.",
        "Rats can have up to 20 babies at once.",
        "Rats have a good memory and sense of taste. They can recognize and remember the taste of rat poison.",
        "Rats are Rats",
        "The y have legs",
        "U are a rat",
        "skree skree",
        "Cinderblock: Hard white or gray blocks used in buildings",
        "Question: Are rats useful? Answer: Rats have been used to develop medical cures.",
        "Thanks to their body shape, rats are able to fit through the tiniest holes and gaps. Their bodies are long and flexible so they can squeeze themselves down to fit into spaces much smaller than themselves!",
        "A rat’s front teeth are always growing, so they need things to chew on (otherwise it could cause a lot of painful problems for them). It’s super important to feed them the right diet to keep their teeth in good condition – you can read more advice on this. Their teeth are super strong, too, and wild rats have even been known to chew through some metals!",
        "Unlike us, rats don’t get sweaty pits. Nor do they pant like some other animals. They only have sweat glands on the skin of their paws (which isn’t enough to cool them down). Instead, they use their naked tails to help regulate their body temperatures.",
        "So we wouldn’t recommend forcing your rat to take a dip, but some rats are known to love water and be really strong swimmers. There are some types that can swim over a mile at once!",
        "In Ancient Rome, rats were actually considered lucky. Ancient Egyptians and Mayans even worshipped rats. Not sure how that worked alongside worshipping cats, but there you go.",
        "rats dont usually like rats",
        "sorry we're out of facts come back later :)",
        "If you have pet rats, you should always have more than one. They hate to be alone and while they do bond with their owners, they need the company of other rats to stay happy. Best to keep the same gender together though to avoid any unplanned baby rats!",
        "A group of rats is called a mischief.",
        "https://www.automatictrap.com/pages/101-rat-facts",
        "A kangaroo rat can go its average 10-year life span without any water.",
        "When Pixar created the 2007 film Ratatouille, the animators kept rats in their offices to bring their likeness to life with greater accuracy.",
        "Rats make sounds similar to laughter when they are happy.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.channel.DMChannel):
            return

        if message.content.startswith("."):
            return

        if "rat fact" in message.content.lower():
            i = random.randrange(len(self.rat_fact))
            await message.author.send(f"{self.rat_fact[i]}")

        elif "among us" in message.content.lower() and message.author.id == 146353541244649473: #KHAN
            await message.author.send("**NO**")

        elif "hello there" in message.content.lower():
            await message.author.send("https://tenor.com/view/grevious-general-kenobi-star-wars-gif-11406339")

def setup(client):
    client.add_cog(Meme(client))
