import json
import time
from datetime import datetime, timedelta
import random
import sys
import select
from typing import List
from src.model.dlinkedlist import DLinkedList, DNode
from src.model.song import Song

class Playlist:
    def __init__(self):
        self.songs = DLinkedList()
        self.current_node = None
        self.shuffle_mode = False
        self.shuffle_order = []
        self.shuffle_index = -1
        self.shuffle_played = set()

    def add_song(self, song: Song):
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
        current = self.songs.head
        found = False
        while current and (found is False):
            if current.value.title.lower() == title.lower():
                found = True
                if current == self.current_node:
                    self.next_song(auto_play=False)
                    if self.songs.size == 1:
                        self.current_node = None
                self.songs.delete_node(current)
                print(f"✅ Song '{title}' removed successfully.")
                break
            current = current.next
        if not found:
            print(f"❌ Song '{title}' not found in the playlist.")

    def _read_input_nonblocking(self):
        dr, dw, de = select.select([sys.stdin], [], [], 0)
        if dr:
            return sys.stdin.readline().strip().lower()
        return None

    def play_current(self):
        if not self.current_node:
            print("No song to play.")
            return
        song = self.current_node.value
        total = int(song.duration)
        print(f"\n▶ Now playing: {song}")
        print("Comandos durante reproducción: 5=next, 6=prev, 9=skip%, m=menu, q=quit")

        start = datetime.now()
        end = start + timedelta(seconds=total)
        elapsed = 0

        while datetime.now() < end:
            bar_len = 20
            filled = int((elapsed / total) * bar_len) if total else 0
            bar = '#' * filled + ' ' * (bar_len - filled)
            print(f"\r[{bar}] {elapsed}/{total} sec", end="")
            time.sleep(1)
            elapsed += 1

            cmd = self._read_input_nonblocking()
            if cmd:
                if cmd == 'q':
                    print("\n⏹️ Playback stopped.")
                    return
                if cmd == 'm':
                    print("\n🔙 Returning to menu.")
                    return
                if cmd == '5':
                    print("\n⏭️ Skipping to next song.")
                    self.next_song(auto_play=False)
                    self.play_current()
                    return
                if cmd == '6':
                    print("\n⏮️ Going to previous song.")
                    self.previous_song(auto_play=False)
                    self.play_current()
                    return
                if cmd == '9':
                    try:
                        percent = float(input("Enter skip percentage: "))
                        self.skip_ahead(percent)
                    except ValueError:
                        print("⚠️ Invalid percentage.")
                    return

        print("\n🔄 Song ended. Moving to the next song...")
        self.next_song()

    def next_song(self, auto_play=True):
        if not self.current_node:
            print("No next song available.")
            return
        if self.shuffle_mode:
            if len(self.shuffle_played) >= len(self.shuffle_order):
                self._init_shuffle_order()
            else:
                for i in range(len(self.shuffle_order)):
                    self.shuffle_index = (self.shuffle_index + 1) % len(self.shuffle_order)
                    next_candidate = self.shuffle_order[self.shuffle_index]
                    if next_candidate not in self.shuffle_played:
                        self.current_node = next_candidate
                        self.shuffle_played.add(next_candidate)
                        break
            if auto_play:
                self.play_current()
            return

        self.current_node = self.current_node.next
        if auto_play:
            self.play_current()

    def previous_song(self, auto_play=True):
        if not self.current_node:
            print("No previous song available.")
            return
        if self.shuffle_mode:
            self.shuffle_index = (self.shuffle_index - 1) % len(self.shuffle_order)
            self.current_node = self.shuffle_order[self.shuffle_index]
            self.shuffle_played.add(self.current_node)
            if auto_play:
                self.play_current()
            return

        self.current_node = self.current_node.prev
        if auto_play:
            self.play_current()

    def skip_ahead(self, percentage: float):
        if not self.current_node:
            print("No song to skip ahead in.")
            return
        song = self.current_node.value
        skip_time = int(song.duration * (percentage / 100))
        print(f"⌛ Skipping ahead {skip_time} seconds...")
        if skip_time >= song.duration:
            self.next_song()
        else:
            remaining = int(song.duration) - skip_time
            start = datetime.now()
            end = start + timedelta(seconds=remaining)
            elapsed = skip_time
            while datetime.now() < end:
                print(f"\r⏩ {elapsed}/{int(song.duration)} sec", end="")
                time.sleep(1)
                elapsed += 1
                cmd = self._read_input_nonblocking()
                if cmd == 'q':
                    print("\n⏹️ Playback stopped.")
                    return
            print("\n🔄 Song ended after skipping. Moving to the next song...")
            self.next_song()

    def show_playlist(self):
        print("\n📻 Playlist:")
        current_song = self.current_node.value if self.current_node else None
        idx = 1
        node = self.songs.head
        for _ in range(self.songs.size):
            song = node.value
            mark = "→ " if song == current_song else "   "
            print(f"{mark}{idx}. {song.title} - {song.artist} ({int(song.duration)}s)")
            node = node.next
            idx += 1

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
        self.shuffle_mode = not self.shuffle_mode
        if self.shuffle_mode:
            print("🔀 Shuffle mode activated.")
            self._init_shuffle_order()
        else:
            print("🔀 Shuffle mode deactivated.")
            self.shuffle_index = -1
            self.shuffle_order.clear()
            self.shuffle_played.clear()

    def _init_shuffle_order(self):
        nodes = []
        current = self.songs.head
        for _ in range(self.songs.size):
            nodes.append(current)
            current = current.next
        random.shuffle(nodes)
        self.shuffle_order = nodes
        self.shuffle_index = 0
        self.shuffle_played = set()
        self.current_node = self.shuffle_order[self.shuffle_index]
        self.shuffle_played.add(self.current_node)

    def generate_subplaylist(self, titles: List[str]) -> 'Playlist':
        sub = Playlist()
        title_set = {t.strip().lower() for t in titles}
        for song in self.songs:
            if song.title.lower() in title_set:
                sub.add_song(song)
        print(f"✅ Subplaylist created with {len(list(sub.songs))} songs.")
        return sub
