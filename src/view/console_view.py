# src/view/console_view.py

import time
from src.model.playlist import Playlist, Song

def show_menu():
    print("\n" + "=" * 50)
    print("🎧 Welcome to PyPlay Music Player")
    print("=" * 50)
    print("1. Load playlist from file")
    print("2. Show current playlist")
    print("3. Add a new song")
    print("4. Play current song")
    print("5. Next song")
    print("6. Previous song")
    print("7. Remove a song")
    print("8. Activate/Deactivate shuffle mode")
    print("9. Skip ahead in current song")
    print("10. Generate subplaylist")
    print("11. Save playlist to file")
    print("0. Exit")
    print("=" * 50)

def get_song_input() -> Song:
    print("\n🎼 Enter song details:")
    title = input("Title: ").strip()
    artist = input("Artist: ").strip()
    album = input("Album: ").strip()
    while True:
        try:
            duration = float(input("Duration (in seconds, e.g., 12): "))
            if duration <= 0:
                raise ValueError
            break
        except ValueError:
            print("⚠️ Please enter a valid positive number for duration.")
    genre = input("Genre: ").strip()
    return Song(title, artist, album, duration, genre)

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
            title = input("Enter the title of the song to remove: ").strip()
            playlist.remove_song(title)
        elif choice == '8':
            playlist.activate_shuffle()
        elif choice == '9':
            try:
                percent = float(input("Enter skip percentage (e.g., 50): "))
                playlist.skip_ahead(percent)
            except ValueError:
                print("⚠️ Please enter a valid number for percentage.")
        elif choice == '10':
            titles_input = input("Enter the titles of songs for subplaylist (separated by commas): ")
            titles = titles_input.split(",")
            subplaylist = playlist.generate_subplaylist(titles)
            sub_choice = input("Do you want to play the subplaylist? (y/n): ").strip().lower()
            if sub_choice == 'y':
                run_subplaylist(subplaylist)
        elif choice == '11':
            playlist.save_to_file(filepath)
        elif choice == '0':
            print("\n👋 Thanks for using PyPlay Music Player. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please try again.")
        time.sleep(1)

def run_subplaylist(subplaylist: Playlist):
    """A separate menu loop for a subplaylist."""
    while True:
        print("\n" + "=" * 40)
        print("🎵 Subplaylist Menu")
        print("1. Show subplaylist")
        print("2. Play current song")
        print("3. Next song")
        print("4. Previous song")
        print("5. Return to main menu")
        print("=" * 40)
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            subplaylist.show_playlist()
        elif choice == '2':
            subplaylist.play_current()
        elif choice == '3':
            subplaylist.next_song()
        elif choice == '4':
            subplaylist.previous_song()
        elif choice == '5':
            break
        else:
            print("❌ Invalid option. Please try again.")
        time.sleep(1)
