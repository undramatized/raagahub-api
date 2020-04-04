import json

JSON_PATH = '../fixtures/chords.json'

def populate_chords():
    chord_list = open('./chord_list.txt', 'r').readlines()
    chord_count = 1
    formatted_list = []

    for chord in chord_list:
        if chord == '\n':
            break
        attributes = chord.split('|')
        pk = chord_count
        name = attributes[0].strip()
        formula = attributes[1].strip()
        affix = attributes[2].strip()
        description = attributes[3].strip()
        chord_obj = {
            "model": "raagaapi.chord",
            "pk": pk,
            "fields": {
                "name": name,
                "formula": formula,
                "affix": affix,
                "description": description
            }
        }
        chord_count += 1
        formatted_list.append(chord_obj)

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(formatted_list, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    populate_chords()
