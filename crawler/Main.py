from urllib.request import Request
from urllib.request import urlopen
from urllib.error import HTTPError
from threading import Thread
import time

from bs4 import BeautifulSoup

from crawler import AppUI

running = False
url_to_crawl = []
url_crawled = []
output = []
base_href = None
global_time = 0


def crawl():
    global main_frame
    result = True
    while result is not False:
        result = next_item()
    main_frame.reset()


def next_item():
    global url_crawled
    global url_to_crawl
    global base_href
    global running

    black_list = ['.pdf', '.doc', 'docx', '.jpg', '.png', '.gif', '.jpeg']

    if running is False or len(url_to_crawl) == 0:
        running = False
        return False

    url = url_to_crawl.pop(0)

    start_time = time.clock()

    req = Request(url)

    try:
        f = urlopen(req)
    except HTTPError as e:
        diff = time.clock() - start_time
        diff = round(diff, 2)
        update_ui(url, e.code, diff)
        return True

    html = f.read()

    b = BeautifulSoup(html)

    if base_href is None:
        base_href = b.find('base')['href']

    links = b.findAll('a')

    for link in links:
        href = link.get('href')
        if href is None or 'http://' in href or 'https://' in href or 'mailto:' in href or 'javascript:' in href or href == '#' or href.strip() == '' or href == '/' or href[-4:] in black_list:
            continue

        if href[0] == '/':
            href = href[1:]
        href = href.split('#')[0]
        href = base_href + href
        if href not in url_crawled and href not in url_to_crawl:
            url_to_crawl.append(href)

    diff = time.clock() - start_time

    diff = round(diff, 2)

    update_ui(url, f.getcode(), diff)
    return True


def update_ui(_done_url, _code, _time):
    global main_frame
    global url_crawled
    global url_to_crawl
    global global_time

    global_time += _time

    url_crawled.append(_done_url)
    output.insert(0, str(_code)+"\t"+str(_time)+"\t"+_done_url)

    remaining = (global_time/len(url_crawled)) * len(url_to_crawl)
    main_frame.update(url_to_crawl, output, global_time, remaining)


def toggle_crawl(_running, _url):
    global url_crawled
    global url_to_crawl
    global base_href
    global running
    global global_time
    global output

    running = _running

    if running is True:
        global_time = 0
        output = []
        url_crawled = []
        url_to_crawl = [_url]
        base_href = None
        Thread(target=crawl).start()

main_frame = AppUI.Main()
main_frame.toggle_handler = toggle_crawl
main_frame.mainloop()