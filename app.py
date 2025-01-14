import streamlit as st
import requests

# TMDB API key (replace with your key)
api_key = 'e9049fef70036ad6e036411e17e24ac4'

# Search for a movie by title
def search_movie(query):
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}'
    response = requests.get(url)
    data = response.json()

    if 'results' not in data:
        st.error("No results found.")
        return []
    
    return data['results']

# Search for an actor by name
def search_actor(query):
    url = f'https://api.themoviedb.org/3/search/person?api_key={api_key}&query={query}'
    response = requests.get(url)
    data = response.json()

    if 'results' not in data:
        st.error("No actor found.")
        return []

    return data['results']

# Fetch the poster URL for the movie
def fetch_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Fetch trending movies
def fetch_trending_movies():
    url = f'https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    
    if 'results' not in data:
        st.error("Unable to fetch trending movies.")
        return []
    
    return data['results']

# Fetch recommended movies (we use popular for now)
def fetch_recommended_movies():
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'results' not in data:
        st.error("Unable to fetch recommended movies.")
        return []
    
    return data['results']

# Fetch movies for a specific actor
def fetch_movies_by_actor(actor_id):
    url = f'https://api.themoviedb.org/3/person/{actor_id}/movie_credits?api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'cast' not in data:
        st.error("Unable to fetch movies for this actor.")
        return []
    
    return data['cast']

# Apply dark mode styles
def apply_styles():
    st.markdown("""
        <style>
            body {
                background-color: #121212;
                color: white;
            }

            .cool-title {
                font-size: 48px;
                font-weight: bold;
                background: linear-gradient(to left, #ff6347, #6a5acd, #32cd32);
                -webkit-background-clip: text;
                color: transparent;
                text-align: center;
                animation: fadeIn 2s ease-out;
                text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.7);
            }

            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }

            .stTextInput>div>div>input {
                background-color: #333333;
                color: white;
                border: 1px solid #555555;
                border-radius: 5px;
                padding: 12px;
                width: 100%;
                max-width: 600px;
            }

            .stButton>button {
                background-color: #444444;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
            }

            .stButton>button:hover {
                background-color: #555555;
            }

            .movie-card {
                display: flex;
                flex-direction: column;
                align-items: center;
                margin: 10px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }

            .movie-card:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.7);
            }

            .movie-img {
                border-radius: 15px;
                transition: transform 0.3s ease;
            }

            .movie-img:hover {
                transform: scale(1.1);
            }

            /* Responsive Columns */
            @media only screen and (max-width: 600px) {
                .stColumn { flex: 1 1 50%; }
                .movie-img { width: 100%; }
            }

            @media only screen and (min-width: 601px) and (max-width: 1024px) {
                .stColumn { flex: 1 1 33%; }
                .movie-img { width: 100%; }
            }

            @media only screen and (min-width: 1025px) {
                .stColumn { flex: 1 1 18%; }
                .movie-img { width: 150px; }
            }
        </style>
    """, unsafe_allow_html=True)

# Streamlit UI
apply_styles()  # Apply dark mode styles

# Cool system title
st.markdown('<h1 class="cool-title">FindMovie: A Movie Recommendation System</h1>', unsafe_allow_html=True)

# Search bar for movies
search_query = st.text_input("Search for a movie:", placeholder="Enter movie name...", key="search_query")

# Add a search button
search_button = st.button("Search")

# Perform search if the user enters a query or clicks the button
if search_query or search_button:
    movies = search_movie(search_query)

    if movies:
        st.write(f"Results for '{search_query}':")
        
        # Display movies in a grid layout with responsive columns
        cols = st.columns(5)  # Display 5 posters per row on large screens
        for i, movie in enumerate(movies):
            with cols[i % 5]:  # Cycle through columns for each movie
                poster_url = fetch_poster_url(movie['poster_path'])
                if poster_url:
                    # Movie poster without a title box beneath
                    st.markdown(f'''
                        <div class="movie-card">
                            <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                                <img src="{poster_url}" class="movie-img" />
                            </a>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.write("Poster not available")

# Actor Search Section
actor_query = st.text_input("Search for an actor:", placeholder="Enter actor name...", key="actor_query")
actor_search_button = st.button("Search Actor")

if actor_query or actor_search_button:
    actors = search_actor(actor_query)

    if actors:
        actor_names = [actor['name'] for actor in actors]
        selected_actor = st.selectbox("Select an actor:", actor_names)
        actor_id = next((actor['id'] for actor in actors if actor['name'] == selected_actor), None)

        if actor_id:
            actor_movies = fetch_movies_by_actor(actor_id)
            if actor_movies:
                st.write(f"Movies with {selected_actor}:")
                cols = st.columns(5)
                for i, movie in enumerate(actor_movies):
                    with cols[i % 5]:
                        poster_url = fetch_poster_url(movie['poster_path'])
                        if poster_url:
                            st.markdown(f'''
                                <div class="movie-card">
                                    <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                                        <img src="{poster_url}" class="movie-img" />
                                    </a>
                                </div>
                            ''', unsafe_allow_html=True)

# Trending Now Section
st.markdown("## Trending Now")
trending_movies = fetch_trending_movies()
if trending_movies:
    cols = st.columns(5)
    for i, movie in enumerate(trending_movies):
        with cols[i % 5]:
            poster_url = fetch_poster_url(movie['poster_path'])
            if poster_url:
                st.markdown(f'''
                    <div class="movie-card">
                        <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                            <img src="{poster_url}" class="movie-img" />
                        </a>
                    </div>
                ''', unsafe_allow_html=True)

# Recommended for You Section
st.markdown("## Recommended for You")
recommended_movies = fetch_recommended_movies()
if recommended_movies:
    cols = st.columns(5)
    for i, movie in enumerate(recommended_movies):
        with cols[i % 5]:
            poster_url = fetch_poster_url(movie['poster_path'])
            if poster_url:
                st.markdown(f'''
                    <div class="movie-card">
                        <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                            <img src="{poster_url}" class="movie-img" />
                        </a>
                    </div>
                ''', unsafe_allow_html=True)
