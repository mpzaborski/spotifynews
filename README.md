# spotifynews

<p float="left">
  <img src="https://github.com/mpzaborski/spotifynews/blob/master/docs/images/news.jpg" width="400" />
  <img src="https://github.com/mpzaborski/spotifynews/blob/master/docs/images/collections.jpg" width="400" />
</p>

##### Python library for creating news and collections

![workflow name](https://github.com/mpzaborski/spotifynews/workflows/Python%20package/badge.svg)

## Description

[Spotifynews](https://github.com/mpzaborski/spotifynews) is a wrapper on [spotipy](https://github.com/plamere/spotipy)
that provides new more complex functionalities: [news](#news-anchor) and [collections](#collections-anchor). It also
extends spotipy with additional functions that aim to simplify spotipy usage.

## Installation

```bash
pip install spotifynews
```

or upgrade

```bash
pip install spotifynews --upgrade
```

## Quick Start

To get started, install spotifynews and create an app on https://developers.spotify.com/.
Add your new SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET to your environment.
After script run for the first time authorize on spotify webpage by logging and allowing scope playlist-modify-public.

### <a name="news-anchor"></a>News

This functionality accumulates song from source playlist in local database and based on that it is able to notice truly
new tracks, because new trucks are not yet in database. If this situation occurs, it creates clone of original playlist
with only new tracks.

To utilize this functionality run script once a week and enjoy new hits from your favorite playlist :coffee:

```python
from spotifynews.update import news
todays_top_hits_id = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
news(database_f="test.db", original_playlist_id=todays_top_hits_id)
```

### <a name="collections-anchor">Collections

This functionality creates playlist from all songs stored from source playlist in local database (songs which were
stored after 'news' function call). If you follow a playlist with 50 songs, which rotates 3 new songs per week, after
a year your clone playlist collection will have 86 tracks.

```python
from spotifynews.update import collections
todays_top_hits_id = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
collections(database_f="test.db", original_playlist_id=todays_top_hits_id)
```
