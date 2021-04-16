# when u add a new cmd you will need to update the following things:
#   - add it in its correct category dict and its desc
#   - add it in the emoji category dict
#   - add it in the all_cmds dict

# when u add a new category you will need to update the following things:
#   - add it in the cmd_categories and help_categories
#   - make a new dict with the name of the new category
#   - make a new dict with the emoji name of the new category
#   - make a new title dict for the new category

# make sure to vote epicbot uwu | epic-bot.com/vote OwO

MAIN_COLOR = 0x00FFFF
RED_COLOR = 0xFF0000
ORANGE_COLOR = 0xFFA500
PINK_COLOR = 0xe0b3c7
PINK_COLOR_2 = 0xFFC0CB

CHANGE_LOG = """
`-` \🟢 Added new `e!chat` command, chat with me! UwU
`-` \🟢 Added `e!afk` command
`-` \🟢 Added improved Music system \🎶
"""

CONTRIBUTORS = """
- [`Nirlep_5252_`](https://github.com/Nirlep5252) - Owner
- [`TheUndeadBowman`](https://github.com/TheUndeadBowman) - Supporter, Helper
- [`CAT`](https://github.com/KittyKart) - Supporter, Helper
- [`Craftzman7`](https://github.com/Craftzman7) - Helper
- [`Motzumoto`](https://github.com/Motzumoto) - Helper
- [`WindowsCmd`](https://github.com/WindowsCmd) - Supporter, Helper
- [`imkrvishal`](https://github.com/imkrvishal) - Helper
- [`ELEXR`](https://github.com/ELEXR) - Supporter, Helper
- [`Nek`](https://github.com/NekWasTaken) - Retarted idiot 

"""
OTHER_CREDITS = """
- [`Tech-Struck`](https://github.com/FalseDev/Tech-Struck) - Run command
- [`Hexbot`](https://github.com/1Prototype1/HexBot) - Game Commands
"""

cmd_categories = [
  'utility',
  'config',
  'moderation',
  'fun',
  'leveling',
  'music',
  'economy',
  'actions',
  'images',
  'info',
  'bot',
  'games',
  'nsfw',
]

utility = {
  'afk': "Sets you as AFK, so that no one disturbs you while you are gone.",
  'weather': "Find weather info.",
  'define': "Finds the definition for your word in urban dictionary.",
  'run': "Runs your code.",
  'announce': "Make an embedded announement.",
  'giveaway': "Start a giveaway.",
  'reroll': "Reroll a giveaway.",
  'translate': "Translate text from any language.",
  'poll': "Start a poll.",
  'countdown': "Start a countdown.",
  'createinvite': "Create an invite instantly that never expires.",
  'embed': "Convert your message into a beautiful customizable embed."
}

config = {
  'serverconfig': "Shows the server configuration for EpicBot",
  'nqn': "Nitro emojis, Without Nitro!",
  'welcome': "Enable/Disable welcome messages for your server.",
  'welcomechannel': "Configure the welcome channel.",
  'autorole': "Enable/Disable autorole for your server.",
  'leavemessage': "Enable/Disable leave messages for your server.",
  'leavechannel': "Configure the leave channel.",
}

moderation = {
  'kick': "Kick a user from the server.",
  'ban': "Ban a user from the server.",
  'unban': "Unban a user from the server.",
  'clear': "Purge messages in a channel.",
  'warn': "Warn someone.",
  'warnings': "Check any users warnings.",
  'deletechannel': "Delete the mentioned channel.",
  'createchannel': "Create a channel.",
  'addrole': "Add a role to user.",
  'removerole': "Remove a role from user."
}

