# Imports
import discord
import os
import asyncio
from discord.ext import commands, tasks
from zuid import ZUID

from utils.constants import logger, PREFIX, TOKEN

generator = ZUID(prefix="ERROR_", length=32)

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_time = None 

    async def setup_hook(self) -> None:
        cog_count = 0
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f"Loaded cog - {filename[:-3]}")
                    cog_count += 1
                except Exception as e:
                    logger.error(f"Failed to load {filename[:-3]}. {e}")
            
        logger.info(f"Loaded {cog_count} cogs")

    async def on_ready(self):
        logger.info(f"Started {self.user}")

intents = discord.Intents.all()

bot = Bot(command_prefix=",", intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Prevent unnecessary triggers
        return
    elif isinstance(error, commands.MissingRequiredArgument):
       description = "Sorry! Missing a required argument!"
    elif isinstance(error, commands.MissingPermissions):
        description = "Sorry! You don't have sufficient permissions to run this command."
    elif isinstance(error, commands.BotMissingPermissions):
        description = "Sorry! I don't have sufficient permissions to run this command."
    else:
        description = "Sorry! Something went wrong. Please try again later and if the issue persists contact our [support team](https://discord.gg/AV6pa26uxg)."
        error_id_show = True
    
    error_id = generator()
    
    try:
        embed = discord.Embed(title="Error!", description=description, color=discord.Color.red())
        embed.set_footer(text=f"User ID: {ctx.author.id} | Guild ID: {ctx.guild.id}")
        sembed = discord.Embed(title="Error!", description="An unexpected error has been caught. See below for more information.", color=discord.Color.red())
        sembed.add_field(name="Invoking User", value=f"{ctx.author} (`{ctx.author.id}`)", inline=True)
        sembed.add_field(name="Invoked Guild", value=f"{ctx.guild} (`{ctx.guild.id}`)", inline=True)
        sembed.add_field(name="Invoked Command", value=f"{ctx.command}", inline=True)
        sembed.add_field(name="Arguments", value=f"{ctx.args}", inline=True)
        sembed.add_field(name="Error", value=f"{error}", inline=False)
        sembed.add_field(name="Error ID", value=f"{error_id}", inline=False)

        if error_id_show == True:
            logger.warning(f"Error caught - {error}")
            embed.add_field(name="Error ID", value=f"`{error_id}`", inline=False)
        await ctx.send(embed=embed)
        channel = await bot.fetch_channel(1307786066287394847) 
        await channel.send(embed=sembed)


    except Exception as e:
        logger.error(e)

async def main():
    async with bot:
         await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        logger.critical(e)
        
