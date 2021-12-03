import disnake
from disnake.ext import commands

import datetime


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

        """Returns the help message for the bot."""

        embed = disnake.Embed(
            title="HackerOne Bot [!h1]",
            description="An unofficial bot for interacting with the HackerOne API.",
            color=0x303136,
            url="https://abhigyantrips.dev/hackerone-bot",
            timestamp=datetime.datetime.now(),
        )

        embed.set_author(
            name="Abhigyan Trips",
            url="https://github.com/abhigyantrips/hackerone-bot",
            icon_url="https://i.imgur.com/Q0Zj5V4.jpg",
        )

        embed.set_thumbnail(
            url="https://i.imgur.com/NSuNpoX.png",
        )

        embed.add_field(
            name="Commands",
            value="```\n!h1 help (/help)\n└── Returns this embed.\n\n!h1 ping (/ping)\n└── Returns the latency of the HackerOne bot.\n\n!h1 user <username> (/user)\n└── Gets information about a HackerOne user.\n\n!h1 reports <id> (/reports)\n└── Gets a report from HackerOne, as per specified ID.```",
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

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PrefixUtils(client))
