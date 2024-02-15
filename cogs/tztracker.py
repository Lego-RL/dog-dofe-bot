import discord
from discord.ext import commands, tasks

import time
import arrow


class TZTracker(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot: discord.Bot = bot
        self.dofe_guild_id: int = 938179110558105672

        # https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        self.timezones = {
            "CST": "America/Chicago",
            "EST": "America/Detroit",
            "GMT": "Europe/Belfast",
            "IST": "Asia/Calcutta",
        }


    @tasks.loop(minutes=1)
    async def timechannels(self):
        """
        Every half hour, refresh time channels.
        """
        utc = arrow.utcnow()

        # only update twice an hour
        print(str(utc.to(self.timezones["CST"]).format("mm")))
        if str(utc.to(self.timezones["CST"]).format("mm")) not in ["00", "30"]:
            return

        dofe_guild: discord.Guild | None = self.bot.get_guild(self.dofe_guild_id)

        categories: list = dofe_guild.by_category()
        category_info: tuple[discord.CategoryChannel, list[discord.VoiceChannel]] = list(filter(lambda x: x[0].name == "timezones", categories))[0]
        for existing_channel in category_info[1]:
            await existing_channel.delete()

        category: discord.CategoryChannel = category_info[0]

        for tz in self.timezones.keys():
            local_time = utc.to(self.timezones[tz])
            await category.create_voice_channel(name=f"{tz}: {local_time.format('hh:mm A')}")


    @commands.Cog.listener()
    async def on_ready(self):
        self.timechannels.start()
        print("Cog loaded!")

        
    def cog_unload(self):
        self.timechannels.cancel()



def setup(bot):
    bot.add_cog(TZTracker(bot))