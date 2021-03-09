from pathlib import Path
from typing import Optional, Callable, Any

from discord import File, Message
from discord.embeds import Embed
from discord.ext.commands import Context

from fate_of_dice.common.resource_handler import ResourceImageHandler
from fate_of_dice.system import DiceResult


class DiceEmbed(Embed):
    __DEFAULT_AUTHOR_NAME: str = 'FateOfDice'

    def __init__(self, simple=False, **kwargs):
        super().__init__(**kwargs)

        self.simple_presentation = simple
        self.__thumbnail_file = None

        self.set_default_author()

    @classmethod
    def from_dice_result(cls, result: DiceResult, message: Message, simple=False, **kwargs) -> 'DiceEmbed':
        dice_embed = DiceEmbed(simple=simple, **kwargs)
        dice_embed.simple_presentation = dice_embed.simple_presentation or result.simple_presentation

        if dice_embed.simple_presentation:
            dice_embed.description = '\n'.join(result.descriptions)
        else:
            dice_embed.set_author(name=message.author.name, icon_url=str(message.author.avatar_url))

        return dice_embed

    def __setattr__(self, name: str, value: Any) -> None:
        if not value:
            value = Embed.Empty

        super().__setattr__(name, value)

    def __getattribute__(self, item):
        value = super().__getattribute__(item)

        if value == Embed.Empty:
            value = None
        return value

    def add_field(self, *, name: str, value: str, inline: bool = True):
        if not value:
            return None

        return super().add_field(name=name, value=value, inline=inline)

    def add_fields(self, *, name: str, values: [str], inline: bool = True):
        if not values:
            return None

        for value in values:
            super().add_field(name=name, value=value, inline=inline)
        return self

    def set_default_author(self, context: Optional[Context] = None):
        if context:
            bot_user = context.bot.user
            name = bot_user.name
            avatar_url = bot_user.avatar_url
        else:
            name = self.__DEFAULT_AUTHOR_NAME
            avatar_url = ResourceImageHandler.FATE_OF_DICE_IMAGE_URL or Embed.Empty

        return super().set_author(name=name, icon_url=avatar_url)

    def add_empty_field(self, condition: Callable = lambda: True):
        if condition():
            self.add_field(name=u'\u200B', value=u'\u200B', inline=False)

    def add_thumbnail(self, value: str or Path or Embed.Empty):
        if isinstance(value, str):
            super().set_thumbnail(url=value)
            return None
        elif isinstance(value, Path):
            return self.__set_thumbnail_from_path(value)
        else:
            super().set_thumbnail(url=Embed.Empty)
            return None

    def thumbnail_file(self) -> Optional[File]:
        return self.__thumbnail_file

    def __set_thumbnail_from_path(self, file_path: Path) -> None:
        file_name: str = file_path.name
        self.__thumbnail_file = File(str(file_path), filename=file_name)
        super().set_thumbnail(url=f"attachment://{file_name}")
