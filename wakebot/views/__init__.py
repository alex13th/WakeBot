from aiogram.types import ParseMode
# from .reserve import ReserveTelegramView


class TelegramStrings():
    parse_mode = ParseMode.MARKDOWN


class ReserveTelegramStrings(TelegramStrings):
    hello_message = "Reservation service main menu"
    service_text = "Service"
    service_label = f"*{service_text}:*"
    service_type_text = "Reservation"

    list_header = "*Booking list:*"
    list_empty = "Booking list is empty"
    list_footer = ("Please click reservation number button "
                   "to get details")

    icon_stop = "⛔️"
    restrict_list_header = (f"{icon_stop} *WARNING!\n"
                            "Reservation has concurrents:*")

    main_callback = "Main menu"

    back_text = "Back"
    back_button = back_text

    booking_text = "Booking"
    book_header = f"*{booking_text}*"
    start_book_button = f"Start {booking_text.lower()}"
    start_book_button_callback = booking_text

    phone_regex = "^\\+[7]\\s?[-\\(]?\\d{3}\\)?[- ]?\\d{3}-?\\d{2}-?\\d{2}$"
    icon_phone = "📞"
    phone_text = "Phone number"
    phone_label = f"*{phone_text}:*"
    phone_button = f"{icon_phone} Send {phone_text.lower()}"
    phone_button_callback = f"Enter {phone_text.lower()}"
    phone_message = (
        f"*Acceptable {phone_text} formats:*"
        "\n+79103123167"
        "\n+7-910-221-22-22"
        "\n+7 (910) 221-22-22"
        "\n+7(910) 221-22-22"
        "\n+7 (910)-221-22-22"
        "\n+7(910)-221-22-22")
    phone_success_message = f"{phone_text} accepted"
    phone_error_message = (
        f"{icon_stop} *{phone_text} has wrong format*"
        f"\n\n{phone_message}")
    phone_warning = f"⚠️ {phone_text} required."
    date_format = "%d.%m.%Y"
    date_text = "Date"
    date_label = f"*{date_text}:*"
    date_button = f"Choose {date_text}"
    date_button_callback = date_button

    time_format = "%H:%M"
    time_zone = 0
    time_text = "Time"
    hour_text = "Hour"
    minute_text = "Minute"
    time_button = f"Choose {time_text.lower()}"
    time_button_callback = f"Choose {hour_text.lower()}"
    hour_button_callback = f"Choose {hour_text.lower()}s"
    minute_button_callback = f"Choose {hour_text.lower()}s"
    start_label = f"*Start {time_text.lower()}:*"
    end_label = f"*End {time_text.lower()}:*"

    name_text = "Name"
    name_label = f"*{name_text}:*"

    admin_text = "Adminitsrator"
    admin_label = f"*{admin_text}:*"

    count_text = "Count"
    count_label = f"*{count_text}:*"
    count_button = f"{count_text}"
    count_button_callback = f"Choose {count_text.lower()}"

    list_text = f"{booking_text}s list"
    list_button = list_text
    list_button_callback = list_text

    details_button_callback = "Booking information"

    cancel_button = f"❌ Cancel {booking_text.lower()}"
    cancel_button_callback = f"{booking_text} is canceled"
    cancel_notify_header = f"❌ *{booking_text} is canceled*"

    notify_text = "Notify"
    notification_text = "Notification"
    notify_button = f"ℹ️ {notify_text}"
    notify_button_callback = f"{notification_text} is sent"
    notify_message = "Booking needs to be confirmed"

    options_text = "Options"
    options_label = f"*{options_text}:*"

    icon_set = "\u23f1"
    set_text = "Set"
    sets_text = f"{set_text}s"
    set_button = f"{icon_set} {set_text}"
    set_button_callback = f"Choose {count_text.lower()} {sets_text.lower()}"

    icon_hour = "\u23f0"
    hour_button = f"{icon_hour} {hour_text}"
    hour_button_callback = (f"Choose {count_text.lower()} of "
                            f"{hour_text.lower()}s")

    set_type_text = "Set type"
    set_type_label = f"*{set_text}:*"
    set_types = {}
    set_types["set"] = set_text
    set_types["hour"] = hour_text

    apply_text = "Book"
    apply_button = f"👌 {apply_text}"
    apply_button_callback = f"{booking_text} applied"
    apply_error_callback = "Booking error"
    apply_header = ""
    apply_footer = ""


class RuReserveTelegramStrings(ReserveTelegramStrings):
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
        f"\n\n{phone_message}")
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
    apply_header = ""
    apply_footer = ""


# if __name__ == "__main__":
#     ReserveTelegramView
