# DevSoc Discord Bot
A repository containing the DevSoc discord server's python bot.

Originally Created by [@emiipo](https://github.com/emiipo)

Maintained/updated by [@petelampy](https://github.com/petelampy)

## Adding a command
To add a command either do it in `commands.py` or make a new cog(class with its own listeners and commands):

### Adding it in commands.py:
```python
@commands.command #Register the command with the bot.
async def command(self, ctx, arg): #Define the command name.
  await ctx.send(arg) #Execute the command. In this case we send the argument passed back to the user.
```
* A command must always have at least one parameter, ctx, which is the [Context](https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#discord.ext.commands.Context) as the first one.
* The command is triggered using `prefix+command`. The current prefix is `.` so the command would be `.command`.

### Making a new cog:
* Make a new file or a class in `commands.py`
* If making a new file don't forget this import:
```python
from discord.ext import commands
```
* Set up the cog, make sure it has __init__:
```python
class Cog_Name: #Setup the cog.
  def __init__(self, bot):
    self.bot = bot #If you don't have this the commands won't work as they won't be able to get ctx(context).
```
* Write your commands the same way as in `commands.py`
* Don't forget to add this at the end:
```python
def setup(bot):
  bot.add_cog(Cog_Name(bot))
```
* Add your cog to the extensions list in `bot.py`


More on commands: [here](https://discordpy.readthedocs.io/en/rewrite/ext/commands/commands.html)

## API Documentation
The documentation for the API can be found [here](https://discordpy.readthedocs.io/en/rewrite/index.html)


## Requirements
* [Python 3.6.7](https://www.python.org/downloads/release/python-367/)
* [discord.py](https://github.com/Rapptz/discord.py)
