from src.recommender import Song, UserProfile, Recommender, score_song


def make_pop_song() -> Song:
    return Song(
        id=1, title="Test Pop Track", artist="Artist A", genre="pop", mood="happy",
        energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2,
        popularity=80, release_decade=2000, mood_tag="uplifting",
        instrumentalness=0.05, liveness=0.15,
    )


def make_lofi_song() -> Song:
    return Song(
        id=2, title="Chill Lofi Loop", artist="Artist B", genre="lofi", mood="chill",
        energy=0.4, tempo_bpm=80, valence=0.6, danceability=0.5, acousticness=0.9,
        popularity=50, release_decade=2020, mood_tag="dreamy",
        instrumentalness=0.55, liveness=0.07,
    )


def make_pop_user() -> UserProfile:
    return UserProfile(
        favorite_genre="pop", favorite_mood="happy",
        target_energy=0.8, target_valence=0.9, target_acousticness=0.2,
        target_tempo=120.0, target_danceability=0.8,
        target_popularity=80, preferred_decade=2000, preferred_mood_tag="uplifting",
        target_instrumentalness=0.05, target_liveness=0.15,
    )


def make_small_recommender() -> Recommender:
    return Recommender([make_pop_song(), make_lofi_song()])


def song_to_dict(song: Song) -> dict:
    return {
        "genre": song.genre, "mood": song.mood, "energy": song.energy,
        "valence": song.valence, "acousticness": song.acousticness,
        "tempo_bpm": song.tempo_bpm, "danceability": song.danceability,
        "popularity": song.popularity, "release_decade": song.release_decade,
        "mood_tag": song.mood_tag, "instrumentalness": song.instrumentalness,
        "liveness": song.liveness,
    }


def user_to_dict(user: UserProfile) -> dict:
    return {
        "favorite_genre": user.favorite_genre, "favorite_mood": user.favorite_mood,
        "target_energy": user.target_energy, "target_valence": user.target_valence,
        "target_acousticness": user.target_acousticness, "target_tempo": user.target_tempo,
        "target_danceability": user.target_danceability, "target_popularity": user.target_popularity,
        "preferred_decade": user.preferred_decade, "preferred_mood_tag": user.preferred_mood_tag,
        "target_instrumentalness": user.target_instrumentalness, "target_liveness": user.target_liveness,
    }


# --- Existing tests (fixed) ---

def test_recommend_returns_songs_sorted_by_score():
    results = make_small_recommender().recommend(make_pop_user(), k=2)
    assert len(results) == 2
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    rec = make_small_recommender()
    explanation = rec.explain_recommendation(make_pop_user(), rec.songs[0])
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


# --- New tests ---

def test_genre_matching_song_scores_higher_than_non_matching_song():
    user_prefs = user_to_dict(make_pop_user())
    pop_score, _ = score_song(user_prefs, song_to_dict(make_pop_song()))
    lofi_score, _ = score_song(user_prefs, song_to_dict(make_lofi_song()))
    assert pop_score > lofi_score


def test_diversity_filter_prevents_same_artist_appearing_twice_in_top_results():
    songs = [
        Song(id=i, title=f"Song {i}", artist="Same Artist", genre="pop", mood="happy",
             energy=0.8, tempo_bpm=120, valence=0.9, danceability=0.8, acousticness=0.2,
             popularity=80, release_decade=2020, mood_tag="uplifting",
             instrumentalness=0.05, liveness=0.15)
        for i in range(1, 5)
    ] + [make_lofi_song()]

    from src.recommender import recommend_songs
    user_prefs = user_to_dict(make_pop_user())
    song_dicts = [song_to_dict(s) | {"id": s.id, "title": s.title, "artist": s.artist} for s in songs]
    results = recommend_songs(user_prefs, song_dicts, k=3, diversity=True)
    artists = [song["artist"] for song, _, _ in results]
    assert artists.count("Same Artist") <= 1
