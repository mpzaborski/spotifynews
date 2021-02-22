from spotifynews.update import news, append


def test_news(tmp_path):
    top_hits_id = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
    assert news(database_f=tmp_path / "test.db", original_playlist_id=top_hits_id)
    assert not news(database_f=tmp_path / "test.db", original_playlist_id=top_hits_id)


def test_append(tmp_path):
    top_hits_id = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
    assert news(database_f=tmp_path / "test.db", original_playlist_id=top_hits_id)
    append(database_f=tmp_path / "test.db", original_playlist_id=top_hits_id)
