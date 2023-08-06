import requests
import unittest
from unittest import mock

import allmusic


class TestAlbumReview(unittest.TestCase):
    # This is the only test that actually makes a request to allmusic.com
    def test_live_request(self):
        review = allmusic.getAlbumReviewForAllMusicUrl(
            'https://www.allmusic.com/album/mw0002927433')
        self.assertEqual(review.artist, 'The Kills')
        self.assertEqual(review.name, 'Ash & Ice')
        self.assertEqual(review.rating, 7)
        self.assertEqual(
            review.review_url,
            'https://www.allmusic.com/album/ash-ice-mw0002927433')
        self.assertEqual(review.review_author, 'Heather Phares')
        pass


if __name__ == '__main__':
    unittest.main()
