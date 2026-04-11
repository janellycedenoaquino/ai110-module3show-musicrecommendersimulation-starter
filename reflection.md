# Reflection: Profile Comparisons

## High-Energy Pop Fan vs. Chill Lofi Listener

Results are almost entirely non-overlapping. The Pop Fan gets upbeat, high-valence pop songs; the Lofi Listener gets slow, acoustic tracks. The genre weight (+2.5) acts more like a hard filter than a soft preference — it decides the top results before any other attribute is considered.

## High-Energy Pop Fan vs. Intense Rock Fan

Both prefer high energy, so their energy scores partially overlap. But the genre boundary separates them completely. A metal song (Iron Curtain) ranked below a rock song (Storm Runner) for the Rock Fan even though its energy was a closer match — because "metal" ≠ "rock" earns zero genre points. The system treats sub-genres as completely separate categories.

## Intense Rock Fan vs. Adversarial (Sad + High Energy)

The Rock Fan gets focused high-energy rock results. The Adversarial profile (sad mood, r&b genre, high energy) gets scattered results — no "sad" songs exist in the catalog, so mood earns zero points for every song. Rankings collapse to numeric features only (energy and low valence), exposing how the system silently degrades when categorical signals fail.

## Chill Lofi Listener vs. Adversarial (Sad + High Energy)

The Lofi Listener is served well because lofi songs exist in the catalog. The Adversarial profile is served poorly because "sad" mood and r&b genre are underrepresented. This contrast shows that recommendation quality depends as much on catalog coverage as on scoring logic — users with niche tastes always lose.
