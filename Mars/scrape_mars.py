from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
from selenium import webdriver
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    listings = {}

    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    # JPL Space Image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)

    
    browser.click_link_by_partial_text('more info')

    
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    
    feat_img_url = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{feat_img_url}'
   
   # Visit Twitter url for latest Mars Weather
    weather_url = "https://twitter.com/marswxreport"
    browser.visit(weather_url)
    time.sleep(5)
    html = browser.html

    
    soup = BeautifulSoup(html, 'html.parser')

    
    tweets = soup.find_all('div', class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0")

  
    for tweet in tweets: 
        mars_weather = tweet.find('span').text
        if 'InSight' and 'winds' in mars_weather:
            print(mars_weather)
            break
        else: 
            pass

    #Mars Facts
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    html = browser.html

    table = pd.read_html(url)
    mars_facts = table[2]
    
    mars_facts.columns = ['Description','Value']
    mars_facts.set_index('Description', inplace=True)
    
    mars_facts.to_html('Facts_table.html')

    # USGS Astrogeology webpage 
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    soup = BeautifulSoup(html, "html.parser")
    hemisphere_image_urls = []

    results = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

# loop through images to get the links
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
    
    All_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()
    
    return All_data


