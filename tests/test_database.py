import pytest

from spotifynews.database import Database


@pytest.fixture()
def test_db(tmp_path):
    database = Database(file=tmp_path / "test.db")
    yield database
    database.close()


def test_insert_select_db(test_db):
    song_uri = "abc"
    playlist_uri = "def"
    test_db.create_db()
    test_db.insert_song(song_uri, playlist_uri)
    db_song_uri = test_db.select_songs(playlist_uri)
    assert song_uri in db_song_uri
