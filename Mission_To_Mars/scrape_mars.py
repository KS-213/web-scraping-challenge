#Dependencies
from bs4 import BeautifulSoup as bs
import requests as req
from splinter import Browser
import pandas as pd

#scraping data
def scrape():
    data = {}
    output = mars_news()
    data["mars_news"] = output[0]
    data["mars_paragraph"] = output[1]
    data["mars_image"] = mars_images()
    data["mars_facts"] = mars_facts()
    data["mars_hemisphere"] = mars_hemi()

    return data


#NASA Mars News
def mars_news():

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    response = req.get(url)
    soup = bs(response.text, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[0].find('a').text.strip()
    news_p = soup.find_all('div', class_='rollover_description_inner')[0].text.strip()

    output = [news_title, news_p]

    return output


#JPL MARS Featured Image
def mars_images():

    #Navigation
    exe_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **exe_path, headless=False)

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    partial_address = soup.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()
    featured_image_url = "https://www.jpl.nasa.gov"+partial_address

    return featured_image_url


#Mars Facts
def mars_facts():

    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    df = tables[0]

    df.columns = ['description','value']
    df.set_index('description', inplace=True)
    mars_facts=df.to_html(justify='left')
    return mars_facts


#Mars Hemispheres
def mars_hemi():

    exe_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **exe_path, headless=False)

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html,"html.parser")

    hemisphere_image_urls = []

    all_images = soup.find("div", class_ = "result-list" )
    results = all_images.find_all("div", class_="item")

    for hemisphere in results:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    return hemisphere_image_urls
