import disnake
from disnake.ext import commands

class SlashUtils(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command(
        name="h1"
    )
    async def h1(self, ctx):
        pass

    @h1.sub_command(
        name="ping",
        description="Returns the latency of the bot.",
    )
    async def ping(self, ctx):
        await ctx.response.send_message(
            f"<:h1hourglass:915993528813912074>  **Bot latency is **`{round(self.client.latency*1000)}ms`"
        )
    
    @h1.sub_command(
        name="help",
        description="Returns the help message for the bot.",
    )
    async def help(self, ctx):
        await ctx.response.send_message("The bot is currently under development.")

def setup(client):
    client.add_cog(SlashUtils(client))