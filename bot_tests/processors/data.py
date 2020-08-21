from wakebot.entities import User

users = []
users.append(User(firstname="AdminName1", is_admin=True,
             telegram_id=101, phone_number="+7101"))
users.append(User(firstname="UserName1", is_admin=False,
             telegram_id=201, phone_number="+7201"))
users.append(User(firstname="UserName2", is_admin=False,
             telegram_id=202, phone_number="+7202"))
users.append(User(firstname="UserName3", is_admin=False,
             telegram_id=203, phone_number="+7203"))
users.append(User(firstname="AdminName2", is_admin=True,
             telegram_id=102, phone_number="+7102"))
