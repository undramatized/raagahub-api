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

    # Returns same as get_chord_notes_with_omitted without the omitted data
    # ['F', 'A', 'C']
    def get_chord_notes(self, chord, root):
        chord_formula = chord.formula.split()
        semitone_interval = []

        for note in chord_formula:
            semitones = self.get_semitone(note)
            semitone_interval.append(semitones)
        return self.semitones_to_notes(semitone_interval, root)

    def get_chord_semitones(self, chord):
        chord_formula = chord.formula.split()
        semitones = []

        for note in chord_formula:
            semitone = self.get_semitone(note)
            semitones.append(semitone)

        return semitones

    # Given a root note, returns the semitones of chord relative to the root note
    # ('A', Chord(maj)) for root F => A[0, 4, 7] -> F[4, 8, 11]
    # Maximum value of semitone is 11
    def get_chord_semitones_with_root(self, chord, root):
        chord_root = chord[0]
        chord_obj = chord[1]
        chord_formula = chord_obj.formula.split()
        semitones = []

        for note in chord_formula:
            semitone = self.get_semitone(note)
            semitones.append(semitone)

        transpose_val = self.NOTES.index(chord_root) - self.NOTES.index(root)
        return [(semitone+transpose_val)%12 for semitone in semitones]





class SampleChord:
    def __init__(self, id, formula, affix):
        self.name = 'Generic Name'
        self.id = id
        self.formula = formula
        self.affix = affix
        self.description = 'description'

    def get_semitones(self):
        return ChordHelper().get_chord_semitones(self)

if __name__ == '__main__':
    chordmaj = SampleChord(1, "1 3 5", "maj")
    chordmin = SampleChord(2, "1 b3 5", "min")
    helper = ChordHelper()
    semitones = helper.get_chord_semitones(chordmaj)
    print(semitones)

    print(helper.semitones_to_notes(semitones, 'C'))
    print(helper.get_chord_notes_with_omitted(chordmaj, 'C'))

    print(helper.get_chord_notes(chordmaj, 'C'))