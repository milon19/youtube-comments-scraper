import time

from selenium import webdriver
from bs4 import BeautifulSoup

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications")

browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=chrome_options)


def _scroll_page(numOfScroll):
    last_height = browser.execute_script("return document.documentElement.scrollHeight")
    i = 0
    print('Scrolling to load comment...')
    while True:
        i += 1
        # Scroll down 'til "next load".
        browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(5)

        if i == numOfScroll:
            break
        new_height = browser.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # One last scroll just in case.
    browser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")


def _find_channel_name(content):
    print('Finding Channel Name...')
    _name = content.findAll("div", {"class": "style-scope ytd-channel-name"})
    _name = _name[0].find('a').text
    return _name


def _find_comment_section():
    print('Loading Comments...')

    comment_section = browser.find_element_by_xpath('//*[@id="comments"]')
    browser.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(5)


def _find_comments(browser):
    print('Finding all comments....')
    author_names = browser.find_elements_by_xpath('//*[@id="author-text"]')
    comment_texts = browser.find_elements_by_xpath('//*[@id="content-text"]')
    comments = []
    for author_name, comment in zip(author_names, comment_texts):
        a_comment = {
            'author_name': author_name.text,
            'comment': comment.text
        }
        comments.append(a_comment)
    print('Storing all comments')
    return comments


def run_scraper(urls, numOfScrolls=3):
    allData = []
    for url in urls:

        browser.get(url)
        print('Visiting page: {}'.format(browser.title))
        browser.maximize_window()
        time.sleep(5)

        _find_comment_section()
        _scroll_page(numOfScrolls)
        page_source = browser.page_source
        BS_data = BeautifulSoup(page_source, 'html.parser')
        channel_name = _find_channel_name(BS_data)
        video_title = browser.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comments = _find_comments(browser)
        a_data = {
            'channel_name': channel_name,
            'video_title': video_title,
            'comments': comments
        }
        allData.append(a_data)
    return allData
