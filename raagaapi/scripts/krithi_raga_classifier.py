import requests
import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raagahubapi.settings')
django.setup()

from raagaapi.models import Raga

KRITHIS_JSON_PATH = '../fixtures/krithis_a.json'
MELAKARTHA_JSON_PATH = '../fixtures/melakarta_ragas.json'
JANYA_JSON_PATH = '../fixtures/janya_ragas.json'


def get_json(path):
    """
    Returns data of a JSON file
    :param path: path of JSON file
    :return: JSON data
    """
    with open(path) as f:
        data = json.load(f)
    return data


def get_raaga_ids():
    all_ragas = Raga.objects.all()
    raga_ids = {}

    for raga in all_ragas:
        raga_ids[raga.name.lower()] = raga.pk
        aliases = raga.aliases.split(',')
        for alias in aliases:
            raga_ids[alias.lower()] = raga.pk

    return raga_ids


def update_raga_alias(raga_id, alias):
    raga_obj = Raga.objects.get(pk=raga_id)
    raga_aliases = raga_obj.aliases
    alias_list = raga_aliases.split(',')

    if alias not in alias_list:
        alias_list.append(alias)

    updated_aliases = ','.join(alias_list)
    raga_obj.aliases = updated_aliases
    raga_obj.save()

def update_raga_json_alias(raga_id, alias):
    if raga_id < 73:
        json_path = MELAKARTHA_JSON_PATH
    else:
        json_path = JANYA_JSON_PATH

    data = get_json(json_path)

    for index, raga in enumerate(data):
        if raga['pk'] == raga_id:
            raga_aliases = raga['fields']['aliases']
            alias_list = raga_aliases.split(',')

            if alias not in alias_list:
                alias_list.append(alias)

            updated_aliases = ','.join(alias_list)
            data[index]['fields']['aliases'] = updated_aliases

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    krithis = get_json(KRITHIS_JSON_PATH)
    raaga_ids = get_raaga_ids()

    unknown_raagas = []

    for krithi in krithis:
        if krithi['raaga'].lower() in list(raaga_ids.keys()):
            krithi['raaga_id'] = raaga_ids[krithi['raaga'].lower()]
        else:
            if (krithi['raaga'], 0) not in unknown_raagas:
                unknown_raagas.append((krithi['raaga'], 0))

    print(unknown_raagas)

    raga_aliases_a = [
        ("aabheri", 136),
        ('aabhOgi', 137),
        ('ahIrbhairav', 118),
        ('aahiri', 73),
        ('aahir bhairav', 118),
        ('Ananda', 81),
        ('Anandabhairavi', 121),
        ('aananda bhairavi', 121),
        ('Ananda bhairavi', 121),
        ('aanandabhairavi', 121),
        ('Anndabhairavi', 121),
        ('AndOLikA', 138),
        ('aandOLikaa', 138),
        ('aarabi', 227),
        ('Arabhi/hamsAnandi', 227),
        ('amrtavAhini', 120),
        ('amritavaahini', 120),
        ('amrtavarSiNi', 286),
        ('amritavarshini', 286),
        ('amrtavarSaNi', 286),
        ('amrtavarSaNI', 286),
        ('ArdradEshi', 82),
        ('asaavEri', 74),
        ('aThANA', 228),
        ('aThaaNaa', 228),
        ('aThAna', 228),
        ('AThANA', 228),
        ('aThANa', 228)
    ]

    for alias in raga_aliases_a:
        update_raga_json_alias(alias[1], alias[0])
