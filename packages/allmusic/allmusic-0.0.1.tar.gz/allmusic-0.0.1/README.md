# AllMusic

![build status](https://travis-ci.org/fortes/allmusic.svg?branch=master)

An unofficial scraper [AllMusic](https://allmusic.com) reviews.

## Installation

```sh
pip install allmusic
```

Alternatively, clone directly from `master` to run with the freshest bugs:

```sh
pip install git+git://github.com/fortes/allmusic.git@master
```

## Usage

```
>>> import allmusic
>>> review = allmusic.getAlbumReviewForAllMusicUrl('https://www.allmusic.com/album/beauty-and-the-beat-mw0000736440')
>>> print(review.album)
'Beauty and the Beat'
>>> print(review.rating)
9
```

## Tests

There is one test, you can try it:

```bash
python -m unittest
```

## License

MIT

## Contributions

Please do
