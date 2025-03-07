# Group_04
Advanced Programming for Data Science - Project

Group members: 
- Jakob Lindner (53722): 57322@novasbe.pt
- Ben Bumann (64810): 64810@novasbe.pt
- Marvin Schumann (63529): 63529@novasbe.pt
- Valeska Pachelbel (64062): 64062@novasbe.pt

## Prerequisites

To run the project, ensure you have the following dependencies installed.

### Recommended Installation:
Create and activate a virtual environment, then install all dependencies from `requirements.txt`:

```sh
python -m venv env
source env/bin/activate  # On macOS/Linux
env\Scripts\activate  # On Windows
pip install -r requirements.txt
```

## Running the App

To start the Streamlit app, run the following command in your terminal:

```sh
streamlit run Movie_and_Actor_Insights.py
```

This will launch the app and open it in your default web browser.



## Third Page - Genre Classification

The third page of the app introduces **automated genre classification** using a local **LLM model**.

### Model Used:
The app utilizes the **Mistral model** from **Ollama** for **genre classification**. This model processes movie summaries and predicts their genres.

### Setting Up the Model:
To ensure the model is available in your environment, you need to first install Ollama (https://ollama.com/download) 
and then pull mistral using the following command:

```sh
ollama pull mistral
```

### How It Works:
- The user selects a movie, and its **title, summary, and genres** are displayed.
- The **Mistral model** classifies the movie's summary into predicted genres.
- The app **compares** the LLM-detected genres with the database genres.
- A **success/warning message** is shown based on the model’s accuracy.
- A **score visualization** displays the genre detection success rate.

This feature enhances **automated movie categorization** and enables **genre verification** using AI. 
