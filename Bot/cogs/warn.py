import discord
import datetime
import time
import os 
from pymongo import MongoClient
from discord.ext import commands

conn = MongoClient(os.environ.get("MONGODB_LINK"))
db = conn["EpicBot"]

warns = db["warns"]

class Warn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def deletewarn(self, ctx, member: discord.Member, *, id = None):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to remove a warn from has a higher role than you, so you can't do that.")
            return

        elif int(ctx.author.top_role.position) == int(member.top_role.position):
            await ctx.send(f"The user you are trying to remove a warn from has a higher role than you, so you can't do that.")
            return

        elif member.bot:
            await ctx.send(f"You can't remove a warn from a bot cmon :joy:")
            return

        elif id == None:
            await ctx.send(f"Please enter a warning ID.")

        else:
            pass

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def warn(self, ctx, member: discord.Member, *, reason = None):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to warn has a higher role than you, so you can't warn them.")
            return

        if int(ctx.author.top_role.position) == int(member.top_role.position):
            await ctx.send(f"The user you are trying to warn has the same role as you, so you can't warn them.")
            return

        if member.bot:
            await ctx.send(f"You can't warn a bot cmon :joy:")
            return

        try:
            if reason == None:
                warnings = warns.find_one({"_id": f"{member.id}, {ctx.guild.id}"})
                if warnings == None:
                    warns.insert_one(
                        {
                            "_id": f"{member.id}, {ctx.guild.id}",
                            "warns": 1
                        }
                    )
                    await member.create_dm()
                    await member.dm_channel.send(
                        f":warning: **WARNING** :warning: \n\n-You have been warned by a moderator on the server `{ctx.guild}`\n\nReason: `No reason provided`\nModerator: `{ctx.author.name}#{ctx.author.discriminator}`")
                    await ctx.send(f":warning: {member.mention} was warned. They now have 1 warnings.")
                else:
                    warns.update_one(
                        {
                            "_id": f"{member.id}, {ctx.guild.id}",
                        },
                        {
                            "$inc": {"warns": 1}
                        }
                    )
                    await member.create_dm()
                    await member.dm_channel.send(
                        f":warning: **WARNING** :warning: \n\n-You have been warned by a moderator on the server `{ctx.guild}`\n\nReason: `No reason provided`\nModerator: `{ctx.author.name}#{ctx.author.discriminator}`")
                    await ctx.send(f":warning: {member.mention} was warned. They now have {warnings['warns'] + 1} warnings.")

            else:
                warnings = warns.find_one({"_id": f"{member.id}, {ctx.guild.id}"})
                if warnings == None:
                    warns.insert_one(
                        {
                            "_id": f"{member.id}, {ctx.guild.id}",
                            "warns": 1
                        }
                    )
                    await member.create_dm()
                    await member.dm_channel.send(
                        f":warning: **WARNING** :warning: \n\n-You have been warned by a moderator on the server `{ctx.guild}`\n\nReason: `{reason}`\nModerator: `{ctx.author.name}#{ctx.author.discriminator}`")
                    await ctx.send(f":warning: {member.mention} was warned. They now have 1 warnings.")
                else:
                    warns.update_one(
                        {
                            "_id": f"{member.id}, {ctx.guild.id}",
                        },
                        {
                            "$inc": {"warns": 1}
                        }
                    )
                    await member.create_dm()
                    await member.dm_channel.send(
                        f":warning: **WARNING** :warning: \n\n-You have been warned by a moderator on the server `{ctx.guild}`\n\nReason: `{reason}`\nModerator: `{ctx.author.name}#{ctx.author.discriminator}`")
                    await ctx.send(f":warning: {member.mention} was warned. They now have {warnings['warns'] + 1} warnings.")
        except:
            await ctx.send(f"I can't send messages to this user, I increased their warnings by one.")

    @commands.command(aliases = ['warnings'])
    async def warns(self, ctx, user: discord.User = None):
        if user == None:
            await ctx.send("Please enter a user.")
        else:
            warnings = warns.find_one({"_id": f"{user.id}, {ctx.guild.id}"})
            if warnings == None:
                await ctx.send(f"This user has no warnings.")
            else:
                await ctx.send(f"This user has {warnings['warns']} warnings.")

    # @warn.error
    # async def warn_error(self, ctx, error):
    #     if isinstance(error, commands.CommandInvokeError):
    #         await ctx.send(f"I can't send messages to this user")

def setup(client):
    client.add_cog(Warn(client))