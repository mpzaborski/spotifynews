import sqlite3


class Database:
    def __init__(self, file='spotifynews.db'):
        self.conn = sqlite3.connect(file)
        self.c = self.conn.cursor()
        self.c.row_factory = lambda cursor, row: row[0]

    def close(self):
        self.conn.close()

    def create_db(self):
        self.c.execute("""CREATE TABLE songs (id INTEGER PRIMARY KEY AUTOINCREMENT, songName TEXT);""")
        self.c.execute("""CREATE TABLE playlists (id INTEGER PRIMARY KEY AUTOINCREMENT, playlistName TEXT);""")
        self.c.execute("""CREATE TABLE songs_playlists (song_id INTEGER, playlist_id INTEGER, FOREIGN KEY(song_id)
                  REFERENCES song(id), FOREIGN KEY(playlist_id) REFERENCES playlist(id));""")
        self.conn.commit()

    def insert_song(self, song_uri, playlist_uri):
        self.c.execute("""INSERT INTO songs VALUES(NULL, ?)""", (song_uri,))
        self.c.execute("""INSERT INTO playlists VALUES(NULL, ?)""", (playlist_uri,))
        self.c.execute("""INSERT INTO songs_playlists VALUES(?, ?)""", (song_uri, playlist_uri))
        self.conn.commit()

    def select_songs(self, playlist_uri):
        self.c.execute("""SELECT song_id FROM 'songs_playlists' WHERE playlist_id=:playlist_id""",
                       {"playlist_id": playlist_uri})
        return self.c.fetchall()
