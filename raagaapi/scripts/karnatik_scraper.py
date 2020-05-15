import json
import time
import re
import string
from collections import OrderedDict

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup, Comment, NavigableString

URL_FORMAT = 'https://www.karnatik.com/ragas{letter}.shtml'
KRITHI_URL = 'https://www.karnatik.com/{krithi_id}'
JSON_PATH = '../fixtures/krithis.json'

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                print("Received Response")
                return resp.content
            else:
                return None

    except RequestException as e:
        print('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def get_krithi_url_list(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    krithi_list = soup.select('ul a')
    url_list = []

    for krithi in krithi_list:
        url = krithi['href']
        url_list.append(url)

    return url_list

def filter_chunks(chunks):
    """

    :param chunks: List of chunks to be filtered
    :return: A list of filtered chunks
    """
    filtered_content = []
    elements_to_filter = ['', 'first', '|', 'previous', '|', 'next', 'Contact us']
    for element in chunks:
        if element.strip() not in elements_to_filter:
            filtered_content.append(element.strip())

    return filtered_content

def get_krithi_details(html_content):
    pretty_content = BeautifulSoup(html_content, 'html.parser').prettify()
    soup = BeautifulSoup(pretty_content, 'html.parser')
    comments = soup.find_all(string=lambda text: isinstance(text, Comment))

    data = []

    # Filtering out the relevent elements for the song content
    for comment in comments:
        if comment.strip() == '*BEGIN MAIN RIGHTHAND SECTION*':
            next_node = comment.next_sibling

            while next_node and next_node.next_sibling:
                data.append(next_node)
                next_node = next_node.next_sibling

                if not next_node.name and next_node.strip() == '*END RIGHTHAND SECTION*': break;

    all_text = ""
    for chunk in data:
        if isinstance(chunk, NavigableString):
            all_text += str(chunk).strip()
        else:
            all_text += chunk.get_text().strip()

    all_text_spl = all_text.split('\n')

    filtered_content = filter_chunks(all_text_spl)
    print(filtered_content)

    song_name = song_raagam = song_taalam = song_composer = song_lang = ""
    song_lyrics, song_meaning, song_notation, song_info = ([] for i in range(4))

    indices = OrderedDict()

    for index, chunk in enumerate(filtered_content):
        if 'song:' in chunk.lower():
            indices['song'] = index
            if 'raagam' not in filtered_content[index+1].lower() and 'click' not in chunk.lower():
                song_name = filtered_content[index+1].strip()
            else:
                chunk_spl = filter_chunks(re.split('\:|_|-|!', chunk))
                song_name = chunk_spl[1].strip()
        elif 'raagam:' in chunk.lower():
            indices['raagam'] = index
            if 'janya' not in filtered_content[index+1].lower():
                song_raagam = filtered_content[index+1].strip()
        elif 'taalam:' in chunk.lower():
            indices['taalam'] = index
            if len(chunk.split(':')) == 2:
                song_taalam = chunk.split(':')[1].strip().lower()
        elif 'composer:' in chunk.lower():
            indices['composer'] = index
            chunk_spl = filter_chunks(re.split('\:|_|-|!', chunk))
            if len(chunk_spl) >= 2:
                song_composer = chunk_spl[1]
            elif 'language' not in filtered_content[index + 1].lower():
                song_composer = filtered_content[index + 1].strip()
        elif 'language:' in chunk.lower():
            indices['language'] = index
            chunk_spl = filter_chunks(re.split('\:|_|-|!', chunk))
            if len(chunk_spl) >= 2:
                song_lang = chunk_spl[1]
            elif 'pallavi' not in filtered_content[index+1].lower():
                song_lang = filtered_content[index+1].strip()
        elif 'pallavi' in chunk.lower() and 'anupallavi' not in chunk.lower():
            indices['pallavi'] = index
            i = 0
            while index+i < len(filtered_content):
                if any(x in filtered_content[index+i].lower() for x in ['meaning','information','notation']):
                    break
                song_lyrics.append(filtered_content[index+i].strip())
                i += 1
        elif 'meaning:' in chunk.lower():
            indices['meaning'] = index
            i = 1
            while index+i < len(filtered_content):
                if any(x in filtered_content[index+i].lower() for x in ['information','notation']):
                    break
                song_meaning.append(filtered_content[index+i].strip())
                i += 1
        elif 'notation:' in chunk.lower():
            indices['notation'] = index
            i = 1
            while index+i < len(filtered_content):
                if 'information' in filtered_content[index+i].lower():
                    break
                song_notation.append(filtered_content[index+i].strip())
                i += 1
        elif 'information:' in chunk.lower():
            indices['information'] = index
            i = 1
            while index+i < len(filtered_content):
                song_info.append(filtered_content[index+i].strip())
                i += 1

    if len(song_lyrics) == 0:
        keys = list(indices.keys())
        end_key = keys[keys.index('language')+1]
        for i in range(indices['language']+1, indices[end_key]):
            song_lyrics.append(filtered_content[i])

    krithi = {'name': song_name,
              'raaga': song_raagam,
              'taala': song_taalam,
              'composer': song_composer,
              'language': song_lang,
              'lyrics': song_lyrics,
              'meaning': song_meaning,
              'notation': song_notation,
              'other_info': song_info}

    print(krithi)
    return krithi


if __name__ == '__main__':
    # for l in string.ascii_lowercase:
    #     print(l)

    letter = 'a'
    url = URL_FORMAT.format(letter=letter)
    html = simple_get(url)

    urls = get_krithi_url_list(html)
    print(urls)

    krithi_details = []

    for url in urls:
        print(url)
        krithi_url = KRITHI_URL.format(krithi_id=url)
        content = simple_get(krithi_url)
        if content:
            krithi = get_krithi_details(content)
            krithi_details.append(krithi)

        time.sleep(1)

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(krithi_details, f, ensure_ascii=False, indent=4)

    # krithi_url = KRITHI_URL.format(krithi_id='c0000.shtml')
    # content = simple_get(krithi_url)
    #
    # krithi = get_krithi_details(content)
