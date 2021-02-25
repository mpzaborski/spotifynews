import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_user_uri = 'spotify:user:spotify'
top_hits_uri = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
armanigio_uri = 'spotify:user:g79v8cz5ma6n4l9od93ebt3u6'
slow_potato_uri = 'spotify:playlist:0uUGP7T2r47EHlj75FUk06'
fresh_potato_uri = 'spotify:playlist:2jy0fdFot5DUgctVaXjx8U'


class Client(spotipy.Spotify):
    def __init__(self):
        scope = 'playlist-modify-public'
        os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback/'
        super().__init__(client_credentials_manager=SpotifyOAuth(scope=scope))

    def update_mirror_playlist(self, original_playlist_id, known_track_ids, playlist_part_name=''):
        mirror_playlist_id = self.get_mirror_playlist_id(original_playlist_id, playlist_part_name)
        self.playlist_remove_all_items(mirror_playlist_id)
        mirror_playlist_item_ids = self.get_mirror_playlist_item_ids(original_playlist_id, known_track_ids)
        if mirror_playlist_item_ids:
            self.playlist_add_items(mirror_playlist_id, mirror_playlist_item_ids)
        return mirror_playlist_item_ids

    def playlist_remove_all_items(self, playlist_id):
        playlist_item_ids = self._get_playlist_track_ids_by_playlist_id(playlist_id)
        self.playlist_remove_all_occurrences_of_items(playlist_id=playlist_id, items=playlist_item_ids)

    def get_mirror_playlist_id(self, original_playlist_id, playlist_part_name):
        original_playlist_name = self.playlist(playlist_id=original_playlist_id)['name']
        format_playlist_part_name = lambda x: f' {x} ' if x else ' '  # noqa: E731
        user_name = self.current_user()['display_name']
        mirror_playlist_name = user_name + format_playlist_part_name(playlist_part_name) + original_playlist_name
        mirror_playlist_id = self._get_user_playlist_id_by_name(mirror_playlist_name)
        if not mirror_playlist_id:
            mirror_playlist_id = self.user_playlist_create(self.me()['id'], mirror_playlist_name)['uri']
        return mirror_playlist_id

    def get_mirror_playlist_item_ids(self, original_playlist_id, known_track_ids):
        original_playlist = self.playlist(playlist_id=original_playlist_id)
        mirror_playlist_item_ids = []
        for item in original_playlist['tracks']['items']:
            if item['track']['uri'] not in known_track_ids:
                mirror_playlist_item_ids.append(item['track']['uri'])
        return mirror_playlist_item_ids

    def _get_user_playlist_id_by_name(self, name):
        results = self.current_user_playlists(limit=50)
        for item in results['items']:
            if item['name'] == name:
                return item['uri']

    def _get_playlist_track_ids_by_playlist_id(self, playlist_id):
        playlist = self.playlist(playlist_id=playlist_id)
        playlist_item_ids = []
        for item in playlist['tracks']['items']:
            playlist_item_ids.append(item['track']['uri'])
        return playlist_item_ids
