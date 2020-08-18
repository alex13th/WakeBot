class Bot:

    async def send_message(self, chat_id, text, parse_mode, reply_markup=None):
        self.text = text


class Dispatcher:
    """ Имитатор объекта телеграм бота """

    bot = Bot()

    def register_message_handler(self, callback, commands=None):
        pass

    def register_callback_query_handler(self, callback, filters=None):
        pass
