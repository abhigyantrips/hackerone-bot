import disnake
from disnake.ext import commands

class PrefixUtils(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(
            f"<:h1hourglass:915993528813912074>  **Bot latency is **`{round(self.client.latency*1000)}ms`"
        )
    
    @commands.command()
    async def help(self, ctx):
        await ctx.send("The bot is currently under development.")

def setup(client):
    client.add_cog(PrefixUtils(client))