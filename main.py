import disnake
from disnake.ext import commands

from dotenv import load_dotenv

load_dotenv()

import os

client = commands.Bot(
    command_prefix="!h1",
    help_command=None,
    strip_after_prefix=True,
    allowed_mentions=disnake.AllowedMentions(
        users=True,
        everyone=False,
        roles=False,
        replied_user=True,
    )
)

print("---------- BASIC COMMANDS ----------")
for filename in os.listdir("./basic-cmds"):
    try:
        if filename.endswith(".py"):
            client.load_extension(f"basic-cmds.{filename[:-3]}")
            print(f"|  Loaded {filename}.")
    except Exception as e:
        print(f"|  Could not load {filename} due to exception: \n{e}")

print("---------- SLASH COMMANDS ----------")
for filename in os.listdir("./slash-cmds"):
    try:
        if filename.endswith(".py"):
            client.load_extension(f"slash-cmds.{filename[:-3]}")
            print(f"|  Loaded {filename}.")
    except Exception as e:
        print(f"|  Could not load {filename} due to exception: \n{e}")


@client.event
async def on_ready():
    await client.change_presence(
        status=disnake.Status.idle,
        activity=disnake.Activity(type=disnake.ActivityType.watching, name="bug bounties."),
    )
    print(f"The bot is online. \nLogged in as {client.user}({client.user.id}).")


BOT_TOKEN = os.getenv("BOT_TOKEN")
client.run(BOT_TOKEN)
