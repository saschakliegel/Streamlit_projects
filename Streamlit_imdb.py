import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from scipy.spatial.distance import hamming
import seaborn as sns
from scipy import stats
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
# from surprise import SVD
# from surprise import Dataset
# from surprise.model_selection import cross_validate
import warnings; warnings.simplefilter('ignore')




meta = pd.read_csv('/Users/Sergiokl1/Downloads/Streamlit_projects/meta.csv', header = 0)
meta_cleaned = pd.read_csv('/Users/Sergiokl1/Downloads/Streamlit_projects/meta_cleaned.csv',header = 0)

def movie_recommender(distance_method, id, N):
    
    df_distance = pd.DataFrame(data=meta['id'])
    md_ver5 = meta.drop_duplicates(subset="id", keep="first")
    md_ver5 = md_ver5.set_index('id')
    df_distance = df_distance[df_distance['id'] != int(id)]
    try:
        df_distance['distance'] = df_distance['id'].apply(lambda x: distance_method(np.array(md_ver5.loc[x]),np.array(md_ver5.loc[int(id)])))
    except:
        df_distance['distance'] = df_distance['id'].apply(lambda x: distance_method(np.array(md_ver5.loc[x].iloc[0]),np.array(md_ver5.loc[int(id)])))
    df_distance.sort_values(by='distance', inplace=True)
   
    rec = df_distance.head(N)

    l1 = rec['id'].to_list()
    recom = ()
    for i in l1:
        # index = int(index)
        idx = meta_cleaned[meta_cleaned['id']==str(i)]
        # print(idx)
        title = idx["original_title"].to_string(index=False)
        date = idx["release_date"].to_string(index=False)
        genre = idx["genres"].to_string(index=False)
        genre_toprint = genre.replace("[","").replace("]","").replace("'","")
        recom = "Title: ", title ,  " Release Date: ", date, "\n" ,"Genre: ", genre_toprint
        print(recom)
    return l1

# movie_recommender(hamming,choice_id,10)

def load_css(file_name:str)->None:
    """
    Function to load and render a local stylesheet
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
load_css('style.css')


st.title("Movie Recommender")

list_of_choices = list(meta_cleaned["original_title"])

list_of_choices.append(" ")
movie_choice = st.selectbox("Choose a movie",list_of_choices, index=len(list_of_choices)-1)

if movie_choice != " ":
    choice_id = meta_cleaned[meta_cleaned['original_title'] == movie_choice]['id']
    result_list = movie_recommender(hamming,choice_id,10)

    for i in result_list:
        movie_title = meta_cleaned[meta_cleaned['id'] == str(i)]['original_title'].to_string(index=False)
        
        st.text(movie_title)

#st.text(movie_recommender(hamming,choice_id,10))