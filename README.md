<p align="center">
    <img src="https://i.imgur.com/zOhm97u.png" width="100%">
</p>

# HackerOne Bot

The HackerOne bot is an unofficial Discord bot that interacts with and displays information from the [HackerOne API](https://api.hackerone.com/). This refers to fetching information about a specific user or report, searching a query, etc.

## Commands

The prefix of the bot is `!h1`.

`!h1 help` - Returns the help embed for the bot.

`!h1 ping` - Returns the bot latency.

`!h1 user <username>` - Fetches information about a HackerOne user, as per specified username.

`!h1 reports <id>` - Fetches infomraiton about a HackerOne report, as per specified ID.

These features have also been implemented as Discord slash commands. Thus, a user can also use `/user`, `/reports`, etc., giving a first-class way to interact with the bot.

## Contributing

You're welcome to contribute other useful commands, and more efficient command processes to the bot. 

Note that contributions regarding changing embed colors, guild-specific prefixes, etc. are not the prioritized, since in the end, the aim of the bot is to fetch information from the API and display it.

## Issues

If you find an issue with the bot that could lead to a negative user experience, feel free to [open up an issue](https://github.com/abhigyantrips/hackerone-bot/issues/new) in the repository. I'm currently solely handling the development of this bot, so I apologize in advance for any delay in looking at the issue.

## Credits

I do not claim to own any assets or icons used in the development of this bot - all HackerOne assets belong to the [HackerOne company](https://www.hackerone.com/), and have been used here to indicate the organization the information has been displayed from.

I essentially made this for a friend, but I believed that this could be useful to more people out there; so the bot is public and can be invited via [this link](https://www.abhigyantrips.dev/hackerone-bot). If you found this project useful, feel free to give it a star!