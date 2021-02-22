import pytest

from spotifynews.database.sqlite3db import Sqlite3db


@pytest.fixture()
def database_fixture(tmp_path):
    database = Sqlite3db(database_f=tmp_path / "test.db")
    yield database
    database.close()


def test_insert_select_db(database_fixture):
    song_id = "spotify:track:51Dae1jpRALuKCnR9LofRZ"
    playlist_id = "spotify:playlist:37i9dQZF1DX3qCx5yEZkcJ"
    database_fixture.insert_song(playlist_id=playlist_id, song_id=song_id)
    db_song_ids = database_fixture.select_songs(playlist_id=playlist_id)
    assert song_id in db_song_ids
