from bs4 import BeautifulSoup as bs
import requests
import splinter
from splinter import Browser
import pandas as pd
from flask import Markup


#urls
hemisphere_image_urls = [
    {"Cerberus_Hemisphere":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif"},
    {"Schiaparelli_Hemisphere":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif"},
    {"Syrtis_Major_Hemisphere":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif"},
    {"Valles_Marineris_Hemisphere":"http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif"}
    
]

news_url = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
featured_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
facts_url = "https://space-facts.com/mars/"
twitter_url = "https://twitter.com/marswxreport?lang=en"


#Scrapes different sites for Mars content
def scrape(): 
    # visit news url, return latest headline and body
    resp = requests.get(news_url).json()
    news_title = resp.get("items")[0].get('title')
    news_b = bs(resp.get("items")[0].get('body'), 'html.parser').get_text()
    news = {"title": news_title, "body": news_b}

    #add hemisphere images
    
    news.update({"Hemisphere_image": hemisphere_image_urls})
        

    #get featured image on jpl spaceimages
    resp = requests.get(featured_image_url)
    image = bs(resp.text, 'lxml')
    image_class = image.find("section", {"class": "centered_text clearfix main_feature primary_media_feature single"})
    jpg = image_class.a['data-fancybox-href']
    jpg_url = 'https://www.jpl.nasa.gov' + jpg
    news.update({"featured_image": jpg_url})

    #scrape mars Twitter for weather info
    t_resp = requests.get(twitter_url).text
    soup = bs(t_resp, "html.parser")
    weather = soup.find("p", {'class':"TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).getText()
    news.update({"weather" : weather})

    #get facts table from space facts
    facts_resp = requests.get(facts_url)
    facts_soup = bs(facts_resp.text, 'html.parser')
    facts_table = Markup(facts_soup.find('table', {"class": "tablepress tablepress-id-comp-mars blue-table"}))
    facts_df = pd.read_html(str(facts_table))[0]
    news.update({"facts_table": facts_table})


    return news

