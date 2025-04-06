# src/view/console_view.py

import time
from src.model.playlist import Playlist, Song

def show_menu():
    print("\n" + "=" * 40)
    print("🎧 Welcome to PyPlay Music Player")
    print("=" * 40)
    print("1. Load playlist from file")
    print("2. Show current playlist")
    print("3. Add a new song")
    print("4. Play current song")
    print("5. Next song")
    print("6. Previous song")
    print("7. Save playlist to file")
    print("0. Exit")
    print("=" * 40)

def get_song_input():
    print("\n🎼 Enter song details:")
    title = input("Title: ").strip()
    artist = input("Artist: ").strip()
    while True:
        try:
            duration = int(input("Duration (in seconds): "))
            if duration <= 0:
                raise ValueError
            break
        except ValueError:
            print("⚠️ Please enter a valid positive number.")
    genre = input("Genre: ").strip()
    return Song(title, artist, duration, genre)

def run_console():
    playlist = Playlist()
    filepath = "playlist.json"

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            playlist.load_from_file(filepath)
        elif choice == '2':
            playlist.show_playlist()
        elif choice == '3':
            song = get_song_input()
            playlist.add_song(song)
            print(f"\n✅ Song '{song.title}' added to playlist.")
        elif choice == '4':
            playlist.play_current()
        elif choice == '5':
            playlist.next_song()
        elif choice == '6':
            playlist.previous_song()
        elif choice == '7':
            playlist.save_to_file(filepath)
        elif choice == '0':
            print("\n👋 Thanks for using PyPlay Music Player. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")

        time.sleep(1)  # Smooth UX pause
