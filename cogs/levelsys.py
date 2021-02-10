import discord
import os
import time
from discord.ext import commands
from pymongo import MongoClient

cluster = MongoClient(os.environ.get("MONGODB_LINK"))

levelling = cluster["discord"]["levelling"]
guild_levels = cluster["discord"]["guild_levels"]
levels_cooldown = cluster["discord"]["levels_cooldown"]

class LevelSys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def levels(self, ctx, choice = None):
        hmph = guild_levels.find_one({"_id": ctx.guild.id})
        if choice == None:
            await ctx.message.reply("Invalid command usage, please use it like this: `e!levels enable/disable`")
            return
        if choice.lower() == "enable":
            if hmph != None:
                await ctx.message.reply("Levelling system is already **enabled** for this server.")
                return
            guild_levels.insert_one({"_id": ctx.guild.id})
            await ctx.message.reply("Levelling system has now been **enabled** for this server. To configure level up message channel please use `e!levelupchannel <channel>`.")
        elif choice.lower() == "disable":
            if hmph == None:
                await ctx.message.reply("Levelling system is already **disabled** for this server. To enabled it please use `e!levels enable`")
                return
            guild_levels.delete_one({"_id": ctx.guild.id})
            await ctx.message.reply("Levelling system has now been **disabled** for this server. To enable it back you can use `e!levels enable`")
        else:
            await ctx.message.reply("That's an invalid option. Please try again.")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['levelupchannel', 'lvlupchannel'])
    @commands.has_permissions(manage_guild=True)
    async def level_up_channel(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            await ctx.message.reply("You didn't mention a channel. Please try again.")
            return
        hmmm_yes = guild_levels.find_one({"_id": ctx.guild.id})
        if hmmm_yes == None:
            await ctx.message.reply("Levels have not been enabled for this server yet. Please use `e!levels enable`.")
            return
        guild_levels.update_one(
            {"_id": ctx.guild.id},
            {"$set": {"channel_id": channel.id}}
        )
        await ctx.message.reply(f"The level up channel has now been set to {channel.mention}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        eeee = guild_levels.find_one({"_id": message.guild.id})
        if eeee == None:
            return
        stats = levelling.find_one({"id": message.author.id, "guild_id": message.guild.id})
        if not message.author.bot:



            lolol = levels_cooldown.find_one({"id": message.author.id, "guild_id": message.guild.id})

            if lolol != None:
                xd = time.time() - lolol["time"]
                if xd < 15:
                    return
                else:
                    levels_cooldown.update_one(
                        {"id": message.author.id, "guild_id": message.guild.id},
                        {"$set": {"time": time.time()}}
                    )

            if lolol == None:
                levels_cooldown.insert_one({"id": message.author.id, "guild_id": message.guild.id, "time": time.time()})



            if stats is None:
                newuser = {"id": message.author.id, "guild_id": message.guild.id, "xp": 25}
                levelling.insert_one(newuser)
            else:
                xp = stats["xp"] + 5
                levelling.update_one({"id": message.author.id, "guild_id": message.guild.id}, {"$set": {"xp": xp}})
                lvl = 0
                while True:
                    if xp < ((50*(lvl**2)) + (50*(lvl))):
                        break
                    lvl += 1
                xp -= ((50*((lvl - 1)**2)) + (50*(lvl - 1)))
                if xp == 0:
                    try:
                        level_up_channel = self.client.get_channel(eeee["channel_id"])
                        await level_up_channel.send(f"Pog! {message.author.mention} has levelled up to **level {lvl}**")
                    except:
                        await message.channel.send(f"Pog! {message.author.mention} has levelled up to **level {lvl}**")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def rank(self, ctx, user: discord.Member = None):
        eeee = guild_levels.find_one({"_id": ctx.guild.id})
        if eeee == None:
            await ctx.message.reply("Levels have not been enabled in this server yet!")
            return
        if user == None:
            user = ctx.author
        stats = levelling.find_one({"id": user.id, "guild_id": ctx.guild.id})
        if stats is None:
            embed = discord.Embed(
                description = "That user hasn't sent any messages yet, they are not ranked!",
                color = 0xFF0000
            )
            await ctx.message.reply(embed = embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50 * (lvl ** 2)) + (50 * (lvl))):
                    break
                lvl += 1
            xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
            boxes = int((xp/(200*((1/2) * lvl)))*20)
            ranking = levelling.find({"guild_id": ctx.guild.id}).sort("xp", -1)
            for x in ranking:
                rank += 1
                if stats["id"] == x['id']:
                    break
            embed = discord.Embed(
                title = "{}'s level stats".format(ctx.author.name),
                color = 0x00FFFF
            )
            embed.add_field(name="Name", value=ctx.author.mention, inline = True)
            embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline = True)
            embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline = True)
            embed.add_field(name="Level", value=lvl, inline = True)
            embed.add_field(name="Progress Bar [lvl]", value=boxes*":blue_square:" + (20-boxes)*":white_large_square:", inline = False)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.message.reply(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['lb'])
    async def leaderboard(self, ctx):
        eeee = guild_levels.find_one({"_id": ctx.guild.id})
        if eeee == None:
            await ctx.message.reply("Levels have not been enabled in this server yet!")
            return
        rankings = levelling.find({"guild_id": ctx.guild.id}).sort("xp", -1)
        i = 1
        embed = discord.Embed(title = "Rankings:", color = 0x00FFFF)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                tempxp = x["xp"]
                templvl = 0
                while True:
                    if tempxp < ((50 * (templvl ** 2)) + (50 * (templvl))):
                        break
                    templvl += 1
                tempxp -= ((50 * ((templvl - 1) ** 2)) + (50 * (templvl - 1)))
                embed.add_field(name=f"{i}: {temp.name}#{temp.discriminator}", value = f"XP: {tempxp}/{int(200*((1/2)*templvl))}\nLevel: {templvl}", inline = False)
                i += 1
            except:
                pass
            if i == 11:
                break
        await ctx.message.reply(embed=embed)


def setup(client):
    client.add_cog(LevelSys(client))