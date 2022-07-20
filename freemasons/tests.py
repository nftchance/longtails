from django.test import TestCase

from freemasons.models import FreeMasonProject

class FreeMasonsTestCase(TestCase):
    def setUp(self):
        self.project, self.created = FreeMasonProject.objects.get_or_create(
            contract_address="0x23581767a106ae21c074b2276d25e5c3e136a68b"
        )

    def test_sync(self):
        """ Can pull down collection members from data source"""
        sync_response = self.project.sync()
        self.assertEqual(sync_response['status'], 200)