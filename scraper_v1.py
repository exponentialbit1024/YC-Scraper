from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mode", required = True, help = "Mode to run the scraper")
ap.add_argument("-s", "--save", required = False)
args = vars(ap.parse_args())

def parse_html(tr_ob):
    all_cos = []
    for idx, company in enumerate(tr_ob):
        co_ob = {}
        co_info = company.find_all('td')
        co_name = co_info[0]
        co_descp = co_info[2]
        link_ob = co_name.find('a')
        co_link = None
        if link_ob is not None:
            co_link = link_ob.get('href')
        co_ob['name'] = co_name.text
        co_ob['link'] = co_link
        co_ob['description'] = co_descp.text
        all_cos.append(co_ob)
    return all_cos

if args['mode'] == 'o':

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    url = "https://www.ycombinator.com/companies/"

    browser = webdriver.Chrome("<PATH_TO_CHROMEDRIVER>", chrome_options = chrome_options)
    browser.get(url)
    html = browser.page_source
    f = open("yc_co.html", "w")
    f.write(html)
    f.close()
    soup = BeautifulSoup(html, 'lxml')
    all_cos = parse_html(soup.find_all('tr'))
else:
    f = open("yc_co.html")
    html = f.read()
    f.close()
    soup = BeautifulSoup(html, 'lxml')
    all_cos = parse_html(soup.find_all('tr'))

if args['save'] is not None:
    import pandas as pd
    df = pd.DataFrame(all_cos)
    df.to_csv("yc_cos_list.csv")
