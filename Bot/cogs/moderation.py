import discord 
import asyncio
from discord.ext import commands 

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount+1)
        msg = await ctx.send(f'{amount} messages deleted.')

        await asyncio.sleep(2)

        new_msg = await ctx.channel.fetch_message(msg.id)
        await new_msg.delete()

    @commands.cooldown(1, 5, commands.BucketType.user)
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

        embed = discord.Embed(
            title = "👢  Member Kicked!",
            description = f"I have kicked **{member.name}#{member.discriminator}** from this server!",
            color = 0x00FFFF
        )

        # await ctx.send(f':crossed_swords: {member.mention} was kicked.\nReason: {reason}')
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
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

        embed = discord.Embed(
            title = "<:bonk:818034352176103434>  Bonk!",
            description = f"I have yeeted **{member.name}#{member.discriminator}** out of this server! We'll never see them again, Amazing!",
            color = 0x00FFFF
        )

        # await ctx.send(f':hammer: {member.mention} was banned.\nReason: {reason}')
        await ctx.send(embed=embed)

        try:
            await member.create_dm()

            if reason == None:
                real_reason = "None"
            elif reason != None:
                real_reason = reason

            embed = discord.Embed(title = "🔨  BAN  🔨", description = f"You were banned from `{ctx.guild}`.", color = 0xFF0000)
            embed.add_field(name = "Moderator:", value = f"`{ctx.author}`", inline = False)
            embed.add_field(name = "Reason:", value = f"`{real_reason}`", inline = False)

            await member.dm_channel.send(embed = embed)
        except:
            await ctx.send(f"After banning them I tried to DM them but they have their DMs off or something so I wasn't able to DM them. They are still banned tho :D")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['addrole'])
    @commands.has_permissions(manage_roles = True)
    async def add_role(self, ctx, member: discord.Member, role: discord.Role):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to add role to has a higher role than you, so you can't add this role to them.")
            return

        await member.add_roles(role)
        embed = discord.Embed(title = "Role Added", description = f"Successfully added {role.mention} role to {member.mention}.", color = 0x00FF0C)
        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['removerole'])
    @commands.has_permissions(manage_roles = True)
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):

        if int(ctx.author.top_role.position) < int(member.top_role.position):
            await ctx.send(f"The user you are trying to remove role from has a higher role than you, so you can't remove this role from them.")
            return

        await member.remove_roles(role)
        embed = discord.Embed(title = "Role Removed", description = f"Successfully removed {role.mention} role from {member.mention}.", color = 0xFF0000)
        await ctx.send(embed = embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['deletechannel', 'delete-channel', 'nukechannel'])
    @commands.has_permissions(manage_channels = True)
    async def delete_channel(self, ctx, channel: discord.TextChannel = None):

        if channel == None:
            channel = ctx.channel

        msg = await ctx.send(f"Deleting `{channel}`... <a:EpicLoading1:762919634336088074>")
        await channel.delete()
        await msg.edit(content = f"Deleted `{channel}` <a:EpicTik:766172079179169813>")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['createchannel', 'create-channel'])
    @commands.has_permissions(manage_channels = True)
    async def create_channel(self, ctx, channelName = None):

        if channelName == None:
            await ctx.message.reply(f"You didn't mention what name you want the channel to have, please try again.")
            return

        msg = await ctx.send(f"Creating `{channelName}`... <a:EpicLoading1:762919634336088074>")
        await ctx.guild.create_text_channel(name = channelName)
        await msg.edit(content = f"Created `{channelName}` <a:EpicTik:766172079179169813>")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases = ['changenick', 'nickname'])
    @commands.has_permissions(manage_nicknames = True)
    async def nick(self, ctx, member: discord.Member = None, *,nickname):

        old_nick = member.nick
        await member.edit(nick = f"{nickname}")
        new_nick = member.nick
        await ctx.send(f"{member.mention}'s nickname changed from `{old_nick}` to `{new_nick}` <a:EpicTik:766172079179169813>")

    @commands.cooldown(1, 5, commands.BucketType.user)
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
    #lockdown
    @client.command(aliases=['lock'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            E = discord.Embed(description=f"⚠ {channel.mention} on lockdown.")

            await ctx.send(embed= E)
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            E = discord.Embed(description=f"⚠ {channel.mention} on lockdown.")

            await ctx.send(embed= E)
        else:
            E = discord.Embed(description=f"⚠ {channel.mention} is already on lockdown.")

            await ctx.send(embed= E)

    @client.command(aliases=['unlock'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def removelockdown(self,ctx,channel:discord.TextChannel=None):
        channel = channel or ctx.channel

        if channel.overwrites[ctx.guild.default_role].send_messages == False:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            E = discord.Embed(description=f"⚠ Removed lockdown from {channel.mention}")

            await ctx.send(embed= E)
        elif channel.overwrites[ctx.guild.default_role].send_messages == None or channel.overwrites[ctx.guild.default_role].send_messages == True:
            E = discord.Embed(description=f"⚠ The specified channel {channel.mention} is already open.\n Please run another command specifying the channel to remove lockdown.")

            await ctx.send(embed= E)
        else:
            return()            
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
