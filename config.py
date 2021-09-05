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

import time
import os

# LOL TOKEN GO BRR
BOT_TOKEN = os.environ.get("TOKEN")  # your discord bot token
BOT_TOKEN_BETA = os.environ.get("TOKEN_BETA")  # the token of the beta bot (optional)

MONGO_DB_URL = os.environ.get("MONGO")  # your mongodb database connection url string
MONGO_DB_URL_BETA = os.environ.get("MONGO_BETA")  # database for the beta bot (optional)
DB_UPDATE_INTERVAL = 60  # the interval at which the database is updated

PREFIX = "e!"  # the default prefix for the bot
OWNERS = [558861606063308822]  # the bot owners
COOLDOWN_BYPASS = [558861606063308822, 344313283714613248, 679677267164921866]  # the users that bypass the cooldown
EPICBOT_GUILD_ID = 746202728031584358  # the id of the epicbot guild
PREMIUM_GUILDS = [746202728031584358, 749996055369875456]  # the ids of the premium guilds (it bypasses some cmd requirements)

# AFK KEYS

UD_API_KEY = os.environ.get("UD_API_KEY")
WEATHER_API_KEY = os.environ.get("WEATHER")
TOP_GG_TOKEN = os.environ.get("SHIT_GG_TOKEN")
TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")
CHAT_BID = os.environ.get("CHAT_BID")
CHAT_API_KEY = os.environ.get("CHAT_API_KEY")
DAGPI_KEY = os.environ.get("DAGPI_KEY")
STATCORD_KEY = os.environ.get("STATCORD_KEY")
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# SECRET LOGS HEHE :3

ONLINE_LOG_CHANNEL = 757168151141285929
SHARD_LOG_CHANNEL = 832645114459324507
ADD_REMOVE_LOG_CHANNEL = 793832499645644800
DATABASE_LOG_CHANNEL = 832645226799300609
COMMANDS_LOG_CHANNEL = 775949886842994698
ERROR_LOG_CHANNEL = 832645286098239488
DM_LOG_CHANNEL = 793482521076695070
BUG_REPORT_CHANNEL = 834665587010568252
RANK_CARD_SUBMIT_CHANNEL = 856512113580703814
SUGGESTION_CHANNEL = 746202728648146986
USER_REPORT_CHANNEL = 863768592159473694

# WEBHOOK LOGS

WEBHOOKS = {
    "startup": (880847339378573403, os.environ.get("startup_webhook")),
    "add_remove": (880847516537585734, os.environ.get("add_remove_webhook")),
    "cmd_uses": (880847705809760276, os.environ.get("cmd_uses_webhook")),
    "cmd_error": (880846787349446778, os.environ.get("cmd_error_webhook")),
    "event_error": (880844779565506601, os.environ.get("event_error_webhook")),
}

# COLORS

# MAIN_COLOR = 0xDC143C # crimson
MAIN_COLOR = 0x459fff  # light blue kinda
RED_COLOR = 0xFF0000
ORANGE_COLOR = 0xFFA500
PINK_COLOR = 0xe0b3c7
PINK_COLOR_2 = 0xFFC0CB
STARBOARD_COLOR = 15655584

# LINK

WEBSITE_LINK = "https://epic-bot.com"
SUPPORT_SERVER_LINK = "https://discord.gg/Zj7h8Fp"
INVITE_BOT_LINK = "https://discord.com/oauth2/authorize?client_id=751100444188737617&scope=bot&permissions=2146958847"
VOTE_LINK = "https://top.gg/bot/751100444188737617/vote"

# ROLES

BOT_MOD_ROLE = 857146993464967169
OWNER_ROLE = 746202728375648267
SUPPORTER_ROLE = 842241145584484362
PARTNER_ROLE = 785404547883204608
STAFF_ROLE = 764425511707344928
BOOSTER_ROLE = 787336331474370563
DESIGN_HELPER_ROLE = 856100670780342272
VIP_ROLE = 746202728031584366

# EMOJIS

