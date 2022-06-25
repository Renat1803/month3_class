from bs4 import BeautifulSoup
import requests

URL = "http://jut.su"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}

def get_requests(url, params=''):
    req = requests.get(url, headers=HEADERS, params= params)
    return req

def get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_='media_content')
    print(items)
    anime = []

    for item in items:
        anime.append(
            {
                # "link": URL + item.find("a", class_='media_link l_e_m_l'),
                # # get("href")
                "title": item.find("div", class_="b-g-title").get_text(),
                # "image": URL + item.find("a", class_="media_link l_e_m_l")

            }
        )
    print(anime)

html = get_requests(URL)
get_data(html.text)

def scrapy_script():
    html = get_requests
    if html.status_code == 200:
        anime = []
        for page in range(0, 3):
            html = get_requests(f"https://jut.su/{page}")
            anime.extend(get_data(html.text))
        return anime
    else:
        raise Exception("Error in scrapy script function")


