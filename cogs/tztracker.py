import discord
from discord.ext import commands


class TZTracker(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot
        self.dofe_guild_id: int = 938179110558105672
        self.monitor_list: list[str] = ["cst, est, gmt, ist"]


    @commands.Cog.listener()
    async def on_ready(self):
        print("Cog loaded!")

        dofe_guild: discord.Guild | None = self.bot.get_guild(self.dofe_guild_id)
        categories: list = dofe_guild.by_category()
        tz_category = list(filter(lambda x: x[0].name == "timezones", categories))
        
        # get category object out of list 
        tz_category: discord.CategoryChannel = tz_category[0]
        tz_channels: list[discord.TextChannel] = tz_category[1]
        print(tz_category)

        for tz in self.monitor_list:
            for channel in tz_channels:
                # await channel.edit(name=f"{tz}: 1:50")
                if channel.name.startswith(tz):
                    await channel.edit(name=f"{tz}: 1:50")
        




def setup(bot):
    bot.add_cog(TZTracker(bot))