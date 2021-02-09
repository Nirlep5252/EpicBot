import discord
import datetime
import requests
import typing as t
from typing import Optional
from discord.ext import commands
from discord import Member

class Info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['guildinfo', 'server_info', 'guild_info'])
    async def serverinfo(self, ctx):

        embed = discord.Embed(title = f"Server Information about **{ctx.guild}**", color = 0x00FFFF)
        embed.set_author(name = ctx.guild, icon_url = ctx.guild.icon_url)
        # embed.set_thumbnail(url = ctx.guild.icon_url)
        embed.add_field(name = "<:EpicOwner:794075390980653106>  Owner:", value = f"{ctx.guild.owner.mention}", inline = True)
        embed.add_field(name = "🌏  Region:", value = f"{str(ctx.guild.region).title()}", inline = True)
        embed.add_field(name = "⏰  Created At:", value = ctx.guild.created_at.strftime("%d/%m/%y | %H:%M:%S"), inline = True)
        embed.add_field(name = "<:EpicMembers:794075799422238720>  Members:", value = len(ctx.guild.members), inline = True)
        embed.add_field(name = "👨  Humans:", value = len(list(filter(lambda m: not m.bot, ctx.guild.members))), inline = True)
        embed.add_field(name = "🤖  Bots:", value = len(list(filter(lambda m: m.bot, ctx.guild.members))), inline = True)
        embed.add_field(name = "<:EpicTextChannel:794076501208465469>  Text Channels:", value = f"{len(ctx.guild.text_channels)}", inline = True)
        embed.add_field(name = "<:EpicVoiceChannel:794076949541814302>  Voice Channels:", value = len(ctx.guild.voice_channels), inline = True)
        try:
            embed.add_field(name = "💤  AFK Channel", value = ctx.guild.afk_channel, inline = True)
            embed.add_field(name = "💤  AFK Timeout", value = f"{ctx.guild.afk_timeout}s", inline = True)
            embed.add_field(name = "🛡️  Moderation Level:", value = str(ctx.guild.verification_level).title())
            embed.add_field(name = "<:EpicInvite:794081254156140554>  Invites", value = len(await ctx.guild.invites()))
            embed.add_field(name = "<:EpicRules:794079278639349781>  Rules Channel:", value = ctx.guild.rules_channel.mention, inline = True)
        except:
            pass
        try:
            embed.add_field(name = "🟠  Roles", value = len(ctx.guild.roles), inline = True)
        except:
            pass
        try:
            embed.add_field(name = "😊  Emojis", value = len(ctx.guild.emojis), inline = True)
        except:
            pass
        embed.add_field(name = "<:EpicBoost:794078431721291797>  Server Boosts", value = ctx.guild.premium_subscription_count, inline = True)
        try:
            embed.add_field(name = "<:EpicBoost:794078431721291797>  Server Boosters", value = len(ctx.guild.premium_subscribers), inline = True)
        except:
            pass
        embed.add_field(name = "🔗  Server Icon", value = f"[Click Here]({ctx.guild.icon_url})", inline = True)
        embed.add_field(name = "🆔  Server ID:", value = f"{ctx.guild.id}", inline = True)

        embed.add_field(name = "‎",
                    value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                    inline = False)
        # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
        embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)

        # embed = discord.Embed(title = "__**Server Information**__", color = 0x00FF0C)
        # embed.set_thumbnail(url = ctx.guild.icon_url)
        # embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
        # embed.timestamp = datetime.datetime.utcnow()
        #
        # fields = [("ID", f"`{ctx.guild.id}`", False),
        #             ("Owner", f"`{ctx.guild.owner}`", True),
        #             ("Region", ctx.guild.region, True),
        #             ("Created At", ctx.guild.created_at.strftime("%d/%m/%y | %H:%M:%S"), True),
        #             ("Members", len(ctx.guild.members), True),
        #             ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
        #             ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
        #             ("Banned Members", len(await ctx.guild.bans()), True),
        #             ("Text Channels", len(ctx.guild.text_channels), True),
        #             ("Voice Channels", len(ctx.guild.voice_channels), True),
        #             ("Categories", len(ctx.guild.categories), True),
        #             ("Roles", len(ctx.guild.roles), True),
        #             ("Invites", len(await ctx.guild.invites()), True),
        #             ("\u200b", "\u200b", True)]
        #
        # for name, value, inline in fields:
        #     embed.add_field(name=name, value=value, inline=inline)
        # await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['profile', 'pfp'])
    async def avatar(self, ctx, target: Optional[Member]):
        target = target or ctx.author

        embed = discord.Embed(title = f"**Avatar of {target.name}#{target.discriminator}**", color = 0x00FF0C)
        embed.set_image(url = target.avatar_url)
        embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    # @commands.command(aliases = ['memberinfo', 'user_info', 'member_info'])
    # async def userinfo(self, ctx, target: Optional[Member]):
    #     target = target or ctx.author

    #     embed = discord.Embed(title = "__**User Information**__", color = 0x00FF0C)
    #     embed.set_thumbnail(url = target.avatar_url)
    #     embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
    #     embed.timestamp = datetime.datetime.utcnow()

    #     fields = [("ID", f"`{target.id}`", False),
    #                 ("Username", f"`{str(target)}`", True),
    #                 ("Top Roles", target.top_role.mention, True),
    #                 ("Server Boosts", bool(target.premium_since), False),
    #                 ("Status", str(target.status).title(), False),
    #                 ("Created At", target.created_at.strftime("%d/%m/%y | %H:%M:%S"), False),
    #                 ("Joined At", target.joined_at.strftime("%d/%m/%y | %H:%M:%S"), False)]

    #     for name, value, inline in fields:
    #         embed.add_field(name=name, value=value, inline=inline)

    #     await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def botinfo(self, ctx):
        embed = discord.Embed(title = "**Bot Info**", description = f"I was built by `Nirlep_5252_` on 3rd September. My help command is `e!help`. I am currently in `{len(self.client.guilds)}` servers, and i have more than `{len(set(self.client.get_all_members()))}` users. I have a total of `98` commands.", color = 0x00FFFF)
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/757168151141285929/763336446328438784/bot_profile.png')
        embed.add_field(name = "**Invite EpicBot**",
                        value = f"[Click Here](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847)",
                        inline = True)
        embed.add_field(name = "**Support Server**",
                        value = f"[Click Here](https://discord.gg/Zj7h8Fp)",
                        inline = True)
        embed.add_field(name = "**Bug Report**",
                        value = f"[Click Here](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo/edit?usp=sharing)",
                        inline = True)
        embed.add_field(name = "**Vote EpicBot**",
                        value = f"[Click Here](https://botrix.cc/vote/751100444188737617/)",
                        inline = True)
        embed.add_field(name = "**Our Website**",
                        value = f"[Click Here](https://epicbot.gq)",
                        inline = True)
        embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def vote(self, ctx):
        # try:
        #     url = "https://botrix.cc/api/v1/bot/751100444188737617"

        #     response = requests.get(url)

        #     votes = response.json()
        #     vote_count = votes['bot']['votes']
        # except:
        #     pass

        try:
            eeee = requests.get("https://top.gg/api/bots/751100444188737617").json()
            vote_count = eeee['points']
            monthly_vote_count = eeee['monthlyPoints']
        except Exception as e:
            print(e)

        embed = discord.Embed(title = "**<:EpicVote:779977591292952576>  Vote EpicBot**",
                                description = f"Voting EpicBot supports us.\nThanks for voting us and bringing us where we are now.\n\n",
                                color = 0x00FFFF)
        embed.add_field(name = "**Vote**",
                        value=f"**[Click Here](https://top.gg/bot/751100444188737617/vote)** to vote.",
                        inline = False)
        try:
            embed.add_field(name = "**Total Votes**",
                            value = f"\> {vote_count}",
                            inline = False)
            embed.add_field(name = "**Monthly Votes**",
                            value = f"\> {monthly_vote_count}",
                            inline = False)
        except:
            embed.add_field(name = "**Total Votes**",
                            value = f"An error occured.",
                            inline = False)

        embed.add_field(name = "‎",
                        value = "[Invite Bot](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847) | [Discord Server](https://discord.gg/Zj7h8Fp) | [Bug Report](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo)",
                        inline = False)
        # embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/749996055369875459/771644964542349322/bot_profile.png")
        embed.set_footer(text=f"{ctx.author.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['role-info', 'role_info'])
    async def roleinfo(self, ctx, role: discord.Role):
        embed = discord.Embed(
            title = f"**Role Information**",
            color = role.colour)
        embed.add_field(name = "ID:", value = f"{role.id}", inline = False)
        embed.add_field(name = "Name:", value = f"{role.name}", inline = False)
        embed.add_field(name = "Position:", value = f"{role.position}", inline = False)
        embed.add_field(name = "Created At:", value = f"{role.created_at.strftime('%I : %M : %S %p')} | {role.created_at.day} / {role.created_at.month} / {role.created_at.year}", inline = False)
        embed.add_field(name = "Hoisted:", value = f"{bool(role.hoist)}")
        embed.add_field(name = "Members with this role:", value = f"{role.members}", inline = False)
        embed.add_field(name = "Permissions:", value = f"{role.permissions}", inline = False)
        embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def invite(self, ctx):
        try:

            # \nTo invite EpicBot [Click Here](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847)

            url = "https://api.statcord.com/v3/751100444188737617"
            response = requests.get(url)
            yes = response.json()

            embed = discord.Embed(
                title = 'Invite EpicBot',
                description = f"EpicBot is currently in `{len(self.client.guilds)}` Servers and has over `{yes['data'][0]['users']}` Users.",
                color = 0x00FFFF
            )
            embed.add_field(name = "**Invite**",
                            value = f"**[Click Here](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847)**",
                            inline = False)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/757168151141285929/763336446328438784/bot_profile.png')
            embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(
                title = 'Invite EpicBot',
                description = f"EpicBot is currently in `{len(self.client.guilds)}` Servers and has over `{len(set(self.client.get_all_members()))}` Users.",
                color = 0x00FFFF
            )
            embed.add_field(name = "**Invite**",
                            value = f"**[Click Here](https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847)**",
                            inline = False)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/757168151141285929/763336446328438784/bot_profile.png')
            embed.set_footer(text=f"{ctx.guild}", icon_url=f"{ctx.guild.icon_url}")
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def bug_report(self, ctx):
        user = ctx.author

        embed = discord.Embed(title=str("**Bug Report**"), color=0x00FF0C, description=f"Hey {user.mention}! In order to report a bug [Click Here](https://docs.google.com/forms/d/1PYkQSB0rMSfZePp7o_iqC1cfecnvlys62GGhfHt9OYo/edit?usp=sharing).")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/749996055369875459/751648770185494548/EP2.png")
        embed.add_field(name = "**Support Server**", value = f"You should join out [Support Server](https://discord.gg/Zj7h8Fp) if you need help.")
        embed.set_footer(text=f"{user.guild}", icon_url=f"{user.guild.icon_url}")
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['discord'])
    async def support(self, ctx):
        embed = discord.Embed(title = "<:EpicDiscord:770889292746194964>  Support Server", description = f"Hey {ctx.author.mention}! You can join our discord support server by [Clicking Here](https://discord.gg/Zj7h8Fp), OR by using this link - https://discord.gg/Zj7h8Fp", color = 0x008080)
        embed.set_footer(text = f"{ctx.author.guild}", icon_url = ctx.author.guild.icon_url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)
def setup(client):
    client.add_cog(Info(client))
