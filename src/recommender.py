from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_acousticness: float
    target_tempo: float
    target_danceability: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by score against the given user profile."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "target_valence": user.target_valence,
            "target_acousticness": user.target_acousticness,
            "target_tempo": user.target_tempo,
            "target_danceability": user.target_danceability,
        }
        scored = sorted(
            self.songs,
            key=lambda song: score_song(user_prefs, {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "valence": song.valence,
                "acousticness": song.acousticness,
                "tempo_bpm": song.tempo_bpm,
                "danceability": song.danceability,
            })[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended for the given user."""
        user_prefs = {
            "favorite_genre": user.favorite_genre,
            "favorite_mood": user.favorite_mood,
            "target_energy": user.target_energy,
            "target_valence": user.target_valence,
            "target_acousticness": user.target_acousticness,
            "target_tempo": user.target_tempo,
            "target_danceability": user.target_danceability,
        }
        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "valence": song.valence,
            "acousticness": song.acousticness,
            "tempo_bpm": song.tempo_bpm,
            "danceability": song.danceability,
        }
        _, explanation = score_song(user_prefs, song_dict)
        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dicts with numeric fields converted to float/int."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": int(row["popularity"]),
                "release_decade": int(row["release_decade"]),
                "mood_tag": row["mood_tag"],
                "instrumentalness": float(row["instrumentalness"]),
                "liveness": float(row["liveness"]),
            })
    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Scores a single song against user preferences and returns (score, explanation)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.5
        reasons.append("genre match (+2.5)")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 2.0
        reasons.append("mood match (+2.0)")

    energy_pts = max(0.0, 2.0 * (1 - abs(song["energy"] - user_prefs["target_energy"])))
    score += energy_pts
    reasons.append(f"energy closeness (+{energy_pts:.2f})")

    valence_pts = 1.5 * (1 - abs(song["valence"] - user_prefs["target_valence"]))
    score += valence_pts
    reasons.append(f"valence closeness (+{valence_pts:.2f})")

    acousticness_pts = 1.0 * (1 - abs(song["acousticness"] - user_prefs["target_acousticness"]))
    score += acousticness_pts
    reasons.append(f"acousticness closeness (+{acousticness_pts:.2f})")

    tempo_pts = max(0.0, 1.0 * (1 - abs(song["tempo_bpm"] - user_prefs["target_tempo"]) / 100))
    score += tempo_pts
    reasons.append(f"tempo closeness (+{tempo_pts:.2f})")

    danceability_pts = 1.0 * (1 - abs(song["danceability"] - user_prefs["target_danceability"]))
    score += danceability_pts
    reasons.append(f"danceability closeness (+{danceability_pts:.2f})")

    popularity_pts = max(0.0, 0.5 * (1 - abs(song["popularity"] / 100 - user_prefs["target_popularity"] / 100)))
    score += popularity_pts
    reasons.append(f"popularity closeness (+{popularity_pts:.2f})")

    if song["release_decade"] == user_prefs["preferred_decade"]:
        score += 1.0
        reasons.append("decade match (+1.0)")

    if song["mood_tag"] == user_prefs["preferred_mood_tag"]:
        score += 1.0
        reasons.append("mood tag match (+1.0)")

    instrumentalness_pts = max(0.0, 0.5 * (1 - abs(song["instrumentalness"] - user_prefs["target_instrumentalness"])))
    score += instrumentalness_pts
    reasons.append(f"instrumentalness closeness (+{instrumentalness_pts:.2f})")

    liveness_pts = max(0.0, 0.5 * (1 - abs(song["liveness"] - user_prefs["target_liveness"])))
    score += liveness_pts
    reasons.append(f"liveness closeness (+{liveness_pts:.2f})")

    return score, ", ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores all songs against user preferences and returns the top k as (song, score, explanation) tuples."""
    scored = [
        (song, *score_song(user_prefs, song))
        for song in songs
    ]
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]
