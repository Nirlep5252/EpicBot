# when u add a new cmd you will need to update the following things:
#   - add it in its correct category dict and its usage
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

cmd_categories = [
  'utility',
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
  'nqn': "Nitro emojis, Without Nitro!",
  'prefix': "Change the bot's prefix.",
  'weather': "Find weather info.",
  'announce': "Make an embedded announement.",
  'giveaway': "Start a giveaway.",
  'reroll': "Reroll a giveaway.",
  'translate': "Translate text from any language.",
  'poll': "Start a poll.",
  'countdown': "Start a countdown.",
  'createinvite': "Create an invite instantly that never expires.",
  'embed': "Convert your message into a beautiful customizable embed."
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
  'howgay': "Check how gay someone is.",
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
  'connect': "I will join your voice channel.",
  'play': "I will play music in your ears.",
  'nowplaying': "Shows which song is playing currently.",
  'pause': "Pauses the music.",
  'resume': "Resumes the music.",
  'queue': "Shows the music queue.",
  'skip': "Skips the current song.",
  'stop': "Stops the music and clears the queue.",
  'volume': "Changes the volume."
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
  'cat': "Gives a random cute cat picture.",
  'dog': "Gives a random cute dog picture.",
  'fox': "Gives a random cute fox picture.",
  'anime': "Gives a random anime picture.",
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
  'kiss': "Kiss someone 💋",
  'pat': "Pat someone",
  'slap': "Slap someone 🤚",
  'tickle': "Tickle someone"
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
😍-NQN
❔-Prefix
⛅-Weather
📢-Announce
🎉-Giveaway
🎉-Reroll
📑-Translate
📊-Poll
⏰-Countdown
🔗-Create Invite
📨-Embed```
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
🌈-Howgay
😍-Simpfor
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
🔊-Connect
🎶-Play
🎵-Nowplaying
⏸-Pause
⏯-Resume
🧾-Queue
⏭-Skip
⏹-Stop
🔉-Volume```
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
🐱-Cat
🐶-Dog
🦊-Fox
🥰-Anime
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
💋-Kiss
💞-Pat
🖐-Slap
😆-Tickle```
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
    ":tools: • Moderation Commands (Page 3)",
    ":grinning: • Fun Commands(Page 4)",
    "⬆ • Levelling Commands(Page 5)",
    ":notes: • Music Commands(Page 6)",
    ":money_with_wings: • Economy Commands(Page 7)",
    ":frame_photo: • Image Commands(Page 8)",
    "<:HugPlease:801710974117740554> • Action Commands(Page 9)",
    "<:EpicInfo:766498653753049109> • Info Commands(Page 10)",
    "<a:PetEpicBot:797142108611280926> • Bot Commands(Page 11)",
    ":video_game: • Game Commands(Page 12)",
    "🔞 • NSFW Commands(Page 13)",
]


total_cmds = 0
voter_cmds = 0
premium_cmds = 0

for category in help_categories:
    total_cmds += len(category)





all_cmds = {

  # utility 

  'nqn': [
    "Use nitro emojis, WITHOUT nitro!",
    "nqn enable/disable"
],
  'prefix': [
    utility['prefix'],
    "prefix <new prefix>"
],
  'weather': [
    utility['weather'],
    "weather <location>"
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
  'howgay': [
    fun['howgay'],
    "howgay [user]"
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

  'connect': [
    music['connect'],
    "connect"
],
  'play': [
    music['play'],
    "play <song>"
],
  'nowplaying': [
    music['nowplaying'],
    "nowplaying"
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
  'stop': [
    music['stop'],
    "stop"
],
  'volume': [
    music['volume'],
    "volume <number>"
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
  'anime': [
    images['anime'],
    "anime"
],
  'burn': [
    images['burn'],
    "burn [user]"
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
  'kiss': [
    actions['kiss'],
    "kiss <user>"
],
  'pat': [
    actions['pat'],
    "pat <user>"
],
  'slap': [
    actions['slap'],
    "slap <user>"
],
  'tickle': [
    actions['tickle'],
    "tickle <user>"
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