from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def scrape():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    ##NASA MARS NEWS###
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')

    results = soup.find_all('div', class_="list_text")
    news_list = []

    for result in results:
        try:
            # Identify and return title of listing
            news_title = result.find('a').text
            # Identify and return price of listing
            news_p = result.find('div', class_="article_teaser_body").text

            # Print results only if title, price, and link are available
            #if (news_title and news_p):
                #print('-------------')
                #print(f'Title: {news_title}')
                #print('')
                #print(f'Description: {news_p}')
            news_dict = {'News Title': news_title,
                        'News Description': news_p}
            news_list.append(news_dict)

        except AttributeError as e:
            print(e)

    #REMEMBER YOU WILL LIKELY NEED TO CREATE DICTIONARY TO INPUT TO MONGODB

    url_jpl_base = 'https://www.jpl.nasa.gov'
    url_jpl_spaceimages_home_endpoint = '/spaceimages/?search=&category=Mars'
    url_jpl = url_jpl_base + url_jpl_spaceimages_home_endpoint
    browser.visit(url_jpl)

    html_jpl = browser.html
    soup_jpl = bs(html_jpl, 'html.parser')
    #print(soup_jpl.prettify())


    featured_image_filter = soup_jpl.find('div', class_="default floating_text_area ms-layer")
    #featured_image_filter

    featured_image_endpoint = featured_image_filter.footer.a['data-fancybox-href']
    #featured_image_endpoint

    featured_image_url = url_jpl_base + featured_image_endpoint
    #featured_image_url

    ## Mars Facts ##

    url_mars_facts_base = 'https://space-facts.com/mars/'
    browser.visit(url_mars_facts_base)

    tables = pd.read_html(url_mars_facts_base)

    #type(tables)

    df = tables[0]
    df.columns = ['Description', 'Information']
    #df.head()


    df.set_index('Description', inplace=True)
    df.index.name = ''
    #df.head()


    html_table = df.to_html()
    #html_table

    ## Mars Hemispheres ##

    url_mars_hemi_base = 'https://astrogeology.usgs.gov'
    url_mars_hemi_search_main_endpoint = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    url_mars_hemi_main_page = url_mars_hemi_base + url_mars_hemi_search_main_endpoint
    browser.visit(url_mars_hemi_main_page)

    html_mars_hemi = browser.html
    soup_mars_hemi = bs(html_mars_hemi, 'html.parser')
    #print(soup_mars_hemi.prettify())

    mars_hemi_filter = soup_mars_hemi.find_all('div', class_="item")
    #mars_hemi_filter

    hemisphere_image_urls = []

    for entry in mars_hemi_filter:
        image_endpoint = entry.a['href']
        image_url = url_mars_hemi_base + image_endpoint
        browser.visit(image_url)
        html_entry = browser.html
        soup_entry = bs(html_entry, 'html.parser')
        image_src_filter = soup_entry.find('img', class_= 'wide-image')['src']
        image_src_filter_url = url_mars_hemi_base + image_src_filter
        image_title_filter = soup_entry.find('h2', class_= 'title').get_text()
        image_dict = {'title': image_title_filter,
                    'img_url': image_src_filter_url}
        hemisphere_image_urls.append(image_dict)
        #print(image_src_filter_url)
        #print(image_title_filter)

    #hemisphere_image_urls

    scraped_data = {
        'News Clippings' : news_list,
        'Featured Image URL': featured_image_url,
        'HTML Table': html_table,
        'Hemisphere Info': hemisphere_image_urls
    }
    return scraped_data
    
#scrape()