fun = {
  'freenitro': "I'll let you figure this out yourself 😉",
  'snipe': "Snipe the last deleted message.",
  'editsnipe': "Snipe the last edited message.",
  'howcute': "Check howcute someone is, you're pretty cute 😊",
  'howhorny': "Check howhorny someone it.",
  'howgay': "Check how gay someone is.",
  'chat': "Chat with me!",
  'whendie': "Check when someone is gonna die!",
  'simpfor': "Simp for someone.",
  'owo': "OwO",
  'hack': "Hack someone",
  'mock': "Mock someone",
  'aesthetic': "Makes your text look beautiful",
  'dadjoke': "Funny, funny jokes!",
  'meme': "Funny, funny memes!",
  'quote': "A random quote from someone.",
  'advice': "A random advice from someone.",
  'say': "I will repeat what you say.",
  'ascii': "Converts your text into ascii",
  'predict': "I will predict the answer to your question.",
  'randomname': "Gives a random name.",
  'coin': "Flips the coin.",
  'randomnumber': "Get a random number.",
  'dice': "Throw dice."
}

leveling = {
  'levels': "Enable/Disable leveling for your server.",
  'levelupchannel': "Configure the level up channel for your server.",
  'rank': "Check your rank.",
  'leaderboard': "Check the server's leaderboard."
}

music = {
  'join': "I will join your voice channel.",
  'summon': "Make the bot join a specific channel.",
  'play': "I will play music in your ears.",
  'nowplaying': "Shows which song is playing currently.",
  'shuffle': "Shuffles the queue.",
  'pause': "Pauses the music.",
  'resume': "Resumes the music.",
  'queue': "Shows the music queue.",
  'skip': "Vote to skip a song. The requester can automatically skip.",
  'remove': "Removes a song from the queue at a given index.",
  'stop': "Stops the music and clears the queue.",
  'leave': "Clears the queue and leaves the voice channel.",
}

economy = { 
  'balance': "Shows your balanace.",
  'inventory': "Shows your inventory.",
  'shop': "Shows the shop.",
  'slots': "Get a change to win 5x your money or lose it.",
  'buy': "Buy an item from the shop.",
  'sell': "Sell an item from your inventory.",
  'withdraw': "Withdraw some money from your bank.",
  'deposit': "Deposit some money in your bank.",
  'give': "Give some money of yours to someone cute 😊",
  'beg': "Beg for money"
}

images = { 
  'anime': "Gives a random anime picture.",
  'cat': "Gives a random cute cat picture.",
  'dog': "Gives a random cute dog picture.",
  'fox': "Gives a random cute fox picture.",
  'panda': "Gives a random panda picture.",
  'redpanda': "Gives a random redpanda picture.",
  'pikachu': "Gives a random pikachu picture.",
  'comment': "Makes a YouTube comment.",
  'wasted': "The user is wasted (meme)",
  'burn': "Burns the user into ashes.",
  'trash': "Trashes the user.",
  'angry': "The user made someone angry 😬",
  'fact': "Whatever you put here is a fact. Always.",
  'illness': "Your mental illness.",
  'shock': "The reason why ramaziz is shocked 😱",
  'wanted': "The user is wanted.",
}

actions = { 
  'hug': "Hug someone 🤗",
  'cuddle': "Cuddle with someone",
  'kiss': "Kiss someone 💋",
  'bite': "Bite someone OwO",
  'pat': "Pat someone",
  'slap': "Slap someone 🤚",
  'wink': "Wink at someone 😉",
  'tickle': "Tickle someone",
  'facepalm': "Facepalm at someone",
}

info = {
  'covid': "Get covid stats for your country.",
  'userinfo': "Get information about a user.",
  'serverinfo': "Get information about the server.",
  'botinfo': "Get information about me 😊",
  'avatar': "Shows user's avatar."
}

bot = {
  'help': "Shows the help menu.",
  'stats': "Shows my stats, Thank you <3",
  'uptime': "Shows how long I have been up for.",
  'ping': "Shows my ping.",
  'invite': "Invite me to your server \💖",
  'vote': "Vote for me \💖",
  'discord': "Join support server!",
  'credits': "Credits to all contributors!",
  'privacy': "Shows the privacy policy.",
  'bugreport': "Report a bug."
}

