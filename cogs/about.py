import discord
from discord.ext import commands
import sys
import time
import psutil
from datetime import datetime

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(help="Shows the response time of the bot", with_app_commands=True)
    async def ping(self, ctx: commands.Context):
        latency = round(self.bot.latency * 1000)

        start_time = time.time() 
        end_time = time.time()
        rtt = (end_time - start_time) * 1000

        embed=discord.Embed(title="Pong!", description=f"Latency: {latency:.2f} ms ", color=2780206)
        embed.add_field(name="Round Trip Time", value=f"{rtt:.2f} ms")
        embed.set_footer(text=f"{ctx.guild} ({ctx.guild.id})")
        embed.timestamp = datetime.now()

        await ctx.send(embed=embed)

    @commands.hybrid_command(help="Display information about the bot", with_app_commands=True)
    async def about(self, ctx: commands.Context):
        try:
            py = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            process = psutil.Process()
            ram_usage = process.memory_info().rss / (1024 ** 2) 
        except Exception as e:
            ram_usage = "Error retrieving RAM usage"

        try:
            embed = discord.Embed(title=f"{self.bot.user.name}", description="A custom multi-purpose bot assisting with the management of the companies.", color=2780206)
            embed.add_field(name="Server", value=f"{ctx.guild} (`{ctx.guild.id}`)", inline=True)
            embed.add_field(name="Language", value=f"Python {py}", inline=True)
            embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
            embed.add_field(name="RAM Usage", value=f"{ram_usage:.2f} MB", inline=True)

            embed.set_footer(text=f"Created by loafofbread | {ctx.guild} ({ctx.guild.id})")
            embed.timestamp = datetime.now()

            await ctx.send(embed=embed)
        except Exception as e:
            print(e)


    @commands.command()
    async def error(self, ctx):
        raise FileNotFoundError("Error")

async def setup(bot):
    await bot.add_cog(About(bot))