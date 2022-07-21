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
        print('Built', self.project.members.count(), 'members.')
        self.assertNotEqual(self.project.members.count(), 0)

    def test_member_sync(self):
        """ Update the base level stats of a Member with its Twitter stats """
        member_obj = self.project.members.first()
        
        sync_response = member_obj.sync(self.twitter_client)
        self.assertEqual(sync_response['status'], 200)

        self.assertNotEqual(member_obj.followers.count(), 0)
        self.assertNotEqual(member_obj.following.count(), 0)
        self.assertNotEqual(self.project.members.filter(
            wallet_address__isnull=False).count(), 0)

    def test_member_summary(self):
        """ Get the compiled results of the recent follows. """
        summary = self.project.member_follower_summary
        self.assertNotEqual(summary, [])
        self.assertNotEqual(summary[0]['overlap_count'], 0)