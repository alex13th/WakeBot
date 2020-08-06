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


class RuReserve:
    book_message = "Выберите действие:"

    main_callback = "Главное меню"

    start_book_button = "Начать бронирование"
    start_book_button_callback = "Бронирование"

    list_button = "Список бронирований"
    list_button_callback = "Список бронирований"

    set_button_callback = "Выберите количество сетов"
    hour_button_callback = "Выберите количество часов"

    apply_text = "Забронировать"
    apply_button = f"👌 {apply_text}"

    message_header = "*Бронирование*"

    type_label = "*Услуга:*"
    date_label = "*Дата:*"

    start_label = "*Время начала:*"
    end_label = "*Время окончания:*"

    set_types = {}
    set_types["set"] = "Сет"
    set_types["hour"] = "Час"
    set_type_label = "*Вид:*"


class RuWake:
    hello_message = ("*Вейкборд - великолепный выбор!*"
                     "\nРекомендуем перед бронированием посмотреть список"
                     " активных бронирований.")

    icon_set = "\u23f1"
    set_button = f"{icon_set} Сет"
    icon_hour = "\u23f0"
    hour_button = f"{icon_hour} Час"

    options_text = "Опции"
    options_label = f"*{options_text}:*"

    icon_board = "🏄‍♂️"
    wake_text = "Вейкборд"
    board_button = f"{icon_board} {wake_text}"
    board_button_add = f"{wake_text} добавлен"
    board_button_remove = f"{wake_text} удален"

    icon_hydro = "👙"
    hydro_text = "Гидрокостюм"
    hydro_button = f"{icon_hydro} {hydro_text}"
    hydro_button_add = f"{hydro_text} добавлен"
    hydro_button_remove = f"{hydro_text} удален"


class RuGeneral:
    default = RuDefault
    reserve = RuReserve
    wake = RuWake

    icon_phone = "📞"
    phone_text = "Телефон"
    phone_label = f"*{phone_text}:*"
    phone_button = f"{icon_phone} Внести {phone_text}"
    phone_button_callback = "Введите номер телефона"
    phone_reply_button = "Отправить номер телефона"
    phone_refuse_button = "Не отправлять номер"
    phone_message = ("Отправьте номер Вашего телефона простым сообщением")
    phone_success_message = "Ваш номер успешно внесен."

    callback_error = "Ошибка обработки ответа"

    date_button = "Выбрать дату"
    date_button_callback = "Выберите дату"
    date_format = "%d.%m.%Y"
    time_button = "Выбрать время"
    time_button_callback = "Выберите час"
    time_format = "%H:%M"
    time_zone = +9
    hour_button_callback = "Выберите минуты"

    back_button = "Назад"

    name_text = "Имя"
    name_label = f"*{name_text}:*"

    count_label = "*Количество:*"
