"""
Command line runner for the Music Recommender Simulation.
"""

from recommender import load_songs, recommend_songs

SEPARATOR = "─" * 62


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    print(f"\n\n{'═' * 62}")
    print(f"  {label}")
    print(f"  Genre: {user_prefs['genre']}  |  Mood: {user_prefs['mood']}")
    print(f"{'═' * 62}")

    results = recommend_songs(user_prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(results, 1):
        bar_filled = int((score / 7.0) * 24)
        bar        = "█" * bar_filled + "░" * (24 - bar_filled)
        pct        = (score / 7.0) * 100

        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       [{bar}]  {score:.2f}/7.0  ({pct:.0f}%)")
        print(f"       {song['genre']} · {song['mood']} · "
              f"energy={song['energy']} · bpm={int(song['tempo_bpm'])}")
        print("       Reasons:")
        for reason in explanation.split(" | "):
            print(f"         • {reason}")

    print(f"\n{SEPARATOR}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"\nLoaded songs: {len(songs)}")

    # ── 1. High-Energy Pop ─────────────────────────────────────────────────
    high_energy_pop = {
        "genre":                   "pop",
        "mood":                    "happy",
        "target_energy":           0.90,
        "target_valence":          0.85,
        "target_tempo_bpm":        128,
        "target_acousticness":     0.08,
        "target_bass_level":       0.75,
        "target_instrumentalness": 0.04,
        "target_speechiness":      0.10,
    }

    # ── 2. Chill Lofi ──────────────────────────────────────────────────────
    chill_lofi = {
        "genre":                   "lofi",
        "mood":                    "focused",
        "target_energy":           0.40,
        "target_valence":          0.60,
        "target_tempo_bpm":        80,
        "target_acousticness":     0.70,
        "target_bass_level":       0.42,
        "target_instrumentalness": 0.75,
        "target_speechiness":      0.04,
    }

    # ── 3. Deep Intense Rock ───────────────────────────────────────────────
    intense_rock = {
        "genre":                   "rock",
        "mood":                    "intense",
        "target_energy":           0.92,
        "target_valence":          0.45,
        "target_tempo_bpm":        150,
        "target_acousticness":     0.08,
        "target_bass_level":       0.80,
        "target_instrumentalness": 0.18,
        "target_speechiness":      0.06,
    }

    # ── 4. EDGE CASE: High energy but sad/dark mood ────────────────────────
    #    Conflicting signals — does the system handle the contradiction?
    sad_bangers = {
        "genre":                   "metal",
        "mood":                    "melancholic",
        "target_energy":           0.90,
        "target_valence":          0.20,    # dark/sad
        "target_tempo_bpm":        155,
        "target_acousticness":     0.06,
        "target_bass_level":       0.85,
        "target_instrumentalness": 0.25,
        "target_speechiness":      0.05,
    }

    # ── 5. EDGE CASE: Genre orphan ─────────────────────────────────────────
    #    Classical has only ONE song in the catalog — what fills spots 2–5?
    classical_fan = {
        "genre":                   "classical",
        "mood":                    "peaceful",
        "target_energy":           0.22,
        "target_valence":          0.70,
        "target_tempo_bpm":        60,
        "target_acousticness":     0.95,
        "target_bass_level":       0.12,
        "target_instrumentalness": 0.95,
        "target_speechiness":      0.02,
    }

    # ── 6. EDGE CASE: Perfectly average — no strong preference anywhere ────
    #    All numeric targets at 0.5, neutral genre — tests scoring floor
    plain_listener = {
        "genre":                   "indie pop",
        "mood":                    "relaxed",
        "target_energy":           0.50,
        "target_valence":          0.50,
        "target_tempo_bpm":        100,
        "target_acousticness":     0.50,
        "target_bass_level":       0.50,
        "target_instrumentalness": 0.50,
        "target_speechiness":      0.05,
    }

    profiles = [
        ("🎵  Profile 1 — High-Energy Pop",              high_energy_pop),
        ("📚  Profile 2 — Chill Lofi (Study Session)",   chill_lofi),
        ("🤘  Profile 3 — Deep Intense Rock",            intense_rock),
        ("⚡  Edge Case 1 — Sad Bangers (high energy + dark valence)", sad_bangers),
        ("🎻  Edge Case 2 — Classical Fan (genre orphan)",             classical_fan),
        ("😐  Edge Case 3 — Perfectly Average (no strong preference)", plain_listener),
    ]

    for label, prefs in profiles:
        print_recommendations(label, prefs, songs, k=5)


if __name__ == "__main__":
    main()
