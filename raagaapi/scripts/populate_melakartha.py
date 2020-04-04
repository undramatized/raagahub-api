import json, datetime

JSON_PATH = '../fixtures/melakarta_ragas.json'

def format_name(name):
    clean_name = ""
    for c in name:
        if c.isalpha():
            clean_name += c.lower()
    return clean_name.capitalize()

def populate_melakarta():
    melakarta_list = open('./melakarta_ragas.txt', 'r').readlines()

    formatted_list = []
    for raga in melakarta_list:
        attributes = raga.split('|')
        pk = int(attributes[0].strip())
        name = attributes[1].strip()
        arohanam = attributes[2].strip()
        avarohanam = attributes[3].strip()
        ragaobj = {
            "model": "raagaapi.raga",
            "pk": pk,
            "fields": {
                "created": datetime.time().strftime('%Y-%m-%d %H:%M:%S'),
                "name": name,
                "format_name": format_name(name),
                "arohanam": arohanam,
                "avarohanam": avarohanam,
                "melakarta": None
            }
        }

        formatted_list.append(ragaobj)

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(formatted_list, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    populate_melakarta()
