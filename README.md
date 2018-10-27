# DevSoc Bot
A python Discord bot for the DevSoc server :) Just started working on it so going through many changes.

## Adding a command
Adding a command follows this syntax:
```python
@bot.command
async def command(ctx, arg):
  await ctx.send(arg)
```
* A command must always have at least one parameter, ctx, which is the [Context](https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#discord.ext.commands.Context) as the first one.
* The command is triggered using `prefix+command`. The current prefix is `.` so the command would be `.command`.

More on commands: [here](https://discordpy.readthedocs.io/en/rewrite/ext/commands/commands.html)

## API Documentation
The documentation for the API can be found [here](https://discordpy.readthedocs.io/en/rewrite/index.html)


## Requirements
* [Python 3.6.7](https://www.python.org/downloads/release/python-367/)
* [discord.py[voice]](https://github.com/Rapptz/discord.py/tree/rewrite)
