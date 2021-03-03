import pytest
from spotifynews.spotify.client import Client


@pytest.fixture()
def client_fixture(tmp_path):
    database = Client()
    yield database


def test_update_mirror_playlist(client_fixture):
    sample_playlist_id = 'spotify:playlist:5FmmxErJczcrEwIFGIviYo'
    client_fixture.update_mirror_playlist(original_playlist_id=sample_playlist_id,
                                          known_track_ids=[])
