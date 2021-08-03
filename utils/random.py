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

import random

from discord.ext import commands

letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
characters = "!@#$%&amp;*"
numbers = "1234567890"
email_fun = [
    '69420', '8008135', 'eatsA$$', 'PeekABoo',
    'TheShire', 'isFAT', 'Dumb_man', 'Ruthless_gamer',
    'Sexygirl69', 'Loyalboy69', 'likesButts'
]
passwords = [
    'animeislife69420', 'big_awoogas', 'red_sus_ngl',
    'IamACompleteIdiot', 'YouWontGuessThisOne',
    'yetanotherpassword', 'iamnottellingyoumypw',
    'SayHelloToMyLittleFriend', 'ImUnderYourBed',
    'TellMyWifeILoveHer', 'P@$$w0rd', 'iLike8008135', 'IKnewYouWouldHackIntoMyAccount',
    'BestPasswordEver', 'JustARandomPassword', 'VoteEpicBotUwU'
]
DMs = [
    "send nudes please", "i invited epicbot and i got a cookie",
    "i hope my mum doesn't find my nudes folder",
    "please dont bully me", "https://youtu.be/oHg5SJYRHA0",
    "i like bananas", "i use discord in light mode",
    "if you are reading this u shud vote epicbot", "send feet pics when",
    "sUbScRiBe To mY yOuTuBe ChAnNeL", "the impostor is sus", "python makes me horny"
]
discord_servers = [
    "Sons of Virgins", "Small Benis Gang", "Gamers United",
    "Anime Server 69420", "Cornhub", "Femboy Gang"
]


def gen_random_string(l_: int):
    uwu = ""
    for i in range(l_ + 1):
        uwu += random.choice((letters + numbers))
    return uwu


async def send_random_tip(ctx: commands.Context, msg: str, chances: int):
    if random.randint(1, chances) == chances:
        return await ctx.send(f"**Pro Tip:** {msg}")
    else:
        pass
