# -*- coding: utf-8 -*-

from aiogram.types import ParseMode

parse_mode = ParseMode.MARKDOWN


class RuDefault:
    start_message = (
        "*Привет!*\n"
        "Это наш новый сервис для бронирования времени на вейк-станции. "
        "Сейчас он находится в процессе тестирования, "
        "но вполне работоспособен.")

    help_message = (
        "*Список команд*\n"
        "\n/wake - забронировать катание на Вейкборде"
        "\n/help - справка по командам бота")

    wake_text = "Вейкборд"
    wake_button = f"{wake_text}"
    hydro_text = "Гидрокостюм"
    hydro_button = f"{hydro_text}"


class RuReserve:
    reserve_book_message = "Выберите действие:"

    start_book_button = "Начать бронирование"
    list_button = "Список бронирований"
    set_button = "Сет"
    hour_button = "Час"

    reserve_message_header = "*Бронирование*"
    reserve_type_label = "*Услуга*"
    reserve_date_label = "*Дата*"
    reserve_start_label = "*Время начала*"
    reserve_end_label = "*Время окончания*"


class RuWake:
    hello_message = ("*Вейкборд - великолепный выбор!*"
                     "\nРекомендуем перед бронированием посмотреть список"
                     " активных бронирований.")


class RuGeneral:
    default = RuDefault
    reserve = RuReserve
    wake = RuWake

    date_format = "%d.%m.%Y"

    date_button = "Выбрать дату"
    time_button = "Выбрать время"
    back_button = "Назад"
