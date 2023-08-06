import extruct
import requests
import w3lib.html

SCHEMA_RATING_URL = "https://schema.org/Rating"
SCHEMA_MUSIC_ALBUM_URL = "https://schema.org/MusicAlbum"
SCHEMA_MUSIC_GROUP_URL = "https://schema.org/MusicGroup"
SCHEMA_REVIEW_URL = "https://schema.org/Review"


class AlbumReview:
    """
    Class representing the fetched review

    Includes the following fields:
    - artist
    - name
    - rating
    - review_url
    - review_author
    - review_body
    """

    def __init__(self, microdata):
        for data in microdata:
            type = data.get('type')
            properties = data.get('properties')

            if not type or not properties:
                continue

            if type == SCHEMA_RATING_URL:
                self.rating = int(properties.get('ratingValue'))
                continue

            if type == SCHEMA_MUSIC_ALBUM_URL:
                self.review_url = properties.get('url')
                self.name = properties.get('name')

                artist = properties.get('byArtist')
                if artist and artist.get('type') == SCHEMA_MUSIC_GROUP_URL:
                    artist_properties = artist.get('properties')
                    if artist_properties:
                        self.artist = artist_properties.get('name')

                review = properties.get('review')
                if review and review.get('type') == SCHEMA_REVIEW_URL:
                    review_properties = review.get('properties')
                    if review_properties:
                        self.review_author = review_properties.get('author')
                        self.review_body = review_properties.get('reviewBody')
                    else:
                        print('no review properties')
                else:
                    print('no review found')


def isValidAllMusicAlbumReviewUrl(url):
    return True


def fetchAlbumReviewHTML(url):
    if not isValidAllMusicAlbumReviewUrl(url):
        raise ValueError('Invalid AllMusic album url')

    headers = {'User-Agent': 'AllMusic Python Scraper'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise IndexError(
            'Non-200 status code from Allmusic %s' % r.status_code)

    return r.text


def getAlbumReviewForAllMusicUrl(url):
    """
    Get `AlbumReview` object for an AllMusic review URL
    """
    html = fetchAlbumReviewHTML(url)
    base_url = w3lib.html.get_base_url(html, url)
    data = extruct.extract(html, base_url=base_url)
    microdata = data.get('microdata')
    if not microdata:
        raise IndexError('No microdata found in URL: %s' % url)

    return AlbumReview(microdata)
