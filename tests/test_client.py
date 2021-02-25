import pytest
from spotifynews.spotify.client import Client


@pytest.fixture()
def client_fixture(tmp_path):
    database = Client()
    yield database


def test_update_mirror_playlist(client_fixture):
    playlist_len = 50
    sample_playlist_id = 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'
    mirror_playlist_item_ids = client_fixture.update_mirror_playlist(original_playlist_id=sample_playlist_id,
                                                                     known_track_ids=[])
    assert len(mirror_playlist_item_ids) == playlist_len