BADGE_EMOJIS = {
    "normie": "<:members:853203090001887232>",
    "cutevi": "<:avi:875400894919872562>",
    "bot_mod": "<:certifiedmod:857158455269130242>",
    "owner_of_epicness": "👑",
    "staff_member": "<:staff:857194745289113641>",
    "supporter": "<:Heawt:802801495153967154>",
    "booster": "<:CB_boosting24month:857196485778866177>",
    "partner": "<:DiscordPartnerBG:857195796051132416>",
    "bug_hunter": "<:bughunter:857188620678201375>",
    "elite_bug_hunter": "<:DiscordGoldBug:857188634478641173>",
    "early_supporter": "<:supporter:857190710487154698>",
    "Big_PP": "<a:jerk:857215645431103489>",
    "No_PP": "<:ppgone:857198841320964106>",
    "aw||oo||sh": "<a:PetAwish:819234104817877003>",
    "wendo": "<a:MH_wii_clap:857201084727689246>",
    "cat": "<a:CatRainbowJam:857201249447444530>",
    "best_streamer": "<:RamHeart:851480978668781648>",
    "voter": "<:upvote:857205463350116353>",
    "cutie": "<:mmm:834782050006466590>",
    "helper": "<:thanks:800741855805046815>",
    "savior": "🙏",
    "very_good_taste": "<a:petartorol:857212043375280160>",
    "samsung_girl": "<:catgirlboop:857213250512879626>",
    "love_magnet": "<:love_magnet:857215765043347527>",
    "designer": "🎨",
}
EMOJIS = {
    'heawt': '<:Heawt:802801495153967154> ',
    'loading': '<a:loading:820988150813949982> ',
    'hacker_pepe': '<a:Hackerman:832863861975154698> ',
    # 'tick_yes': '<:tickYes:828260365908836423> ',
    'tick_yes': '<:ok:857098227944652801> ',  # '<a:EpicTik:766172079179169813> ',
    # 'tick_no': '<:tickNo:828262032495214643> ',
    'tick_no': '<:EpicCross:782551854662942741> ',
    'wave_1': '<:CB_wave:835817344172687370> ',
    'shy_uwu': '<:shy_uwu:836452300179374111> ',
    'add': '<:EpicRemove:771674521731989536> ',
    'remove': '<:EpicAdd:771674521471549442> ',
    'pepe_jam': '<a:pepeJAM:836819694002372610> ',
    'pog_stop': '<:PC_PogStop:836870370027503657> ',
    'catjam': '<a:1CatJam:836896091014037555> ',
    'epic_coin': '<:epiccoin:837959671532748830> ',
    'bruh': '<:PogBruh:838345056154812447> ',
    'mmm': '<:mmm:842687641639452673> ',
    'sleepy': '<:CB_sleepy:830641591394893844> ',
    'muted': '<:muted:843472761342132294> ',
    'unmuted': '<:unmuted:843488852063682582> ',
    'reminder': '⏰ ',
    'cool': '<a:cool:844813588476854273> ',
    'settings': '<:settings:825008012867534928> ',
    'settings_color': '<a:settings_color:848495459882237962> ',
    'lb': '<a:leaderboard:850573823677431818> ',
    'poglep': '<:poglep:836173704249344011> ',
    'weirdchamp': '<:WeirdChamp:851062483090800640> ',
    'twitch': '<:twitch:852475334419021835> ',
    'members': '<:members:853203090001887232> ',
    'ramaziHeart': '<:RamHeart:851480978668781648> ',
    'leveling': '<a:leveling:849535096838815775> ',
    'vay': '<:vay:849994877629497365> ',
    'chat': '<:Chat:859651327391170591> ',
    'hu_peng': '<:whopingme:861230622525882378> ',
    'disboard': '<:disboard:861565998510637107> ',
    'online': '<:status_online:862599876741955584> ',
    'idle': '<:status_idle:862600144917364737> ',
    'dnd': '<:status_dnd:862600241851924480> ',
    'arrow': '<:Arrow:869101378822373417> ',
    'reaction': '<:add_reaction:873891867610210304> ',
    'cmd_arrow': '<:join_arrow:876313929402417172> '
}
EMOJIS_FOR_COGS = {
    'actions': '<a:hugs:839739273083224104>',
    'emojis': '<a:cool:844813588476854273>',
    'fun': '<a:laugh:849534486869442570>',
    'games': '🎮',
    'image': '📸',
    'info': '<:info:849534946170241034>',
    'leveling': '<a:leveling:849535096838815775>',
    'misc': '<a:PetEpicBot:797142108611280926>',
    'mod': '🛠️',
    'music': '<a:music:849539543103569941>',
    'nsfw': '🔞',
    'config': '<:settings:825008012867534928>',
    'starboard': '⭐',
    'utility': '🔧',
    'user': '<:EpicMembers:794075799422238720>',
    'notifications': '<:notif:883324701181620304>'
}
CUTE_EMOJIS = [
    "<:shy:844039614032904222>",
    "<:shy_peek:844039614309466134>",
    "<:Shy:851665918236557312>",
    "<:shy2:851666263922966588>",
    "<a:HeartOwO:849179336041168916>",
    "<:Heawt:802801495153967154>",
    "<:UwUlove:836174204108931072>",
    "<:Pikaluv:842981646424473601>",
    "<:mmm:834782050006466590>",
    "<a:kissl:808235261708337182>",
    "<:ur_cute:845151161039716362>",
    "<:thanks:800741855805046815>",
    "<a:hugs:839739273083224104>"
]
THINKING_EMOJI_URLS = [
    'https://cdn.discordapp.com/emojis/862387505852055602.png',
    'https://cdn.discordapp.com/emojis/768302864685727755.png',
    'https://cdn.discordapp.com/emojis/854206416830988318.png',
    'https://cdn.discordapp.com/emojis/853192295277002752.png',
    'https://cdn.discordapp.com/emojis/585956493392871424.png',
    'https://cdn.discordapp.com/emojis/819207595876417546.png'
]

# CREDITS

