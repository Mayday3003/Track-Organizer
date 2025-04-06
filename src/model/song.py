class Song:
    def __init__(self, title: str, artist: str, album: str, duration: float, genre: str):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.genre = genre

    def __str__(self):
        return f"🎵 {self.title} by {self.artist} | Album: {self.album} | {self.duration} min | Genre: {self.genre}"

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": self.duration,
            "genre": self.genre
        }

    @staticmethod
    def from_dict(data: dict) -> 'Song':
        return Song(
            title=data["title"],
            artist=data["artist"],
            album=data["album"],
            duration=data["duration"],
            genre=data.get("genre", "Unknown")  # usa "Unknown" si no existe
        )
