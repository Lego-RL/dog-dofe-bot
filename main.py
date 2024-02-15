import discord

from dotenv import load_dotenv, dotenv_values

## bot config
load_dotenv()
config: dict = dotenv_values(".env")

bot = discord.Bot()
extensions: list[str] = ["rpg", "tztracker"]

for extension in extensions:
    bot.load_extension(f"cogs.{extension}")


@bot.event
async def on_ready():
    print("Bot loaded!")

if __name__ == "__main__":
    if "TOKEN" in config:
        bot.run(config["TOKEN"])

    else:
        print("Could not find TOKEN in .env file!")