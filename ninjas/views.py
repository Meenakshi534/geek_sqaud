from django.shortcuts import render
from requests.compat import quote_plus

import requests
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from . import models
import re

# Create your views here.

#BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/sss?query={}'
BASE_EBAY_URL = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw={}&_sacat=0'

BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg'

def home(request):

    return render(request, 'base.html')
def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    print(quote_plus(search))
    final_url = BASE_EBAY_URL.format(quote_plus(search))
    

    print(final_url)
    response = requests.get(final_url, verify=False)
    data = response.text
    
    """header = {
        "Accept-Language": "en-GB,en;q=0.9,te-IN;q=0.8,te;q=0.7,en-US;q=0.6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }"""
    

    soup = BeautifulSoup(data, features='html.parser')
    
    #post_listings = soup.find_all('li')

    #post_listings2 = soup.find_all('li', {'class':'cl-search result cl-search-view-mode-list'})
    #post2= soup.select("li.cl-search result.cl-search-view-mode-list")
    posts_ebay = soup.find('div', {'id': 'srp-river-results'})
    #print(posts_ebay)
    
    post_listings = posts_ebay.find_all('li')
    final_postings = []
    for post in post_listings:
        if post.find(class_ = 's-item__title'):
            post_title = post.find('span').text
        else:
            post_title = "No title"

        if post.find(class_='s-item__link'):
            post_url = post.find('a').get('href')
        
        if post.find('span', class_ ='s-item__price'):
            post_price = post.find('span', class_ = 's-item__price').text
        
        if post.find('img'):
            post_img_url = post.find('img').get('src')
            
        if post_title != "No title" and post_title !='':
            final_postings.append((post_title, post_url, post_price, post_img_url))

        

    #print(final_postings)
    
    


    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
        
    }

    

    return render(request, 'ninjas/new_search.html', stuff_for_frontend)
