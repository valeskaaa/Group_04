"""
Movie and Actor Insights Streamlit App

This module provides a Streamlit application for analyzing movie and actor data.
It includes visualizations for movie types, actor counts, and actor height distributions.
"""

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from movie_dataset import MovieDataset

# Initialize the MovieDataset instance
test_instance = MovieDataset()

# Set Streamlit page configuration
st.set_page_config(page_title="Movie & Actor Insights", page_icon="🎬", layout="wide")

st.title("Movie Dataset Analysis")

def plot_movie_type_histogram():
    """
    Plots a histogram of the top N movie types.

    Allows the user to select the number of top movie types to display.
    """
    st.header("Movie Type Histogram")
    N = st.number_input("Select N (Top N Movie Types):", min_value=1, max_value=50, value=10, step=1)
    movie_type_df = test_instance.movie_type(N)
    fig, ax = plt.subplots()
    ax.bar(movie_type_df["Movie_Type"], movie_type_df["Count"], color="skyblue", edgecolor="black")
    ax.set_xlabel("Movie Type")
    ax.set_ylabel("Count")
    ax.set_title("Top Movie Types")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

def plot_actor_count_histogram():
    """
    Plots a histogram of the number of actors per movie.

    Displays the distribution of movies based on the number of actors.
    """
    st.header("Actor Count Histogram")
    actor_count_df = test_instance.actor_count()
    fig, ax = plt.subplots()
    ax.bar(actor_count_df["Number_of_Actors"], actor_count_df["Movie_Count"], color="lightcoral", edgecolor="black")
    ax.set_xlabel("Number of Actors")
    ax.set_ylabel("Movie Count")
    ax.set_title("Movies by Number of Actors")
    st.pyplot(fig)

def plot_actor_height_distribution():
    """
    Plots the height distribution of actors based on selected gender and height range.

    Allows the user to filter by gender and specify minimum and maximum heights.
    """
    st.header("Actor Height Distribution")
    gender = st.selectbox("Select Gender:", ["All"] + list(test_instance.character_metadata["actor_gender"].dropna().unique()))
    col1, col2 = st.columns(2)
    with col1:
        min_height = st.number_input("Minimum Height (m):", min_value=1.0, max_value=2.5, value=1.5, step=0.01)
    with col2:
        max_height = st.number_input("Maximum Height (m):", min_value=1.0, max_value=2.5, value=2.0, step=0.01)

    actor_dist_df = test_instance.actor_distributions(gender, max_height, min_height, plot=False)
    fig, ax = plt.subplots()
    sns.kdeplot(actor_dist_df["actor_height"], ax=ax, color="blue", fill=True)
    ax.set_ylabel("Density")
    ax.set_xlabel("Actor Height (m)")
    ax.set_title("Actor Height Distribution")
    st.pyplot(fig)

# Plot the visualizations
plot_movie_type_histogram()
plot_actor_count_histogram()
plot_actor_height_distribution()