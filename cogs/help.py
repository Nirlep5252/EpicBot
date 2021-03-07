import discord
import datetime
import time 
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext.commands import (CommandOnCooldown)
from disputils import BotEmbedPaginator, BotConfirmation, BotMultipleChoice

# yes - this cog is the worst cog pls dont look at this code thx <3 

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client # e

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['test'])
    async def ping(self, ctx):
        
        time_lol = time.time()
        
        msg = await ctx.message.reply(embed=discord.Embed(title="Pinging...", color = 0x00FFFF))
        
        ping = discord.Embed(title="Pong!", description=f"API Latency: **{round(self.client.latency * 1000)}ms**\nBot Latency: **{round((time.time() - time_lol) * 1000)}ms**", color=0x00FFFF)
        
        await msg.edit(embed=ping)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def help(self, ctx, *, category = None):
        if category == None:
            # embed = discord.Embed(title = "**All Commands(89)**",
            #                         description = "To get detailed help for a command, do `e!help [command]`.",
            #                         color = 0x00FFFF)
            # embed.add_field(name = "🔧 • Utility(14)",
            #                 value = f"Type `e!help utility` for more info.```\n😍-NQN\n❔-Prefix\n⛅-Weather\n😵-SelfDestruct\n📢-Announce\n🎉-Giveaway\n📑-Translate\n📊-Poll\n⏰-Countdown\n🔗-Create Invite\n🟠-Coin Flip\n🔢-Random Number\n🎲-Dice\n📨-Embed\n```",
            #                 inline = True)
            # embed.add_field(name = "🛠️ • Moderation(10)",
            #                 value = f"Type `e!help moderation` for more info.```\n⚠️-Warn\n⚠ - Warnings\n🔨-Ban\n⛏️-Kick\n🍀-Unban\n🔴-Clear\n❌-Delete Channel\n✅-Create Channel\n➕-Add Role\n➖-Remove Role\n```",
            #                 inline = True)
            # embed.add_field(name = "😀 • Fun(16)",
            #                 value = f"Type `e!help fun` for more info.```\n😂-Freenitro\n🔫-Snipe\n🔫-EditSnipe\n😊-Howcute\n😍-Simpfor\n😊-OWO\n💻-Hack\n😁-Mock\n💓-Aesthetic\n😂-Dad Joke\n🤣-Meme\n📜-Quote\n👩‍🏫-Advice\n🗣️-Say\n💬-Ascii\n🕵️‍♀️-Predict\n```",
            #                 inline = True)
            # embed.add_field(name = "💸 • Economy(10)",
            #                 value = f"Type `e!help economy` for more info.```\n💰-Balance\n👜-Inventory\n🏪-Shop\n🎰-Slots\n🛒-Buy\n🛍️-Sell\n💱-Withdraw\n💱-Deposit\n🎁-Give\n🙏-Beg\n```",
            #                 inline = True)
            # embed.add_field(name = "🖼️ • Image(12)",
            #                 value = f"Type `e!help image` for more info.```\n🐱-Cat\n🐶-Dog\n🦊-Fox\n🔥-Burn\n🚮-Trash\n😡-Angry\n📚-Fact\n🧠-Illness\n😱-Shock\n🗡️-Wanted\n🤗-Hug\n🥰-Anime\n```",
            #                 inline = True)
            # embed.add_field(name = "ℹ️ • Info(5)",
            #                 value = f"Type `e!help info` for more info.```\n🦠-Covid-19\n👥-UserInfo\n📈-ServerInfo\n🤖-BotInfo\n🖼️-Avatar\n```",
            #                 inline = True)
            # embed.add_field(name = "🤖 • Bot(8)",
            #                 value = f"Type `e!help bot` for more info.```\n✅-Help\n📈-Stats\n⬆️-Uptime\n❤️-Invite\n🔼-Vote\n🔗-Discord\n👤-Privacy\n🐞-Bug Report\n```",
            #                 inline = True)
            # embed.add_field(name = "🎮 • Games(2)",
            #                 value = f"Type `e!help games` for more info.```\n✅-Tic-Tac-Toe\n📃-Rock-Paper-Scissors\n```",
            #                 inline = True)
            # embed.add_field(name = "🎶 • Music(9)",
            #                 value = f"Type `e!help music` for more info.```\n🔊-Connect\n🎶-Play\n🎵-Nowplaying\n⏸-Pause\n▶-Resume\n🧾-Queue\n⏭-Skip\n⏹-Stop\n🔉-Volume```",
            #                 inline = True)
            # if ctx.channel.is_nsfw():
            #     embed.add_field(name = "🔞 • NSFW(3)",
            #                     value = "Type `e!help nsfw` for more info.```🤤-Hentai\n😋-Thighs\n🥰-Nekogif```",
            #                     inline = True)
            # else:
            #     pass

            # embed.add_field(name = "‎",
            #                 value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
            #                 inline = False)
            # # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            # embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            # embed.timestamp = datetime.datetime.utcnow()
            # await ctx.send(embed = embed)

            embeds = [
                discord.Embed(
                    title = "Help Menu (Page 1)",
                    description = "React to this message to navigate the help menu.\nFor more info on commands or categories please use `e!help <cmd>`\n\n**Total Commands:** 102\n**Voter Only Commands:** 0\n**Premium Commands:** 0",
                    color = 0x00FFFF
                ),
                discord.Embed(
                    title=":wrench: • Utility Commands (Page 2)",
                    description = "For more info please use `e!help utility`.",
                    color = 0x00FFFF
                ).add_field(
                    name = "Commands(14)",
                    value = """
                        ```
😍-NQN
❔-Prefix
⛅-Weather
😵-SelfDestruct
📢-Announce
🎉-Giveaway
📑-Translate
📊-Poll
⏰-Countdown
🔗-Create Invite
🟠-Coin Flip
🔢-Random Number
🎲-Dice
📨-Embed```
                    """
                ),
                discord.Embed(
                    title=":tools: • Moderation Commands (Page 3)",
                    description="For more info please use `e!help moderation`.",
                    color=0x00FFFF
                ).add_field(
                    name="Commands(10)",
                    value="""
                        ```
⚠️-Warn
⚠️-Warnings
🔨-Ban
⛏️-Kick
🍀-Unban
🔴-Clear
❌-Delete Channel
✅-Create Channel
➕-Add Role
➖-Remove Role```
                    """
                ),
                discord.Embed(
                    title=":grinning: • Fun Commands(Page 4)",
                    description="For more info please use `e!help fun`.",
                    color = 0x00FFFF
                ).add_field(
                    name="Commands(17)",
                    value="""
                        ```
😂-Freenitro
🔫-Snipe
🔫-EditSnipe
😊-Howcute
😍-Simpfor
😊-OWO
💻-Hack
😁-Mock
💓-Aesthetic
😂-Dad Joke
🤣-Meme
📜-Quote
👩‍🏫-Advice
🗣️-Say
💬-Ascii
🕵️‍♀️-Predict
👨-Randomname```
                    """
                ),
                discord.Embed(
                    title = "⬆ • Levelling Commands(Page 5)",
                    description="For more info please use `e!help levelling`.",
                    color=0x00FFFF
                ).add_field(
                    name = "Commands(4)",
                    value = """
                    ```
🔼-Levels
💬-Levelupchannel
💹-Rank
📊-Leaderboard```
                    """
                ),
                discord.Embed(
                    title=":notes: • Music Commands(Page 6)",
                    description="For more info please use `e!help music`.",
                    color=0x00FFFF
                ).add_field(
                    name="Commands(9)",
                    value="""
                        ```
🔊-Connect
🎶-Play
🎵-Nowplaying
⏸-Pause
⏯-Resume
🧾-Queue
⏭-Skip
⏹-Stop
🔉-Volume```
                    """
                ),
                discord.Embed(
                    title=":money_with_wings: • Economy Commands(Page 7)",
                    description="For more info please use `e!help economy`.",
                    color=0x00FFFF
                ).add_field(
                    name="Commands(10)",
                    value="""
                        ```
💰-Balance
👜-Inventory
🏪-Shop
🎰-Slots
🛒-Buy
🛍️-Sell
💱-Withdraw
💱-Deposit
🎁-Give
🙏-Beg```
                    """
                ),
                discord.Embed(
                    title=":frame_photo: • Image Commands(Page 8)",
                    description="For more info please use `e!help image`.",
                    color=0x00FFFF
                ).add_field(
                    name="Commands(11)",
                    value="""
                        ```
🐱-Cat
🐶-Dog
🦊-Fox
🔥-Burn
🚮-Trash
😡-Angry
📚-Fact
🧠-Illness
😱-Shock
🗡️-Wanted
🥰-Anime```
                    """
                ),
                discord.Embed(
                    title = "<:HugPlease:801710974117740554> • Action Commands(Page 9)",
                    description="For more info please use `e!help action`.",
                    color = 0x00FFFF
                ).add_field(
                    name = "Commands(5)",
                    value = """
```🤗-Hug
💋-Kiss
💞-Pat
🖐-Slap
😆-Tickle```
                    """
                ),

                discord.Embed(
                    title="<:EpicInfo:766498653753049109> • Info Commands(Page 10)",
                    description="For more info please use `e!help info`.",
                    color=0x00FFFF
                ).add_field(
                    name="Commands(5)",
                    value="""
                        ```
🦠-Covid-19
👥-UserInfo
📈-ServerInfo
🤖-BotInfo
🖼️-Avatar```
                    """
                ),
                discord.Embed(
                    title="<a:PetEpicBot:797142108611280926> • Bot Commands(Page 11)",
                    description="For more info please use `e!help bot`.",
                    color=0x00FFFF
                ).add_field(
                    name="Commands(8)",
                    value="""
                        ```
✅-Help
📈-Stats
⬆️-Uptime
❤️-Invite
🔼-Vote
🔗-Discord
👤-Privacy
🐞-Bug Report```
                    """
                ),
                discord.Embed(
                    title=":video_game: • Game Commands(Page 12)",
                    description="For more info please use `e!help games`.",
                    color=0x00FFFF
                ).add_field(
                    name="Commands(2)",
                    value="""
                        ```
✅-Tic-Tac-Toe
📃-Rock-Paper-Scissors```
                    """
                )
            ]

            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()

        elif category.lower() == "leveling" or category.lower() == "levelling":
            embed = discord.Embed(title = "**Level Commands(4)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "🔼 - Levels",
                            value = "Usage: `e!levels enable/disable`",
                            inline = True)
            embed.add_field(name = "💬 - Levelupchannel",
                            value = "Usage: `e!levelupchannel <channel>`",
                            inline = True)
            embed.add_field(name = "💹 - Rank",
                            value = "Usage: `e!rank [user]`",
                            inline = True)
            embed.add_field(name = "📊 - Leaderboard",
                            value = "Usage: `e!leaderboard`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "music":
            embed = discord.Embed(title = "**Music Commands(9)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "🔊 - Connect",
                            value = "Usage: `e!connect`",
                            inline = True)
            embed.add_field(name = "🎶 - Play",
                            value = "Usage: `e!play <song/url>`",
                            inline = True)
            embed.add_field(name = "🎵 - Nowplaying",
                            value = "Usage: `e!nowplaying`",
                            inline = True)
            embed.add_field(name = "⏸ - Pause",
                            value = "Usage: `e!pause`",
                            inline = True)
            embed.add_field(name = "▶ - Resume",
                            value = "Usage: `e!resume`",
                            inline = True)
            embed.add_field(name = "🧾 - Queue",
                            value = "Usage: `e!queue`",
                            inline = True)
            embed.add_field(name = "⏭ - Skip",
                            value = "Usage: `e!skip`",
                            inline = True)
            embed.add_field(name = "⏹ - Stop",
                            value = "Usage: `e!stop`",
                            inline = True)
            embed.add_field(name = "🔉 - Volume",
                            value = "Usage: `e!volume <amount>`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "action" or category.lower() == "actions":
            embed = discord.Embed(
                    title = "**Action Commands(5)**",
                    description = "To get detailed help for a command, do `e!help [command]`.",
                    color = 0x00FFFF
                )
            embed.add_field(name = "🤗 - Hug",
                            value = "Usage: `e!hug <user>`",
                            inline = True)
            embed.add_field(name = "💋 - Kiss",
                            value = "Usage: `e!kiss <user>`",
                            inline = True)
            embed.add_field(name = "💞 - Pat",
                            value = "Usage: `e!pat <user>`",
                            inline = True)
            embed.add_field(name = "🖐 - Slap",
                            value = "Usage: `e!slap <user>`",
                            inline = True)
            embed.add_field(name = "😆 - Tickle",
                            value = "Usage: `e!tickle <user>`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "utility" or category.lower() == "utils" or category.lower() == "util":
            embed = discord.Embed(title = "**Utility Commands(14)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "😍 - NQN",
                            value = "Usage: `e!nqn enable/disable`",
                            inline = True)
            embed.add_field(name = "❔ - Prefix",
                            value = "Usage: `e!prefix [new prefix]`",
                            inline = True)
            embed.add_field(name = "⛅ - Weather", value = "Usage: `e!weather <location>`", inline = True)
            embed.add_field(name = "📨 - Embed", value = "Usage: `e!embed <#hexcolor> | <title> | description`", inline = True)
            embed.add_field(name = "🎉 - Giveaway", value = "Usage: `e!giveaway`", inline = True)
            embed.add_field(name = "😵 - SelfDestruct", value = "Usage `e!selfdestruct <text channel> <time> <message>`", inline = True)
            embed.add_field(name = "📢 - Announce", value = "Usage: `e!announce`", inline = True)
            embed.add_field(name = "📑 - Translate", value = "Usage: `e!translate [language] [text]`", inline = True)
            embed.add_field(name = "📊 - Poll", value = "Usage: `e!poll \"[topic]\" [option1] [option2] [option3]...`", inline = True)
            embed.add_field(name = "⏰ - Countdown", value = "Usage: `e!countdown`", inline = True)
            embed.add_field(name = "🔗 - Create Invite", value = "Usage: `e!create_invite`", inline = True)
            embed.add_field(name = "🎲 - Dice",
                            value = "Usage: `e!dice`",
                            inline = True)
            embed.add_field(name = ":coin: - CoinFlip",
                            value = "Usage: `e!flip`",
                            inline = True)
            embed.add_field(name = "🔢 - Random Number",
                            value = "Usage: `e!randomnumber [num1] [num2]`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "nsfw":
            if ctx.channel.is_nsfw():
                embed = discord.Embed(
                    title = "**NSFW Commands(7)**",
                    description = "To get detailed help for a command, do `e!help [command]`.",
                    color = 0x00FFFF
                )
                embed.add_field(
                    name = "🤤 - Hentai",
                    value = "Usage: `e!hentai`",
                    inline = True
                )
                embed.add_field(
                    name = "😋 - Thighs",
                    value = "Usage: `e!thighs`",
                    inline = True
                )
                embed.add_field(
                    name = "🥰 - Nekogif",
                    value = "Usage: `e!nekogif`",
                    inline = True
                )
                embed.add_field(
                    name = "😊 - Boobs",
                    value = "Usage: `e!boobs`",
                    inline = True
                )
                embed.add_field(
                    name = "🍆 - Blowjob",
                    value = "Usage: `e!blowjob`",
                    inline = True
                )
                embed.add_field(
                    name = "🍑 - Pussy",
                    value = "Usage: `e!pussy`",
                    inline = True
                )
                embed.add_field(
                    name = "🖐 - Spank",
                    value = "Usage: `e!spank <user>`",
                    inline = True
                )

                embed.add_field(name = "‎",
                                value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                                inline = False)
                # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
                embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed = embed)
            else:
                await ctx.send("This command can only be used in a NSFW channel.")

        elif category.lower() == "moderation" or category.lower() == "mod" or category.lower() == "admin":
            embed = discord.Embed(title = "**Moderation Commands(10)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "🔴 - Clear",
                            value = "Usage: `e!clear [amount]`",
                            inline = True)
            embed.add_field(name = "⛏️ - Kick",
                            value = "Usage: `e!kick [user] [reason(optional)]`",
                            inline = True)
            embed.add_field(name = "🔨 - Ban",
                            value = "Usage: `e!ban [user] [reason(optional)]`",
                            inline = True)
            embed.add_field(name = "🍀 - Unban",
                            value = "Usage: `e!unban [user]`",
                            inline = True)
            embed.add_field(name = "⚠️ - Warn",
                            value = "Usage: `e!warn [user] [reason]`",
                            inline = True)
            embed.add_field(name = f"⚠  - Warnings",
                            value = f"Usage: `e!warns [user]`",
                            inline = True)
            embed.add_field(name = "✅ - Create Channel",
                            value = "Usage: `e!createchannel [name]`",
                            inline = True)
            embed.add_field(name = "❌ - Delete Channel",
                            value = "Usage: `e!deletechannel [name]`",
                            inline = True)
            embed.add_field(name = "<:EpicRemove:771674521731989536> - Add Role",
                            value = "Usage: `e!addrole [user] [role]`",
                            inline = True)
            embed.add_field(name = "<:EpicAdd:771674521471549442> - Remove Role",
                            value = "Usage: `e!removerole [user] [role]`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "fun":
            embed = discord.Embed(title = "**Fun Commands(17)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "😂 - Freenitro",
                            value = "Usage: `e!freenitro`",
                            inline = True)
            embed.add_field(name = "🔫 - Snipe",
                            value = "Usage: `e!snipe`",
                            inline = True)
            embed.add_field(name = "🔫 - EditSnipe",
                            value = "Usage: `e!editsnipe`",
                            inline = True)
            embed.add_field(name = "😊 - Howcute",
                            value = "Usage: `e!howcute [user]`",
                            inline = True)
            embed.add_field(name = "😍 - Simpfor",
                            value = "Usage: `e!simpfor <user>`",
                            inline = True)
            embed.add_field(name = "💻 - Hack",
                            value = "Usage: `e!hack <user>`",
                            inline = True)
            embed.add_field(name = "😊 - OWO",
                            value = "Usage: `e!owo <text>`",
                            inline = True)
            embed.add_field(name = "💓 - Aesthetic",
                            value = "Usage: `e!aesthetic <text> | [type]`",
                            inline = True)
            embed.add_field(name = "😂 - Dad Jokes",
                            value = "Usage: `e!dadjoke`",
                            inline = True)
            embed.add_field(name = "🤣 - Meme",
                            value = "Usage: `e!meme`",
                            inline = True)
            embed.add_field(name = "👩‍🏫 - Advice",
                            value = "Usage: `e!advice`",
                            inline = True)
            embed.add_field(name = "🗣️ - Say",
                            value = "Usage: `e!say <text>`",
                            inline = True)
            embed.add_field(name = "💬 - Ascii",
                            value = "Usage: `e!ascii <text>`",
                            inline = True)
            embed.add_field(name = "📜 - Quote",
                            value = "Usage: `e!quote`",
                            inline = True)
            embed.add_field(name = "🕵️‍♀️ - Predict",
                            value = "Usage: `e!predict <question>`",
                            inline = True)
            embed.add_field(name = "😁 - Mock",
                            value = "Usage: `e!mock <text>`",
                            inline = True) # 👨-Randomname
            embed.add_field(name = "👨 - Randomname",
                            value = "Usage: `e!randomname`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "economy" or category.lower() == "money" or category.lower() == "currency":
            embed = discord.Embed(title = "**Economy Commands(10)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "💰 - Balance",
                            value = "Usage: `e!balance`",
                            inline = True)
            embed.add_field(name = "👜 - Inventory",
                            value = "Usage: `e!bag`",
                            inline = True)
            embed.add_field(name = "🏪 - Shop",
                            value = "Usage: `e!shop`",
                            inline = True)
            embed.add_field(name = "🎰 - Slots",
                            value = "Usage: `e!slots [money]`",
                            inline = True)
            embed.add_field(name = "🛒 - Buy",
                            value = "Usage: `e!buy [item]`",
                            inline = True)
            embed.add_field(name = "🛍️ - Sell",
                            value = "Usage: `e!sell [item]`",
                            inline = True)
            embed.add_field(name = "💱 - Withdraw",
                            value = "Usage: `e!withdraw [amount]`",
                            inline = True)
            embed.add_field(name = "💱 - Deposit",
                            value = "Usage: `e!deposit [amount]`",
                            inline = True)
            embed.add_field(name = "🎁 - Give",
                            value = "Usage: `e!give [user] [amount]`",
                            inline = True)
            embed.add_field(name = "🙏 - Beg",
                            value = "Usage: `e!beg`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "image":
            embed = discord.Embed(title = "**Image Commands(12)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "🐱 - Cat",
                            value = "Usage: `e!cat`",
                            inline = True)
            embed.add_field(name = "🐶 - Dog",
                            value = "Usage: `e!dog`",
                            inline = True)
            embed.add_field(name = "🦊 - Fox",
                            value = "Usage: `e!fox`",
                            inline = True)
            embed.add_field(name = "🥰 - Anime",
                            value = "Usage: `e!anime`",
                            inline = True)
            embed.add_field(name = "🤗 - Hug",
                            value = "Usage: `e!hug [user]`",
                            inline = True)
            embed.add_field(name = "🔥 - Burn",
                            value = "Usage: `e!burn [user]`",
                            inline = True)
            embed.add_field(name = "🚮 - Trash",
                            value = "Usage: `e!trash [user]`",
                            inline = True)
            embed.add_field(name = "😡 - Angry",
                            value = "Usage: `e!angry [user]`",
                            inline = True)
            embed.add_field(name = "📚 - Fact",
                            value = "Usage: `e!fact [text]`",
                            inline = True)
            embed.add_field(name = "🧠 - Illness",
                            value = "Usage: `e!illness [text]`",
                            inline = True)
            embed.add_field(name = "😱 - Shock",
                            value = "Usage: `e!shock [text]`",
                            inline = True)
            embed.add_field(name = "🗡️ - Wanted",
                            value = "Usage: `e!wanted [user]`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "info":
            embed = discord.Embed(title = "**Info Commands(5)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "<:EpicCovid:768701899959697408> - Covid-19",
                            value = "Usage: `e!covid [country]`",
                            inline = True)
            embed.add_field(name = "👥 - UserInfo",
                            value = "Usage: `e!userinfo [user]`",
                            inline = True)
            embed.add_field(name = "📈 - ServerInfo",
                            value = "Usage: `e!serverinfo`",
                            inline = True)
            embed.add_field(name = "🤖 - BotInfo",
                            value = "Usage: `e!botinfo`",
                            inline = True)
            embed.add_field(name = "🖼️ - Avatar",
                            value = "Usage: `e!avatar [user]`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "bot" or category.lower() == "epicbot":
            embed = discord.Embed(title = "**Bot Commands(8)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "✅ - Help",
                            value = "Usage: `e!help [cmd]`",
                            inline = True)
            embed.add_field(name = "<:RamHeart:758103228058566656> - Invite",
                            value = "Usage: `e!invite`",
                            inline = True)
            embed.add_field(name = "📈 - Stats",
                            value = "Usage: `e!stats`",
                            inline = True)
            embed.add_field(name = "⬆️ - Uptime",
                            value = "Usage: `e!uptime`",
                            inline = True)
            embed.add_field(name = "⬆️ - Vote",
                            value = f"Usage: `e!vote`",
                            inline = True)
            embed.add_field(name = "<:EpicDiscord:770889292746194964> - Discord",
                            value = "Usage: `e!discord`",
                            inline = True)
            embed.add_field(name = "👤 - Privacy",
                            value = "Usage: `e!privacy`",
                            inline = True)
            embed.add_field(name = "🐞 - Bug Report",
                            value = "Usage: `e!bug_report`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "games" or category.lower() == "game":
            embed = discord.Embed(title = "**Game Commands(2)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "📃 - Rock, Paper, Scissors",
                            value = "Usage: `e!rps [rock/paper/scissors]`",
                            inline = True)
            embed.add_field(name = "✅ - Tic-Tac-Toe",
                            value = "Usage: `e!tictactoe`",
                            inline = True)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "announce":
            embed = discord.Embed(title = "**Announcement Command**",
                                    description = "**Usage**: `e!announce` \n- This will make an announcement in the desired channel. Make sure that the bot has enough permissions to send messages in that channel.\n\n**Required User Permissions:** `Manage Server`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "giveaway":
            embed = discord.Embed(title = "**Giveaway Command**",
                                    description = "**Usage:** `e!giveaway` \n- This will start a giveaway in the desired channel. Make sure that the bot has enough permissions to send messages in that channel.\n\n**Required User Permissions:** `Manage Server`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "translate":
            embed = discord.Embed(title = "**Translate Command**",
                                    description = "**Usage:** `e!translate [language] [text]` \n- This will translate the text to the desired language using Google Translate.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "poll":
            embed = discord.Embed(title = "**Poll Command**",
                                    description = "**Usage:** `e!poll [topic] [option1] [option2] [option3]...` \n- This will make a poll in the desired channel.\n\n**Required User Permissions:** `Manage Server`\n**Required Bot Permissions:** `Send Messages, Add Reactions`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "countdown":
            embed = discord.Embed(title = "**Countdown Command**",
                                    description = "**Usage:** `e!countdown` \n- This will start a countdown in the desired channel.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "createinvite" or category.lower() == "create_invite":
            embed = discord.Embed(title = "**Create Invite Command**",
                                    description = "**Usage:** `e!create_invite` \n- The bot will create a permanent invite link for the server and send it to you.\n\n**Required User Permissions:** `Create Invites`\n**Required Bot Permissions:** `Send Messages, Create Invites`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "warn":
            embed = discord.Embed(title = "**Warning Command**",
                                    description = "**Usage:** `e!warn [user] [reason(optional)]` \n- This will warn the user.\n\n**Required User Permissions:** `Kick Members`\n**Required Bot Permissions:** `Send Messages, Kick Members`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "ban":
            embed = discord.Embed(title = "**Ban Command**",
                                    description = "**Usage:** `e!ban [user] [reason(optional)]` \n- This will ban the user mentioned.\n\n**Required User Permissions:** `Ban Members`\n**Required Bot Permissions:** `Send Messages, Ban Members`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "kick":
            embed = discord.Embed(title = "**Kick Command**",
                                    description = "**Usage:** `e!kick [user] [reason(optional)]` \n- This will kick the user.\n\n**Required User Permissions:** `Kick Members`\n**Required Bot Permissions:** `Send Messages, Kick Members`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "unban":
            embed = discord.Embed(title = "**Unban Command**",
                                    description = "**Usage:** `e!unban [user]` \n- This will unban the user.\n\n**Required User Permissions:** `Ban Members`\n**Required Bot Permissions:** `Send Messages, Ban Members`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "clear":
            embed = discord.Embed(title = "**Purge/Clear Command**",
                                    description = "**Usage:** `e!clear [amount]` \n- This will delete the amount of messages mentioned in that channel.\n\n**Required User Permissions:** `Manage Messages`\n**Required Bot Permissions:** `Send Messages, Manage Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "deletechannel" or category.lower() == "delete_channel" or category.lower() == "delete-channel":
            embed = discord.Embed(title = "**Delete Channel Command**",
                                    description = "**Usage:** `e!deletechannel [text-channel]` \n- This will delete the mentioned channel.\n\n**Required User Permissions:** `Manage Channels`\n**Required Bot Permissions:** `Send Messages, Manage Channels`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "createchannel" or category.lower() == "create_channel" or category.lower() == "create-channel":
            embed = discord.Embed(title = "**Create Channel Command**",
                                    description = "**Usage:** `e!createchannel [name]` \n- This will create a text-channel.\n\n**Required User Permissions:** `Manage Channels`\n**Required Bot Permissions:** `Send Messages, Manage Channels`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "addrole" or category.lower() == "add_role" or category.lower() == "add-role":
            embed = discord.Embed(title = "**Add Role Command**",
                                    description = "**Usage:** `e!addrole [user] [role]` \n- This will add the role to the user.\n\n**Required User Permissions:** `Manage Roles`\n**Required Bot Permissions:** `Send Messages, Manage Roles`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "removerole" or category.lower() == "remove-role" or category.lower() == "remove_role":
            embed = discord.Embed(title = "**Remove Role Command**",
                                    description = "**Usage:** `e!removerole [user] [role]` \n- This will remove the role from the user.\n\n**Required User Permissions:** `Manage Roles`\n**Required Bot Permissions:** `Send Messages, Manage Roles`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "owo":
            embed = discord.Embed(title = "**OWO Command**",
                                    description = "**Usage:** `e!owo [text]` \n- This will make your text look adorable.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "meme":
            embed = discord.Embed(title = "**Meme Command**",
                                    description = "**Usage:** `e!meme` \n- This will give you some memes.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "say":
            embed = discord.Embed(title = "**Say Command**",
                                    description = "**Usage:** `e!say [text]`\n- This will make the bot say that.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "predict":
            embed = discord.Embed(title = "**Predict Command**",
                                    description = "**Usage:** `e!predict [question]` \n- The bot will predict and answer your question.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "dice":
            embed = discord.Embed(title = "**Dice Command**",
                                    description = "**Usage:** `e!dice` \n- The bot will roll a dice for you.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "coin" or category.lower() == "flip" or category.lower() == "coinflip":
            embed = discord.Embed(title = "**Coin Flip Command**",
                                    description = "**Usage:** `e!flip` \n- The bot will flip a coin for you.\n\n**Required User Permissions:** `None\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "randomnumber" or category.lower() == "random_number":
            embed = discord.Embed(title = "**Random Number Command**",
                                    description = "**Usage:** `e!randomnumber [num01] [num02]` \n- The bot will pick a random number between [num01] and [num02].\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "balance" or category.lower() == "bal":
            embed = discord.Embed(title = "**Balance Command**",
                                    description = "**Usage:** `e!balance` \n- This will show your balance.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "inventory" or category.lower() == "bag":
            embed = discord.Embed(title = "**Inventory Command**",
                                    description = "**Usage:** `e!bag` \n- This will show your inventory.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "shop":
            embed = discord.Embed(title = "**Shop Command**",
                                    description = "**Usage:** `e!shop`\n- This will show the shop.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "slots":
            embed = discord.Embed(title = "**Slots Command**",
                                    description = "**Usage:** `e!slots [amount]` \n- You will have a chance to quintuple your money or lose it in slots.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "buy":
            embed = discord.Embed(title = "**Buy Command**",
                                    description = "**Usage:** `e!buy [item]` \n- You bought the item.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "sell":
            embed = discord.Embed(title = "**Sell Command**",
                                    description = "**Usage:** `e!sell [item]` \n- You sold the item.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "withdraw":
            embed = discord.Embed(title = "**Withdraw Command**",
                                    description = "**Usage:** `e!withdraw [amount]` \n- You withdrew [amount] money from your bank.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "deposit":
            embed = discord.Embed(title = "**Deposit Command**",
                                    description = "**Usage:** `e!deposit [amount]` \n- You deposited [amount] money in your bank.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "give":
            embed = discord.Embed(title = "**Give Command**",
                                    description = "**Usage:** `e!give [user] [amount]` \n- The [user] will be given [amount] money from your wallet.\n\n**Required User Permissions:** `Manage Server`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "beg":
            embed = discord.Embed(title = "**Beg Command**",
                                    description = "**Usage:** `e!beg` \n- You begged for money so i gave you some.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "cat":
            embed = discord.Embed(title = "**Cat Command**",
                                    description = "**Usage:** `e!cat` \n- You like cats? Well here are some cat images.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "dog":
            embed = discord.Embed(title = "**Dog Command**",
                                    description = "**Usage:** `e!dog` \n- You like dogs? Well here are some dog images.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "burn":
            embed = discord.Embed(title = "**Burn Command**",
                                    description = "**Usage:** `e!burn [user]` \n- Spongebob burned the [user]. F.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages, Attach Files`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "trash":
            embed = discord.Embed(title = "**Trash Command**",
                                    description = "**Usage:** `e!trash [trash]` \n- Some lady thinks that the [user] is trash.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages, Attach Files`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "angry":
            embed = discord.Embed(title = "**Angry Command**",
                                    description = "**Usage:** `e!angry [user]` \n- Seems like this guy doesn't like the [user] and is angry because of it.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages, Attach Files`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "fact":
            embed = discord.Embed(title = "**Fact Command**",
                                    description = "**Usage:** `e!fact [text]` \n- [text] is a fact, even the image shows that.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages, Attach Files`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "illness":
            embed = discord.Embed(title = "**Illness Command**",
                                    description = "**Usage:** `e!illness [text]` \n- Shows the mental illness meme with the [text] in it.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages, Attach Files`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "shock":
            embed = discord.Embed(title = "**Shock Command**",
                                    description = "**Usage:** `e!shock [text]` \n- This guy is shocked because of [text].\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages, Attach Files`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "wanted":
            embed = discord.Embed(title = "**Wanted Command**",
                                    description = "**Usage:** `e!wanted [user]` \n- The [user] is wanted.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages, Attach Files`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "hug":
            embed = discord.Embed(title = "**Hug Command**",
                                    description = "**Usage:** `e!hug [user]` \n- You just hugged [user] virtually.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "anime":
            embed = discord.Embed(title = "**Anime Command**",
                                    description = "**Usage:** `e!anime` \n- You like anime? Well here are some anime pictures.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "covid" or category.lower() == "covid-19":
            embed = discord.Embed(title = "**Covid-19 Command**",
                                    description = "**Usage:** `e!covid [country]` \n- This will show covid-19 information/stats for the country mentioned.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "userinfo" or category.lower() == "user-info" or category.lower() == "user_info":
            embed = discord.Embed(title = "**User Info Command**",
                                    description = "**Usage:** `e!userinfo [user]` \n- This will show the information about the user.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "serverinfo" or category.lower() == "server-info" or category.lower() == "server_info":
            embed = discord.Embed(title = "**Server Info Command**",
                                    description = "**Usage:** `e!serverinfo` \n- This will show the information about the server.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages, Manage Server, View Audit Log, View Members List`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "avatar":
            embed = discord.Embed(title = "**Avatar Command**",
                                    description = "**Usage:** `e!avatar [user]` \n- This will show the avatar of the user.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "prefix":
            embed = discord.Embed(title = "**Prefix Command**",
                                    description = "**Usage:** `e!prefix [new prefix]` \n- This will change the prefix of the bot.\n\n**Required User Permissions:** `Administrator`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "invite":
            embed = discord.Embed(title = "**Invite Command**",
                                    description = "**Usage:** `e!invite` \n- This will give you a link to invite EpicBot to your own server.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "discord":
            embed = discord.Embed(title = "**Discord Command**",
                                    description = "**Usage:** `e!discord` \n- This will give you a link to join our Discord Server.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "botinfo":
            embed = discord.Embed(title = "**Bot Info Command**",
                                    description = "**Usage:** `e!botinfo` \n- This will show all the information about EpicBot.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "bugreport" or category.lower() == "bug_report":
            embed = discord.Embed(title = "**Bug Report Command**",
                                    description = "**Usage:** `e!bug_report` \n- This will give you a link with which you can report a bug for EpicBot.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "rps":
            embed = discord.Embed(title = "**Rock, Paper, Scissors Command**",
                                    description = "**Usage:** `e!rps [rock/paper/scissors]` \n- Play a game of Rock, Paper, Scissors with EpicBot.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "hack":
            embed = discord.Embed(title = "**Hack Command**",
                                    description = "**Usage:** `e!hack [user]` \n- The user will be hacked.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)


        elif category.lower() == "vote":
            embed = discord.Embed(title = "**Vote Command**",
                                    description = "**Usage:** `e!vote` \n- This will give you a link with which you can vote EpicBot.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "quote":
            embed = discord.Embed(title = "**Quote Command**",
                                    description = "**Usage:** `e!quote` \n- This will send some quotes.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "dadjoke":
            embed = discord.Embed(title = "**Dad Joke Command**",
                                    description = "**Usage:** `e!dadjoke` \n- This will send some dadjokes.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "uptime":
            embed = discord.Embed(title = "**Uptime Command**",
                                    description = "**Usage:** `e!uptime` \n- This will show how long has the bot been online.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "fox":
            embed = discord.Embed(title = "**Fox Command**",
                                    description = "**Usage:** `e!fox` \n- This will show some fox images.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Attach Files`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "advice":
            embed = discord.Embed(title = "**Advice Command**",
                                    description = "**Usage:** `e!advice` \n- This will give you a random advice.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "ascii":
            embed = discord.Embed(title = "**Ascii Command**",
                                    description = "**Usage:** `e!ascii <text>` \n- This will convert your text to ascii.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "stats":
            embed = discord.Embed(title = "**Stats Command**",
                                    description = "**Usage:** `e!stats` \n- This will show the stats of the bot.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)
            # "Usage: `e!tictactoe`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`, `Add Reactions`, `Manage Messages`"

        elif category.lower() == "tictactoe" or category.lower() == "ttt":
            embed = discord.Embed(title = "**Tic-Tac-Toe Command**",
                                    description = "**Usage:** `e!tictactoe` \n- This will start a tic-tac-toe game between you and EpicBot.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Add Reactions`, `Manage Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "warns" or category.lower() == "warnings":
            embed = discord.Embed(title="**Warnings Command**",
                                  description="**Usage:** `e!warns [user]` \n- This will show the number of warns this user has.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                  color=0x00FFFF)

            embed.add_field(name="‎",
                            value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline=False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "privacy":
            embed = discord.Embed(title="**Privacy Policy Command**",
                                  description="**Usage:** `e!privacy` \n- This will show our privacy policy.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                  color=0x00FFFF)

            embed.add_field(name="‎",
                            value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline=False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "snipe":
            embed = discord.Embed(title="**Snipe Command**",
                                  description="**Usage:** `e!snipe` \n- This will show the last deleted message in the channel.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                  color=0x00FFFF)

            embed.add_field(name="‎",
                            value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline=False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "editsnipe":
            embed = discord.Embed(title="**EditSnipe Command**",
                                  description="**Usage:** `e!editsnipe` \n- This will show the last edited message in the channel.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                  color=0x00FFFF)

            embed.add_field(name="‎",
                            value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline=False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "weather":
            embed = discord.Embed(title = "**Weather Command**",
                                    description = "**Usage:** `e!weather <location>` \n- This will show weather stats for the location.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "howcute":
            embed = discord.Embed(title = "**How Cute Command**",
                                    description = "**Usage:** `e!howcute [user]` \n- This will show the cuteness of the user.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "simpfor":
            embed = discord.Embed(title = "**Simp For Command**",
                                    description = "**Usage:** `e!simpfor <user>` \n- You simped for this user >_<.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "freenitro":
            embed = discord.Embed(title = "**Free Nitro(FAKE) Command**",
                                    description = "**Usage:** `e!freenitro` \n- Bait someone with free nitro fake link and rick roll them.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "selfdestruct":
            embed = discord.Embed(title = "**Self Destruct Command**",
                                    description = "**Usage:** `e!selfdestruct <text channel> <time> <message>` \n- Send a timed message to the desired channel that gets auto deleted after the mentioned time.\n\n**Required User Permissions:** `Manage Server`\n**Required Bot Permissions:** `Send Messages, Manage Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "hentai":
            if ctx.channel.is_nsfw():
                embed = discord.Embed(title = "**Hentai Command**",
                                        description = "**Usage:** `e!hentai` \n- Sends a random hentai image.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                        color = 0x00FFFF)

                embed.add_field(name="‎",
                                  value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                                  inline=False)
                  # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
                embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                await ctx.send("This command can only be used in a NSFW channel.")

        elif category.lower() == "thighs":
            if ctx.channel.is_nsfw():
                embed = discord.Embed(title = "**Thighs Command**",
                                        description = "**Usage:** `e!thighs` \n- Sends a random anime thighs image.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                        color = 0x00FFFF)

                embed.add_field(name="‎",
                                  value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                                  inline=False)
                  # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
                embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                await ctx.send("This command can only be used in a NSFW channel.")

        elif category.lower() == "nekogif":
            if ctx.channel.is_nsfw():
                embed = discord.Embed(title = "**Nekogif Command**",
                                        description = "**Usage:** `e!nekogif` \n- Sends a random nsfw neko gif.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                        color = 0x00FFFF)

                embed.add_field(name="‎",
                                  value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                                  inline=False)
                  # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
                embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                await ctx.send("This command can only be used in a NSFW channel.")

        elif category.lower() == "boobs":
            if ctx.channel.is_nsfw():
                embed = discord.Embed(title = "**Boobs Command**",
                                        description = "**Usage:** `e!boobs` \n- Sends a random boobs image.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                        color = 0x00FFFF)

                embed.add_field(name="‎",
                                  value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                                  inline=False)
                  # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
                embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                await ctx.send("This command can only be used in a NSFW channel.")

        elif category.lower() == "blowjob":
            if ctx.channel.is_nsfw():
                embed = discord.Embed(title = "**Blowjob Command**",
                                        description = "**Usage:** `e!blowjob` \n- Sends a random blowjob image/gif.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                        color = 0x00FFFF)

                embed.add_field(name="‎",
                                  value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                                  inline=False)
                  # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
                embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                await ctx.send("This command can only be used in a NSFW channel.")

        elif category.lower() == "pussy":
            if ctx.channel.is_nsfw():
                embed = discord.Embed(title = "**Pussy Command**",
                                        description = "**Usage:** `e!pussy` \n- Sends a random pussy image/gif.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                        color = 0x00FFFF)

                embed.add_field(name="‎",
                                  value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                                  inline=False)
                  # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
                embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                await ctx.send("This command can only be used in a NSFW channel.")

        elif category.lower() == "spank":
            if ctx.channel.is_nsfw():
                embed = discord.Embed(title = "**Spank Command**",
                                        description = "**Usage:** `e!spank <user>` \n- You spanked the user.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                        color = 0x00FFFF)

                embed.add_field(name="‎",
                                  value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                                  inline=False)
                  # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
                embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
            else:
                await ctx.send("This command can only be used in a NSFW channel.")

        elif category.lower() == "mock":
            embed = discord.Embed(title = "**Mock Command**",
                                    description = "**Usage:** `e!mock <text>` \n- Mock someone.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "embed":
            embed = discord.Embed(title = "**Embed Command**",
                                    description = "**Usage:** `e!embed <#hexcolor> | <title> | <description>` \n- Make an embed from your message.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "aesthetic" or category.lower() == "atc":
            embed = discord.Embed(title = "**Aesthetic Command**",
                                    description = "**Usage:** `e!aesthetic <text> | [mode]` \n- Applies an awesome aesthetic filter to your text 😳.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "connect" or category.lower() == "join":
            embed = discord.Embed(title = "**Connect Command**",
                                    description = "**Usage:** `e!connect` \n- The bot will connect to your voice channel.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "play":
            embed = discord.Embed(title = "**Play Command**",
                                    description = "**Usage:** `e!play <song/url>` \n- The bot will play this song.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "nowplaying":
            embed = discord.Embed(title = "**Nowplaying Command**",
                                    description = "**Usage:** `e!nowplaying` \n- This bot will show the current playing song.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "pause":
            embed = discord.Embed(title = "**Pause Command**",
                                    description = "**Usage:** `e!pause` \n- This will pause the current playing song.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "resume":
            embed = discord.Embed(title = "**Resume Command**",
                                    description = "**Usage:** `e!resume` \n- This will resume the music if it's paused.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "queue":
            embed = discord.Embed(title = "**Queue Command**",
                                    description = "**Usage:** `e!queue` \n- This will show the current queue.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "skip":
            embed = discord.Embed(title = "**Skip Command**",
                                    description = "**Usage:** `e!skip` \n- This will skip the current song.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "stop":
            embed = discord.Embed(title = "**Stop Command**",
                                    description = "**Usage:** `e!stop` \n- This will stop the music and clear the queue.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "volume":
            embed = discord.Embed(title = "**Volume Command**",
                                    description = "**Usage:** `e!volume <amount>` \n- This will change the volume.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`, `Connect`, `Speak`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "nqn":
            embed = discord.Embed(title = "**NQN Command**",
                                    description = "**Usage:** `e!nqn enable/disable` \n- This will enable/disable NQN mode for your server.\n\n**Required User Permissions:** `Manage Server`\n**Required Bot Permissions:** `Send Messages`, `Manage Webhooks`, `Manage Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "hug":
            embed = discord.Embed(title = "**Hug Command**",
                                    description = "**Usage:** `e!hug <user>` \n- You give a warm hug to the user.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "kiss":
            embed = discord.Embed(title = "**Kiss Command**",
                                    description = "**Usage:** `e!kiss <user>` \n- You give a kiss to the user.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "pat":
            embed = discord.Embed(title = "**Pat Command**",
                                    description = "**Usage:** `e!pat <user>` \n- You pat the user.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "slap":
            embed = discord.Embed(title = "**Slap Command**",
                                    description = "**Usage:** `e!slap <user>` \n- Someone's misbehaving? SLAP THEM!.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "tickle":
            embed = discord.Embed(title = "**Tickle Command**",
                                    description = "**Usage:** `e!tickle <user>` \n- Tickle, tickle!\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "randomname":
            embed = discord.Embed(title = "**Randomname Command**",
                                    description = "**Usage:** `e!randomname` \n- Sends a random generated name.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "levels":
            embed = discord.Embed(title = "**Levels Command**",
                                    description = "**Usage:** `e!levels enable/disable` \n- This enables/disables levelling for your server.\n\n**Required User Permissions:** `Manage Server`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "levelupchannel":
            embed = discord.Embed(title = "**Levelupchannel Command**",
                                    description = "**Usage:** `e!levelupchannel <channel>` \n- Changes the level up channel.\n\n**Required User Permissions:** `Manage Server`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "rank":
            embed = discord.Embed(title = "**Rank Command**",
                                    description = "**Usage:** `e!rank [user]` \n- Shows the rank of you or the user mentioned.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        elif category.lower() == "leaderboard":
            embed = discord.Embed(title = "**Leaderboard Command**",
                                    description = "**Usage:** `e!leaderboard` \n- Shows the levels leaderboard for the server.\n\n**Required User Permissions:** `None`\n**Required Bot Permissions:** `Send Messages`",
                                    color = 0x00FFFF)

            embed.add_field(name="‎",
                              value="[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                              inline=False)
              # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

        else:
            await ctx.send("Couldn't find the command.")



def setup(client):
    client.add_cog(Help(client))
