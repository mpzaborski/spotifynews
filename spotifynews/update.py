from .database.sqlite3db import Sqlite3db
from .spotify.client import Client, chunk_playlist


def news(database_f, original_playlist_id):
    db = Sqlite3db(database_f=database_f)
    client = Client()
    known_track_ids = db.select_songs(playlist_id=original_playlist_id)
    mirror_playlist_item_ids = client.update_mirror_playlist(original_playlist_id=original_playlist_id,
                                                             known_track_ids=known_track_ids,
                                                             playlist_part_name='news')
    db.insert_songs(playlist_id=original_playlist_id, song_ids=mirror_playlist_item_ids)
    return mirror_playlist_item_ids


def collections(database_f, original_playlist_id):
    db = Sqlite3db(database_f=database_f)
    client = Client()
    known_track_ids = db.select_songs(playlist_id=original_playlist_id)
    playlist_id = client.get_mirror_playlist_id(original_playlist_id=original_playlist_id,
                                                playlist_part_name='complete')
    client.playlist_remove_all_items(playlist_id=playlist_id)

    for chunk in chunk_playlist(known_track_ids):
        client.playlist_add_items(playlist_id=playlist_id, items=chunk)
    return known_track_ids
