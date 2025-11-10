import os
import pygame
from player import Player
from characters import Character
from save import SaveManager
from story_engine import run_story
from utils import safe_input_int

# Dinamikus projektalapú útvonal
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEXT_DIR = os.path.join(BASE_DIR, "texts")
CHAPTER_1_PATH = os.path.join(TEXT_DIR, "chapter_01.txt")
MUSIC_PATH = os.path.join(BASE_DIR, "Celestial Quest.mp3")

def init_music():
    pygame.init()
    pygame.mixer.init()
    try:
        music_path = os.path.join(BASE_DIR, "songs", "Celestial Quest.mp3")
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)
        print("Zene elindítva: Celestial Quest.mp3")
    except Exception as e:
        print(f"Zene betöltése sikertelen: {e}")


def create_character():
    print("\nKarakter létrehozása")
    name = input("Név: ").strip()

    valid_races = ["orc", "elf", "human"]
    while True:
        race = input("Faj (orc / elf / human): ").strip().lower()
        if race in valid_races:
            break
        print("Érvénytelen faj. Csak: orc, elf, human")

    valid_classes = ["warrior", "thief", "mage"]
    while True:
        pclass = input("Osztály (warrior / thief / mage): ").strip().lower()
        if pclass in valid_classes:
            break
        print("Érvénytelen osztály. Csak: warrior, thief, mage")

    return Character(name, race, pclass)

def new_game():
    player = Player()
    hero = create_character()
    player.add_character(hero)
    run_story(CHAPTER_1_PATH, player, player.party)

def continue_game():
    slot = safe_input_int("Betöltés slot (1-3): ", 1, 3)
    loaded_party = SaveManager.load_party(slot)
    if loaded_party:
        print("Mentés betöltve.")
        player = Player()
        player.party = loaded_party
        run_story(CHAPTER_1_PATH, player, loaded_party)
    else:
        print("Nincs mentés ebben a slotban.")

def show_credits():
    print("\nElérhetőségek:")
    print("Fejlesztő: Boronen")
    print("Projekt: Magical Journey")
    print("GitHub: github.com/boronen")
    print("Discord: discord.gg/boronenprojects")
    print("Email: boronenprojects@gmail.com")

def main_menu():
    init_music()
    while True:
        print("\n=== Főmenü ===")
        print("1. Új játék")
        print("2. Folytatás")
        print("3. Elérhetőségek")
        print("4. Kilépés")

        choice = input("> ").strip()

        if choice == "1":
            new_game()
        elif choice == "2":
            continue_game()
        elif choice == "3":
            show_credits()
        elif choice == "4":
            print("Kilépés...")
            pygame.mixer.music.stop()
            break
        else:
            print("Érvénytelen választás.")

if __name__ == "__main__":
    main_menu()
