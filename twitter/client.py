import requests
import time

from django.conf import settings

USER_HEAD = "https://api.twitter.com/2/users/"
TWEETS_HEAD = "https://api.twitter.com/2/tweets/"

URLS = {
    "USERNAME_TO_ID": USER_HEAD + "by/username/{0}",
    "USERNAMES_TO_ID": USER_HEAD + "by?usernames={0}",
    "FOLLOWERS": USER_HEAD + "{0}/followers",
    "FOLLOWING": USER_HEAD + "{0}/following",
    "LIKES": USER_HEAD + "{0}/liked_tweets",
    "RETWEETS": TWEETS_HEAD + "{0}/retweeted_by"
}


class TwitterClient:
    """
    Client that enables the ability to interface with the Twitter API with ease.

    Must have acecss to the Twitter API.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers = {
            'Authorization': f'Bearer {settings.TWITTER_BEARER_TOKEN}',
        }

    def handle_request(self, url):
        print('handling request', url)
        return requests.get(
            url,
            headers=self.headers
        )

    def handle_response(self, response):
        print('handling response', response.json())

        time.sleep(5)

        if response.status_code == 200:
            return response.json()['data']

        return {} 

    def get_username_ids(self, usernames):
        response = self.handle_request(
            URLS["USERNAMES_TO_ID"].format(','.join(usernames)))
        return self.handle_response(response)

    def get_followers(self, user_id):
        response = self.handle_request(URLS["FOLLOWERS"].format(user_id))
        return self.handle_response(response)

    def get_following(self, user_id):
        response = self.handle_request(URLS["FOLLOWING"].format(user_id))
        return self.handle_response(response)

    def get_likes(self, user_id):
        response = self.handle_request(URLS["LIKES"].format(user_id))
        return self.handle_response(response)

    def get_retweets(self, user_id):
        response = self.handle_request(URLS["RETWEETS"].format(user_id))
        return self.handle_response(response)
