from django.test import TransactionTestCase
from concierge_paas_plugin.api import create_profile, queryprofile, disableProfile
from concierge_paas_plugin.models import Configuration


class CreateProfileTest(TransactionTestCase):
    def setUp(self):
        self.configuration = Configuration(token='045d5617bbbd13c523be1fa6b86486e3c8a57b00', end_point="http://localhost:8001/protected", default=True, trigger=True)
        self.configuration.save()

        self.userId = 123456
        self.username = "custom_username"
        self.email = self.username + '@sometest.com'

        response = create_profile(self.userId, self.username, self.email)
        self.assertIsNotNone(response)

    def tearDown(self):
        disableProfile(self.userId)

    def test_createBasicProfile(self):
        response = queryprofile(self.userId)
        self.assertTrue(self.username in str(response))

    def test_userAlreadyExist(self):
        response = create_profile(self.userId, self.username, self.email)
        self.assertIsNone(response)
