from aiogram.types import ParseMode


class Icons:
    stop: str = "⛔️"
    cancel: str = "❌"
    phone: str = "📞"
    warning: str = "⚠️"
    ok: str = "👌"


class BookStrings:
    text: str = "Бронирование"
    text_plural: str = "Бронирований"
    header: str = f"*{text}*"
    button: str = f"Начать {text.lower()}"
    button_callback: str = text


class ListStrings:
    header: str = "*Список бронирований:*"
    header_warn: str = (f"{Icons.stop} *ВНИМАНИЕ!\n"
                        "Совпадение с активными бронированиями:*")
    footer: str = ("Для получения дополнительной информации, "
                   "нажмите на кнопку с номером бронирования")
    empty: str = "На текущий момент нет активных бронирований"


class PhoneStrings:
    regex: str = "^\\+[7]\\s?[-\\(]?\\d{3}\\)?[- ]?\\d{3}-?\\d{2}-?\\d{2}$"
    text: str = "Телефон"
    label: str = f"*{text}:*"
    button: str = f"{Icons.phone} Внести {text}"


class ServiceStrings:
    text: str = "Услуга"
    label: str = f"*{text}:*"
    type_name: str = "Бронирование"


class UserStrings:
    name: str = "Имя"
    label: str = f"*{name}:*"


class DateStrings:
    template: str = "%d.%m.%Y"
    text: str = "Дата"
    label: str = f"*{text}:*"
    button: str = "Выбрать дату"
    button_callback: str = "Выберите дату"


class TimeStrings:
    template: str = "%H:%M"
    zone: int = +9
    text: str = "Время"
    hour: str = ""
    label_start: str = f"*{text} начала:*"
    label_end: str = f"*{text} окончания:*"


class DefaultConfig:
    parse_mode = ParseMode.MARKDOWN
    icons = Icons

    book = BookStrings
    list = ListStrings
    phone = PhoneStrings
    service = ServiceStrings
    user = UserStrings
    date = DateStrings
