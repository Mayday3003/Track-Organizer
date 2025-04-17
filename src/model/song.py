class Song:
    def __init__(self, title: str, artist: str, album: str, duration: float, genre: str):
        """
        Initialize a Song with title, artist, album, duration (in seconds) and genre.
        """
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.genre = genre

    def __str__(self) -> str:
        return f"🎵 {self.title} by {self.artist} | Album: {self.album} | {self.duration} sec | Genre: {self.genre}"

    def to_dict(self) -> dict:
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
            genre=data.get("genre", "Unknown")
        )
