from dataclasses import dataclass, field
from typing import Dict, Optional, Union


@dataclass
class Profile:
    """User profile class for EpicBot's profile system."""

    # basic stuff
    _id: int
    description: str = "A very cool EpicBot user!"
    badges: list = field(default_factory=lambda: ["normie"])
    cmds_used: int = 0
    bugs_reported: int = 0
    suggestions_submitted: int = 0
    rank_card_template: str = "default"
    snipe: bool = True
    votes: Dict[str, Union[int, dict]] = field(default_factory=lambda: {"top.gg": 0, "bots.discordlabs.org": 0, "discordbotlist.com": 0, "reminders": False, "last_voted": {}})

    # globalchat stuff
    gc_avatar: Optional[str] = None
    gc_nick: Optional[str] = None
    gc_rules_accepted: bool = False

    # marriage stuff
    married_at: Optional[int] = None
    married_to: Optional[int] = None

    # actions stuff
    times_simped: int = 0
    times_thanked: int = 0
    bites: int = 0
    blushes: int = 0
    cries: int = 0
    cuddles: int = 0
    facepalms: int = 0
    feeds: int = 0
    hugs: int = 0
    kisses: int = 0
    licks: int = 0
    pats: int = 0
    slaps: int = 0
    tail_wags: int = 0
    tickles: int = 0
    winks: int = 0

    # incomplete things
    accepted_bugs: int = 0
    accepted_suggestions: int = 0
    most_used_cmd: str = ""
    rating: int = 0
    accent_color: Optional[int] = None
