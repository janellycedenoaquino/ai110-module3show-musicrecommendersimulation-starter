# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**SoundMatch 1.0**

---

## 2. Intended Use  

**Goal / Task:** Suggest songs from a small catalog that match a user's taste profile.

**Intended use:** Classroom exploration of how content-based music recommendation works.

**Not intended for:** Real music apps, promotion decisions, or use with real listener data. This is a simulation only.

---

## 3. How the Model Works  

**Algorithm Summary:**

- Each song is compared to the user's preferences and given a score.
- Genre match earns +2.5 points. Mood match earns +2.0 points.
- For energy, valence, acousticness, tempo, and danceability, songs earn more points the closer they are to the user's target value.
- The max possible score is 11.0.
- Songs are sorted from highest to lowest score. The top 5 are returned as recommendations.
- Each result includes a plain-language reason explaining why it was picked.

---

## 4. Data  

**Data Used:**

- 25 songs in `data/songs.csv`.
- Started with 10 songs. Added 15 more for diversity, including Latin artists.
- Genres covered: pop, lofi, rock, hip-hop, r&b, folk, electronic, jazz, ambient, synthwave, metal, classical, indie pop.
- Moods covered: happy, chill, intense, energetic, romantic, moody, relaxed, focused, nostalgic.
- Limit: No songs have a "sad" mood tag. Pop and lofi have the most songs. Metal, jazz, and classical have only one each.

---

## 5. Strengths  

- Works well for users whose genre and mood are well-represented in the catalog.
- Pop Fan and Lofi Listener profiles both produced results that matched musical intuition.
- Every recommendation comes with a clear explanation of why it was selected.
- Simple enough to understand and trace by hand — good for learning.

---

## 6. Limitations and Bias  

**Observed Behavior / Biases:**

- Genre dominates. A genre match (+2.5) can outweigh a near-perfect score on every other feature.
- Users with niche genres almost always see only songs from that genre — even if other songs fit better.
- No "sad" mood songs exist in the catalog. Users who prefer sad music get zero mood points on every song.
- Removing the mood check in an experiment barely changed results — confirming genre alone drives most decisions.
- The system works best for pop and lofi listeners, and poorly for edge cases.

---

## 7. Evaluation  

**Evaluation Process:**

- Tested four profiles: High-Energy Pop Fan, Chill Lofi Listener, Intense Rock Fan, and an Adversarial profile (sad mood + high energy).
- Pop and Lofi profiles matched expectations well.
- Rock Fan revealed a surprise: Iron Curtain (metal) ranked lower than Storm Runner (rock) only because "metal" ≠ "rock" as a string — even though the energy and mood matched.
- Adversarial profile showed that missing mood data makes a signal useless.
- Ran one experiment: temporarily removed the mood check. Rankings barely changed, confirming genre weight dominates.
- No numeric metric used — evaluation was based on whether results matched musical intuition.

---

## 8. Future Work  

**Ideas for Improvement:**

1. Add a diversity penalty so the same artist cannot appear more than once or twice in the top 5.
2. Support multiple ranking modes (e.g., "Genre-First" vs "Mood-First") so users can switch strategies.
3. Expand the catalog to 100+ songs with balanced genre and mood coverage to reduce data bias.

---

## 9. Personal Reflection  

Building this system made it clear how much a recommendation depends on what data you choose to collect. The system can only surface what the catalog contains — gaps in the data become gaps in the output. The most surprising discovery was how a single genre weight of 2.5 points could quietly override everything else, making the system feel smart for some users but useless for edge cases. It also changed how I think about real apps like Spotify: what feels like personalized discovery is likely a much larger version of the same basic logic — score, sort, return top results — with more signals and a bigger catalog underneath.
