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

# Fetch the poster URL for the movie
def fetch_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Streamlit UI
st.title("FindMovie: A Movie Recommendation System")

# Apply custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #141414;
            color: white;
        }
        .movie-card {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 10px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .movie-card:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5);
        }
        .movie-img {
            border-radius: 15px;
            transition: transform 0.3s ease;
        }
        .movie-img:hover {
            transform: scale(1.1);
        }
        .search-bar {
            width: 100%;
            max-width: 600px;
            margin-bottom: 20px;
        }
        .stTextInput>div>div>input {
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Search bar for movies
search_query = st.text_input("Search for a movie:")

# Perform search if the user enters a query
if search_query:
    movies = search_movie(search_query)

    if movies:
        st.write(f"Results for '{search_query}':")
        
        # Display movies in a grid layout
        cols = st.columns(5)  # Display 5 posters per row
        
        for i, movie in enumerate(movies):
            with cols[i % 5]:  # Cycle through columns for each movie
                poster_url = fetch_poster_url(movie['poster_path'])
                if poster_url:
                    # Movie poster without a title box beneath
                    st.markdown(f'''
                        <div class="movie-card">
                            <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                                <img src="{poster_url}" class="movie-img" width="150"/>
                            </a>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.write("Poster not available")
