import json, datetime

JSON_PATH = '../fixtures/janya_ragas.json'

def format_name(name):
    clean_name = ""
    for c in name:
        if c.isalpha():
            clean_name += c.lower()
    return clean_name.capitalize()

def populate_janya():
    janya_list = open('./janya_ragas.txt', 'r').readlines()
    formatted_list = []

    curr_raga_count = 73
    curr_melakartha_id = 0

    for raga in janya_list:
        if raga == '\n':
            continue
        attributes = raga.split('|')
        if len(attributes) == 2:
            curr_melakartha_id = attributes[0]
        else:
            pk = curr_raga_count
            name = attributes[0].strip()
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
                    "melakarta": int(curr_melakartha_id)
                }
            }
            formatted_list.append(ragaobj)
            curr_raga_count += 1

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(formatted_list, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    populate_janya()
