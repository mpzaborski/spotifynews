from spotifynews.update import news, collections
from spotifynews.spotify.client import Client

sample_playlist_id = 'spotify:playlist:4emCBDUuTxIAMnMjqksexT'
same_songs = ['spotify:track:2MMFpdctgwEkUlfP3kyPDG', 'spotify:track:1ToprX3cpBiXoAe5eNSk74']
old_song = ['spotify:track:1iSqfoUFnQwV0QW1EfUit8']
new_song = ['spotify:track:5yDiYRQlbCJMVtz1jCj1vL']
playlist_before_update = same_songs + old_song
playlist_after_update = same_songs + new_song
playlist_all = same_songs + old_song + new_song


def test_news(tmp_path):
    client = Client()
    client.playlist_remove_all_items(sample_playlist_id)
    client.playlist_add_items(sample_playlist_id, playlist_before_update)

    news_songs = news(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)
    assert news_songs == playlist_before_update

    client.playlist_remove_all_items(sample_playlist_id)
    client.playlist_add_items(sample_playlist_id, playlist_after_update)

    new_songs = news(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)
    assert (len(new_songs) == len(new_song) and new_songs[0] == new_song[0])


def test_collections(tmp_path):
    client = Client()
    client.playlist_remove_all_items(sample_playlist_id)
    client.playlist_add_items(sample_playlist_id, playlist_before_update)
    assert news(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)
    client.playlist_remove_all_items(sample_playlist_id)
    client.playlist_add_items(sample_playlist_id, playlist_after_update)
    assert news(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)

    collections_songs = collections(database_f=tmp_path / "test.db", original_playlist_id=sample_playlist_id)
    assert len(collections_songs) == len(playlist_all) and collections_songs == playlist_all
