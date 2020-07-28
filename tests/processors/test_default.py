# -*- coding: utf-8 -*-
from tests import BaseTestCase
from aiogram.types import Message
from wakebot.processors.default import DefaultProcessor
from wakebot.processors import RuGeneral
from tests.mocks.aiogram import Dispatcher


class DefaultProcessorTestCase(BaseTestCase):

    def setUp(self):
        dp = Dispatcher()
        self.processor = DefaultProcessor(dp, RuGeneral)

    async def answer_mock(self, text, parse_mode=None):
        self.result_text = text

    async def test_cmd_start(self):
        """Proceed /start command"""

        message = Message()
        message.text = "/start"
        message.answer = self.answer_mock

        await self.processor.cmd_start(message)

        self.assertEqual(self.result_text, RuGeneral.default.start_message)

    async def test_cmd_help(self):
        """Proceed /help command"""

        message = Message()
        message.text = "/help"
        message.answer = self.answer_mock

        await self.processor.cmd_help(message)

        self.assertEqual(self.result_text, RuGeneral.default.help_message)


DefaultProcessorTestCase().run_tests_async()
