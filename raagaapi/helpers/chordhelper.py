import re


class ChordHelper:
    NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    NOTE_INTERVALS = {
        '1': 0,
        '2': 2,
        '3': 4,
        '4': 5,
        '5': 7,
        '6': 9,
        '7': 11,
        '8': 12,
        '9': 14,
        '10': 16,
        '11': 17,
        '12': 19,
        '13': 21,
        '14': 23,
        '15': 24,
    }

    NOTE_FEATURES = {
        'bb': -2,
        'b': -1,
        '#': 1,
        '()': "omitted",
    }

    # Converts the chord formula interval to semitones from root
    # ie. b3 => 3
    def get_semitone(self, interval):
        if interval[0] == '(':
            return self.get_semitone(interval[1:-1])
        elif interval.isdigit():
            return self.NOTE_INTERVALS[interval]
        else:
            feature_strip = re.sub(r'\d+', '', interval)
            int_strip = re.sub(r'\D+', '', interval)
            feature = self.NOTE_FEATURES[feature_strip]
            semitones = self.NOTE_INTERVALS[int_strip]
            return semitones + feature

    # Converts the chord formula interval to semitones from root, including omitted detail
    # ie. b3 => [3, False]
    def get_semitone_with_omitted(self, interval, omitted=False):
        if interval[0] == '(':
            return self.get_semitone_with_omitted(interval[1:-1], True)
        elif len(interval) == 1:
            return [self.NOTE_INTERVALS[interval], omitted]
        else:
            feature = self.NOTE_FEATURES[interval[:-1]]
            semitones = self.NOTE_INTERVALS[interval[len(interval) - 1]]
            return [semitones + feature, omitted]

    # Converts single semitone to a note, given a root note
    # 3 , C => D#
    def semitone_to_note(self, semitone, root):
        root_index = self.NOTES.index(root)
        note_index = root_index + semitone
        note = self.NOTES[note_index % 12]
        return note

    # Converts semitones to notes, given a root note
    # [0, 1, 3, 5, 7, 9, 11] , C => ['C', 'C#', 'D#', 'F', 'G', 'A', 'B']
    def semitones_to_notes(self, semitones, root):
        notes = []
        for semitone in semitones:
            note = self.semitone_to_note(semitone, root)
            notes.append(note)
        return notes

    # Converts semitones to notes, given a root note
    # [[0, False], [3, False], [7, False]] , C =>
    # [{'note': 'C', 'omitted': False},
    # {'note': 'D#', 'omitted': False},
    # {'note': 'G', 'omitted': False}]
    def semitones_with_omitted_to_notes(self, semitones, root):
        root_index = self.NOTES.index(root)
        notes = []
        for semitone in semitones:
            note_index = root_index + semitone[0]
            note = self.NOTES[note_index % 12]
            notes.append({'note': note, 'omitted': semitone[1]})
        return notes

    # Takes a Chord Object, eg. '1 3 5' interval formula
    # Takes root note eg. F

    # Identify '1 3 5' intervals as [0, 4, 7] semitones
    # Identify [0, 4, 7] as ['F', 'A', 'C']

    # Returns [{'note': 'F', 'omitted': False}, {'note': 'A', 'omitted': False}, {'note': 'C', 'omitted': False}]
    def get_chord_notes_with_omitted(self, chord, root):
        chord_formula = chord.formula.split()
        semitone_interval = []

        for note in chord_formula:
            semitones = self.get_semitone_with_omitted(note)
            semitone_interval.append(semitones)
        return self.semitones_with_omitted_to_notes(semitone_interval, root)

    def get_chord_semitones(self, chord):
        chord_formula = chord.formula.split()
        semitones = []

        for note in chord_formula:
            semitone = self.get_semitone(note)
            semitones.append(semitone)

        return semitones


class SampleChord:
    def __init__(self):
        self.name = 'Minor 6th'
        self.formula = '1 b3 5 6'
        self.affix = 'min6'
        self.description = 'Minor chord with 6th major scale note added'

if __name__ == '__main__':
    chord = SampleChord()
    helper = ChordHelper()
    semitones = helper.get_chord_semitones(chord)

    print(helper.semitones_to_notes(semitones, 'C'))
    print(helper.get_chord_notes_with_omitted(chord, 'C'))

    # print get_chord_notes(chord, 'F')