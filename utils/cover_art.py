import requests
from bs4 import BeautifulSoup

def cover_art(query: str) -> str:
    '''
    Returns a URL of an image relevant to the search query.

        Parameters:
            query (str): string to find an image for

        Returns:
            URL of image relevant to the query
    '''

    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(query)
    content = requests.get(url).content
    soup = BeautifulSoup(content, 'html.parser')
    images = soup.find_all('img')

    return images[1].get('src')