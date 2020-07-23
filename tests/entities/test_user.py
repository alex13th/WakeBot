# -*- coding: utf-8 -*-
import unittest

from wakebot.entities.user import User


class UserTestCase(unittest.TestCase):
    """Тесты модуля произвольного резервирования """

    def test_create_properties(self):
        user = User("Firstname", "Lastname", "Middlename",
                    "Displayname", "+7999555443322", 9876, 3456)

        self.assertEqual(user.firstname, "Firstname")
        self.assertEqual(user.lastname, "Lastname")
        self.assertEqual(user.middlename, "Midlename")
        self.assertEqual(user.displayname, "Displayname")
        self.assertEqual(user.phone_number, "+7999555443322")
        self.assertEqual(user.telegram_id, 9876)
        self.assertEqual(user.user_id, 3456)

    def test_diplay_name_full(self):
        """Формирование отображаемого имени с отчеством"""
        user = User("Firstname", "Lastname", "Middlename",
                    "+7999555443322", 9876, 3456)
        self.assertEqual(user.displayname, "Lastname Firstname Middlename")

    def test_diplay_name_without_middlename(self):
        """Формирование отображаемого имени без отчества"""
        user = User("Firstname", "Lastname")
        self.assertEqual(user.displayname, "Lastname Firstname")

    def test_diplay_name_without_lastname(self):
        """Формирование отображаемого имени без фамилии"""
        user = User("Firstname", None, "Middlename")
        self.assertEqual(user.displayname, "Firstname Middlename")

    def test_diplay_name_firstname_only(self):
        """Формирование отображаемого имени только из имени"""
        """Формирование отображаемого имени без фамилии"""
        user = User("Firstname")
        self.assertEqual(user.displayname, "Firstname Middlename")

    def test_to_str(self):
        """Строка"""
        user = User("Firstname", "Lastname", "Middlename",
                    "Displayname", "+7999555443322", 9876, 3456)

        self.assertEqual(str(user), "Lastname Firstname Middlename (tg:9876)")


try:
    unittest.main()
except SystemExit:
    pass
