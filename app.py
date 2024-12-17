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

# Fetch movie recommendations from TMDB based on movie ID
def fetch_recommendations(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/recommendations?api_key={api_key}'
    response = requests.get(url)
    data = response.json()

    if 'results' not in data:
        st.error("No recommendations found.")
        return []

    return data['results']

# Fetch the poster URL for the movie
def fetch_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Streamlit UI
st.title("FindMovie: A Movie Recommendation System")
st.markdown("### Search and discover new movies")

# Customizing the search bar
search_query = st.text_input("Search for a movie:", placeholder="Search for a movie...", key="search_query", label_visibility="collapsed")

# Perform search if the user enters a query
if search_query:
    movies = search_movie(search_query)

    if movies:
        st.write(f"Results for '{search_query}':")
        
        # Grid Layout for displaying movies
        cols = st.columns(5)  # Display 5 posters per row
        
        for i, movie in enumerate(movies):
            with cols[i % 5]:  # Cycle through columns for each movie
                poster_url = fetch_poster_url(movie['poster_path'])
                if poster_url:
                    # Displaying movie posters with hover effect
                    st.markdown(
                        f'''
                        <a href="https://www.themoviedb.org/movie/{movie["id"]}" target="_blank">
                            <div style="position:relative;">
                                <img src="{poster_url}" width="150" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); transition: transform 0.3s ease;">
                                <div style="position:absolute; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.6); border-radius: 8px; display:none; justify-content:center; align-items:center;">
                                    <div style="color: white; font-size: 16px; text-align:center; font-weight:bold; padding:10px;">{movie["title"]}</div>
                                </div>
                            </div>
                        </a>
                        ''', unsafe_allow_html=True)
                else:
                    st.write("Poster not available")