games = {
  '2048': "Play 2048 game.",
  'tictactoe': "Play tic-tac-toe with me!",
  'minesweeper': "Play Minesweeper",
  'wumpus': "Play Wumpus game.",
  'rps': "Play rock, paper, scissors with me."
}

nsfw = {
  'fuck': "Fuck someone!",
  'cum': "Cum inside someone ><",
  'spank': "Someones being naughty? Spank them!",
  'hentai': "Hentai...",
  'thighs': "Thighs...",
  'nekogif': "Nekos but gifs",
  'boobs': "Boobs...",
  'blowjob': "Blowjob...",
  'pussy': "Pussies...",
}


utility_with_emojis = """```
😴-AFK
⛅-Weather
📖-Define
💻-Run
📢-Announce
🎉-Giveaway
🎉-Reroll
📑-Translate
📊-Poll
⏰-Countdown
🔗-Create Invite
📨-Embed```
"""

config_with_emojis = """```
🔧-Serverconfig
😍-NQN
🎊-Welcome
💬-Welcomechannel
🤖-Autorole
😢-Leavemessage
💬-Leavechannel
```
"""

moderation_with_emojis = """```
⛏️-Kick
🔨-Ban
🍀-Unban
🔴-Clear
⚠️-Warn
⚠️-Warnings
❌-Delete Channel
✅-Create Channel
➕-Add Role
➖-Remove Role```
"""

fun_with_emojis = """```
😂-Freenitro
🔫-Snipe
🔫-EditSnipe
😊-Howcute
😳-Howhorny
🌈-Howgay
😍-Simpfor
💬-Chat
💀-Whendie
😊-OWO
💻-Hack
😁-Mock
💓-Aesthetic
😂-Dad Joke
🤣-Meme
📜-Quote
👩‍🏫-Advice
🗣️-Say
💬-Ascii
🕵️‍♀️-Predict
👨-Randomname
🟠-Coin Flip
🔢-Random Number
🎲-Dice```
"""

leveling_with_emojis = """```
🔼-Levels
💬-Levelupchannel
💹-Rank
📊-Leaderboard```
"""

music_with_emojis = """```
🔊-Join
🔊-Summon
🎶-Play
🎵-Nowplaying
🔀-Shuffle
⏸-Pause
⏯-Resume
🧾-Queue
⏭-Skip
❌-Remove
⏹-Stop
👋-Leave```
"""

economy_with_emojis = """```
💰-Balance
👜-Inventory
🏪-Shop
🎰-Slots
🛒-Buy
🛍️-Sell
💱-Withdraw
💱-Deposit
🎁-Give
🙏-Beg```
"""

images_with_emojis = """```
🥰-Anime
🐱-Cat
🐶-Dog
🦊-Fox
🐼-Panda
🐼-RedPanda
😻-Pikachu
💬-Comment
💀-Wasted
🔥-Burn
🚮-Trash
😡-Angry
📚-Fact
🧠-Illness
😱-Shock
🗡️-Wanted```
"""

actions_with_emojis = """
```🤗-Hug
😊-Cuddle
💋-Kiss
👄-Bite
💞-Pat
🖐-Slap
😉-Wink
😆-Tickle
🤦‍♂️-Facepalm```
"""

info_with_emojis = """```
🦠-Covid-19
👥-UserInfo
📈-ServerInfo
🤖-BotInfo
🖼️-Avatar```
"""

bot_with_emojis = """```
✅-Help
📈-Stats
⬆️-Uptime
📉-Ping
❤️-Invite
🔼-Vote
🔗-Discord
🧾-Credits
👤-Privacy
🐞-Bug Report```
"""

games_with_emojis = """```
🔢-2048
✅-Tic-Tac-Toe
💣-Minesweeper
🤖-Wumpus
📃-Rock-Paper-Scissors```
"""

