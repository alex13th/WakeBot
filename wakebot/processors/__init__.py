from aiogram.types import ParseMode
from .default import DefaultProcessor
from .reserve import ReserveProcessor
from .wake import WakeProcessor
from .supboard import SupboardProcessor

parse_mode = ParseMode.MARKDOWN


class RuGeneral:
    parse_mode = ParseMode.MARKDOWN

    callback_error = "Ошибка обработки ответа"


class RuDefault(RuGeneral):
    start_message = (
        "*Привет!*\n"
        "Это наш новый сервис для бронирования времени на вейк-станции. "
        "Сейчас он находится в процессе тестирования, "
        "но вполне работоспособен.")

    help_message = (
        "*Список команд*\n"
        "\n/wake - забронировать катание на *Вейкборде*"
        "\n/sup - забронировать прокат *Сапборда*"
        "\n/start - приветствие"
        "\n/help - справка по командам бота")


class RuReserve(RuGeneral):
    service_text = "Услуга"
    service_label = f"*{service_text}:*"
    service_type_text = "Бронирование"

    list_header = "*Список бронирований:*"
    list_empty = "На текущий момент нет активных бронирований"
    list_footer = ("Для получения дополнительной информации, "
                   "нажмите на кнопку с номером бронирования")

    icon_stop = "⛔️"
    restrict_list_header = (f"{icon_stop} *ВНИМАНИЕ!\n"
                            "Совпадение с активными бронированиями:*")

    main_callback = "Главное меню"

    back_text = "Назад"
    back_button = back_text

    book_text = "Бронирование"
    books_text = "Бронирований"
    book_header = f"*{book_text}*"
    start_book_button = f"Начать {book_text.lower()}"
    start_book_button_callback = book_text

    # phone_regex = "\\+\\d{10}"
    phone_regex = "^\\+[7]\\s?[-\\(]?\\d{3}\\)?[- ]?\\d{3}-?\\d{2}-?\\d{2}$"
    icon_phone = "📞"
    phone_text = "Телефон"
    phone_label = f"*{phone_text}:*"
    phone_button = f"{icon_phone} Внести {phone_text}"
    phone_button_callback = "Введите номер телефона"
    phone_message = (
        "*Допустимые форматы номера:*"
        "\n+79103123167"
        "\n+7-910-221-22-22"
        "\n+7 (910) 221-22-22"
        "\n+7(910) 221-22-22"
        "\n+7 (910)-221-22-22"
        "\n+7(910)-221-22-22")
    phone_success_message = "Ваш номер успешно внесен."
    phone_error_message = (
        f"{icon_stop} *Номер указан в неверном формате*"
        "\n\nДопустимые форматы номера:"
        "\n+79103123167"
        "\n+7-910-221-22-22"
        "\n+7 (910) 221-22-22"
        "\n+7(910) 221-22-22"
        "\n+7 (910)-221-22-22"
        "\n+7(910)-221-22-22")
    phone_warning = "⚠️ Обязательно укажите номер телефона."
    date_format = "%d.%m.%Y"
    date_text = "Дата"
    date_label = f"*{date_text}:*"
    date_button = "Выбрать дату"
    date_button_callback = "Выберите дату"

    time_format = "%H:%M"
    time_zone = +9
    time_text = "Время"
    time_button = f"Выбрать {time_text.lower()}"
    time_button_callback = "Выберите час"
    hour_button_callback = "Выберите часы"
    minute_button_callback = "Выберите минуты"
    start_label = f"*{time_text} начала:*"
    end_label = f"*{time_text} окончания:*"

    name_text = "Имя"
    name_label = f"*{name_text}:*"

    admin_text = "Администратор"
    admin_label = f"*{admin_text}:*"

    count_text = "Количество"
    count_label = f"*{count_text}:*"
    count_button = f"{count_text}"
    count_button_callback = f"Выберите {count_text.lower()}"

    list_text = f"Список {books_text}"
    list_button = list_text
    list_button_callback = list_text

    details_button_callback = "Информация по бронированию"

    cancel_button = f"❌ Отменить {book_text.lower()}"
    cancel_button_callback = f"{book_text} отменено"
    cancel_notify_header = f"❌ *Отменено {book_text.lower()}*"

    notify_text = "Оповестить"
    notification_text = "Оповещение"
    notify_button = f"ℹ️ {notify_text}"
    notify_button_callback = f"{notification_text} отправлено"
    notify_message = ("Обратитесь к админстратору для уточнения информации"
                      " по бронированию")

    options_text = "Опции"
    options_label = f"*{options_text}:*"

    icon_set = "\u23f1"
    set_text = "Сет"
    sets_text = "Сетов"
    set_button = f"{icon_set} {set_text}"
    set_button_callback = f"Выберите {count_text.lower()} {sets_text.lower()}"

    icon_hour = "\u23f0"
    hour_text = "Час"
    hours_text = "Часов"
    hour_button = f"{icon_hour} {hour_text}"
    hour_button_callback = (f"Выберите {count_text.lower()} "
                            f"{hours_text.lower()}")

    set_type_text = "Вид"
    set_type_label = f"*{set_text}:*"
    set_types = {}
    set_types["set"] = set_text
    set_types["hour"] = hour_text

    apply_text = "Забронировать"
    apply_button = f"👌 {apply_text}"
    apply_button_callback = f"{book_text} добавлено"
    apply_error_callback = "Ошибка бронирования"


class RuWake(RuReserve):
    hello_message = ("*Вейкборд - великолепный выбор!*"
                     "\nРекомендуем перед бронированием посмотреть список"
                     " активных бронирований.")

    service_type_text = "Вейкборд"

    icon_board = "🏄‍♂️"
    wake_text = "Вейкборд"
    board_button = f"{icon_board} {wake_text}"
    board_button_callback = "Аренда вейкборда"

    icon_hydro = "👙"
    hydro_text = "Гидрокостюм"
    hydro_button = f"{icon_hydro} {hydro_text}"
    hydro_button_callback = "Аренда гидрокостюма"


class RuSupboard(RuReserve):
    hello_message = ("*Сапборд - современно и душевно!*"
                     "\nРекомендуем перед бронированием посмотреть список"
                     " активных бронирований.")
    service_type_text = "Сапборд"


if __name__ == "__main__":
    DefaultProcessor, ReserveProcessor, WakeProcessor, SupboardProcessor
