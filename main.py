import disnake
from disnake.ext import commands

from dotenv import load_dotenv
load_dotenv()

import os

client = commands.Bot(
    command_prefix="!h1",
    help_command=None,
    test_guilds=[int(os.getenv("TEST_GUILD"))],
    strip_after_prefix=True,
)

@client.event
async def on_ready():
    await client.change_presence(
        status=disnake.Status.idle,
        activity=disnake.Activity(
            type=disnake.ActivityType.watching, name="bug bounties."
        ),
    )
    print(f"The bot is online. \nLogged in as {client.user}({client.user.id}).")

@client.command()
async def ping(ctx):
    await ctx.send(f"<:h1hourglass:915993528813912074>  **Bot latency is **`{round(client.latency*1000)}ms`")

BOT_TOKEN = os.getenv("BOT_TOKEN")
client.run(BOT_TOKEN)