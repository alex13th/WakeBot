# -*- coding: utf-8 -*-

from aiogram.types import ParseMode

parse_mode = ParseMode.MARKDOWN


class RuDefault:
    start_message = (
        "*Привет!*\n"
        "Это наш новый сервис для бронирования времени на вейк-станции. "
        "Сейчас он находится в процессе тестирования, но вполне работоспособен.")

    help_message = (
        "*Список команд*\n\n"
        "/help - справка по командам бота")


class RuReserve:
    reserve_book_message = "Выберите действие:"
    book_button = "Начать бронирование"

    reserve_message_header = "*Бронирование*"
    reserve_type_label = "*Услуга*"
    reserve_date_label = "*Дата*"
    reserve_start_label = "*Время начала*"
    reserve_end_label = "*Время окончания*"


class RuGeneral:
    default = RuDefault
    reserve = RuReserve
    back_str = "Назад"
