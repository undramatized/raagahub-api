from raagaapi.helpers.chordhelper import ChordHelper

class RagaHelper:
    SWARAS = ["S", "R1", "R2", "R3", "G1", "G2", "G3", "M1", "M2",
              "P", "D1", "D2", "D3", "N1", "N2", "N3"]

    SWARA_INTERVALS = {
        'S': 0,
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'G1': 2,
        'G2': 3,
        'G3': 4,
        'M1': 5,
        'M2': 6,
        'P': 7,
        'D1': 8,
        'D2': 9,
        'D3': 10,
        'N1': 9,
        'N2': 10,
        'N3': 11,
    }

    # Returns a list of semitone intervals that a list of swaras represent
    # eg. [S, R2, G3, P, D2] => [0, 2, 4, 7, 9]
    def get_semitones(self, swaras):
        semitones = []
        for swara in swaras:
            semitones.append(self.SWARA_INTERVALS[swara])

        return semitones

    # Returns the western scale note for a swara, given a root note
    # eg. R2 in the key D => E
    def get_swara_note(self, swara, root):
        swara_semitone = self.SWARA_INTERVALS[swara]
        return ChordHelper().semitone_to_note(swara_semitone, root)

    # Returns a chord transposed to a particular swara's semitone position, to get it's relative position in a raaga
    # eg. [0,4,7] for swara at 2 => [2,6,9]
    def transpose_chord(self, swara_semitone, chord_semitones):
        transposed = []
        for note in chord_semitones:
            transposed.append((note + swara_semitone) % 12)
        return transposed

    # Arguments: All swaras, all chords, root note
    # ["S", "R1", "G2", "M1", "P", "D2", "N3"]
    # chordlist = [chordmaj, chordmin, chordsus4] => from Chord Model
    # C
    # Returns a list of chords per swaras
    # {
    #   'S' : {'note': 'F', 'chord_ids': [1, 4, 7]},
    #   'R2' : {'note': 'G', 'chord_ids': [3, 4, 5]}
    # }

    def get_chords_from_swaras(self, swaras, chords, root):
        swara_semitones = self.get_semitones(swaras)
        swara_semi_set = set(swara_semitones)
        all_swara_chords = {}

        for i in range(len(swaras)):
            note = self.get_swara_note(swaras[i], root)
            swara_chords = []
            for chord in chords:
                chord_semitones = chord.get_semitones()
                transposed_semitones = self.transpose_chord(swara_semitones[i], chord_semitones)
                transposed_set = set(transposed_semitones)

                if transposed_set.issubset(swara_semi_set):
                    chord_details = {
                        'chord_name': note + chord.affix,
                        'chord_id': chord.id,
                        'chord_formula': chord.formula
                    }
                    swara_chords.append(chord_details)
            swara_chord_obj = {
                'note': note,
                'chords': swara_chords
            }
            all_swara_chords[swaras[i]] = swara_chord_obj

        return all_swara_chords

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
    swaras = ["S", "R1", "G2", "M1", "P", "D2", "N3"]
    helper = RagaHelper()
    chord = helper.get_semitones(swaras)

    print(helper.get_swara_note("R1", "C"))
    print(chord)
    print(helper.transpose_chord(3, chord))

    chordmaj = SampleChord(1, "1 3 5", "maj")
    chordmin = SampleChord(2, "1 b3 5", "min")
    chordsus4 = SampleChord(3, "1 4 5", "sus4")

    chordlist = [chordmaj, chordmin, chordsus4]

    print(helper.get_chords_from_swaras(swaras, chordlist, 'C'))
