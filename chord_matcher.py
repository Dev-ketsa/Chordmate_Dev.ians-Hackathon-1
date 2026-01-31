# Expanded Chord Database with normalized note sets
CHORDS = {
    # MAJOR CHORDS
    frozenset(['C', 'E', 'G']): 'C Major',
    frozenset(['D', 'F#', 'A']): 'D Major',
    frozenset(['E', 'G#', 'B']): 'E Major',
    frozenset(['F', 'A', 'C']): 'F Major',
    frozenset(['G', 'B', 'D']): 'G Major',
    frozenset(['A', 'C#', 'E']): 'A Major',
    frozenset(['B', 'D#', 'F#']): 'B Major',

    # MINOR CHORDS
    frozenset(['C', 'D#', 'G']): 'C Minor',
    frozenset(['D', 'F', 'A']): 'D Minor',
    frozenset(['E', 'G', 'B']): 'E Minor',
    frozenset(['F', 'G#', 'C']): 'F Minor',
    frozenset(['G', 'A#', 'D']): 'G Minor',
    frozenset(['A', 'C', 'E']): 'A Minor',
    frozenset(['B', 'D', 'F#']): 'B Minor',

    # COMMON 7THS
    frozenset(['G', 'B', 'D', 'F']): 'G7',
    frozenset(['A', 'C#', 'E', 'G']): 'A7',
    frozenset(['E', 'G#', 'B', 'D']): 'E7'
}


def match_chord(detected_notes):
    """
    Identifies the best chord match using subset logic to ignore
    overtones and extra octaves.
    """
    if not detected_notes:
        return "None"

    # Convert incoming list to a set for fast comparison
    # If the FFT detects ['E', 'G#', 'B', 'E'], the set becomes {'E', 'G#', 'B'}
    input_set = set(detected_notes)

    # 1. Check for Exact or Super-set Matches
    # This handles cases where you play extra octaves (e.g., E Major with 2 Es)
    for chord_notes, chord_name in CHORDS.items():
        if chord_notes.issubset(input_set):
            return chord_name

    # 2. Check for Best Partial Match (if no exact match is found)
    # This helps if one note in the triad was too quiet to be detected
    best_partial = "Unknown Chord"
    max_overlap = 0

    for chord_notes, chord_name in CHORDS.items():
        overlap = len(input_set.intersection(chord_notes))
        if overlap > max_overlap and overlap >= 2:
            max_overlap = overlap
            best_partial = f"{chord_name} (?)"

    # 3. Single Note fallback
    if len(detected_notes) == 1:
        return f"Single Note: {detected_notes[0]}"

    return best_partial