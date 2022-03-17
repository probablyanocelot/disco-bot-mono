

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def download_file(session, link, path):
    r = session.get(link, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r:
                f.write(chunk)


base_url = "http://www.e-radio.gr"
url = "http://www.e-radio.gr/Rainbow-89-Thessaloniki-i92/live"

with requests.Session() as session:
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'}
    response = session.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    frame = soup.find(id="playerControls1")
    frame_url = urljoin(base_url, frame["src"])

    response = session.get(frame_url)
    soup = BeautifulSoup(response.content, "html.parser")
    link = soup.select_one(".onerror a")['href']
    flash_url = urljoin(response.url, link)

    response = session.get(flash_url)
    soup = BeautifulSoup(response.content, "html.parser")
    mp3_link = soup.select_one("param[name=flashvars]")[
        'value'].split("url=", 1)[-1]
    print(mp3_link)

    download_file(session, mp3_link, "download.mp3")
