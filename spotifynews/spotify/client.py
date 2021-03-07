# -*- coding: utf-8 -*-

""" Python library for operations with Spotify Web API """

import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify_user_uri = 'spotify:user:spotify'
top_hits_uri = 'spotify:playlist:37i9dQZF1DXcBWIGoYBM5M'
armanigio_uri = 'spotify:user:g79v8cz5ma6n4l9od93ebt3u6'
slow_potato_uri = 'spotify:playlist:0uUGP7T2r47EHlj75FUk06'
fresh_potato_uri = 'spotify:playlist:2jy0fdFot5DUgctVaXjx8U'

SPOTIFY_MAX_PLAYLIST_ITEMS = 10000
SPOTIFY_MAX_READ_ITEMS = 100


def chunk_playlist(item_ids):
    return [item_ids[x:x + SPOTIFY_MAX_READ_ITEMS] for x in range(0, len(item_ids), SPOTIFY_MAX_READ_ITEMS)]


class Client(spotipy.Spotify):
    def __init__(self):
        """ Create Client object. Playlist scope will be supplied intuitievly. For most cases user token have to allow
            for playlist/track remove/add operations.
        """
        super().__init__(client_credentials_manager=SpotifyOAuth())

    def update_mirror_playlist(self, original_playlist_id, known_track_ids, playlist_part_name=''):
        """ Update mirror playlist or create it if does not exist. Tracks that are not in known_track_ids will be added.

            :param original_playlist_id: playlist ID that have to be mirrored, URI or URL
            :param known_track_ids: a list of track IDs
            :param playlist_part_name: string that will be injected in mirror playlist name during process of mirror
                   playlist creation.
            :return: a list of track IDs
        """
        mirror_playlist_id = self.get_mirror_playlist_id(original_playlist_id, playlist_part_name)
        self.playlist_remove_all_items(mirror_playlist_id)
        mirror_playlist_item_ids = self.get_mirror_playlist_item_ids(original_playlist_id, known_track_ids)
        for chunk in chunk_playlist(mirror_playlist_item_ids):
            self.playlist_add_items(playlist_id=mirror_playlist_id, items=chunk)
        return mirror_playlist_item_ids

    def playlist_remove_all_items(self, playlist_id):
        """ Remove all tracks from user playlist with ID playlist_id.

            :param playlist_id: playlist ID, URI or URL
        """
        playlist_item_ids = self._get_playlist_track_ids_by_playlist_id(playlist_id)
        for chunk in chunk_playlist(playlist_item_ids):
            self.playlist_remove_all_occurrences_of_items(playlist_id=playlist_id, items=chunk)

    def get_mirror_playlist_id(self, original_playlist_id, playlist_part_name):
        """ Get mirror playlist id knowing the name of original playlist and playlist_part_name.

            :param original_playlist_id: playlist ID, URI or URL
            :param playlist_part_name: string that was injected in mirror playlist name during process of mirror
                   playlist creation.
            :return: mirror playlist ID
        """
        original_playlist_name = self.playlist(playlist_id=original_playlist_id)['name']
        format_playlist_part_name = lambda x: f' {x} ' if x else ' '  # noqa: E731
        user_name = self.current_user()['display_name']
        mirror_playlist_name = user_name + format_playlist_part_name(playlist_part_name) + original_playlist_name
        mirror_playlist_id = self._get_user_playlist_id_by_name(mirror_playlist_name)
        if not mirror_playlist_id:
            mirror_playlist_id = self.user_playlist_create(self.me()['id'], mirror_playlist_name)['uri']
        return mirror_playlist_id

    def get_mirror_playlist_item_ids(self, original_playlist_id, known_track_ids):
        """ Get tracks for mirror playlist by getting the tracks from original playlist and excluding tracks which are
            present in known_track_ids.

            :param original_playlist_id: playlist ID, URI or URL
            :param known_track_ids: a list of track IDs
            :return: a list of track IDs
        """
        original_playlist_item_ids = self._get_playlist_track_ids_by_playlist_id(playlist_id=original_playlist_id)
        mirror_playlist_item_ids = []
        for item_id in original_playlist_item_ids:
            if item_id not in known_track_ids:
                mirror_playlist_item_ids.append(item_id)
        return mirror_playlist_item_ids

    def _get_user_playlist_id_by_name(self, name):
        """ Get user playlist id knowing the name of playlist. Current limit for this solution is 50 playlists.

            :param name: string with playlist name
            :return: playlist ID
        """
        results = self.current_user_playlists(limit=50)
        for item in results['items']:
            if item['name'] == name:
                return item['uri']

    def _get_playlist_track_ids_by_playlist_id(self, playlist_id):
        """ Get all track IDs from user playlist with ID playlist_id.

            :param playlist_id: playlist ID, URI or URL
            :return: a list of track IDs
        """
        tracks = self.playlist(playlist_id)['tracks']
        items = tracks['items']
        while tracks['next']:
            tracks = self.next(tracks)
            items.extend(tracks['items'])

        playlist_item_ids = []
        for item in items:
            playlist_item_ids.append(item['track']['uri'])
        return playlist_item_ids
