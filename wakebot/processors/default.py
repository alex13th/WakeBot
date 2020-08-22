from aiogram.dispatcher import Dispatcher
from aiogram.types import Message, ParseMode


class DefaultProcessor:
    """Proceed common commands: start, help.

    Attributes:
        strings:
            A locale strings class
    """

    __dispatcher: Dispatcher
    strings: any
    parse_mode = ParseMode.MARKDOWN

    def __init__(self, dispatcher: Dispatcher, strings: any,
                 parse_mode=ParseMode.MARKDOWN):
        """Initialize ChatProvider object

        Args:
            dispatcher:
                A telegram bot dispatcher.
            strings:
                A locale strings class.
            parse_mode:
                A parse mode of telegram messages (aiogram.types.ParseMode).
                Default value: ParseMode.MARKDOWN
        """
        self.__dispatcher = dispatcher
        self.strings = strings
        self.parse_mode = parse_mode

        dispatcher.register_message_handler(self.cmd_start, commands=["start"])
        dispatcher.register_message_handler(self.cmd_help, commands=["help"])

    async def cmd_start(self, message: Message):
        """Proceed /start"""
        await message.answer(self.strings.start_message,
                             self.parse_mode)

    async def cmd_help(self, message: Message):
        """Proceed /help"""
        await message.answer(self.strings.help_message,
                             self.parse_mode)
