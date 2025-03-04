import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from movie_dataset import MovieDataset

# Create an instance of MovieDataset
test_instance = MovieDataset()

# Streamlit page title
st.title("Movie Release Chronology")

# Select a genre from a predefined set
genres = ["Drama", "Comedy", "Action", "Thriller", "Horror", "Romance Film", "Science Fiction", "Fantasy", "Mystery", "Documentary"]
selected_genre = st.selectbox("Select a Genre:", [None] + genres)

# Compute the release data
releases_df = test_instance.releases(selected_genre)

# Plot the results
st.header("Movies Released Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(releases_df.index, releases_df["Movie_Count"], color="royalblue", edgecolor="black")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Movies Released")
ax.set_title("Movie Releases Per Year")
st.pyplot(fig)