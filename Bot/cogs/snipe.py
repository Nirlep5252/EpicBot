import discord
from discord.ext import commands


class Snipe(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.sniped_messages = {}
        self.client.edit_sniped_messages = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        self.client.sniped_messages[message.guild.id, message.channel.id] = (
            message.content, message.author, message.channel.name,
            message.created_at, message.attachments)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        self.client.edit_sniped_messages[before.guild.id, before.channel.id] = (
                                                before.content,
                                                after.content,
                                                before.author,
                                                before.channel.name
                                                )

    @commands.command(aliases=['s'])
    async def snipe(self, ctx):
        try:
            contents, author, channel_name, time, attachments = self.client.sniped_messages[
                ctx.guild.id, ctx.channel.id]
            
            files = ""
            for file in attachments:
                files += f"[{file.filename}]({file.proxy_url})" + "\n"
            embed = discord.Embed(
                description=contents, color=0x00FFFF, timestamp=time)
            embed.set_author(
                name=f"{author.name}#{author.discriminator}",
                icon_url=author.avatar_url)
            embed.add_field(
                name="Attachments",
                value=files[:-1] if len(attachments) != 0 else "None"
            )
            embed.set_footer(text=f"Deleted in #{channel_name}")

            await ctx.send(embed=embed)
        except:
            await ctx.send("No messages were deleted here.")

    @commands.command(aliases = ['es'])
    async def editsnipe(self, ctx):
        try:
            before_content, after_content, author, channel_name = self.client.edit_sniped_messages[ctx.guild.id, ctx.channel.id]

            embed = discord.Embed(description = f"**Before:**\n{before_content}\n\n**After:**\n{after_content}", color=0x00FFFF)
            embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
            embed.set_footer(text=f"Edited in #{channel_name}")

            await ctx.send(embed=embed)
        except:
            await ctx.send("No messages were edited here.")


def setup(client):
    client.add_cog(Snipe(client))
