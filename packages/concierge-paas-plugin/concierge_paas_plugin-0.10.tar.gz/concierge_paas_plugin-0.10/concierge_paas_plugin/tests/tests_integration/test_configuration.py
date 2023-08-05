from django.test import TransactionTestCase
from concierge_paas_plugin.models import Configuration

class CreateProfileTest(TransactionTestCase):
    def setUp(self):
        self.configuration = Configuration(token='sometoken', end_point="http://localhost:8001/protected", default=True)
        self.configuration.save()
    def test_createBasicProfile(self):
        previously_createdConfiguration = Configuration.objects.get(default=True)
        self.assertEqual(previously_createdConfiguration.end_point, self.configuration.end_point)