import discord
from discord.ext import commands, tasks
from datetime import datetime
import datetime

class Misato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.misato_gifs = {
            0: "https://media1.tenor.com/m/fD3LCHay5YAAAAAd/misato-misato-monday.gif",
            1: "https://media1.tenor.com/m/l9k-t4ScMlUAAAAC/misato-tuesday.gif",
            2: "https://media1.tenor.com/m/DryUiR59TuQAAAAd/evangelion-nge.gif",
            3: "https://media1.tenor.com/m/B-mhOCb9qyMAAAAC/misato-thursday-misato.gif",
            4: "https://media1.tenor.com/m/WFzl5E9tyl8AAAAd/misato-friday.gif",
            5: "https://media1.tenor.com/m/dfNoWpyCh78AAAAC/misato-misato-saturday.gif",
            6: "https://media1.tenor.com/m/RM0fCdR7bfQAAAAC/sunday-misato-sunday.gif",
        }
        self.special_holidays = {
            "10-31": "https://media1.tenor.com/m/vjwCzVNF_LsAAAAd/misato-halloween.gif",  # Halloween
            "12-25": "https://media1.tenor.com/m/Nan8i_zaNmgAAAAd/misato-christmas-christmas.gif",  # Christmas
            "01-01": "https://media1.tenor.com/m/33YF7X418cwAAAAC/misato-new-year.gif",  # New Year
        }
        self.channel_id = 513829298860326913
        self.daily_misato_gif.start()

    def cog_unload(self):
        self.daily_misato_gif.cancel()

    @tasks.loop(time=datetime.datetime.strptime("09:00:00", "%H:%M:%S").time())
    async def daily_misato_gif(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            print(f"Channel with ID {self.channel_id} not found.")
            return

        today = datetime.datetime.now()
        today_str = today.strftime("%m-%d")

        # Check for special holiday
        gif_url = self.special_holidays.get(today_str)
        if not gif_url:
            # If no special holiday, use the regular day-of-week gif
            day_of_week = today.weekday()
            gif_url = self.misato_gifs.get(day_of_week, None)

        if gif_url:
            await channel.send(gif_url)
        else:
            print(f"No gif found for day {today_str} or day {today.weekday()}.")

    @daily_misato_gif.before_loop
    async def before_daily_misato_gif(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Misato(bot))