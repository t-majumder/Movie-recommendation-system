import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c8c890e819039b211799406ac0f26702&language=en-US"

    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path'] is not None:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image+Available"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommendation System')

selected_movie_name = st.selectbox(
    'Movies',
    movies['title'].values
)

col1, col2, col3, col4, col5 = st.columns(5)
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    with col1:
        st.markdown(f"<h4 style='text-align: center; font-size:15px;'>{names[0]}</h4>", unsafe_allow_html=True)
        st.image(posters[0])
    with col2:
        st.markdown(f"<h4 style='text-align: center; font-size:15px;'>{names[1]}</h4>", unsafe_allow_html=True)
        st.image(posters[1])
    with col3:
        st.markdown(f"<h4 style='text-align: center; font-size:15px;'>{names[2]}</h4>", unsafe_allow_html=True)
        st.image(posters[2])
    with col4:
        st.markdown(f"<h4 style='text-align: center; font-size:15px;'>{names[3]}</h4>", unsafe_allow_html=True)
        st.image(posters[3])
    with col5:
        st.markdown(f"<h4 style='text-align: center; font-size:15px;'>{names[4]}</h4>", unsafe_allow_html=True)
        st.image(posters[4])
