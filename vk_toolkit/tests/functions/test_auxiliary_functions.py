from unittest import TestCase

from vk_toolkit.access_token import access_token
from vk_toolkit.functions.auxiliary_functions import getMembersCount


class TestGetMembersCount(TestCase):
    def test_getMembersCount(self):
        print("Group number is: " + str(getMembersCount("1", access_token)))
        self.assertIsInstance(getMembersCount("1", access_token), int)