"""
Copyright 2021 Nirlep_5252_

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import discord
import random
import time

from discord.ext import commands, tasks
from config import CUTE_EMOJIS, EPICBOT_GUILD_ID
from utils.ui import Paginator
from utils.embed import success_embed
from utils.bot import EpicBot


class VoteTracking(commands.Cog):
    def __init__(self, client: EpicBot):
        self.client = client
        self.vote_tracking_bot_id = 891172840181743697
        self.vote_scraping_channel_id = 851658500118413313
        self.vote_sending_channel_id = 776015595354325002
        self.default_vote_dict = {
            "top.gg": 0,
            "bots.discordlabs.org": 0,
            "reminders": False,
            "last_voted": {}
        }
        self.roles = {
            10: 780047658861199390,
            20: 780047650556215296,
            30: 780047640208998451,
            40: 780047631442903091,
            50: 780047621640683521
        }
        self.top_voter = 780047611105247252
        self.voter_role = 764479085392297984
        self.remove_voter_role.start()
        self.update_top_voters.start()

    @commands.command()
    @commands.is_owner()
    async def vote_lb(self, ctx: commands.Context):
        """Shows the top 10 voters."""
        all_vote_dicts = [e.copy() for e in self.client.user_profile_cache if "votes" in e]
        sorted_voters = sorted(all_vote_dicts, key=lambda x: sum(list(x['votes'].values())[0:2]), reverse=True)
        paginator = commands.Paginator(prefix='', suffix='', max_size=500)
        for i, e in enumerate(sorted_voters):
            paginator.add_line(f"`{i + 1}.` <@{e['_id']}> - `{sum(list(e['votes'].values())[0:2])}`")
        embeds = [success_embed("Vote Leaderboard", page
                    ).set_author(name=self.client.user, icon_url=self.client.user.display_avatar.url
                    ).set_footer(text=f"{len(sorted_voters)} total voters", icon_url=self.client.user.display_avatar.url)
                for page in paginator.pages]
        view = Paginator(ctx, embeds) if len(embeds) > 1 else None
        await ctx.reply(embed=embeds[0], view=view)

    @commands.Cog.listener("on_message")
    async def haha_vot_go_brr(self, message: discord.Message):
        if message.author.id != self.vote_tracking_bot_id:
            return
        if message.channel.id != self.vote_scraping_channel_id:
            return
        if len(message.embeds) != 1:
            return
        embed = message.embeds[0]
        desc = embed.description
        web = 'top.gg' if 'top.gg' in desc else 'bots.discordlabs.org'
        try:
            voter_id = int(desc[2:20])
            usr_profile = await self.client.get_user_profile_(voter_id)
            vote_dict = usr_profile.get("votes", self.default_vote_dict)
            votes = vote_dict[web]
            votes += 1
            vote_dict[web] = votes
            last_voted = vote_dict['last_voted']
            last_voted[web] = int(message.created_at.timestamp())
            usr_profile["votes"] = vote_dict

            channel = self.client.get_channel(self.vote_sending_channel_id)
            await channel.send(
                f"Thank you <@{voter_id}> for voting me! UwU~ {random.choice(CUTE_EMOJIS)}\nYou have a total of **{sum(list(vote_dict.values())[0:2])}** votes now! {random.choice(CUTE_EMOJIS)}",
                allowed_mentions=discord.AllowedMentions(
                    users=True,
                    everyone=False,
                    roles=False,
                    replied_user=False
                )
            )

            member = channel.guild.get_member(voter_id)
            if member is not None:
                await self.update_roles(member, sum(list(vote_dict.values())[0:2]))
            user = self.client.get_user(voter_id)
            if user is not None:
                await self.send_thank_you(user, web, votes)
        except Exception as e:
            print(e)

    async def update_roles(self, member: discord.Member, votes: int, remove_voter_role: bool = False) -> None:
        """Updates user roles based on current vote count."""
        roles_to_add = []
        roles_to_remove = []
        voter_role = member.guild.get_role(self.voter_role)
        if remove_voter_role:
            roles_to_remove.append(voter_role)
        else:
            roles_to_add.append(voter_role)
        for num, role_id in self.roles.items():
            role = member.guild.get_role(role_id)
            if role is not None:
                if votes >= num:
                    roles_to_add.append(role)
                else:
                    roles_to_remove.append(role)
        await member.add_roles(*roles_to_add, reason='vot go br')
        await member.remove_roles(*roles_to_remove, reason='vot go br')

    async def send_reminder(self, user: discord.User, web: str) -> None:
        """Remindes the user to vote again."""
        try:
            await user.send(f"""
It's been 12 hours since you voted me!
I'd appreciate if you voted me again!

- https://{web}/bot/{self.client.user.id}/vote

Thanks a lot for your support! {random.choice(CUTE_EMOJIS)} :kiss:
            """)
        except discord.Forbidden:
            pass

    async def send_thank_you(self, user: discord.User, web: str, votes: int) -> None:
        """Sends a thank you message to the user."""
        try:
            await user.send(f"""
Heya! :kiss:

Thanks a lot for voting me on `{web}`!
You have a total of **{votes}** votes now!

Your votes help me a lot and in return I'll give you rewards like:
- Special roles
- Badges
- Access to special commands
- And kisses :kiss:
            """)
        except discord.Forbidden:
            pass

    @tasks.loop(minutes=30)
    async def update_top_voters(self):
        ep = self.client.get_guild(EPICBOT_GUILD_ID)
        if ep is None:
            return
        top_voter = ep.get_role(self.top_voter)
        top = {}
        top1 = 0
        top2 = 0
        top3 = 0
        for up in self.client.user_profile_cache:
            vote_dict = up.get("votes")
            if vote_dict is None:
                continue
            member = ep.get_member(up['_id'])
            if member is None:
                continue
            total_votes = sum(list(vote_dict.values())[0:2])
            if total_votes > top1:
                top3 = top2
                top2 = top1
                top1 = total_votes
                top[top1] = member
            elif total_votes > top2:
                top3 = top2
                top2 = total_votes
                top[top2] = member
            elif total_votes > top3:
                top3 = total_votes
                top[top3] = member
        for mem in top.values():
            await mem.add_roles(top_voter, reason='top voter')

    @tasks.loop(minutes=5)
    async def remove_voter_role(self):
        ep = self.client.get_guild(EPICBOT_GUILD_ID)
        for up in self.client.user_profile_cache:
            vote_dict = up.get("votes")
            if vote_dict is None:
                continue
            user = self.client.get_user(up['_id'])
            if user is None:
                continue
            last_voted = vote_dict['last_voted']
            to_pop = []
            for web, timestamp in last_voted.items():
                if timestamp + 43200 < int(time.time()):
                    to_pop.append(web)
                    if vote_dict['reminders']:
                        await self.send_reminder(user, web)
                    if ep is not None:
                        member = ep.get_member(user.id)
                        if member is not None:
                            await self.update_roles(member, sum(list(vote_dict.values())[0:2]), True)
            for python_is_weird in to_pop:
                del last_voted[python_is_weird]
            vote_dict['last_voted'] = last_voted
            up['votes'] = vote_dict

    def cog_unload(self) -> None:
        self.remove_voter_role.stop()
        self.update_top_voters.stop()


def setup(client):
    client.add_cog(VoteTracking(client))
