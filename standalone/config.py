from wakebot.processors import RuDefault, RuReserve, RuGeneral
from wakebot.processors import RuWake, RuSupboard


class GeneralStrings(RuGeneral):

    company_name = "WAKEPLAZA"
    admin_phone_number = "922-111"


class DefaultStrings(RuDefault):

    help_message = (
        "*Список команд*"
        "\n/wake - бронирование Вейкборда"
        "\n/sup - бронирование проката Сапборда"
        "\n/start - приветствие"
        "\n/help - справка по командам бота"
        "\n\nВ случае необходимости, Вы всегда можете связаться"
        f"с администратором *{GeneralStrings.company_name}* "
        f"по телефону: *{GeneralStrings.admin_phone_number}*")

    start_message = (
        "*Привет!*\n"
        "Это наш новый сервис для бронирования услуг вейк-станции. "
        "Сейчас он находится в процессе тестирования, "
        f"но вполне работоспособен.\n\n{help_message}")


class ReserveStrings(RuReserve):

    notify_message = (
        "Для подтверждения бронирования просим Вас "
        f"связаться с администратором *{GeneralStrings.company_name}* "
        f"{RuReserve.icon_phone}*{GeneralStrings.admin_phone_number}*.")


class WakeStrings(RuWake):

    notify_message = ReserveStrings.notify_message


class SupboardStrings(RuSupboard):

    notify_message = ReserveStrings.notify_message
