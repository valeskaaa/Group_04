import streamlit as st
import random
from movie_dataset import MovieDataset
from ollama import chat, ChatResponse

# Create an instance of MovieDataset
test_instance = MovieDataset()

# Set page configuration
st.set_page_config(page_title="Random Movie Information", page_icon="🎬", layout="wide")

# Streamlit page title
st.title("Random Movie Information")

# Filter movies with existing summaries and genres
valid_movies = test_instance.movie_metadata[
    (test_instance.movie_metadata["wiki_movie_id"].isin(test_instance.plot_summaries["wiki_movie_id"])) &
    (test_instance.movie_metadata["genres"].notna())
]

# Shuffle button
if st.button("Shuffle"):
    # Ensure there are valid movies to choose from
    if valid_movies.empty:
        st.error("No movies with summaries and genres available.")
    else:
        # Select a random movie from the filtered list
        random_index = random.randint(0, len(valid_movies) - 1)
        movie = valid_movies.iloc[random_index]
        movie_id = movie["wiki_movie_id"]
        
        # Get the movie title and summary
        movie_title = movie["movie_name"]
        plot_summary_row = test_instance.plot_summaries[test_instance.plot_summaries["wiki_movie_id"] == movie_id]
        
        if not plot_summary_row.empty:
            movie_summary = plot_summary_row["plot_summary"].values[0]
        else:
            movie_summary = "Summary not available."
        
        # Get the movie genres
        movie_genres = eval(movie["genres"]).values()
        
        # Display the information in text boxes
        st.markdown(f"### {movie_title}\n\n{movie_summary}")
        st.text_area("Genres", ", ".join(movie_genres))
        
        # Use local LLM to classify the genre
        response: ChatResponse = chat(model='mistral', messages=[
            {
                'role': 'user',
                'content': f'Classify the following movie summary into genres: {movie_summary}. Only list the genres.',
            },
        ])
        
        # Extract and display the genre classification
        llm_genres = response.message.content.strip()
        st.text_area("Genre by LLM", llm_genres)