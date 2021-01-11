import discord
import datetime
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['test'])
    async def ping(self, ctx):
        await ctx.message.reply(f'Latency: {round(self.client.latency * 1000)}ms')

    @commands.command()
    async def help(self, ctx, *, category = None):
        if category == None:
            embed = discord.Embed(title = "**All Commands(76)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "🔧 • Utility(12)",
                            value = f"Type `e!help utility` for more info.```\n❔-Prefix\n⛅-Weather\n😵-SelfDestruct\n📢-Announce\n🎉-Giveaway\n📑-Translate\n📊-Poll\n⏰-Countdown\n🔗-Create Invite\n🟠-Coin Flip\n🔢-Random Number\n🎲-Dice\n```",
                            inline = True)
            embed.add_field(name = "🛠️ • Moderation(10)",
                            value = f"Type `e!help moderation` for more info.```\n⚠️-Warn\n⚠ - Warnings\n🔨-Ban\n⛏️-Kick\n🍀-Unban\n🔴-Clear\n❌-Delete Channel\n✅-Create Channel\n➕-Add Role\n➖-Remove Role\n```",
                            inline = True)
            embed.add_field(name = "😀 • Fun(14)",
                            value = f"Type `e!help fun` for more info.```\n😂-Freenitro\n🔫-Snipe\n🔫-EditSnipe\n😊-Howcute\n😍-Simpfor\n😊-OWO\n💻-Hack\n😂-Dad Joke\n🤣-Meme\n📜-Quote\n👩‍🏫-Advice\n🗣️-Say\n💬-Ascii\n🕵️‍♀️-Predict\n```",
                            inline = True)
            embed.add_field(name = "💸 • Economy(10)",
                            value = f"Type `e!help economy` for more info.```\n💰-Balance\n👜-Inventory\n🏪-Shop\n🎰-Slots\n🛒-Buy\n🛍️-Sell\n💱-Withdraw\n💱-Deposit\n🎁-Give\n🙏-Beg\n```",
                            inline = True)
            embed.add_field(name = "🖼️ • Image(12)",
                            value = f"Type `e!help image` for more info.```\n🐱-Cat\n🐶-Dog\n🦊-Fox\n🔥-Burn\n🚮-Trash\n😡-Angry\n📚-Fact\n🧠-Illness\n😱-Shock\n🗡️-Wanted\n🤗-Hug\n🥰-Anime\n```",
                            inline = True)
            embed.add_field(name = "ℹ️ • Info(5)",
                            value = f"Type `e!help info` for more info.```\n🦠-Covid-19\n👥-UserInfo\n📈-ServerInfo\n🤖-BotInfo\n🖼️-Avatar\n```",
                            inline = True)
            embed.add_field(name = "🤖 • Bot(8)",
                            value = f"Type `e!help bot` for more info.```\n✅-Help\n📈-Stats\n⬆️-Uptime\n❤️-Invite\n🔼-Vote\n🔗-Discord\n👤-Privacy\n🐞-Bug Report\n```",
                            inline = True)
            embed.add_field(name = "🎮 • Games(2)",
                            value = f"Type `e!help games` for more info.```\n✅-Tic-Tac-Toe\n📃-Rock-Paper-Scissors\n```",
                            inline = True)
            if ctx.channel.is_nsfw():
                embed.add_field(name = "🔞 • NSFW(3)",
                                value = "Type `e!help nsfw` for more info.```🤤-Hentai\n😋-Thighs\n🥰-Nekogif```",
                                inline = True)
            else:
                embed.add_field(name = "🔞 • NSFW(3)",
                                value = "Type `e!help nsfw` for more info.```Will only be shown in a NSFW channel.```",
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
                    title = "**NSFW Commands(3)**",
                    description = "To get detailed help for a command, do `e!help [command]`.",
                    color = 0x00FFFF
                )

                embed.add_field(
                    name = "🤤 - Hentai",
                    value = "Usage: `e!hentai`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                    inline = False
                )

                embed.add_field(
                    name = "😋 - Thighs",
                    value = "Usage: `e!thighs`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                    inline = False
                )

                embed.add_field(
                    name = "🥰 - Nekogif",
                    value = "Usage: `e!nekogif`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                    inline = False
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

        elif category.lower() == "utility" or category.lower() == "utils" or category.lower() == "util":
            embed = discord.Embed(title = "**Utility Commands(8)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "⛅ - Weather", value = "Usage: `e!weather <location>`\nRequired User Permissions: `None`\nReqiured Bot Permissions: `Send Messages`", inline = False)
            embed.add_field(name = "😵 - SelfDestruct", value = "Usage `e!selfdestruct <text channel> <time> <message>`\nRequired User Permissions: `Manage Server`\nRequired Bot Permissions: `Send Messages`", inline = False)
            embed.add_field(name = "📢 - Announce", value = "Usage: `e!announce`\nRequired User Permissions: `Manage Server`\nRequired Bot Permissions: `Send Messages`", inline = False)
            embed.add_field(name = "🎉 - Giveaway", value = "Usage: `e!giveaway`\nRequired User Permissions: `Manage Server`\nRequired Bot Permissions: `Send Messages`, `Add Reactions`", inline = False)
            embed.add_field(name = "📑 - Translate", value = "Usage: `e!translate [language] [text]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`", inline = False)
            embed.add_field(name = "📊 - Poll", value = "Usage: `e!poll [topic] [option1] [option2] [option3]...`\nRequired User Permissions: `Manage Server`\nRequired Bot Permissions: `Send Messages`, `Add Reactions`", inline = False)
            embed.add_field(name = "⏰ - Countdown", value = "Usage: `e!countdown`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`", inline = False)
            embed.add_field(name = "🔗 - Create Invite", value = "Usage: `e!create_invite`\nRequired User Permissions: `Create Invites`\nRequired Bot Permissions: `Create Invites`", inline = False)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "moderation" or category.lower() == "mod" or category.lower() == "admin":
            embed = discord.Embed(title = "**Moderation Commands(10)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "🔴 - Clear",
                            value = "Usage: `e!clear [amount]`\nRequired User Permissions: `Manage Messages`\nRequired Bot Permissions: `Send Messages, Manage Messages`",
                            inline = False)
            embed.add_field(name = "⛏️ - Kick",
                            value = "Usage: `e!kick [user] [reason(optional)]`\nRequired User Permissions: `Kick Members`\nRequired Bot Permissions: `Send Messages, Kick Members`",
                            inline = False)
            embed.add_field(name = "🔨 - Ban",
                            value = "Usage: `e!ban [user] [reason(optional)]`\nRequired User Permissions: `Ban Members`\nRequired Bot Permissions: `Send Messages, Ban Members`",
                            inline = False)
            embed.add_field(name = "🍀 - Unban",
                            value = "Usage: `e!unban [user]`\nRequired User Permissions: `Ban Members`\nRequired Bot Permissions: `Send Messages, Ban Members`",
                            inline = False)
            embed.add_field(name = "⚠️ - Warn",
                            value = "Usage: `e!warn [user] [reason]`\nRequired User Permissions: `Kick Members`\nRequired Bot Permissions: `Send Messages, Kick Members`",
                            inline = False)
            embed.add_field(name = f"⚠  - Warnings",
                            value = f"Usage: `e!warns [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "✅ - Create Channel",
                            value = "Usage: `e!createchannel [name]`\nRequired User Permissions: `Manage Channels`\nRequired Bot Permissions: `Send Messages, Manage Channels`",
                            inline = False)
            embed.add_field(name = "❌ - Delete Channel",
                            value = "Usage: `e!deletechannel [name]`\nRequired User Permissions: `Manage Channels`\nRequired Bot Permissions: `Send Messages, Manage Channels`",
                            inline = False)
            embed.add_field(name = "<:EpicRemove:771674521731989536> - Add Role",
                            value = "Usage: `e!addrole [user] [role]`\nRequired User Permissions: `Manage Roles`\nRequired Bot Permissions: `Send Messages, Manage Roles`",
                            inline = False)
            embed.add_field(name = "<:EpicAdd:771674521471549442> - Remove Role",
                            value = "Usage: `e!removerole [user] [role]`\nRequired User Permissions: `Manage Roles`\nRequired Bot Permissions: `Send Messages, Manage Roles`",
                            inline = False)

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
                            value = "Usage: `e!freenitro`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🔫 - Snipe",
                            value = "Usage: `e!snipe`\nRequired User Permissions: `None`\nReqiured Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🔫 - EditSnipe",
                            value = "Usage: `e!editsnipe`\nRequired User Permissions: `None`\nReqiured Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "😊 - Howcute",
                            value = "Usage: `e!howcute [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "😍 - Simpfor",
                            value = "Usage: `e!simpfor <user>`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "💻 - Hack",
                            value = "Usage: `e!hack [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "😊 - OWO",
                            value = "Usage: `e!owo [text]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "😂 - Dad Jokes",
                            value = "Usage: `e!dadjoke`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🤣 - Meme",
                            value = "Usage: `e!meme`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "👩‍🏫 - Advice",
                            value = "Usage: `e!advice`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🗣️ - Say",
                            value = "Usage: `e!say [text]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "💬 - Ascii",
                            value = "Usage: `e!ascii <text>`\nReqiured User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "📜 - Quote",
                            value = "Usage: `e!quote`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🕵️‍♀️ - Predict",
                            value = "Usage: `e!predict [question]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🎲 - Dice",
                            value = "Usage: `e!dice`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = ":coin: - CoinFlip",
                            value = "Usage: `e!flip`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🔢 - Random Number",
                            value = "Usage: `e!randomnumber [num1] [num2]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)

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
                            value = "Usage: `e!balance`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "👜 - Inventory",
                            value = "Usage: `e!bag`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🏪 - Shop",
                            value = "Usage: `e!shop`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🎰 - Slots",
                            value = "Usage: `e!slots [money]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🛒 - Buy",
                            value = "Usage: `e!buy [item]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🛍️ - Sell",
                            value = "Usage: `e!sell [item]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "💱 - Withdraw",
                            value = "Usage: `e!withdraw [amount]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "💱 - Deposit",
                            value = "Usage: `e!deposit [amount]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🎁 - Give",
                            value = "Usage: `e!give [user] [amount]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🙏 - Beg",
                            value = "Usage: `e!beg`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)

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
                            value = "Usage: `e!cat`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "🐶 - Dog",
                            value = "Usage: `e!dog`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "🦊 - Fox",
                            value = "Usage: `e!fox`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "🥰 - Anime",
                            value = "Usage: `e!anime`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Message, Attach Files`",
                            inline = False)
            embed.add_field(name = "🤗 - Hug",
                            value = "Usage: `e!hug [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "🔥 - Burn",
                            value = "Usage: `e!burn [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "🚮 - Trash",
                            value = "Usage: `e!trash [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "😡 - Angry",
                            value = "Usage: `e!angry [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "📚 - Fact",
                            value = "Usage: `e!fact [text]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "🧠 - Illness",
                            value = "Usage: `e!illness [text]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "😱 - Shock",
                            value = "Usage: `e!shock [text]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)
            embed.add_field(name = "🗡️ - Wanted",
                            value = "Usage: `e!wanted [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "info":
            embed = discord.Embed(title = "**Info Commands(4)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "<:EpicCovid:768701899959697408> - Covid-19",
                            value = "Usage: `e!covid [country]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "👥 - UserInfo",
                            value = "Usage: `e!userinfo [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "📈 - ServerInfo",
                            value = "Usage: `e!serverinfo`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Manage Server, View Audit Log, View Members List`",
                            inline = False)
            embed.add_field(name = "🖼️ - Avatar",
                            value = "Usage: `e!avatar [user]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages, Attach Files`",
                            inline = False)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "bot" or category.lower() == "epicbot":
            embed = discord.Embed(title = "**Bot Commands(10)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "✅ - Help",
                            value = "Usage: `e!help [category/cmd(optional)]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "❔ - Prefix",
                            value = "Usage: `e!prefix [new prefix]`\nRequired User Permissions: `Administrator`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "<:RamHeart:758103228058566656> - Invite",
                            value = "Usage: `e!invite`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "📈 - Stats",
                            value = "Usage: `e!stats`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "⬆️ - Uptime",
                            value = "Usage: `e!uptime`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "⬆️ - Vote",
                            value = f"Usage: `e!vote`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "<:EpicDiscord:770889292746194964> - Discord",
                            value = "Usage: `e!discord`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🤖 - BotInfo",
                            value = "Usage: `e!botinfo`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "👤 - Privacy",
                            value = "Usage: `e!privacy`\nRequired User Permissions: `None`\nReqiured Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "🐞 - Bug Report",
                            value = "Usage: `e!bug_report`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)

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
                            value = "Usage: `e!rps [rock/paper/scissors]`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`",
                            inline = False)
            embed.add_field(name = "✅ - Tic-Tac-Toe",
                            value = "Usage: `e!tictactoe`\nRequired User Permissions: `None`\nRequired Bot Permissions: `Send Messages`, `Add Reactions`, `Manage Messages`",
                            inline = False)

            embed.add_field(name = "‎",
                            value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                            inline = False)
            # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
            embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed = embed)

        elif category.lower() == "music":
            embed = discord.Embed(title = "**Music Commands(0)**",
                                    description = "To get detailed help for a command, do `e!help [command]`.",
                                    color = 0x00FFFF)
            embed.add_field(name = "No music commands are available right now, they will be added soon...",
                            value = "For more info on when they will be added join our [Discord Server](https://discord.gg/Zj7h8Fp).",
                            inline = False)

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

        else:
            await ctx.send("Couldn't find the command.")



def setup(client):
    client.add_cog(Help(client))
