spotifynews
===========

Python library for creating news and collections


.. image:: https://img.shields.io/pypi/v/spotifynews.svg
    :target: https://pypi.org/project/spotifynews/
    :alt: Latest Version

.. image:: https://readthedocs.org/projects/spotifynews/badge/?version=latest
    :target: https://spotifynews.readthedocs.io/en/latest/
    :alt: Latest Docs

.. image:: https://github.com/mpzaborski/spotifynews/workflows/CI/badge.svg?branch=feature/add-badges
    :target: https://github.com/mpzaborski/spotifynews/actions?query=branch%3Amaster

Description
~~~~~~~~~~~

[Spotifynews](https://github.com/mpzaborski/spotifynews) is a wrapper on [spotipy](https://github.com/plamere/spotipy)
that provides new more complex functionalities: news and collections. It also
extends spotipy with additional functions that aim to simplify spotipy usage.

Installation
~~~~~~~~~~~~

```bash
pip install spotifynews
```

or upgrade

```bash
pip install spotifynews --upgrade
```

Quick Start
~~~~~~~~~~~

More information about spotifynews can be found in the
[spotifynews documentation](https://spotifynews.readthedocs.io/en/latest).

More information about spotipy can be found in the
[spotipy documentation](https://spotipy.readthedocs.io/en/latest).

To get started, install spotifynews and create an app on https://developers.spotify.com/.
Add your new SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET to your environment.
After script run for the first time authorize on spotify webpage by logging and allowing scope playlist-modify-public.

News
****

This functionality accumulates song from source playlist in local database and based on that it is able to notice truly
new tracks, because new trucks are not yet in database. If this situation occurs, it creates clone of original playlist
with only new tracks.

To utilize this functionality run script once a week and enjoy new hits from your favorite playlist :coffee:

.. code-block:: pycon
    from spotifynews.update import news
    todays_top_hits_id = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
    news(database_f="test.db", original_playlist_id=todays_top_hits_id)

Collections
***********

This functionality creates playlist from all songs stored from source playlist in local database (songs which were
stored after 'news' function call). If you follow a playlist with 50 songs, which rotates 3 new songs per week, after
a year your clone playlist collection will have 86 tracks.

.. code-block:: pycon
    from spotifynews.update import collections
    todays_top_hits_id = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
    collections(database_f="test.db", original_playlist_id=todays_top_hits_id)
