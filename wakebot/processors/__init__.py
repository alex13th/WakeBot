from aiogram.types import ParseMode
from .default import DefaultProcessor
from .reserve import ReserveProcessor
from .wake import WakeProcessor
from .supboard import SupboardProcessor

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

    list_header = "*Список бронирований:*"
    list_empty = "На текущий момент нет активных бронирований"
    list_footer = ("Для получения дополнительной информации, "
                   "нажмите на кнопку с номером бронирования")

    restrict_list_header = ("⛔️ *ВНИМАНИЕ!\n"
                            "Совпадение с активными бронированиями:*")

    main_callback = "Главное меню"

    start_book_button = "Начать бронирование"
    start_book_button_callback = "Бронирование"

    list_button = "Список бронирований"
    list_button_callback = "Список бронирований"

    details_button_callback = "Информация по бронированию"

    cancel_button = "❌ Отменить бронирование"
    cancel_button_callback = "Бронирование отменено"

    notify_button = "ℹ️ Оповестить"
    notify_button_callback = "Оповещение отправлено"
    notify_message = ("Обратитесь к админстратору для уточнения информации"
                      " по бронированию")

    icon_set = "\u23f1"
    set_button = f"{icon_set} Сет"

    set_button_callback = "Выберите количество сетов"

    icon_hour = "\u23f0"
    hour_button = f"{icon_hour} Час"
    hour_button_callback = "Выберите количество часов"

    apply_text = "Забронировать"
    apply_button = f"👌 {apply_text}"
    apply_button_callback = "Бронь внесена"
    apply_error_callback = "Ошибка бронирования"

    message_header = "*Бронирование*"

    type_label = "*Услуга:*"
    date_label = "*Дата:*"
    count_label = "*Количество:*"
    count_button = "Количество"
    count_button_callback = "Выберите количество"

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
    board_button_callback = "Аренда вейкборда"

    icon_hydro = "👙"
    hydro_text = "Гидрокостюм"
    hydro_button = f"{icon_hydro} {hydro_text}"
    hydro_button_callback = "Аренда гидрокостюма"


class RuSupboard:
    hello_message = ("*Сапборд - современно и душевно!*"
                     "\nРекомендуем перед бронированием посмотреть список"
                     " активных бронирований.")
    supboard_text = "Сапборд"


class RuGeneral:
    default = RuDefault
    reserve = RuReserve
    wake = RuWake
    supboard = RuSupboard

    parse_mode = ParseMode.MARKDOWN

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
    hour_button_callback = "Выберите часы"
    minute_button_callback = "Выберите минуты"

    back_button = "Назад"

    name_text = "Имя"
    name_label = f"*{name_text}:*"

    count_label = "*Количество:*"


if __name__ == "__main__":
    DefaultProcessor, ReserveProcessor, WakeProcessor, SupboardProcessor