nsfw_with_emojis = """```
🔞-Fuck
🔞-Cum
🔞-Spank
🔞-Hentai
🔞-Thighs
🔞-Nekogif
🔞-Boobs
🔞-Blowjob
🔞-Pussy```
"""

help_categories = [
    utility,
    config,
    moderation,
    fun,
    leveling,
    music,
    economy,
    actions,
    images,
    info,
    bot,
    games,
    nsfw,
]
help_emoji_categories = [ 
    utility_with_emojis,
    config_with_emojis,
    moderation_with_emojis,
    fun_with_emojis,
    leveling_with_emojis,
    music_with_emojis,
    economy_with_emojis,
    actions_with_emojis,
    images_with_emojis,
    info_with_emojis,
    bot_with_emojis,
    games_with_emojis,
    nsfw_with_emojis,
]
help_category_titles = [
    ":wrench: • Utility Commands (Page 2)",
    "<:settings:825008012867534928> • Config Commands (Page 3)",
    ":tools: • Moderation Commands (Page 4)",
    ":grinning: • Fun Commands (Page 5)",
    "⬆ • Levelling Commands (Page 6)",
    ":notes: • Music Commands (Page 7)",
    ":money_with_wings: • Economy Commands (Page 8)",
    "<:HugPlease:801710974117740554> • Action Commands (Page 9)",
    ":frame_photo: • Image Commands (Page 10)",
    "<:EpicInfo:766498653753049109> • Info Commands (Page 11)",
    "<a:PetEpicBot:797142108611280926> • Bot Commands (Page 12)",
    ":video_game: • Game Commands (Page 13)",
    "🔞 • NSFW Commands (Page 14)",
]


total_cmds = 0
voter_cmds = 0
premium_cmds = 0

for category in help_categories:
    total_cmds += len(category)





