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

from discord.ext import commands
from typing import Optional


class EnhanceCmdFlags(commands.FlagConverter, prefix="--", delimiter=" ", case_insensitive=True):
    contrast: Optional[float] = 1.0
    color: Optional[float] = 1.0
    brightness: Optional[float] = 1.0
    sharpness: Optional[float] = 1.0


class StickerFlags(commands.FlagConverter, prefix="--", delimiter=" ", case_insensitive=True):
    name: Optional[str] = None
    description: Optional[str] = None
    emoji: Optional[str] = None
