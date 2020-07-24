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
        self.assertEqual(user.middlename, "Middlename")
        self.assertEqual(user.displayname, "Displayname")
        self.assertEqual(user.phone_number, "+7999555443322")
        self.assertEqual(user.telegram_id, 9876)
        self.assertEqual(user.user_id, 3456)

    def test_set_properties(self):
        user = User("Firstname")
        user.firstname = "Newname"
        user.lastname = "Lastname1"
        user.middlename = "Middlename1"
        user.displayname = "Displayname1"
        user.phone_number = "+7999555443311"
        user.telegram_id = 1234
        user.user_id = 9876

        self.assertEqual(user.firstname, "Newname")
        self.assertEqual(user.lastname, "Lastname1")
        self.assertEqual(user.middlename, "Middlename1")
        self.assertEqual(user.displayname, "Displayname1")
        self.assertEqual(user.phone_number, "+7999555443311")
        self.assertEqual(user.telegram_id, 1234)
        self.assertEqual(user.user_id, 9876)

    def test_diplay_name_full(self):
        """Формирование отображаемого имени с отчеством"""
        user = User("Firstname", "Lastname", "Middlename",
                    None, "+7999555443322", 9876, 3456)
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
        self.assertEqual(user.displayname, "Firstname")

    def test_to_str(self):
        """Строка"""
        user = User("Firstname", "Lastname", "Middlename",
                    None, "+7999555443322", 9876, 3456)

        self.assertEqual(str(user), "Lastname Firstname Middlename")


try:
    unittest.main()
except SystemExit:
    pass
