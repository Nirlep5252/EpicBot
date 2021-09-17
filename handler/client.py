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
from .app_commands import update_app_commands, app_command_handler


class InteractionClient:
    def __init__(self, client) -> None:
        self.client = client
        self.client.app_commands_updated = False
        self._add_listeners()

    def _add_listeners(self):
        self.client.add_listener(self._connect_event, 'on_connect')
        self.client.add_listener(self._interaction_event, 'on_interaction')

    async def _connect_event(self):
        if not self.client.app_commands_updated:
            await update_app_commands(self.client)
            self.client.app_commands_updated = True

    async def _interaction_event(self, interaction):
        await app_command_handler(interaction, self.client)
