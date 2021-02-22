import sqlite3


class Sqlite3db:
    def __init__(self, database_f='spotifynews.db'):
        self.conn = sqlite3.connect(database_f)
        self.c = self.conn.cursor()
        self.c.row_factory = lambda cursor, row: row[0]
        self._create_tables()

    def close(self):
        self.conn.close()

    def insert_song(self, playlist_id, song_id):
        self.c.execute("""INSERT INTO songs VALUES(NULL, ?)""", (song_id,))
        self.c.execute("""INSERT INTO playlists VALUES(NULL, ?)""", (playlist_id,))
        self.c.execute("""INSERT INTO songs_playlists VALUES(?, ?)""", (song_id, playlist_id))
        self.conn.commit()

    def insert_songs(self, playlist_id, song_ids):
        for song_id in song_ids:
            self.insert_song(playlist_id, song_id)

    def select_songs(self, playlist_id):
        self.c.execute("""SELECT song_id FROM 'songs_playlists' WHERE playlist_id=:playlist_id""",
                       {"playlist_id": playlist_id})
        return self.c.fetchall()

    def _create_tables(self):
        self.c.execute("""CREATE TABLE if not exists songs (id INTEGER PRIMARY KEY AUTOINCREMENT, songName TEXT);""")
        self.c.execute("""CREATE TABLE if not exists playlists (id INTEGER PRIMARY KEY AUTOINCREMENT, playlistName TEXT);""")
        self.c.execute("""CREATE TABLE if not exists songs_playlists (song_id INTEGER, playlist_id INTEGER, FOREIGN KEY(song_id)
                  REFERENCES song(id), FOREIGN KEY(playlist_id) REFERENCES playlist(id));""")
        self.conn.commit()
