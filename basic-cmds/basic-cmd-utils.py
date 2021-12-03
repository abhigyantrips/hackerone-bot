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

def setup(client):
    client.add_cog(PrefixUtils(client))