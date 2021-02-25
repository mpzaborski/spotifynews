from .database.sqlite3db import Sqlite3db
from .spotify.client import Client


def news(database_f, original_playlist_id):
    db = Sqlite3db(database_f=database_f)
    client = Client()
    known_track_ids = db.select_songs(playlist_id=original_playlist_id)
    mirror_playlist_item_ids = client.update_mirror_playlist(original_playlist_id=original_playlist_id,
                                                             known_track_ids=known_track_ids,
                                                             playlist_part_name='news')
    if not mirror_playlist_item_ids:
        return False
    db.insert_songs(playlist_id=original_playlist_id, song_ids=mirror_playlist_item_ids)
    return True


def collections(database_f, original_playlist_id):
    db = Sqlite3db(database_f=database_f)
    client = Client()
    known_track_ids = db.select_songs(playlist_id=original_playlist_id)
    playlist_id = client.get_mirror_playlist_id(original_playlist_id=original_playlist_id,
                                                playlist_part_name='complete')
    client.playlist_remove_all_items(playlist_id=playlist_id)
    client.playlist_add_items(playlist_id=playlist_id, items=known_track_ids)
