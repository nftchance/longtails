import requests

from django.conf import settings

URL_HEAD = "https://api.twitter.com/2/users/"

URLS = {
    "USERNAME_TO_ID": URL_HEAD + "by/username/{0}",
    "USERNAMES_TO_ID": URL_HEAD + "by?usernames={0}",
    "FOLLOWERS": URL_HEAD + "{0}/followers",
    "FOLLOWING": URL_HEAD + "{0}/following",
    "LIKES": URL_HEAD + "{0}/liked_tweets"
}

class TwitterClient:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.headers = {
            'Authorization': f'Bearer {settings.TWITTER_BEARER_TOKEN}',
            'Cookie': 'guest_id=v1%3A165835497646227262'
        }

    def handle_request(self, url):
        return requests.get(
            url,
            headers=self.headers
        )

    def handle_response(self, response):
        if response.status_code == 200:
            return response.json()['data']

        return {}

    def get_username_ids(self, usernames):
        response = self.handle_request(URLS["USERNAMES_TO_ID"].format(','.join(usernames)))
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