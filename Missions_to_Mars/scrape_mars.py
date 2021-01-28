from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

# Define scrape which will be used in FLASK app.py
# Intent is to allow user to click a button to call this function

def scrape():
    #Define executable path so browser knows where to pull commands from

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    ##NASA MARS NEWS###
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html

    #BeautifulSoup to parse through HTML

    soup = bs(html, 'html.parser')

    #Use soup to parse through HTML to find news snippets

    results = soup.find_all('div', class_="list_text")

    news_list = []

    #For loop to grab title and summary paragraph from each snippet

    for result in results:
        try:
            news_title = result.find('a').text
            news_p = result.find('div', class_="article_teaser_body").text

            #Dictionary included with intent of importing to mongoDB

            news_dict = {'News Title': news_title,
                        'News Description': news_p}
            news_list.append(news_dict)

        except AttributeError as e:
            print(e)


    url_jpl_base = 'https://www.jpl.nasa.gov'
    url_jpl_spaceimages_home_endpoint = '/spaceimages/?search=&category=Mars'
    url_jpl = url_jpl_base + url_jpl_spaceimages_home_endpoint
    browser.visit(url_jpl)

    html_jpl = browser.html
    soup_jpl = bs(html_jpl, 'html.parser')

    jpl_image_filter = soup_jpl.find('div', class_="lg:p-0 w-72 relative z-20 p-2 pl-0 -ml-3 text-base")

    jpl_image_endpoint = jpl_image_filter.img["src"]

    jpl_image_url = url_jpl_base + jpl_image_endpoint

    ## Mars Facts ##

    url_mars_facts_base = 'https://space-facts.com/mars/'
    browser.visit(url_mars_facts_base)

    #Pandas used to read in HTML tables

    tables = pd.read_html(url_mars_facts_base)

    #First table in list provides information about Mars. Extract

    df = tables[0]
    df.columns = ['Description', 'Information']

    #Set index and then remove name. Don't want description column name in final product

    df.set_index('Description', inplace=True)
    df.index.name = ''

    #Convert dataframe to HTML

    html_table = df.to_html()

    ## Mars Hemispheres ##

    url_mars_hemi_base = 'https://astrogeology.usgs.gov'
    url_mars_hemi_search_main_endpoint = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_mars_hemi_main_page = url_mars_hemi_base + url_mars_hemi_search_main_endpoint
    browser.visit(url_mars_hemi_main_page)

    html_mars_hemi = browser.html
    soup_mars_hemi = bs(html_mars_hemi, 'html.parser')

    mars_hemi_filter = soup_mars_hemi.find_all('div', class_="item")

    hemisphere_image_urls = []

    #Run for loop to capture image titles and URLs for each respective hemisphere

    for entry in mars_hemi_filter:
        image_endpoint = entry.a['href']
        image_url = url_mars_hemi_base + image_endpoint
        browser.visit(image_url)
        html_entry = browser.html
        soup_entry = bs(html_entry, 'html.parser')
        image_src_filter = soup_entry.find('img', class_= 'wide-image')['src']
        image_src_filter_url = url_mars_hemi_base + image_src_filter
        image_title_filter = soup_entry.find('h2', class_= 'title').get_text()

        #Create dictionary with intent to enter into mongoDB later

        image_dict = {'title': image_title_filter,
                    'img_url': image_src_filter_url}
        hemisphere_image_urls.append(image_dict)

    #Create dictionary of arrays

    scraped_data = {
        'news_list' : news_list,
        'jpl_image_url': jpl_image_url,
        'html_table': html_table,
        'hemisphere_image_urls': hemisphere_image_urls
    }

    #Close browser

    browser.quit()

    return scraped_data
    


