"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Profile 1: High-energy pop fan — upbeat, positive, danceable, minimal acoustic texture
    pop_fan = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.85,
        "target_valence": 0.90,
        "target_acousticness": 0.15,
        "target_tempo": 120.0,
        "target_danceability": 0.85,
    }

    # Profile 2: Chill lofi listener — low energy, focused mood, slow tempo, highly acoustic
    lofi_listener = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.35,
        "target_valence": 0.60,
        "target_acousticness": 0.85,
        "target_tempo": 75.0,
        "target_danceability": 0.55,
    }

    # Profile 3: Intense rock fan — raw energy, fast tempo, low acousticness, high danceability
    rock_fan = {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.92,
        "target_valence": 0.45,
        "target_acousticness": 0.10,
        "target_tempo": 150.0,
        "target_danceability": 0.70,
    }

    # Profile 4: Adversarial — sad mood + high energy (e.g. "angry crier" or workout grief playlist)
    # Conflict: sad/melancholic mood expects low valence & low energy,
    # but targets push high energy and fast tempo — genre "r&b" adds a second tension
    # against low danceability preference. The scorer must decide which signals win.
    conflicted = {
        "favorite_genre": "r&b",
        "favorite_mood": "sad",
        "target_valence": 0.10,     # very low (sad/dark) — aligns with mood but not energy
        "target_energy": 0.95,      # high energy — contradicts sad mood convention
        "target_acousticness": 0.05, # metal-appropriate, but extreme
        "target_tempo": 160.0,      # fast — contradicts sad mood (usually slow)
        "target_danceability": 0.20, # low — contradicts the high energy/tempo
    }

    profiles = [
        ("High-Energy Pop Fan", pop_fan),
        ("Chill Lofi Listener", lofi_listener),
        ("Intense Rock Fan", rock_fan),
        ("Adversarial: Sad + High Energy", conflicted),
    ]

    for profile_name, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print("\n" + "=" * 50)
        print(f"  Profile: {profile_name}")
        print("=" * 50)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{i}  {song['title']} by {song['artist']}")
            print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"    Score: {score:.2f} / 11.00")
            print(f"    Why: {explanation}")
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
