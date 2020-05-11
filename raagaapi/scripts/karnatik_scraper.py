import string
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup, Comment

URL_FORMAT = 'https://www.karnatik.com/ragas{letter}.shtml'
KRITHI_URL = 'https://www.karnatik.com/{krithi_id}'

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

def get_krithi_info(html_content):
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

    # Get krithi name
    songstr = str(data[2])
    song_name = songstr.split('\n')[2]

    # Get krithi content
    info_elements = data[3]
    raaga_content = info_elements.select('a')[0]

    song_ragam = raaga_content.text.strip()

    song_content = info_elements.select('p p p i')[0].parent.contents[3].text.split('\n')
    filtered_content = []
    elements_to_filter = ['', 'first', '|', 'previous', '|', 'next', 'Contact us']
    for element in song_content:
        if element.strip() not in elements_to_filter:
            filtered_content.append(element.strip())

    # print(filtered_content)

    song_taalam = song_composer = song_lang = song_lyrics = song_meaning = song_notation = song_info = ""

    for index, chunk in enumerate(filtered_content):
        if 'taalam' in chunk.lower():
            if len(chunk.split(':')) == 2:
                song_taalam = chunk.split(':')[1].strip().lower()
        elif 'composer' in chunk.lower():
            if 'language' not in filtered_content[index+1].lower():
                song_composer = filtered_content[index+1].strip().lower()
        elif 'language' in chunk.lower():
            if 'pallavi' not in filtered_content[index+1].lower():
                song_lang = filtered_content[index+1].strip.lower()
        elif 'pallavi' in chunk.lower():
            song_lyrics = []
            i = 0
            while 'meaning' not in filtered_content[index+i].lower():
                song_lyrics.append(filtered_content[index+i].strip())
                i += 1
        elif 'meaning' in chunk.lower():
            song_meaning = []
            i = 1
            while 'notation' not in filtered_content[index+i].lower():
                song_meaning.append(filtered_content[index+i].strip())
                i += 1
        elif 'notation' in chunk.lower():
            song_notation = []
            i = 1
            while 'information' not in filtered_content[index+i].lower():
                song_notation.append(filtered_content[index+i].strip())
                i += 1
        elif 'information' in chunk.lower():
            song_info = []
            i = 1
            while index+i < len(filtered_content):
                song_info.append(filtered_content[index+i].strip())
                i += 1

    krithi = {'name': song_name,
              'raga': song_ragam,
              'taala': song_taalam,
              'composer': song_composer,
              'language': song_lang,
              'lyrics': song_lyrics,
              'meaning': song_meaning,
              'notation': song_notation,
              'other_info': song_info}

    print(krithi)



if __name__ == '__main__':
    # for l in string.ascii_lowercase:
    #     print(l)

    # letter = 'a'
    # url = URL_FORMAT.format(letter=letter)
    # html = simple_get(url)
    #
    # urls = get_krithi_url_list(html)
    # print(urls)

    krithi_url = KRITHI_URL.format(krithi_id='c8930.shtml')
    content = simple_get(krithi_url)

    get_krithi_info(content)
