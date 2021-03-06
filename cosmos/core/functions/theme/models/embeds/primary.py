"""
Cosmos: A General purpose Discord bot.
Copyright (C) 2020 thec0sm0s

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from discord import Embed

from abc import abstractmethod


class Base(Embed):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Primary(Base):

    def __init__(self, bot=None, **kwargs):
        if bot:
            self.bot = bot
        primary_color = self.bot.configs.color_scheme.primary
        try:
            kwargs["color"] = kwargs.get("color") or primary_color
            kwargs.pop("colour")
        except KeyError:
            pass
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def bot(self):
        if not self._bot:
            raise NotImplementedError
        return self._bot

    @bot.setter
    def bot(self, bot):
        self._bot = bot
