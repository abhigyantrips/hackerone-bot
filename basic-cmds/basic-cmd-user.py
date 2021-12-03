import disnake
from disnake.ext import commands

import os, requests, json

import datetime
import dateutil.parser as dp

auth = (os.getenv("HACKERONE_USERNAME"), os.getenv("HACKERONE_API_KEY"))
headers = {"Accept": "application/json"}


class PrefixUser(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="user")
    async def user(self, ctx, *, username: str):

        """Gets information about a HackerOne user.

        Parameters
        ----------
        username: The username of the profile to display.
        """

        userjson = (
            requests.get(
                f"https://api.hackerone.com/v1/users/{username}",
                auth=auth,
                headers=headers,
            )
        ).json()

        try:
            if userjson["errors"][0]["status"] == 401:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **The bot is unauthorized to conduct this action.**"
                )
            elif userjson["errors"][0]["status"] == 403:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **The bot is forbidden to conduct this action.**"
                )
            elif userjson["errors"][0]["status"] == 404:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **Could not find HackerOne user: `{username}`.**"
                )
            elif userjson["errors"][0]["status"] == 429:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **The bot is currently being ratelimited. Please try again later.**"
                )
            elif userjson["errors"][0]["status"] == 500:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **There was an internal server error. Please try again later.**"
                )
            elif userjson["errors"][0]["status"] == 503:
                return await ctx.send(
                    f"<:h1cross:916006021909065728> **The HackerOne API is currently offline. Please try again later.**"
                )
        except KeyError:
            pass

        if "default" in userjson["data"]["attributes"]["profile_picture"]["62x62"]:
            userpic = "https://hackerone.com/assets/avatars/default-71a302d706457f3d3a31eb30fa3e73e6cf0b1d677b8fa218eaeaffd67ae97918.png"
        else:
            userpic = userjson["data"]["attributes"]["profile_picture"]["62x62"]

        embed = disnake.Embed(
            title=f"HackerOne User",
            color=0x303136,
            timestamp=datetime.datetime.now(),
        )

        embed.set_author(
            name=f"{userjson['data']['attributes']['name']} ({userjson['data']['attributes']['username']})",
            url=f"https://hackerone.com/{username}",
            icon_url=userpic,
        )

        embed.add_field(
            name="Name",
            value=f"{userjson['data']['attributes']['name']}",
            inline=True,
        )
        embed.add_field(
            name="Username",
            value=f"`{username}`",
            inline=True,
        )
        embed.add_field(
            name="\u200b",
            value="\u200b",
            inline=True,
        )
        embed.add_field(
            name="Reputation",
            value=(userjson["data"]["attributes"]["reputation"] or "-"),
            inline=True,
        )
        embed.add_field(
            name="Signal",
            value=round(userjson["data"]["attributes"]["signal"] or 0),
            inline=True,
        )
        embed.add_field(
            name="Impact",
            value=round(userjson["data"]["attributes"]["impact"] or 0),
            inline=True,
        )
        embed.add_field(
            name="Bio",
            value=(userjson["data"]["attributes"]["bio"] or "-"),
            inline=False,
        )
        embed.add_field(
            name="Website",
            value=(userjson["data"]["attributes"]["website"] or "-"),
            inline=False,
        )
        embed.add_field(
            name="Joined",
            value=(
                f"<t:{round(dp.parse(userjson['data']['attributes']['created_at']).timestamp())}:f>"
                or "-"
            ),
            inline=False,
        )

        embed.set_thumbnail(url=userpic)

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url,
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(PrefixUser(client))
