import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from movie_dataset import MovieDataset

# Create an instance of MovieDataset
test_instance = MovieDataset()

# Set page configuration
st.set_page_config(page_title="Chronological Trends", page_icon="📊", layout="wide")

# Streamlit page title
st.title("Chronological Trends")

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

# Dropdown to select Year or Month for births
st.header("Actor Births Over Time")
birth_mode = st.selectbox("Select Aggregation Mode:", ["Year", "Month"])
births_df = test_instance.ages("Y" if birth_mode == "Year" else "M")

# Plot the births
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(births_df.index, births_df["Birth_Count"], color="green", edgecolor="black")
ax.set_xlabel(birth_mode)
ax.set_ylabel("Number of Births")
ax.set_title(f"Actor Births Per {birth_mode}")
st.pyplot(fig)