from unittest import TestCase

from vk_toolkit.access_token import access_token
from vk_toolkit.functions.main_functions import getVkGroupMembers, getVkIdsNames
from vk_toolkit.functions.auxiliary_functions import getMembersCount


class TestGetVkGroupMembers(TestCase):
    def test_getVkGroupMembers(self):
        self.assertEqual(len(getVkGroupMembers("1", access_token)), getMembersCount("1", access_token))


class TestGetVkIdsNames(TestCase):
    def test_getVkIdsNames(self):
        self.assertEqual(getVkIdsNames(["436263673"], access_token)["name"].values, ["Vladislav"])
        self.assertEqual(getVkIdsNames(["436263673"], access_token)["surname"].values, ["Akatov"])
