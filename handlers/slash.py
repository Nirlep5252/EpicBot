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
import inspect
import traceback
from typing import Any, Dict, List, Union
from inspect import getfullargspec
from discord.ext import commands
from utils.bot import EpicBot

slash_cmd_option_types = {
    str: 3,
    int: 4,
    bool: 5,
    discord.Member: 6,
    discord.TextChannel: 7,
    discord.CategoryChannel: 7,
    discord.VoiceChannel: 7,
    discord.Thread: 7,
    discord.StageChannel: 7,
    discord.Role: 8,
    # TODO: 9 is mentionable, add that somehow
    float: 10,
}

slash_cmd_option_converters = {
    3: str,
    4: int,
    5: bool,
    6: commands.MemberConverter().convert,
    7: commands.GuildChannelConverter().convert,
    8: commands.RoleConverter().convert,
    # TODO: 9 is mentionable converters????!?!??!?!??! SLASH COMMANDS ARE CANCER
    10: float,
}


class SlashContext(discord.Interaction):
    def __init__(self, interaction: discord.Interaction, bot: EpicBot):
        super().__init__(data=interaction._raw_data, state=interaction._state)
        self._bot = bot

    @property
    def bot(self):
        return self._bot


class SlashCommandChoice:
    def __init__(self, name: str, value: Union[str, int, float]):
        self.name = name
        self.value = value

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "value": self.value
        }

    def __repr__(self) -> str:
        return f"SlashCommandChoice(name={self.name} value={self.value})"


class SlashCommandOption:
    def __init__(
        self, name: str, type: int, description: str,
        required: bool = True, choices: List[SlashCommandChoice] = None
    ):
        choices = choices or []
        self.name = name
        self.type = type
        self.description = description
        self.required = required
        self.choices = choices

    def to_dict(self) -> dict:
        final = {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "required": self.required
        }
        if self.choices:
            final.update({"choices": [choice.to_dict() for choice in self.choices]})
        return final

    def __repr__(self) -> str:
        return f"SlashCommandOption(name={self.name} type={self.type} description={self.description} required={self.required} choices={self.choices})"


class SlashCommand:
    def __init__(self, func, **kwargs) -> None:
        self.callback = func

        self.name = kwargs.get('name', func.__name__)
        self.desc = kwargs.get('help')
        self.guild_ids = kwargs.get('guild_ids', [])
        self._is_global = True if self.guild_ids == [] else False
        _spec = getfullargspec(func)
        _raw_args = _spec.annotations
        _defaults = _spec.defaults or []
        _cog = False
        if 'self' in _spec.args:
            _cog = True
        self._cog = _cog
        for _key in _raw_args:
            # im removing the 'ctx' arg from the func
            del _raw_args[_key]
            break
        _raw_options = self._parse_raw_args(_raw_args, _defaults)
        self.options = kwargs.get('options') or self._parse_options(_raw_options)

    def __repr__(self) -> str:
        return f"SlashCommand(name={self.name} callback={self.callback} desc={self.desc} guild_ids={self.guild_ids} options={self.options})"

    def __str__(self) -> str:
        return self.name

    def _parse_options(self, options: List[Union[dict, SlashCommandOption]]) -> List[SlashCommandOption]:
        final = []
        for option in options:
            if not isinstance(option, SlashCommandOption):
                if option.get('type', str) not in slash_cmd_option_types:
                    raise TypeError(f'Unknown option type {option.get("type")}')
                if 'name' not in option:
                    raise ValueError('Missing option name')
                if 'choices' in option:
                    choices = [SlashCommandChoice(c['name'], c['value']) for c in option['choices']]
                else:
                    choices = []
                final.append(SlashCommandOption(
                    name=option['name'],
                    type=slash_cmd_option_types[option.get('type', str)],
                    description=option.get('help', f"Please enter a {option['name']}"),
                    required=option.get('required', True),
                    choices=choices
                ))
            else:
                final.append(option)
        if len(final) > 25:
            raise TypeError('Max 25 options allowed.')
        return final

    def _parse_raw_args(self, raw_args: Dict[str, Any], defaults: tuple) -> List[Union[dict, SlashCommandOption]]:
        final = []
        i = 0
        if len(defaults) > 0:
            args_copy = list(raw_args)[-(len(defaults)):]
        else:
            args_copy = []
        for arg, type_ in raw_args.items():
            if isinstance(type_, SlashCommandOption):
                final.append(raw_args[arg])
            else:
                final.append({
                    'name': arg,
                    'type': type_,
                    'required': False if arg in args_copy else True,
                })
            i += 1
        return final


