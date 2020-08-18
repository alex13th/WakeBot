# -*- coding: utf-8 -*-
from ..base_test_case import BaseTestCase
from wakebot.entities import User


class UserTestCase(BaseTestCase):
    """Тесты класса данных пользователя """

    async def test_create_properties(self):
        user = User("Firstname", "Lastname", "Middlename",
                    "Displayname", "+7999555443322", 9876, 3456)

        passed, alert = self.assert_params(user.firstname, "Firstname")
        assert passed, alert
        passed, alert = self.assert_params(user.lastname, "Lastname")
        assert passed, alert
        passed, alert = self.assert_params(user.middlename, "Middlename")
        assert passed, alert
        passed, alert = self.assert_params(user.displayname, "Displayname")
        assert passed, alert
        passed, alert = self.assert_params(user.phone_number, "+7999555443322")
        assert passed, alert
        passed, alert = self.assert_params(user.telegram_id, 9876)
        assert passed, alert
        passed, alert = self.assert_params(user.user_id, 3456)
        assert passed, alert

    async def test_set_properties(self):
        user = User("Firstname")
        user.firstname = "Newname"
        user.lastname = "Lastname1"
        user.middlename = "Middlename1"
        user.displayname = "Displayname1"
        user.phone_number = "+7999555443311"
        user.telegram_id = 1234
        user.user_id = 9876

        passed, alert = self.assert_params(user.firstname, "Newname")
        assert passed, alert
        passed, alert = self.assert_params(user.lastname, "Lastname1")
        assert passed, alert
        passed, alert = self.assert_params(user.middlename, "Middlename1")
        assert passed, alert
        passed, alert = self.assert_params(user.displayname, "Displayname1")
        assert passed, alert
        passed, alert = self.assert_params(user.phone_number, "+7999555443311")
        assert passed, alert
        passed, alert = self.assert_params(user.telegram_id, 1234)
        assert passed, alert
        passed, alert = self.assert_params(user.user_id, 9876)
        assert passed, alert

    async def test_diplay_name_full(self):
        """Формирование отображаемого имени с отчеством"""
        user = User("Firstname", "Lastname", "Middlename",
                    None, "+7999555443322", 9876, 3456)
        passed, alert = self.assert_params(user.displayname,
                                           "Lastname Firstname Middlename")
        assert passed, alert

    async def test_diplay_name_without_middlename(self):
        """Формирование отображаемого имени без отчества"""
        user = User("Firstname", "Lastname")
        passed, alert = self.assert_params(user.displayname,
                                           "Lastname Firstname")
        assert passed, alert

    async def test_diplay_name_without_lastname(self):
        """Формирование отображаемого имени без фамилии"""
        user = User("Firstname", None, "Middlename")
        passed, alert = self.assert_params(user.displayname,
                                           "Firstname Middlename")
        assert passed, alert

    async def test_diplay_name_firstname_only(self):
        """Формирование отображаемого имени только из имени"""
        """Формирование отображаемого имени без фамилии"""
        user = User("Firstname")
        passed, alert = self.assert_params(user.displayname, "Firstname")
        assert passed, alert

    async def test_to_str(self):
        """Строка"""
        user = User("Firstname", "Lastname", "Middlename",
                    None, "+7999555443322", 9876, 3456)

        passed, alert = self.assert_params(str(user),
                                           "Lastname Firstname Middlename")
        assert passed, alert
