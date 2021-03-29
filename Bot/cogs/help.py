import discord
from discord.ext import commands
from config import *
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

# you will need config.py from the main Bot folder or else this wont work ><
# vote epicbot OwO | epic-bot.com/vote 😊

category_list = ""
total_cmds = 0
voter_cmds = 0
premium_cmds = 0

for category in help_categories:
    total_cmds += len(category)


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def help(self, ctx, *, hmm_category=None):
        if hmm_category == None:
            embeds = [
                discord.Embed(
                    title="Help Menu (Page 1)",
                    description=f"""
React to this message to navigate the help menu.

**Total Commands:** {total_cmds}
**Voter Only Commands:** {voter_cmds}
**Premium Commands:** {premium_cmds}

`-` [**Website**](https://epic-bot.com)
`-` [**Support Server**](https://discord.gg/Zj7h8Fp)
`-` [**Source Code**](https://github.com/Nirlep5252/EpicBot)

**Latest Update:** 
`-` \🟢 Added new welcome and leave system with autoroles!
`-` \🟢 Added new image and action commands.
`-` \🟢 Added new `e!chat` command, chat with me! UwU
`-` \🟢 Added improved Music system \🎶
""",
                    color=MAIN_COLOR
                ),
            ]

            i = 0

            for title in help_category_titles:
                embed = discord.Embed(
                    title=title,
                    description=f"For more info please use `e!help {cmd_categories[i]}`",
                    color=MAIN_COLOR
                ).add_field(
                    name=f"Commands({len(help_categories[i])})",
                    value=help_emoji_categories[i]
                )
                if not ctx.channel.is_nsfw() and title == "🔞 • NSFW Commands(Page 14)":
                    pass
                else:
                    embeds.append(embed)

                i += 1

            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
            return

        # checks if its a category uwu vote epicbot
        if hmm_category.lower() in cmd_categories:

            embed_description = ""

            i = 0

            for category_ in cmd_categories:
                if category_ == hmm_category.lower():
                    break
                i += 1

            for cmd in help_categories[i]:
                embed_description += f"`{cmd}` - {help_categories[i][cmd]}\n"

            if hmm_category.lower() == "nsfw" and not ctx.channel.is_nsfw():
                embed = discord.Embed(
                    title="Go away horny!",
                    description="This can only be used in a NSFW channel.",
                    color=RED_COLOR
                )
                await ctx.message.reply(embed=embed)
                return

            embed = discord.Embed(
                title=f"{hmm_category.lower().title()} Commands({len(help_categories[i])})",
                description=embed_description,
                color=MAIN_COLOR
            )

            await ctx.message.reply(embed=embed)
            return

        # checks if the thing entered is a cmd UwU
        if hmm_category.lower() in all_cmds:

            if hmm_category.lower() in nsfw and not ctx.channel.is_nsfw():
                embed = discord.Embed(
                    title="Go away horny!",
                    description="This can only be used in a NSFW channel.",
                    color=RED_COLOR
                )
                await ctx.message.reply(embed=embed)
                return

            embed = discord.Embed(
                title=f"{hmm_category.lower().title()}",
                description=f"""
**Usage:** `e!{all_cmds[hmm_category.lower()][1]}`

- {all_cmds[hmm_category.lower()][0]}
""",
                color=MAIN_COLOR
            )

            await ctx.message.reply(embed=embed)
            return

        else:

            embed = discord.Embed(
                title="Sowwy!",
                description=f"I wasn't able to find the command `{hmm_category}`",
                color=RED_COLOR
            )

            await ctx.message.reply(embed=embed)


def setup(client):
    client.add_cog(Help(client))