all_cmds = {

  # utility 


  'afk': [
    utility['afk'],
    "afk [reason]"
],
  'weather': [
    utility['weather'],
    "weather <location>"
],
  'define': [
    utility['define'],
    "define <word>"
],
  'run': [
    utility['run'],
    "run <codeblock>"
],
  'announce': [
    utility['announce'],
    "announce"
],
  'giveaway': [
    utility['giveaway'],
    "giveaway"
],
  'reroll': [
    utility['reroll'],
    "reroll <channel> <id>"
],
  'translate': [
    utility['translate'],
    "translate <language> <text>"
],
  'poll': [
    utility['poll'],
    "poll <topic> <[options]>"
],
  'countdown': [
    utility['countdown'],
    "countdown"
],
  'createinvite': [
    utility['createinvite'],
    "createinvite"
],
  'embed': [
    utility['embed'],
    "embed <#hexcolor> | <title> | <description>"
],

  #config 

  'serverconfig': [
    config['serverconfig'],
    "serverconfig"
],
  'nqn': [
    config['nqn'],
    "nqn enable/disable"
],
  'welcome': [
    config['welcome'],
    "welcome enable/disable"
],
  'welcomechannel': [
    config['welcomechannel'],
    "welcomechannel <channel>"
],
  'autorole': [
    config['autorole'],
    "autorole <role>"
],
  'leavemessage': [
    config['leavemessage'],
    "leavemessage enable/disable"
],
  'leavechannel': [
    config['leavechannel'],
    "leavechannel <channel>"
],

  # moderation

  'kick': [
    moderation['kick'],
    "kick <user> [reason]"
],
  'ban': [
    
    moderation['ban'],
    "ban <user> [reason]"
],
  'unban': [
    
    moderation['unban'],
    "unban <user>"
],
  'clear': [
    
    moderation['clear'],
    "clear <amount>"
],
  'warn': [
    
    moderation['warn'],
    "warn <user> [reason]"
],
  'warnings': [
    
    moderation['warnings'],
    "warnings [user]"
],
  'deletechannel': [
    
    moderation['deletechannel'],
    "deletechannel [channel]"
],
  'createchannel': [
    
    moderation['createchannel'],
    "createchannel [channel]"
],
  'addrole': [
    
    moderation['addrole'],
    "addrole <user> <role>"
],
  'removerole': [
    
    moderation['removerole'],
    "removerole <user> <role>"
],

  # fun

  'freenitro': [
    fun['freenitro'],
    "freenitro"
],
  'snipe': [
    fun['snipe'],
    "snipe"
],
  'editsnipe': [
    fun['editsnipe'],
    "editsnipe"
],
  'howcute': [
    fun['howcute'],
    "howcute [user]"
],
  'howhorny': [
    fun['howhorny'],
    "howhorny [user]"
],
  'howgay': [
    fun['howgay'],
    "howgay [user]"
],
  'chat': [
    fun['chat'],
    "chat <msg>"
],
  'whendie': [
    fun['whendie'],
    "whendie [user]"
],
  'simpfor': [
    fun['simpfor'],
    "simpfor <user>"
],
  'owo': [
    fun['owo'],
    "owo <text>"
],
  'hack': [
    fun['hack'],
    "hack <user>"
],
  'mock': [
    fun['mock'],
    "mock <text>"
],
  'aesthetic': [
    fun['aesthetic'],
    "aesthetic <text> | [mode]"
],
  'dadjoke': [
    fun['dadjoke'],
    "dadjoke"
],
  'meme': [
    fun['meme'],
    "meme"
],
  'quote': [
    fun['quote'],
    "quote"
],
  'advice': [
    fun['advice'],
    "advice"
],
  'say': [
    fun['say'],
    "say <text>"
],
  'ascii': [
    fun['ascii'],
    "ascii <text>"
],
  'predict': [
    fun['predict'],
    "predict <question>"
],
  'randomname': [
    fun['randomname'],
    "randomname"
],
  'coin': [
    fun['coin'],
    "coin"
],
  'randomnumber': [
    fun['randomnumber'],
    "randomnumber <num1> <num2>"
],
  'dice': [
    fun['dice'],
    "dice"
],

  # leveling

  'levels': [
    leveling['levels'],
    "levels enable/disable"
],
  'levelupchannel': [
    leveling['levelupchannel'],
    "levelupchannel <channel>"
],
  'rank': [
    leveling['rank'],
    "rank [user]"
],
  'leaderboard': [
    leveling['leaderboard'],
    "leaderboard"
],

  # music

  'join': [
    music['join'],
    "join"
],
  'summon': [
    music['summon'],
    "summon <voice channel>"
],
  'play': [
    music['play'],
    "play <song>"
],
  'nowplaying': [
    music['nowplaying'],
    "nowplaying"
],
  'shuffle': [
    music['shuffle'],
    "shuffle"
],
  'pause': [
    music['pause'],
    "pause"
],
  'resume': [
    music['resume'],
    "resume"
],
  'queue': [
    music['queue'],
    "queue"
],
  'skip': [
    music['skip'],
    "skip"
],
  'remove': [
    music['remove'],
    "remove <number>"
],
  'stop': [
    music['stop'],
    "stop"
],
  'leave': [
    music['leave'],
    "leave"
],

  # economy

  'balance': [
    economy['balance'],
    "balance"
],
  'inventory': [
    economy['inventory'],
    "inventory"
],
  'shop': [
    economy['shop'],
    "shop"
],
  'slots': [
    economy['slots'],
    "slots <amount>"
],
  'buy': [
    economy['buy'],
    "buy <item> [amount]"
],
  'sell': [
    economy['sell'],
    "sell <item> [amount]"
],
  'withdraw': [
    economy['withdraw'],
    "withdraw <amount>"
],
  'deposit': [
    economy['deposit'],
    "deposit <amount>"
],
  'give': [
    economy['give'],
    "give <user> <amount>"
],
  'beg': [
    economy['beg'],
    "beg"
],

  # images

  'anime': [
      images['anime'],
      "anime"
  ],
  'cat': [
    images['cat'],
    "cat"
],
  'dog': [
    images['dog'],
    "dog"
],
  'fox': [
    images['fox'],
    "fox"
],
  'panda': [
    images['panda'],
    "panda"
],
  'redpanda': [
    images['redpanda'],
    "redpanda"
      ],
  'pikachu': [
      images['pikachu'],
    "pikachu"
  ],
  'comment': [
    images['comment'],
    "comment <text>"
],
  'trash': [
    images['trash'],
    "trash [user]"
],
  'angry': [
    images['angry'],
    "angry [user]"
],
  'fact': [
    images['fact'],
    "fact <text>"
],
  'illness': [
    images['illness'],
    "illness <text>"
],
  'shock': [
    images['shock'],
    "shock <text>"
],
  'wanted': [
    images['wanted'],
    "wanted [user]"
],

  # actions
  
  'hug': [
    actions['hug'],
    "hug <user>"
],
  'cuddle': [
    actions['cuddle'],
    "cuddle <user>"
],
  'kiss': [
    actions['kiss'],
    "kiss <user>"
],
  'bite': [
    actions['bite'],
    "bite <user>"
],
  'pat': [
    actions['pat'],
    "pat <user>"
],
  'slap': [
    actions['slap'],
    "slap <user>"
],
  'wink': [
    actions['wink'],
    "wink <user>"
],
  'tickle': [
    actions['tickle'],
    "tickle <user>"
],
  'facepalm': [
    actions['facepalm'],
    "facepalm"
],

  # info
  
  'covid': [
    info['covid'],
    "covid <country>"
],
  'userinfo': [
    info['userinfo'],
    "userinfo [user]"
],
  'serverinfo': [
    info['serverinfo'],
    "serverinfo"
],
  'botinfo': [
    info['botinfo'],
    "botinfo"
],
  'avatar': [
    info['avatar'],
    "avatar [user]"
],

  # bot
  
  'help': [
    bot['help'],
    "help [cmd/category]"
],
  'stats': [
    bot['stats'],
    "stats"
],
  'uptime': [
    bot['uptime'],
    "uptime"
],
  'ping': [
    bot['ping'],
    "ping"
],
  'invite': [
    bot['invite'],
    "invite"
],
  'vote': [
    bot['vote'],
    "vote"
],
  'discord': [
    bot['discord'],
    "discord"
],
  'credits': [
    bot['credits'],
    "credits"
],
  'privacy': [
    bot['privacy'],
    "privacy"
],
  'bugreport': [
    bot['bugreport'],
    "bugreport"
],

  # games
  
  '2048': [
    games['2048'],
    "2048"
],
  'tictactoe': [
    games['tictactoe'],
    "tictactoe"
],
  'minesweeper': [
    games['minesweeper'],
    "minesweeper <columns> <rows> <bombs>"
],
  'wumpus': [
    games['wumpus'],
    "wumpus"
],
  'rps': [
    games['rps'],
    "rps"
],

  # nsfw omegalul

  'fuck': [
    nsfw['fuck'],
    "fuck <user>"
],
  'cum': [
    nsfw['cum'],
    "cum <user>"
],
  'spank': [
    nsfw['spank'],
    "spank <user>"
],
  'hentai': [
    nsfw['hentai'],
    "hentai"
],
  'thighs': [
    nsfw['thighs'],
    "thighs"
],
  'nekogif': [
    nsfw['nekogif'],
    "nekogif"
],
  'boobs': [
    nsfw['boobs'],
    "boobs"
],
  'blowjob': [
    nsfw['blowjob'],
    "blowjob"
],
  'pussy': [
    nsfw['pussy'],
    "pussy"
],
}
