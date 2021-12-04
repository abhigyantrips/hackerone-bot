import disnake
from disnake.ext import commands

import datetime


class SlashUtils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def ping(self, ctx):

        """Returns the latency of the HackerOne Bot"""

        await ctx.response.send_message(
            f"<:h1hourglass:915993528813912074>  **Bot latency is **`{round(self.client.latency*1000)}ms`"
        )

    @commands.slash_command()
    async def help(self, ctx):

        """Returns the help message for the bot."""

        embed = disnake.Embed(
            title="HackerOne Bot [!h1]",
            description="An unofficial bot for interacting with the HackerOne API.",
            color=0x303136,
            url="https://abhigyantrips.dev/hackerone-bot",
            timestamp=datetime.datetime.now(),
        )

        embed.set_thumbnail(
            url="https://i.imgur.com/NSuNpoX.png",
        )

        embed.add_field(
            name="Commands",
            value="```\n(/help) !h1 help\n ╰ Returns this embed.\n\n(/ping) !h1 ping\n ╰ Returns the latency of the HackerOne bot.\n\n(/user) !h1 user <username>\n ╰ Gets information about a HackerOne user.\n\n(/reports) !h1 reports <id>\n ╰ Gets information about a HackerOne report.```",
            inline=False,
        )

        embed.add_field(
            name="Contribution and Issues",
            value="You can suggest features, report issues and contribute to the bot's source code via the [GitHub repository](https://github.com/abhigyantrips/hackerone-bot).",
            inline=False,
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url,
        )

        await ctx.response.send_message(embed=embed)


def setup(client):
    client.add_cog(SlashUtils(client))
