import discord
from discord import utils
from discord.ext import commands
from pymongo import MongoClient
import os

conn = MongoClient(os.environ.get("MONGODB_LINK"))
db = conn["EpicBot"]

nqn = db["nqn"]
nqn_block = db["nqn_blocked"]

class NQN(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def nqn(self, ctx, nqn_mode = None):
        if nqn_mode == None:
            await ctx.message.reply(f"Please enter a selection. Usage: `e!nqn enable/disable` to turn if on/off.")
            return
        if nqn_mode.lower() == "enable":
            lol = nqn.find_one({"_id": ctx.guild.id})
            if lol == None:
                nqn.insert_one({"_id": ctx.guild.id})
                await ctx.message.reply(f"NQN mode has now been **enabled** for this server. Please make sure I have **Manage Webhooks** permissions for this server.")
                return
            else:
                await ctx.message.reply(f"NQN mode is already **enabled** for this server. To disable it you can use `e!nqn disable`.")
                return
        if nqn_mode.lower() == "disable":
            lmao = nqn.find_one({"_id": ctx.guild.id})
            if lmao != None:
                nqn.delete_one({"_id": ctx.guild.id})
                await ctx.message.reply(f"NQN mode has now been **disabled** for this server. To enable it you can use `e!nqn enable`.")
                return
            else:
                await ctx.message.reply(f"NQN mode hasn't been enabled for this server. To enable it you can use `e!nqn enable`.")
                return
        else:
            await ctx.send(f"That's not a valid option. Please use it like this: `e!nqn enable/disable`")

    async def getemote(self, arg):
        emoji = utils.get(self.client.emojis, name=arg.strip(":"))

        if emoji is not None:
            if emoji.animated:
                add = "a"
            else:
                add = ""
            return f"<{add}:{emoji.name}:{emoji.id}>"
        else:
            return None

    async def getinstr(self, content):
        ret = []

        spc = content.split(" ")
        cnt = content.split(":")

        if len(cnt) > 1:
            for item in spc:
                if item.count(":") > 1:
                    wr = ""
                    if item.startswith("<") and item.endswith(">"):
                        ret.append(item)
                    else:
                        cnt = 0
                        for i in item:
                            if cnt == 2:
                                aaa = wr.replace(" ", "")
                                ret.append(aaa)
                                wr = ""
                                cnt = 0
                            if i != ":":
                                wr += i
                            else:
                                if wr == "" or cnt == 1:
                                    wr += " : "
                                    cnt += 1
                                else:
                                    aaa = wr.replace(" ", "")
                                    ret.append(aaa)
                                    wr = ":"
                                    cnt = 1

                        aaa = wr.replace(" ", "")
                        ret.append(aaa)
                else:
                    ret.append(item)
        else:
            return content

        return ret

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        kek = nqn.find_one({"_id": message.guild.id})
        if kek == None:
            return

        if ":" in message.content:
            msg = await self.getinstr(message.content)
            ret = ""
            em = False
            smth = message.content.split(":")
            if len(smth) > 1:
                for word in msg:
                    if word.startswith(":") and word.endswith(":") and len(word) > 1:
                        emoji = await self.getemote(word)
                        if emoji is not None:
                            em = True
                            ret += f" {emoji}"
                        else:
                            ret += f" {word}"
                    else:
                        ret += f" {word}"
            else:
                ret += msg

            if em:
                webhooks = await message.channel.webhooks()
                await message.delete()
                webhook = utils.get(webhooks, name = "EpicBot NQN")
                if webhook is None:
                    webhook = await message.channel.create_webhook(name = "EpicBot NQN")

                await webhook.send(ret, username = message.author.name, avatar_url = message.author.avatar_url, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False, replied_user=False))

def setup(client):
    client.add_cog(NQN(client))
