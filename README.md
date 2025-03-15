# Group\_04

## Advanced Programming for Data Science - Project RAG-TAG: Movie & Actor Analysis

### Group Members:

- **Jakob Lindner (53722):** [57322@novasbe.pt](mailto:57322@novasbe.pt)
- **Ben Bumann (64810):** [64810@novasbe.pt](mailto:64810@novasbe.pt)
- **Marvin Schumann (63529):** [63529@novasbe.pt](mailto:63529@novasbe.pt)
- **Valeska Pachelbel (64062):** [64062@novasbe.pt](mailto:64062@novasbe.pt)

## About the Project

This project, **RAG-TAG**, was developed as part of the **Advanced Programming for Data Science** course.

The goal is to **analyze movie data** from the **CMU Movie Corpus** using **Python, Streamlit, and AI-based text classification**.

## Key Features

- **Movie Genre Analysis** (Top N movie types)
- **Actor Statistics** (Number of actors per movie & distributions)
- **Chronological Insights** (Movie release trends & birth statistics)
- **LLM-based Text Classification** (Automated genre prediction using **Mistral**)

## Project Structure

- `downloads/` → Stores the downloaded dataset files
- `prototyping/` → Prototyping notebooks
- `movie_dataset.py` → Contains the Python class and related scripts
- `app.py` → Our Streamlit app
- `requirements.txt` → Lists all dependencies for the project

## Dataset

We use the [CMU Movie Corpus](http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz), which includes metadata about movies, actors, and genres.

## Prerequisites

To run the project, ensure you have the following dependencies installed.

### Recommended Installation

Create and activate a virtual environment, then install all dependencies from `requirements.txt`:

```sh
python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Running the App

To start the **Streamlit app**, run the following command in your terminal:

```sh
streamlit run app.py
```

This will launch the app and open it in your default web browser.

## Third Page - Genre Classification

The third page of the app introduces **automated genre classification** using a local **LLM model**.

### Model Used

The app utilizes the **Mistral model** from **Ollama** for **genre classification**. This model processes movie summaries and predicts their genres.

### Setting Up the Model

To ensure the model is available in your environment, you need to first install **Ollama** ([Download Ollama](https://ollama.com/download)) and then pull Mistral using the following command:

```sh
ollama pull mistral
```

### How It Works

- The user selects a movie, and its **title, summary, and genres** are displayed.
- The **Mistral model** classifies the movie's summary into predicted genres.
- The app **compares** the LLM-detected genres with the database genres.
- A **success/warning message** is shown based on the model’s accuracy.
- A **score visualization** displays the genre detection success rate.

This feature enhances **automated movie categorization** and enables **genre verification** using AI.

## Running Tests

To test the project's error handling and functionality, run:

```sh
pytest
```