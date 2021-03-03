from spotifynews.update import news, collections

sample_playlist_id = 'spotify:playlist:5FmmxErJczcrEwIFGIviYo'


def test_news(tmp_path):
    assert news(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)
    assert not news(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)


def test_collections(tmp_path):
    assert news(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)
    assert collections(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)
