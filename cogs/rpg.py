import discord
from discord.ext import commands

import random


class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def d20(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"### {ctx.author.display_name} rolled {random.randint(1, 20)}!")

    @commands.slash_command()
    async def d6(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"### {ctx.author.display_name} rolled {random.randint(1, 6)}!")



def setup(bot):
    bot.add_cog(RPG(bot))