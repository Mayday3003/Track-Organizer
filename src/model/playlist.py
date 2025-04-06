# src/model/playlist.py

import json
import time
import random
from typing import List
from src.model.dlinkedlist import DLinkedList, DNode
from src.model.song import Song
import threading


class Playlist:
    def __init__(self):
        self.songs = DLinkedList()
        self.current_node = None
        self.shuffle_mode = False
        self.shuffle_order = []  # List of DNode
        self.shuffle_index = 0

    def add_song(self, song: Song):
        """Adds a song if its title is not a duplicate."""
        if self._song_exists(song.title):
            print(f"❌ Song '{song.title}' already exists in the playlist.")
            return
        self.songs.insert_back(song)
        if self.songs.size == 1:
            self.current_node = self.songs.head

    def _song_exists(self, title: str) -> bool:
        for s in self.songs:
            if s.title.lower() == title.lower():
                return True
        return False

    def remove_song(self, title: str):
        """Removes a song by its title. If the song being removed is the current one,
        moves to the next song automatically."""
        current = self.songs.head
        found = False
        while current:
            if current.value.title.lower() == title.lower():
                found = True
                # If current song is removed, update pointer.
                if current == self.current_node:
                    self.next_song(auto_play=False)
                    # If it was the only song, set current_node to None.
                    if self.songs.size == 1:
                        self.current_node = None
                self.songs.delete_node(current)
                print(f"✅ Song '{title}' removed successfully.")
                break
            current = current.next
        if not found:
            print(f"❌ Song '{title}' not found in the playlist.")

    def play_current(self):
        """Simulates playing the current song with a progress bar."""
        if not self.current_node:
            print("No song to play.")
            return
        song = self.current_node.value
        print(f"\n▶ Now playing: {song}")
        duration = int(song.duration)
        for sec in range(1, duration + 1):
            print(f"\r⏳ {sec}/{duration} sec", end="")
            time.sleep(1)
        print("\n🔄 Song ended. Moving to the next song...")
        self.next_song()

    def next_song(self, auto_play=True):
        """Advances to the next song, wrapping around if at the end."""
        if not self.current_node:
            print("No next song available.")
            return
        if self.shuffle_mode:
            self._init_shuffle_order_if_needed()
            self.shuffle_index = (self.shuffle_index + 1) % len(self.shuffle_order)
            self.current_node = self.shuffle_order[self.shuffle_index]
            if auto_play:
                self.play_current()
            return

        if self.current_node.next:
            self.current_node = self.current_node.next
        else:
            self.current_node = self.songs.head  # Circular behavior
        if auto_play:
            self.play_current()

    def previous_song(self, auto_play=True):
        """Goes back to the previous song, wrapping around if at the beginning."""
        if not self.current_node:
            print("No previous song available.")
            return
        if self.shuffle_mode:
            self._init_shuffle_order_if_needed()
            self.shuffle_index = (self.shuffle_index - 1) % len(self.shuffle_order)
            self.current_node = self.shuffle_order[self.shuffle_index]
            if auto_play:
                self.play_current()
            return

        if self.current_node.prev:
            self.current_node = self.current_node.prev
        else:
            self.current_node = self.songs.tail
        if auto_play:
            self.play_current()

    def skip_ahead(self, percentage: float):
        """Skips ahead in the current song by a given percentage."""
        if not self.current_node:
            print("No song to skip ahead in.")
            return
        song = self.current_node.value
        skip_time = int(song.duration * (percentage / 100))
        print(f"⌛ Skipping ahead {skip_time} seconds...")
        if skip_time >= song.duration:
            self.next_song()
        else:
            for sec in range(skip_time, int(song.duration) + 1):
                print(f"\r⏩ {sec}/{int(song.duration)} sec", end="")
                time.sleep(1)
            print("\n🔄 Song ended after skipping. Moving to the next song...")
            self.next_song()

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

    def activate_shuffle(self):
        """Toggle shuffle mode on/off."""
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            print("🔀 Shuffle mode activated.")
            self._init_shuffle_order_if_needed()
        else:
            print("🔀 Shuffle mode deactivated.")

    def _init_shuffle_order_if_needed(self):
        """Initializes or updates the shuffle order list."""
        if not self.shuffle_mode:
            return
        nodes = []
        current = self.songs.head
        while current:
            nodes.append(current)
            current = current.next
        if nodes:
            random.shuffle(nodes)
            self.shuffle_order = nodes
            if self.current_node in self.shuffle_order:
                self.shuffle_index = self.shuffle_order.index(self.current_node)
            else:
                self.current_node = nodes[0]
                self.shuffle_index = 0

    def generate_subplaylist(self, titles: List[str]) -> 'Playlist':
        """
        Generates a subplaylist containing songs whose titles match those provided.
        """
        subplaylist = Playlist()
        title_set = {t.strip().lower() for t in titles}
        for song in self.songs:
            if song.title.lower() in title_set:
                subplaylist.add_song(song)
        print(f"✅ Subplaylist created with {len(list(subplaylist.songs))} songs.")
        return subplaylist
