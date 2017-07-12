#!/opt/conda/bin/python


#import redis
import re
import requests
import pandas as pd
import numpy as np
import json
from IPython.display import display
from spacy.en import English
import pickle
import sys
#!pip install pymongo
#!pip install wikipedia
import wikipedia
import pymongo
args = sys.argv
sys.argv.pop(0)



cli = pymongo.MongoClient(host='34.210.97.79')

#Create a reference to a database
wiki_mongo_database = cli.wiki_mongo_database
cli.database_names()

#Create a reference to a collection
wiki_mongo_collection = cli.wiki_mongo_database.wiki_mongo_collection
cli.database_names()

from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument('-q', '--query', type=str, help='Text to query')



def qry_category(category):
    new_str = re.sub('\s','+', category) 
    r = requests.get('http://en.wikipedia.org/w/api.php?\
                     action=query&\
                     format=json&\
                     list=categorymembers&\
                     cmtitle=Category%3A+{}&\
                     cmlimit=max'.format(new_str))
    re.sub('\s','+', category)
    return pd.DataFrame(r.json()['query']['categorymembers'])


def get_page_df(category):
    ml_df = qry_category(category)
    pages_list=[]
    page_df = ml_df[~ml_df['title'].str.contains('Category:')]
    page_df['category'] = category
    pages_list.append(page_df)
    category_df = ml_df[ml_df['title'].str.contains('Category:')]
    categories = category_df[category_df['title'].str.contains('Category:')]['title'].str.replace('Category:',"")
    if category_df.shape[0]>0:      
        try:
            for category in categories:
                pages_list.append(get_page_df(category))
        except KeyError:
            pass
    pages_df = pd.concat(pages_list)
    pages_df = pages_df.sort_values(by='title', axis=0, ascending=True)
    return pages_df

def get_pages_for_category(category):
    df =get_page_df(category)
    df['category'] = category
    df = df.reset_index()
    return df

def insert_to_wiki_mongo(Category='Business software'):
    df = get_page_df(Category)
    dict_list = []
    for i in df['pageid']:
        try:
            page= wikipedia.page(pageid=i)
            print(page.pageid,page.title)
            dict_ = {
                "pageid":page.pageid,
                "title":page.title,
                "content":page.content,
                "category":Category,
                   }
           
            wiki_mongo_collection.update_one(dict_,{'$set': dict_}, upsert=True)
        except AttributeError:
            pass
        except ValueError:
            print(dict_)
            raise
    return cli.database_names(), wiki_mongo_collection.count()

insert_to_wiki_mongo()
#insert_to_wiki_mongo(args)
#insert_to_wiki_mongo('Business_software')