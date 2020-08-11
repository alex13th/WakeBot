# -*- coding: utf-8 -*-
from ..mocks.aiogram import Dispatcher
from ..base_test_case import BaseTestCase

from aiogram.types import Message
from wakebot.processors.default import DefaultProcessor
from wakebot.processors import RuGeneral


class DefaultProcessorTestCase(BaseTestCase):
    """DefaultProcessor class"""
    
    def setUp(self):
        dp = Dispatcher()
        self.processor = DefaultProcessor(dp, RuGeneral)
        self.strings = RuGeneral.default

    async def answer_mock(self, text, parse_mode=None):
        self.result_text = text

    async def test_cmd_start(self):
        """Proceed /start command"""

        message = Message()
        message.answer = self.answer_mock

        await self.processor.cmd_start(message)
        passed, message = self.assert_params(self.result_text,
                                             self.strings.start_message)
        assert passed, message

    async def test_cmd_help(self):
        """Proceed /help command"""

        message = Message()
        message.answer = self.answer_mock

        await self.processor.cmd_help(message)

        await self.processor.cmd_start(message)
        passed, message = self.assert_params(self.result_text,
                                             self.strings.help_message)


DefaultProcessorTestCase().run_tests_async()
