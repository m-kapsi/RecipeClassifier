# import libraries
import numpy as np
import regex as re
import inflect
import nltk
import pickle
from stemming.porter2 import stem

"""
Helper functions to extract ingredients from ingredient lines in recipes
"""
def stem_ingredients(a):
    """
    Function to find stem word for cleaned ingredients
    """
    p = nltk.PorterStemmer()
    for word in a:
        if word[-2:] not in ['ge','ce','te','le', 'se', 'er', 'ne', 'us', 'is', 'ss']:
            word = p.stem(word)
    return a

stemmer = inflect.engine()

# import raw ingredients file
with open('../data/external/ingredients/ingredients.pkl', 'rb') as f:
    raw_ingredients = pickle.load(f)

def clean_ingredients(list_ingredients):
    """
    Function to extract ingredient names from ingredient lines in recipes
    """
    #remove non alphabetical characters from string
    regex = re.compile('[^a-zA-Z ]')
    ingr = [regex.sub(' ', ingr) for ingr in list_ingredients]

    #remove "ground" from ingredient names
    ingr = [re.sub(r'(ground)','', ingr) for ingr in list_ingredients]

    # convert to lower string
    ingr_lower = [str.lower(i) for i in ingr]

    # tokenize ingredient lines
    tokens = nltk.word_tokenize(str(ingr_lower))

    # generate bigrams for ingredient lines
    pairs = [ " ".join(pair) for pair in nltk.bigrams(tokens)]
    pairs = [regex.sub('', p) for p in pairs]
    pairs = [p.strip() for p in pairs]
    pairs = [stemmer.singular_noun(word) if stemmer.singular_noun(word) is not False else word for word in pairs]

    #add bigrams present in raw_ingredients to clean ingredients list
    clean_pairs = [i for i in pairs if i in raw_ingredients]

    # generate list of single ingredient tokens
    pairs_joined = []
    for i in ingr:
        joined_str = re.sub('('+'|'.join('\\b'+re.escape(g)+'\\b' for g in clean_pairs)+')',lambda m: m.group(0).replace(' ', '_'),i)
        pairs_joined.append(joined_str)

    # tokenize single ingredient tokens
    tokens = nltk.word_tokenize(str(pairs_joined))
    token_lower = [str.lower(i) for i in tokens]

    #add tokens present in raw_ingredients to clean ingredients list
    clean_tokens = [i for i in token_lower if i in raw_ingredients]
    clean_tokens = [stemmer.singular_noun(word) if stemmer.singular_noun(word) is not False else word for word in clean_tokens]

    #combine clean tokens and clean pairs lists for final output
    clean_ingr = list(set(clean_tokens + clean_pairs))
    while("" in clean_ingr):
        clean_ingr.remove("")

    # standardize common ingredient names
    standard_dict = {
    'yoghurt': 'yogurt',
    'greek yogurt': 'yogurt',
    'greek yoghurt': 'yogurt',
    'plain yoghurt': 'yogurt',
    'plain yogurt': 'yogurt',
    'hemp seed': 'hemp',
    'delicata squash': 'delicata',
    'honeydew melon' : 'honeydew',
    'chia': 'chia seed',
    'poppy': 'poppy seed',
    'coriander seed': 'coriander',
    'acorn': 'acorn squash',
    'pearled barley': 'barley',
    'cheese ravioli': 'ravioli',
    'marinara': 'marinara sauce',
    'alfredo': 'alfredo sauce',
    'water chestnut':'chestnut',
    'anise': 'star anise',
    'romano': 'romano cheese',
    'mozzarella':'mozzarella cheese',
    'parmesan': 'parmesan cheese',
    'cheddar': 'cheddar cheese',
    'ramen': 'ramen noodle',
    'raman': 'ramen noodle',
    'raman noodle': 'ramen noodle',
    'soba':'soba noodle',
    'udon': 'udon noodle',
    'black cod': 'cod',
    'shirataki': 'shirataki noodle',
    'vermicelli': 'vermicelli noodle',
    'celophane': 'celophane noodle',
    'buckwheat': 'buckwheat noodle',
    'soman': 'somen noodle',
    'cres': 'mustard cress',
    'somen': 'somen noodle',
    'corn tortilla': 'tortilla',
    'sweet corn': 'corn',
    'juniper berry' : 'juniper',
    'prepared mustard': 'mustard',
    'penne pasta': 'penne'

    }

    #use stem function to remove plurals
    clean_ingr = stem_ingredients(clean_ingr)
    clean_ingr = [standard_dict.get(item, item) for item in clean_ingr]
    clean_ingr = list(set(clean_ingr))
    #print clean_ingr
    return clean_ingr
