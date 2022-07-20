from django.test import TestCase

from freemasons.models import FreeMasonProject
from twitter.client import TwitterClient

class FreeMasonsTestCase(TestCase):
    def setUp(self):
        self.project, self.created = FreeMasonProject.objects.get_or_create(
            contract_address="0x23581767a106ae21c074b2276d25e5c3e136a68b"
        )
        
        self.twitter_client = TwitterClient()

    def test_sync(self):
        """ Pull down collection members from data source """
        sync_response = self.project.sync()
        self.assertEqual(sync_response['status'], 200)
        self.assertNotEqual(self.project.members.count(), 0)

    def test_member_sync(self):
        """ Update the base level stats of a Member with its Twitter stats """
        sync_response = self.project.members.first().sync()
        self.assertEqual(sync_response['status'], 200)

    def test_member_sync_wallet(self):
        """ Make sure the wallet of the token owner was updated """
        self.assertNotEqual(self.project.members.filter(wallet_address__isnull=False).count(), 0)

    # def test_twitter_followers(self):
    #     print(self.twitter_client.get_friends("nftchance"))
    #     self.assertEqual('', '') 