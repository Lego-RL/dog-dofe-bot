import discord
from discord import SlashCommandGroup
from discord.ext import commands

import json
import random


class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    setcmd: SlashCommandGroup = SlashCommandGroup(name="set", description="Set information related to the game.", guild_ids=[938179110558105672])

    def get_user_name(self, user_id):
        file_name = "data.json"
        
        # Ensure user_id is treated as a string because JSON keys are stored as strings.
        user_id = str(user_id)
        
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If the file doesn't exist or is malformed, we can't retrieve a name.
            return None
        
        # Navigate to the "rpg" section and return the name if it exists.
        return data.get("rpg", {}).get(user_id)


    @commands.slash_command()
    async def d20(self, ctx: discord.ApplicationContext):
        name: str = self.get_user_name(ctx.author.id)
        await ctx.respond(f"### {name if name else ctx.author.display_name} rolled {random.randint(1, 20)}!")

    @commands.slash_command()
    async def d6(self, ctx: discord.ApplicationContext):
        name: str = self.get_user_name(ctx.author.id)
        await ctx.respond(f"### {name if name else ctx.author.display_name} rolled {random.randint(1, 6)}!")

    @setcmd.command(guild_ids=[938179110558105672])
    async def name(self, ctx: discord.ApplicationContext, name: str):
        file_name = "data.json"
    
        # Attempt to load existing data; if the file doesn't exist, start fresh.
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        # Ensure the "rpg" section exists.
        if "rpg" not in data:
            data["rpg"] = {}
        
        # Use the user's id as the key and the provided name as the value.
        data["rpg"][str(ctx.author.id)] = name
        
        # Write the updated data back to the file.
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)
        
        await ctx.respond(f"Name set to **{name}**!")

    
    @commands.Cog.listener()
    async def on_ready(self):
        # self.bot.add_application_command(setcmd)
        print(f"{self.bot.user} is ready!")



def setup(bot):
    bot.add_cog(RPG(bot))