slash_cmds: Dict[str, SlashCommand] = {}


def slash_command(**kwargs):
    def decorator(func):
        slash_cmd = SlashCommand(func, **kwargs)
        slash_cmds[slash_cmd.name] = slash_cmd
        return func

    return decorator


def get_option(name: str, options: List[SlashCommandOption]):
    for option in options:
        if option.name == name:
            return option
    raise ValueError(f'Option {name} not found')


async def slash_handler(interaction: discord.Interaction, bot: EpicBot):
    class something(object):
        def __init__(self, client):
            self.client = client
    all_slash_commands: Dict[str, SlashCommand] = bot.slash_cmds
    data = interaction.data
    inter_type = data.get('type')
    # checking if it's a slash cmd or not
    # https://discord.com/developers/docs/interactions/application-commands#application-command-object-application-command-types
    if inter_type is None:
        return
    if int(inter_type) != 1:
        return
    # checking if the slash cmd is in the slash cmds dict
    if data.get('name') not in all_slash_commands:
        return
    slash_cmd = all_slash_commands[data.get('name')]
    if not slash_cmd._is_global:
        if interaction.guild_id not in slash_cmd.guild_ids:
            return

    kwargs = {}
    ctx = SlashContext(interaction, bot)
    for option in data.get('options', []):
        _opt = get_option(option['name'], slash_cmd.options)
        if _opt.type not in slash_cmd_option_converters:
            raise TypeError(f'Not known option type {_opt.type}')
        converter = slash_cmd_option_converters[_opt.type]
        kwargs.update({_opt.name: await converter(ctx, option['value']) if inspect.iscoroutinefunction(converter) else converter(option['value'])})
    try:
        if slash_cmd._cog:
            await slash_cmd.callback(something(client=bot), ctx, **kwargs)
        else:
            await slash_cmd.callback(ctx, **kwargs)
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)


async def update_app_commands(bot: EpicBot):
    bot.slash_cmds = slash_cmds
    global_slash_cmds = []
    guild_slash_cmds: Dict[int, list] = {}
    for cmd_name, cmd in slash_cmds.items():
        cmd_payload = {
            "name": cmd_name,
            "type": 1,
            "description": cmd.desc,
            "options": [option.to_dict() for option in cmd.options]
        }
        if not cmd.guild_ids:
            global_slash_cmds.append(cmd_payload)
        else:
            for guild_id in cmd.guild_ids:
                current_guild_cmds = guild_slash_cmds.get(guild_id, [])
                current_guild_cmds.append(cmd_payload)
                guild_slash_cmds.update({guild_id: current_guild_cmds})

    await bot.http.bulk_upsert_global_commands(bot.user.id, global_slash_cmds)
    print(f"Updated {len(global_slash_cmds)} global commands")
    for guild_id, guild_commands in guild_slash_cmds.items():
        try:
            await bot.http.bulk_upsert_guild_commands(bot.user.id, guild_id, guild_commands)
        except discord.Forbidden:
            print(f"Unable to update guild commands for guild ID: {guild_id}\n\nPlease re-add the bot to that guild using the application.commands scope.")
        print(f"Updated {len(guild_commands)} for guild ID: {guild_id}")
    print(f"Updated guild commands for {len(guild_slash_cmds)} guilds")
