import disnake
from disnake.ext import commands

import os, requests, json

import datetime
import dateutil.parser as dp

auth = (os.getenv("HACKERONE_USERNAME"), os.getenv("HACKERONE_API_KEY"))
headers = {"Accept": "application/json"}

default_avatar = "https://hackerone.com/assets/avatars/default-71a302d706457f3d3a31eb30fa3e73e6cf0b1d677b8fa218eaeaffd67ae97918.png"


class PrefixReports(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def report(self, ctx, id: str):

        """Gets information about a HackerOne report.

        Parameters
        ----------
        id: The ID of the report to get.
        """

        reportjson = (
            requests.get(
                f"https://api.hackerone.com/v1/reports/{id}",
                auth=auth,
                headers=headers,
            )
        ).json()

        # API Error Handling

        try:
            if reportjson["errors"][0]["status"] == 401:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **The bot is unauthorized to conduct this action.**",
                    ephemeral=True,
                )
            elif reportjson["errors"][0]["status"] == 403:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **The bot is forbidden to conduct this action.**",
                    ephemeral=True,
                )
            elif reportjson["errors"][0]["status"] == 404:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **Could not find HackerOne report: `#{id}`.**",
                    ephemeral=True,
                )
            elif reportjson["errors"][0]["status"] == 429:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **The bot is currently being ratelimited. Please try again later.**",
                    ephemeral=True,
                )
            elif reportjson["errors"][0]["status"] == 500:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **There was an internal server error. Please try again later.**",
                    ephemeral=True,
                )
            elif reportjson["errors"][0]["status"] == 503:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **The HackerOne API is currently offline. Please try again later.**",
                    ephemeral=True,
                )
        except KeyError:
            pass

        # Report Info

        report_title = reportjson["data"]["attributes"]["title"]
        report_state = reportjson["data"]["attributes"]["state"].capitalize()
        report_handle = reportjson["data"]["relationships"]["program"]["data"]["attributes"]["handle"] or "-"
        report_rating = (reportjson["data"]["relationships"]["severity"]["data"]["attributes"]["rating"] or "-").capitalize()
        report_create_at = f"<t:{round(dp.parse(reportjson['data']['attributes']['created_at']).timestamp())}:f>" or "-"
        report_closed_at = f"<t:{round(dp.parse(reportjson['data']['attributes']['disclosed_at']).timestamp())}:f>" or "-"

        # Reporter Info

        reporter_name = reportjson["data"]["relationships"]["reporter"]["data"]["attributes"]["name"]
        reporter_user = reportjson["data"]["relationships"]["reporter"]["data"]["attributes"]["username"]
        reporter_avatar = reportjson["data"]["relationships"]["reporter"]["data"]["attributes"]["profile_picture"]["62x62"]
        if ("default" in reporter_avatar) or (len(reporter_avatar) >= 2048):
            reporter_avatar = default_avatar
        reporter_profile = f"https://hackerone.com/{reporter_user}"

        # Bounty (If disclosed)

        bounty_crr = reportjson["data"]["relationships"]["bounties"]["data"][0]["attributes"]["awarded_currency"] or ""
        bounty_amt = 0
        for amount in reportjson["data"]["relationships"]["bounties"]["data"]:
            bounty_amt += float(amount["attributes"]["awarded_amount"])

        # Embed Creation

        embed = disnake.Embed(
            title=f"#{id} - {report_title} ({report_state})",
            color=0x303136,
            timestamp=datetime.datetime.now(),
            url=f"https://hackerone.com/reports/{id}",
        )

        embed.set_author(
            name=f"{reporter_name} ({reporter_user})",
            icon_url=reporter_avatar,
            url=reporter_profile,
        )

        embed.add_field(
            name="Created at",
            value=report_create_at,
            inline=True,
        )
        embed.add_field(
            name="Disclosed at",
            value=report_closed_at,
            inline=True,
        )
        embed.add_field(
            name="Program",
            value=f"[@{report_handle}](https://hackerone.com/{report_handle})",
            inline=False,
        )
        embed.add_field(
            name="Severity",
            value=report_rating,
            inline=True,
        )
        embed.add_field(
            name="Bounty",
            value=(f"{bounty_crr} {bounty_amt}"),
            inline=True,
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url,
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PrefixReports(client))
