# import libraries
from string import ascii_lowercase
import urllib.request
from bs4 import BeautifulSoup
import re
import os
import glob
import numpy as np

"""
Helper functions to scrape raw ingredient names from finecooking
"""
def flatten(t):
    """
    flatten a list of sublists
    """
    return [item for sublist in t for item in sublist]

def scrape_finecooking():
    """
    scrape finecooking website to extract list of raw ingredient names
    """
    raw_ingredients = []
    # scrape every page in finecooking ingredients
    for num in range(102):
        file = urllib.request.urlopen('https://www.finecooking.com/ingredients/page/'+ str(num))
        soup = BeautifulSoup(file, "lxml")
        tags = soup.find_all('h2', {'class' : 'article-list__title'})
        for href in tags:
            raw_ingredients.append(re.findall(r'>(.*?)<\/a>', str(href)))
    return raw_ingredients

def create_corpus(raw_ingredients):
    file_list = glob.glob(os.path.join(os.getcwd(), "data/external/ingredients/", "*.txt"))
    txt_ingredients = []

    # add data from every txt file in path
    for file_path in file_list:
        with open(file_path) as f_input:
            txt_ingredients.append(f_input.read().splitlines())
    # flatten ingredients from txt and finecooking
    raw_ingredients = flatten(raw_ingredients)
    txt_ingredients = flatten(txt_ingredients)
    #combine lists
    ingredients = list(set(raw_ingredients + txt_ingredients))
    ingredients = [item.lower() for item in ingredients]

    return ingredients
