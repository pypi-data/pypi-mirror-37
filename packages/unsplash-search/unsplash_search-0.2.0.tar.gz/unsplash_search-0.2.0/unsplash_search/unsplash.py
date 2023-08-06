import requests
import random
from log3 import log


class UnsplashSearch(object):
    """ Retrieve free photos from the official Unsplash API

    Args:
        access_key (str): Your access_key. You can find this in the app developer page.
    """

    def __init__(self, access_key):

        self.access_key = access_key
        self.ses = requests.Session()
        self.ses.headers.update({'Authorization': "Client-ID {}".format(access_key)})

        self.base_endpoint = "https://api.unsplash.com/"
        self.search_photos_endpoint = "/search/photos"

    def search_photo(self, query):
        """ Search for photos using a query.

        Args:
            query (str): The query you want to use to retrieve the photos

        Returns:
            img (tuple): Tuple containing the img URL, and instagram username

        """

        params = {
            'query': query,
            'per_page': '50'
        }
        try:
            resp = self.ses.get(self.base_endpoint+self.search_photos_endpoint, params=params)

        except requests.RequestException as ex:
            log.error('STATUS: {}  TEXT: {}'.format(ex.response.status_code, ex.response))

        else:
            data = resp.json()
            log.success('DATA: {}'.format(data))

            # Choose a random image
            rand_img = random.randint(0, len(data['results']))
            insta_user = data.get('results')[rand_img].get('user').get('instagram_username')

            regular_image = data['results'][rand_img]['urls']['regular']

            img = {
                'img': regular_image,
                'credits': insta_user
            }

            return img









