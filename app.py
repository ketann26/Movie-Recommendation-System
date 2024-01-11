import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np

API_KEY = '99deae501630aa198603e6d9239a9c9c'

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies_df = pd.DataFrame(movies_dict)

similarity1 = pickle.load(open('similarity1.pkl','rb'))
similarity2 = pickle.load(open('similarity2.pkl','rb'))
similarity = np.concatenate((similarity1,similarity2))


def fetch_poster(movie_id):

    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(movie_id,API_KEY))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):

    movie_idx = movies_df[movies_df['title']==movie].index[0]
    distances = similarity[movie_idx]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []

    for i in movies_list:
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movies_df.iloc[i[0]].movie_id))

    return recommended_movies,recommended_movie_posters

st.title('Movie Recommender System')

selected_movie = st.selectbox(
            'Select a movie that you liked',
            movies_df['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])