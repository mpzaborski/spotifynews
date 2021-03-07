# -*- coding: utf-8 -*-

""" Python library for operations with Spotify Web API and database """

from .database.sqlite3db import Sqlite3db
from .spotify.client import Client, chunk_playlist


def news(database_f, original_playlist_id):
    """ Accumulate song from source playlist in local database and based
        on that find new tracks, which are not yet in database.
        If this situation occurs, create clone of original playlist.

        :param database_f: name of sqlite3db file. It will be created if does not exist
        :param original_playlist_id: playlist ID, URI or URL
        :return: A list of track IDs
    """
    db = Sqlite3db(database_f=database_f)
    client = Client()
    known_track_ids = db.select_songs(playlist_id=original_playlist_id)
    mirror_playlist_item_ids = client.update_mirror_playlist(original_playlist_id=original_playlist_id,
                                                             known_track_ids=known_track_ids,
                                                             playlist_part_name='news')
    db.insert_songs(playlist_id=original_playlist_id, song_ids=mirror_playlist_item_ids)
    db.close()
    return mirror_playlist_item_ids


def collections(database_f, original_playlist_id):
    """ Get accumulated songs from local database and based
        on that create clone of original playlist with all tracks.

        :param database_f: name of sqlite3db file. It will be created if does not exist
        :param original_playlist_id: playlist ID, URI or URL
        :return: A list of track IDs
    """
    db = Sqlite3db(database_f=database_f)
    client = Client()
    known_track_ids = db.select_songs(playlist_id=original_playlist_id)
    playlist_id = client.get_mirror_playlist_id(original_playlist_id=original_playlist_id,
                                                playlist_part_name='complete')
    client.playlist_remove_all_items(playlist_id=playlist_id)

    for chunk in chunk_playlist(known_track_ids):
        client.playlist_add_items(playlist_id=playlist_id, items=chunk)
    db.close()
    return known_track_ids
