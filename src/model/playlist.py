# src/model/playlist.py

import json
import time
from .dlinkedlist import DLinkedList
from src.model.song import Song

class Playlist:
    def __init__(self):
        self.songs = DLinkedList()
        self.current_node = None

    def add_song(self, song: Song):
        self.songs.insert_back(song)
        if self.songs.size == 1:
            self.current_node = self.songs.head

    def play_current(self):
        if not self.current_node:
            print("No song to play.")
            return
        print(f"\n🎵 Now playing: {self.current_node.value}")
        time.sleep(self.current_node.value.duration)  # Simulate playing

    def next_song(self):
        if self.current_node and self.current_node.next:
            self.current_node = self.current_node.next
            self.play_current()
        else:
            print("No next song available.")

    def previous_song(self):
        if self.current_node and self.current_node.prev:
            self.current_node = self.current_node.prev
            self.play_current()
        else:
            print("No previous song available.")

    def show_playlist(self):
        print("\n📻 Playlist:")
        print(self.songs)

    def save_to_file(self, filepath: str):
        song_dicts = [song.to_dict() for song in self.songs]
        with open(filepath, 'w') as f:
            json.dump(song_dicts, f, indent=4)
        print(f"\n💾 Playlist saved to {filepath}")

    def load_from_file(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                for song_data in data:
                    self.add_song(Song.from_dict(song_data))
            print(f"\n📂 Loaded playlist from {filepath}")
        except FileNotFoundError:
            print(f"\n⚠️ File {filepath} not found.")
