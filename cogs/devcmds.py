import discord
from discord.ext import commands
import json
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from main import bot

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(with_app_commands=True)
    async def sync(self, ctx: commands.Context, *, scope: str = "guild"):
        
        if scope.lower() == "guild":
            await ctx.bot.tree.sync(guild=ctx.guild)
        elif scope.lower() == "global":
            await ctx.bot.tree.sync()
        else:
            return
        await ctx.send("<:success:1302750399190794261> Synced!")


    @commands.command(with_app_commands=True)
    async def reload(self, ctx: commands.Context, cog: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await ctx.send(f"<:success:1302750399190794261> Reloaded `{cog}`")
        except commands.ExtensionNotLoaded:
            await ctx.send(f"Cog `{cog}` not loaded.")
        except commands.ExtensionNotFound:
            await ctx.send(f"Cog `{cog}` not found.")
        except Exception as e:
            await ctx.send(f"Failed to reload `{cog}`: {e}")

    @commands.command(with_app_commands=True)
    async def load(self, ctx: commands.Context, cog: str):

        try:
            await self.bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"<:success:1302750399190794261> Loaded `{cog}`")
        except Exception as e:
            await ctx.send(f"Failed to load `{cog}`: {e}")

    @commands.command(with_app_commands=True)
    async def unload(self, ctx: commands.Context, cog: str):

        try:
            await self.bot.unload_extension(f"cogs.{cog}")
            await ctx.send(f"<:success:1302750399190794261> Unloaded `{cog}`")
        except Exception as e:
            await ctx.send(f"Failed to unload `{cog}`: {e}")

    @commands.command(with_app_commands=True)
    async def shutdown(self, ctx: commands.Context):
       
        await ctx.send("<:success:1302750399190794261> Shutting down bot...")
        await self.bot.close()

    @commands.command(with_app_commands=True)
    async def cogs(self, ctx: commands.Context):
    
        cogs = list(self.bot.extensions.keys())
        await ctx.send(f"Loaded cogs: {', '.join(cogs)}")

    @commands.command()
    async def raise_exception(self, ctx: commands.Context):
        raise Exception(f'{ctx.author} ({ctx.author.id}) use the raise exception command.')

async def setup(bot):
    await bot.add_cog(dev(bot))
