import discord 
import asyncio
from discord.ext import commands 

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount+1)
        msg = await ctx.send(f'{amount} messages deleted.')

        await asyncio.sleep(2)

        new_msg = await ctx.channel.fetch_message(msg.id)
        await new_msg.delete()

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to kick has a higher role than you, so you can't kick them.")
            return

        if int(ctx.author.top_role.position) == int(member.top_role.position):
            await ctx.send(f"The user you are trying to kick has the same role as you, so you can't kick them.")
            return

        await member.kick(reason=reason)
        kick = discord.Embed(title="👢 Member Kicked!", description=f"I have kicked **{member.name}#{member.discriminator}** from this server!", color=0x89CFF0)
        await ctx.send(embed=kick)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to ban has a higher role than you, so you can't ban them.")
            return

        if int(ctx.author.top_role.position) == int(member.top_role.position):
            await ctx.send(f"The user you are trying to ban has the same role as you, so you can't ban them.")
            return

        await member.ban(reason=reason)
        ban = discord.Embed(title="<a:JD_banned:818014712297029643> Member Banned!", description=f"I have banned **{member.name}#{member.discriminator}** from this server!", color=0x89CFF0)
        await ctx.send(embed=ban)
        await member.create_dm()

        if reason == None:
            real_reason = "NONE"
        elif reason != None:
            real_reason = reason

        embed = discord.Embed(title = "🔨  BAN  🔨", description = f"You were banned from `{ctx.guild}`.", color = 0xFF0000)
        embed.add_field(name = "Moderator:", value = ctx.author, inline = False)
        embed.add_field(name = "Reason:", value = real_reason, inline = False)

        try:
            await member.dm_channel.send(embed = embed)
        except:
            await ctx.send("I tried to DM them about then ban but I failed, they have still been banned tho!")

    @commands.command(aliases = ['addrole'])
    @commands.has_permissions(manage_roles = True)
    async def add_role(self, ctx, member: discord.Member, role: discord.Role):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to add role to has a higher role than you, so you can't add this role to them.")
            return

        await member.add_roles(role)
        embed = discord.Embed(title = "Role Added", description = f"Successfully added {role.mention} role to {member.mention}.", color = 0x00FF0C)
        await ctx.send(embed = embed)

    @commands.command(aliases = ['removerole'])
    @commands.has_permissions(manage_roles = True)
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to remove role from has a higher role than you, so you can't remove this role from them.")
            return

        await member.remove_roles(role)
        embed = discord.Embed(title = "Role Removed", description = f"Successfully removed {role.mention} role from {member.mention}.", color = 0xFF0000)
        await ctx.send(embed = embed)

    # @commands.command()
    # @commands.has_permissions(kick_members = True)
    # async def warn(self, ctx, member: discord.Member, *, reason: str = None):
    #
    #     if int(ctx.author.top_role.position) < int(member.top_role.position):
    #         await ctx.send(f"The user you are trying to warn has a higher role than you, so you can't warn them.")
    #         return
    #
    #     if int(ctx.author.top_role.position) == int(member.top_role.position):
    #         await ctx.send(f"The user you are trying to warn has the same role as you, so you can't warn them.")
    #         return
    #
    #     if reason == None:
    #         await member.create_dm()
    #         await member.dm_channel.send(f":warning: **WARNING** :warning: \n\n-You have been warned by a moderator on the server `{ctx.guild}`\n\nReason: `No reason provided.`\nModerator: `{ctx.author.name}#{ctx.author.discriminator}`")
    #         await ctx.send(f":warning: {member.mention} was warned.")
    #         return
    #
    #     await member.create_dm()
    #     await member.dm_channel.send(f":warning: **WARNING** :warning: \n\n-You have been warned by a moderator on the server `{ctx.guild}`\n\nReason: `{reason}`\nModerator: `{ctx.author.name}#{ctx.author.discriminator}`")
    #     await ctx.send(f":warning: {member.mention} was warned.")

    @commands.command(aliases = ['deletechannel', 'delete-channel', 'nukechannel'])
    @commands.has_permissions(manage_channels = True)
    async def delete_channel(self, ctx, channel: discord.TextChannel = None):

        msg = await ctx.send(f"Deleting `{channel}`... <a:EpicLoading1:762919634336088074>")
        await channel.delete()
        await msg.edit(content = f"Deleted `{channel}` <a:EpicTik:766172079179169813>")

    @commands.command(aliases = ['createchannel', 'create-channel'])
    @commands.has_permissions(manage_channels = True)
    async def create_channel(self, ctx, channelName):

        msg = await ctx.send(f"Creating `{channelName}`... <a:EpicLoading1:762919634336088074>")
        await ctx.guild.create_text_channel(name = channelName)
        await msg.edit(content = f"Created `{channelName}` <a:EpicTik:766172079179169813>")

    @commands.command(aliases = ['changenick', 'nickname'])
    @commands.has_permissions(manage_nicknames = True)
    async def nick(self, ctx, member: discord.Member = None, *,nickname):

        old_nick = member.nick
        await member.edit(nick = f"{nickname}")
        new_nick = member.nick
        await ctx.send(f"{member.mention}'s nickname changed from `{old_nick}` to `{new_nick}` <a:EpicTik:766172079179169813>")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} was unbanned.')
                return

    @nick.error
    async def nick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @create_channel.error
    async def create_channel_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @delete_channel.error
    async def delete_channel_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    # @warn.error
    # async def warn_error(self, ctx, error):
    #     if isinstance(error, commands.CommandInvokeError):
    #         await ctx.send(f"An error occured. The user you are trying to warn either has their DMs closed or they have blocked me. Please try again later.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @add_role.error
    async def add_role_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @remove_role.error
    async def remove_role_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I don't think i have enough permissions to execute this task.")

def setup(client):
    client.add_cog(Moderation(client))
