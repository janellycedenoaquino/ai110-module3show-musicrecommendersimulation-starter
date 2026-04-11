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
        "target_popularity": 80,
        "preferred_decade": 2000,
        "preferred_mood_tag": "uplifting",
        "target_instrumentalness": 0.05,
        "target_liveness": 0.15,
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
        "target_popularity": 50,
        "preferred_decade": 2020,
        "preferred_mood_tag": "dreamy",
        "target_instrumentalness": 0.55,
        "target_liveness": 0.07,
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
        "target_popularity": 65,
        "preferred_decade": 2010,
        "preferred_mood_tag": "aggressive",
        "target_instrumentalness": 0.10,
        "target_liveness": 0.25,
    }

    # Profile 4: Adversarial — sad mood + high energy (e.g. "angry crier" or workout grief playlist)
    conflicted = {
        "favorite_genre": "r&b",
        "favorite_mood": "sad",
        "target_valence": 0.10,
        "target_energy": 0.95,
        "target_acousticness": 0.05,
        "target_tempo": 160.0,
        "target_danceability": 0.20,
        "target_popularity": 85,
        "preferred_decade": 2020,
        "preferred_mood_tag": "melancholic",
        "target_instrumentalness": 0.05,
        "target_liveness": 0.10,
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
        print(f"  Profile: {profile_name}  [mode: default]")
        print("=" * 50)
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{i}  {song['title']} by {song['artist']}")
            print(f"    Genre: {song['genre']} | Mood: {song['mood']}")
            print(f"    Score: {score:.2f} / 14.50")
            print(f"    Why: {explanation}")
        print("\n" + "=" * 50)

    # Mode comparison: run the pop fan through all 3 non-default modes
    print("\n\n" + "#" * 50)
    print("  MODE COMPARISON — High-Energy Pop Fan")
    print("#" * 50)
    for mode in ["genre-first", "mood-first", "energy-focused"]:
        recommendations = recommend_songs(pop_fan, songs, k=3, mode=mode)
        print(f"\n--- Mode: {mode} ---")
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"  #{i}  {song['title']} by {song['artist']}  ({score:.2f})")

    # Diversity comparison: show pop fan with and without diversity filter
    print("\n\n" + "#" * 50)
    print("  DIVERSITY COMPARISON — High-Energy Pop Fan")
    print("#" * 50)
    for label, div_flag in [("Without Diversity", False), ("With Diversity", True)]:
        recommendations = recommend_songs(pop_fan, songs, k=5, diversity=div_flag)
        print(f"\n--- {label} ---")
        for i, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"  #{i}  {song['title']} by {song['artist']}  |  Genre: {song['genre']}  ({score:.2f})")


if __name__ == "__main__":
    main()