CREDITS_CONTRIBUTORS = {
    "Mr Potato": ["MrPotato374", "Staff, Supporter, Helper"],
    "ELEXR": ["ELEXR", "Supporter, Helper"],
    "Sengolda": ["Sengolda", "Helper"],
    "TheUndeadBowman": ["TheUndeadBowman", "Staff, Supporter, Helper"],
    "CAT": ["KittyKart", "Supporter, Helper"],
    "Vishal": ["imkrvishal", "Helper"],
    "Crafterzman": ["Craftzman7", "Helper"],
    "Motzumoto": ["Motzumoto", "Helper"],
    "Windows": ["WindowsCmd", "Helper"],
    "Nek": ["NekWasTaken", "Helper"],
}

# PP

BIG_PP_GANG = [558861606063308822, 344313283714613248, 478623992337530883, 541410668117753876]
NO_PP_GANG = [550083219136053259, 729770314388603020]

# SOME RANDOM STUFF

start_time = time.time()
EMPTY_CHARACTER = "‎"

custom_cmds_tags_lemao = """
**User:**
`{user_name}` - The name of the user.
`{user_nickname}` - The nickname of the user.
`{user_discrim}` - The discriminator of the user.
`{user_tag}` - The complete tag of the user. (Eg. Username#0000)
`{user_id}` - The ID of the user.
`{user_mention}` - The mention of the user.
`{user_avatar}` - The avatar of the user.

**Guild:**
`{guild_name}` - The name of the server.
`{guild_id}` - The ID of the server.
`{guild_membercount}` - The membercount of the server.
`{guild_icon}` - The icon URL of the server.
`{guild_owner_name}` - The name of the owner of the guild.
`{guild_owner_id}` - The ID of the owner of the guild.
`{guild_owner_mention}` - The mention of the owner of the guild.

**Invites:**
`{user_invites}` - The invites of the user.
`{inviter_name}` - The name of the inviter who invited the user.
`{inviter_discrim}` - The discriminator of the inviter.
`{inviter_tag}` - The complete tag of the inviter. (Eg. Username#0000)
`{inviter_id}` - The ID of the inviter.
`{inviter_mention}` - The mention of the inviter.
`{inviter_avatar}` - The avatar of the inviter.
`{inviter_invites}` - The invites of the inviter.
"""

ENABLE = ['enable', 'enabled', 'yes', 'true']
DISABLE = ['disable', 'disabled', 'no', 'false']

DEFAULT_WELCOME_MSG = """
{
    "title": "Welcome",
    "description": "Yay! {user_mention} has joined our server!",
    "color": "MAIN_COLOR",
    "footer": {
        "text": "Invited by {inviter_tag}",
        "icon_url": "{inviter_avatar}"
    },
    "thumbnail": "{user_avatar}"
}
"""
DEFAULT_LEAVE_MSG = """
{
    "title": "Sad!",
    "description": "Sad! **{user_tag}** has left us!",
    "color": "RED_COLOR",
    "footer": {
        "text": "Invited by {inviter_tag}",
        "icon_url": "{inviter_avatar}"
    },
    "thumbnail": "{user_avatar}"
}
"""

DEFAULT_TWITCH_MSG = """
Poggers! **{streamer}** is now live! Go check them out! {url}
"""

DEFAULT_LEVEL_UP_MSG = """
Pog! {user_mention} just leveled up to level {level}!
"""

DEFAULT_AUTOMOD_CONFIG = {
    "banned_words": {  # done
        "enabled": False,
        "words": []
    },
    "all_caps": {  # done
        "enabled": False
    },
    "duplicate_text": {  # done
        "enabled": False
    },
    "message_spam": {  # done
        "enabled": False
    },
    "invites": {  # done
        "enabled": False
    },
    "links": {  # done
        "enabled": False,
        "whitelist": []
    },
    "mass_mentions": {  # done
        "enabled": False
    },
    "emoji_spam": {
        "enabled": False
    },
    "zalgo_text": {  # done
        "enabled": False
    },

    "ignored_channels": [],
    "allowed_roles": []
}

DEFAULT_BANNED_WORDS = [
    'nigg', 'n1gg', 'n*gg',
    'cunt', 'bitch', 'dick',
    'pussy', 'asshole', 'b1tch',
    'b!tch', 'b*tch', 'blowjob',
    'cock', 'c0ck', 'faggot',
    'whore', 'negro', 'retard',
    'slut', 'rape', 'n i g g '
]

GLOBAL_CHAT_RULES = """
**Global chat rules:**

- No Racism, Sexism, Homophobia or anything stupid.
- No NSFW messages or pictures or emotes.
- Do not be rude to anyone.
- No spamming.
- No self promo.
- No malicious links.

**If your message has a "❌" reaction added, that means your message was not sent because you broke one of these rules.**

**If you break any of these rules, you WILL get blacklisted and won't be able to use the bot.**
If you see anyone breaking these rules please report them using the `report` command.
"""

ANTIHOIST_CHARS = "!@#$%^&*()_+-=.,/?;:[]{}`~\"'\\|<>"
