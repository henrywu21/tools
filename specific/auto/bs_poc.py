#! /usr/bin/env python3

from bs4 import BeautifulSoup
from urllib.request import urlopen


def eg_wiki():
    with urlopen('https://en.wikipedia.org/wiki/Main_Page') as response:
        soup = BeautifulSoup(response, 'html.parser')
        for anchor in soup.find_all('a'):
            print(anchor.get('href', '/'))


def eg_bp():
    html_doc = """
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class="title"><b>The Dormouse's story</b></p>

    <p class="story">Once upon a time there were three little sisters; and their names were
    <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
    <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
    <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
    and they lived at the bottom of a well.</p>

    <p class="story">...</p>
    """
    soup = BeautifulSoup(html_doc, 'html.parser')
    # print(soup.prettify())
    # print(soup.get_text())
    # print(soup.title)
    # print(soup.title.name)
    # print(soup.title.string)
    # print(soup.title.parent)
    print(soup.find(id='link2'))
    print(soup.find(id='link2').next_sibling.next_sibling)
    for link in soup.find_all('a', limit=2):
        print(link.get('href'))

    print(soup.select("p:nth-of-type(3)"))

    print(soup.select("p > a:nth-of-type(2)"))
    print(soup.select("p > #link1"))

if __name__ == "__main__":
    eg_bp()
