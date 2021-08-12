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

from discord.ext.commands import Converter, Context, BadArgument
import pytz


class InvalidAddRemoveArgument(BadArgument):
    pass


class InvalidTimeZone(BadArgument):
    pass


class AddRemoveConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        if argument.lower() in ['add']:
            return True
        elif argument.lower() in ['remove']:
            return False
        else:
            raise InvalidAddRemoveArgument(argument)


class Lower(Converter):
    async def convert(self, ctx: Context, argument: str):
        return argument.lower()


class TimeZone(Converter):
    async def convert(self, ctx: Context, argument: str):
        try:
            timezone = pytz.timezone(argument)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            raise InvalidTimeZone(argument)
