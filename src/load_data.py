# import libraries
import os
import pandas as pd
import json

"""
Helper function to output relevant data from json files to dataframe
"""

def load_data(data_folder = '../data/raw/yummly_recipes'):
    '''Helper function to load and concat data'''
    df = None
    for file in os.listdir(data_folder):
        if 'DS_' in file:
            continue
        file_path = os.path.join(data_folder, file)
        with open(file_path) as sd:
            data = json.load(sd)
            recipe_info = {k: v for k, v in data.items() if k in ('totalTime',
                                                       'name',
                                                       'prepTime',
                                                       'id',
                                                       'totalTimeInSeconds',
                                                       'flavors',
                                                       'rating', 'ingredientLines')}

            # add course/cusine data
            attributes = {k: v for k,v in data['attributes'].items() if k in ('course', 'cuisine')}
            recipe_info.update(attributes)

            # add nutrition data
            nutrition_attr = ['PROCNT', 'FAT_KCAL', 'CHOCDF', 'FAT']
            nutrition = {val['attribute']:val['value'] for val in data['nutritionEstimates'] if val['attribute'] in nutrition_attr}
            recipe_info.update(nutrition)

            # add source
            recipe_info['source'] = data['source']['sourceRecipeUrl']

            #concatenate
            recipe_info = [recipe_info]
            cdf = pd.DataFrame(recipe_info)
            df = cdf if df is None else pd.concat([df, cdf])
    return df
