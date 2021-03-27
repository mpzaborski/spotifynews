# -*- coding: utf-8 -*-

""" Python library for database related operations """

import sqlite3


class Sqlite3db:
    def __init__(self, database_f='spotifynews.db'):
        """ Create Sqlite3db object. Connect to database if exists. If database does not exist create it and create
        tables.

        :param database_f: name of sqlite3db file
        """
        self.conn = sqlite3.connect(database_f)
        self.c = self.conn.cursor()
        self.c.row_factory = lambda cursor, row: row[0]
        self._create_tables()

    def close(self):
        """ Close database after final interaction.
        """
        self.conn.close()

    def insert_song(self, playlist_id, song_id):
        """ Add song_id to songs table if song does not exist, playist_id to playlist table if playlist does not exist.
            Add connection between song_id and playlist_id to songs_playlists table.

            :param playlist_id: playlist ID, URI or URL
            :param song_id: song ID, URI or URL
        """
        self.c.execute("""INSERT INTO songs VALUES(NULL, ?)""", (song_id,))
        self.c.execute("""SELECT * FROM playlists WHERE playlistName=:playlist_name""",
                       {"playlist_name": playlist_id})
        playlist_db_id = self.c.fetchall()
        if not playlist_db_id:
            self.c.execute("""INSERT INTO playlists VALUES(NULL, ?)""", (playlist_id,))
        self.c.execute("""INSERT INTO songs_playlists VALUES(?, ?)""", (song_id, playlist_id))
        self.conn.commit()

    def insert_songs(self, playlist_id, song_ids):
        """ Add song_ids to songs table.

            :param playlist_id: playlist ID, URI or URL
            :param song_ids: list of song IDs, URI or URL
        """
        for song_id in song_ids:
            self.insert_song(playlist_id, song_id)

    def select_songs(self, playlist_id):
        """ Get list of songs from playlist with ID playlist_id.

            :param playlist_id: playlist ID, URI or URL
            :return: A list of track IDs
        """
        self.c.execute("""SELECT song_id FROM 'songs_playlists' WHERE playlist_id=:playlist_id""",
                       {"playlist_id": playlist_id})
        return self.c.fetchall()

    def _create_tables(self):
        """ Create tables in database if not exist. Crucial step in freshly created database.
        """
        self.c.execute("""CREATE TABLE if not exists songs (id INTEGER PRIMARY KEY AUTOINCREMENT, songName TEXT);""")
        self.c.execute("""CREATE TABLE if not exists playlists (id INTEGER PRIMARY KEY AUTOINCREMENT, playlistName TEXT NOT NULL UNIQUE);""")
        self.c.execute("""CREATE TABLE if not exists songs_playlists (song_id INTEGER, playlist_id INTEGER, FOREIGN KEY(song_id)
                  REFERENCES song(id), FOREIGN KEY(playlist_id) REFERENCES playlist(id));""")
        self.conn.commit()
