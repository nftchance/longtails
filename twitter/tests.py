from django.test import TestCase

from twitter.client import TwitterClient

class TwitterClientTestCase(TestCase):
    def setUp(self):
        self.client = TwitterClient()
    
    def test_twitter_username_to_id(self):
        self.assertNotEqual(
            len(self.client.get_username_ids(['nftchance'])),
            0
        ) 

    def test_twitter_followers(self):
        self.assertNotEqual(
            len(self.client.get_followers("1355981457710329860")),
            0
        )

    def test_twitter_following(self):
        self.assertNotEqual(
            len(self.client.get_following("1355981457710329860")),
            0
        )

    def twitter_likes(self):
        self.assertNotEqual(
            len(self.client.get_likes("1355981457710329860")),
            0
        ) 