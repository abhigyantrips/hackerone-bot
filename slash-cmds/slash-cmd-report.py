import disnake
from disnake.ext import commands

import os, requests, json

import datetime
import dateutil.parser as dp

auth = (os.getenv("HACKERONE_USERNAME"), os.getenv("HACKERONE_API_KEY"))
headers = {"Accept": "application/json"}


class SlashReports(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
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

        if (
            "default"
            in reportjson["data"]["relationships"]["reporter"]["data"]["attributes"][
                "profile_picture"
            ]["62x62"]
        ):
            reporterpic = "https://hackerone.com/assets/avatars/default-71a302d706457f3d3a31eb30fa3e73e6cf0b1d677b8fa218eaeaffd67ae97918.png"
        else:
            reporterpic = reportjson["data"]["relationships"]["reporter"]["data"][
                "attributes"
            ]["profile_picture"]["62x62"]

        bounty = 0
        for amount in reportjson["data"]["relationships"]["bounties"]["data"]:
            bounty += float(amount["attributes"]["awarded_amount"])

        embed = disnake.Embed(
            title=f"#{id} - {reportjson['data']['attributes']['title']} ({(reportjson['data']['attributes']['state']).capitalize()})",
            color=0x303136,
            timestamp=datetime.datetime.now(),
            url=f"https://hackerone.com/reports/{id}",
        )

        embed.set_author(
            name=f"{reportjson['data']['relationships']['reporter']['data']['attributes']['name']} ({reportjson['data']['relationships']['reporter']['data']['attributes']['username']})",
            icon_url=reporterpic,
            url=f"https://hackerone.com/{reportjson['data']['relationships']['reporter']['data']['attributes']['username']}",
        )

        embed.add_field(
            name="Created at",
            value=f"<t:{round(dp.parse(reportjson['data']['attributes']['created_at']).timestamp())}:f>"
            or "-",
            inline=True,
        )
        embed.add_field(
            name="Disclosed at",
            value=f"<t:{round(dp.parse(reportjson['data']['attributes']['disclosed_at']).timestamp())}:f>"
            or "-",
            inline=True,
        )
        embed.add_field(
            name="Program",
            value=f"[@{reportjson['data']['relationships']['program']['data']['attributes']['handle']}](https://hackerone.com/{reportjson['data']['relationships']['program']['data']['attributes']['handle']})",
            inline=False,
        )
        embed.add_field(
            name="Severity",
            value=(
                reportjson["data"]["relationships"]["severity"]["data"]["attributes"][
                    "rating"
                ]
                or "-"
            ).capitalize(),
            inline=True,
        )
        embed.add_field(
            name="Bounty",
            value=(
                reportjson["data"]["relationships"]["bounties"]["data"][0][
                    "attributes"
                ]["awarded_currency"]
                or ""
            )
            + f" {bounty}",
            inline=True,
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url,
        )

        await ctx.response.send_message(embed=embed)


def setup(client):
    client.add_cog(SlashReports(client))