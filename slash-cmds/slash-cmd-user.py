import disnake
from disnake.ext import commands

import os, requests, json

import datetime
import dateutil.parser as dp

auth = (os.getenv("HACKERONE_USERNAME"), os.getenv("HACKERONE_API_KEY"))
headers = {"Accept": "application/json"}

default_avatar = "https://hackerone.com/assets/avatars/default-71a302d706457f3d3a31eb30fa3e73e6cf0b1d677b8fa218eaeaffd67ae97918.png"

class SlashUser(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
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

        # API Error Handilng

        try:
            if userjson["errors"][0]["status"] == 401:
                return await ctx.response.send_message(
                    f"<:h1cross:916006021909065728> **The bot is unauthorized to conduct this action.**",
                    ephemeral=True,
                )
            elif userjson["errors"][0]["status"] == 403:
                return await ctx.response.send_message(
                    f"<:h1cross:916006021909065728> **The bot is forbidden to conduct this action.**",
                    ephemeral=True,
                )
            elif userjson["errors"][0]["status"] == 404:
                return await ctx.response.send_message(
                    f"<:h1cross:916006021909065728> **Could not find HackerOne user: `{username}`.**",
                    ephemeral=True,
                )
            elif userjson["errors"][0]["status"] == 429:
                return await ctx.response.send_message(
                    f"<:h1cross:916006021909065728> **The bot is currently being ratelimited. Please try again later.**",
                    ephemeral=True,
                )
            elif userjson["errors"][0]["status"] == 500:
                return await ctx.response.send_message(
                    f"<:h1cross:916006021909065728> **There was an internal server error. Please try again later.**",
                    ephemeral=True,
                )
            elif userjson["errors"][0]["status"] == 503:
                return await ctx.response.send_message(
                    f"<:h1cross:916006021909065728> **The HackerOne API is currently offline. Please try again later.**",
                    ephemeral=True,
                )
        except KeyError:
            pass

        # User Info

        user_name = userjson['data']['attributes']['name'] or "-"
        user_rept = userjson["data"]["attributes"]["reputation"] or "-"
        user_sigl = round((userjson["data"]["attributes"]["signal"] or 0), 2)
        user_impt = round((userjson["data"]["attributes"]["impact"] or 0), 2)
        user_bio = userjson["data"]["attributes"]["bio"] or "-"
        user_web = userjson["data"]["attributes"]["website"] or "-"
        user_avt = userjson["data"]["attributes"]["profile_picture"]["62x62"]
        if ("default" in user_avt) or (len(user_avt) >= 2048):
            user_avt = default_avatar
        user_create = f"<t:{round(dp.parse(userjson['data']['attributes']['created_at']).timestamp())}:f>" or "-"

        # Embed Creation

        embed = disnake.Embed(
            title=f"HackerOne Profile",
            color=0x303136,
            timestamp=datetime.datetime.now(),
        )

        embed.set_author(
            name=f"{user_name} ({username})",
            url=f"https://hackerone.com/{username}",
            icon_url=user_avt,
        )

        embed.add_field(
            name="Name",
            value=f"{user_name}",
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
            value=user_rept,
            inline=True,
        )
        embed.add_field(
            name="Signal",
            value=user_sigl,
            inline=True,
        )
        embed.add_field(
            name="Impact",
            value=user_impt,
            inline=True,
        )
        embed.add_field(
            name="Bio",
            value=user_bio,
            inline=False,
        )
        embed.add_field(
            name="Website",
            value=user_web,
            inline=False,
        )
        embed.add_field(
            name="Joined",
            value=user_create,
            inline=False,
        )

        embed.set_thumbnail(url=user_avt)

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url,
        )

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar.url,
        )

        await ctx.response.send_message(embed=embed)


def setup(client):
    client.add_cog(SlashUser(client))
