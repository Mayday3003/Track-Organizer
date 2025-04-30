from colorama import Fore, Style, init
from src.model.playlist import Playlist
from src.model.song import Song

init(autoreset=True)

def show_menu():
    print("\n" + Fore.CYAN + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + "🎧 Welcome to the Music Player" + Style.RESET_ALL)
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)
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
    print("12. Remove least frequent artist")  # Nueva opción
    print("0. Exit")
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

def get_song_input() -> Song:
    print("\n" + Fore.YELLOW + "🎼 Enter song details:" + Style.RESET_ALL)
    title = input("Title: ").strip()
    artist = input("Artist: ").strip()
    album = input("Album: ").strip()
    while True:
        try:
            duration = float(input("Duration (10-15 seconds): "))
            if not 10 <= duration <= 15:
                raise ValueError
            break
        except ValueError:
            print(Fore.RED + "⚠️ Please enter a valid duration between 10 and 15 seconds." + Style.RESET_ALL)
    genre = input("Genre: ").strip()
    return Song(title, artist, album, duration, genre)

def run_console():
    playlist = Playlist()
    filepath = "playlist.json"

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        handle_menu_choice(choice, playlist, filepath)


def handle_menu_choice(choice: str, playlist: Playlist, filepath: str):
    if choice == '1':
        playlist.load_from_file(filepath)
    elif choice == '2':
        playlist.show_playlist()
    elif choice == '3':
        handle_add_song(playlist)
    elif choice == '4':
        playlist.play_current()
    elif choice == '5':
        playlist.next_song()
    elif choice == '6':
        playlist.previous_song()
    elif choice == '7':
        handle_remove_song(playlist)
    elif choice == '8':
        playlist.activate_shuffle()
    elif choice == '9':
        handle_skip_ahead(playlist)
    elif choice == '10':
        handle_generate_subplaylist(playlist)
    elif choice == '11':
        playlist.save_to_file(filepath)
    elif choice == '12':  # Nueva opción
        handle_remove_least_frequent_artist(playlist)
    elif choice == '0':
        print(Fore.GREEN + "\n👋 Thanks for using the Music Player. Goodbye!" + Style.RESET_ALL)
        exit()
    else:
        print(Fore.RED + "❌ Invalid option. Please try again." + Style.RESET_ALL)


def handle_add_song(playlist: Playlist):
    song = get_song_input()
    playlist.add_song(song)
    print(Fore.GREEN + f"\n✅ Song '{song.title}' added to playlist." + Style.RESET_ALL)


def handle_remove_song(playlist: Playlist):
    title = input("Enter the title of the song to remove: ").strip()
    playlist.remove_song(title)


def handle_skip_ahead(playlist: Playlist):
    try:
        percent = float(input("Enter skip percentage (e.g., 50): "))
        playlist.skip_ahead(percent)
    except ValueError:
        print(Fore.RED + "⚠️ Please enter a valid number for percentage." + Style.RESET_ALL)


def handle_generate_subplaylist(playlist: Playlist):
    titles_input = input("Enter the titles of songs for subplaylist (separated by commas): ")
    titles = titles_input.split(",")
    subplaylist = playlist.generate_subplaylist(titles)
    sub_choice = input("Do you want to play the subplaylist? (y/n): ").strip().lower()
    if sub_choice == 'y':
        run_subplaylist(subplaylist)


def run_subplaylist(subplaylist: Playlist):
    while True:
        print("\n" + Fore.BLUE + "=" * 40 + Style.RESET_ALL)
        print(Fore.GREEN + "🎵 Subplaylist Menu" + Style.RESET_ALL)
        print("1. Show subplaylist")
        print("2. Play current song")
        print("3. Next song")
        print("4. Previous song")
        print("5. Return to main menu")
        print(Fore.BLUE + "=" * 40 + Style.RESET_ALL)
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
            print(Fore.RED + "❌ Invalid option.")

def handle_remove_least_frequent_artist(playlist: Playlist):
    print(Fore.YELLOW + "\n🔍 Removing songs by the least frequent artist..." + Style.RESET_ALL)
    playlist.remove_least_frequent_artist()
