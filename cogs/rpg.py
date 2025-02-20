import discord
from discord import Option, SlashCommandGroup
from discord.ext import commands

import json
import random


async def inventory_item_autocomplete(
    interaction: discord.Interaction, current: str
) -> list[str]:
    """Autocomplete callback for the 'item' parameter.
    It suggests items already present in the user's inventory."""
    # Attempt to get the provided user from the interaction options.
    try:
        user = interaction.user
    except AttributeError:
        return []
    suggestions = []
    if user:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        # Navigate to the inventory for the given user.
        inv = (
            data.get("rpg", {})
                .get("inventory", {})
                .get(str(user.id), {})
        )
        # Filter item names by the current input.
        for item_name in inv.keys():
            if current.lower() in item_name.lower():
                suggestions.append(item_name)
    # Return a maximum of 25 suggestions.
    return suggestions[:25]


class RPG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    setcmd: SlashCommandGroup = SlashCommandGroup(name="set", description="Set information related to the game.", guild_ids=[938179110558105672])
    inventory: SlashCommandGroup = SlashCommandGroup(name="inventory", description="Various inventory related commands.")

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


    @inventory.command(guild_ids=[938179110558105672])
    async def view(self, 
                   ctx: discord.ApplicationContext,
                   user: Option(discord.Member, "User to view inventory", required=False) = None
                   ):
        """When a user runs `/inventory`, display their inventory."""
        target = user if user else ctx.author
        file_name = "data.json"
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        # Get the calling user's inventory.
        user_inventory = data.get("rpg", {}).get("inventory", {}).get(str(target.id), {})
        if not user_inventory:
            if target == ctx.author:
                await ctx.respond("### Your inventory is empty.")
            else:
                await ctx.respond(f"### {target.display_name}'s inventory is empty.")
        else:
            lines = [f"__{item}__: {qty}" for item, qty in user_inventory.items()]
            inventory_list = "\n".join(lines)
            if target == ctx.author:
                await ctx.respond(f"### Your inventory:\n{inventory_list}")
            else:
                await ctx.respond(f"### {target.display_name}'s inventory:\n{inventory_list}")

    
    @inventory.command()
    async def add(
        self,
        ctx: discord.ApplicationContext,
        user: Option(discord.Member, "User whose inventory to modify"),
        item: Option(
            str, 
            "Item to add", 
            autocomplete=inventory_item_autocomplete
        ),
        quantity: Option(int, "Quantity to add", default=1)
    ):
        """Adds an item and quantity to a user's inventory."""
        file_name = "data.json"
        # Load existing data; if not available, start with an empty dict.
        try:
            with open(file_name, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # Ensure the proper nested structure exists.
        data.setdefault("rpg", {})
        data["rpg"].setdefault("inventory", {})
        user_id = str(user.id)
        data["rpg"]["inventory"].setdefault(user_id, {})

        # If the item already exists, add to its quantity; otherwise, create it.
        current_quantity = data["rpg"]["inventory"][user_id].get(item, 0)
        data["rpg"]["inventory"][user_id][item] = current_quantity + quantity

        # Write the updated data back to the file.
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)

        await ctx.respond(
            f"Added {quantity} of **{item}** to {user.display_name}'s inventory."
        )


    @commands.Cog.listener()
    async def on_ready(self):
        # self.bot.add_application_command(setcmd)
        print(f"{self.bot.user} is ready!")



def setup(bot):
    bot.add_cog(RPG(bot))