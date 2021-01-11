import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logChannel = self.client.get_channel(793832499645644800)

        embed = discord.Embed(title = f"<:EpicAdd:771674521471549442>  EpicBot Removed",
                                # description = f"EpicBot just got removed from `{guild.name} ({guild.id}) (owner: {guild.owner} ({guild.owner_id}))` which had `{len(guild.members)}` members.",
                                color = 0xFF0000)
        embed.add_field(name = "Server:", value = f"{guild.name} ({guild.id})", inline = False)
        embed.add_field(name = "Owner:", value = f"{guild.owner.mention} `{guild.owner} ({guild.owner_id})`", inline = False)
        embed.add_field(name = "Members:", value = f"{len(guild.members)}", inline = False)
        await logChannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logChannel = self.client.get_channel(793832499645644800)

        embed = discord.Embed(title = f"<:EpicRemove:771674521731989536>  EpicBot Added",
                                # description = f"EpicBot just got added to `{guild.name} ({guild.id}) (owner: {guild.owner} ({guild.owner_id}))` which has `{len(guild.members)}` members.",
                                color = 0x00FFFF)
        embed.add_field(name = "Server:", value = f"{guild.name} ({guild.id})", inline = False)
        embed.add_field(name = "Owner:", value = f"{guild.owner.mention} `{guild.owner} ({guild.owner_id})`", inline = False)
        embed.add_field(name = "Members:", value = f"{len(guild.members)}", inline = False)
        await logChannel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        mention = member.mention
        guild = member.guild

        channel_logging = self.client.get_channel(762597664679788575)

        print(f'{member} has joined {guild.name}.')

        embed = discord.Embed(title = "someone joined some server",
                                color = 0x00FFFF)
        embed.add_field(name = "User:", value = f"{member.mention} `{member} ({member.id})`", inline = False)
        embed.add_field(name = "Server:", value = f"{guild.name} ({guild.id})", inline = False)
        embed.add_field(name = "Server Owner:", value = f"{guild.owner.mention} `{guild.owner} ({guild.owner_id})`", inline = False)

        await channel_logging.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        mention = member.mention
        guild = member.guild

        channel_logging = self.client.get_channel(762597664679788575)

        print(f'{member} has left {guild.name}.')

        embed = discord.Embed(title = "someone left some server",
                                color = 0xFF0000)
        embed.add_field(name = "User:", value = f"{member.mention} `{member} ({member.id})`", inline = False)
        embed.add_field(name = "Server:", value = f"{guild.name} ({guild.id})", inline = False)
        embed.add_field(name = "Server Owner:", value = f"{guild.owner.mention} `{guild.owner} ({guild.owner_id})`", inline = False)

        await channel_logging.send(embed=embed)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        channel_logging = self.client.get_channel(775949886842994698)

        embed = discord.Embed(title = "Command Used", color = 0x00FFFF)
        embed.add_field(name = "Command:", value = f"e!{ctx.command.name}", inline = False)
        embed.add_field(name = f"User:", value = f"`{ctx.author} ({ctx.author.id})`", inline = False)
        embed.add_field(name = f"Server:", value = f"{ctx.guild} ({ctx.guild.id})", inline = False)

        await channel_logging.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel
        channel_logging = self.client.get_channel(762597664679788575)
        dm_logging = self.client.get_channel(793482521076695070)
        user = message.author
        guild = message.guild

        if message.author == self.client.user:
            return

        if str(message.channel.type) == "private":
            embed = discord.Embed(title = "📨  New DM", color = 0x00FFFF)
            embed.add_field(name = "User:", value = f"{message.author.mention} `{message.author} ({message.author.id})`", inline = False)
            embed.add_field(name = "Message:", value = message.content, inline = False)

            await dm_logging.send(embed = embed)

def setup(client):
    client.add_cog(Logs(client))
