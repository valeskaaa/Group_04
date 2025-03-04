# Welcome to project RAG-TAG - part 2
---
## Rules
1. Be sure that the group submits [the link to the repo on moodle](https://moodle.novasbe.pt/mod/assign/view.php?id=350921).
2. We will consider wotk done until 23:59:59, Sunday 16 March 2025. Remember: timestamps are recorded!

---

## Scenario

Your group is participating in a two-day Hackathon where the goal is to analyse Movie information. The aim is to gain experience with a fun dataset so your product can later be used to analyse legal, technical, or any other kind of complicated documents. You decide to create a **python class** to help with the challenge.

## Goal

For this project, we will be using data from [CMU movie corpus](https://www.cmu.edu/). The datasets can be found [here](http://www.cs.cmu.edu/~ark/personas/). We will use just the main [Dataset](http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz).

Go over the datasets with your group. Check the info on the website before you start.

<div class="alert alert-danger">
    <b> THE MOST IMPORTANT TOOLS FOR A DATA SCIENTIST ARE PATIENCE AND COMMUNICATION</b>
    <br>
    <b> Discuss the contents of the dataset with your colleagues. Understanding the data is a priority. </b>
</div>

Use whatever python tools you find apropriate.

## Structure of the project

You are going to build a **[Streamlit app](https://streamlit.io/)** that will showcase your analysis.  
Keep all the .py and .ipynb out of the main directory. The only files in the main directory of the project should be the **files necessary to launch the app** and the several configuration files (.yml, .gitignore, and others). Everything else should have their own directories, like downloaded content.


---
<div class="alert alert-danger">
    <b> NEVER USE USER PROMPTS, IT IS INFINITELY ANNOYING!! </b>
    <br>
    <b> Always use arguments for your methods.</b>
</div>


---
## Scenario (continuation)

Day one has come and gone.

It is now time to do the final tasks and all of the polishing. As you know, your project might be picked up for an analysis presentation, you add an introduction about your group on the _README.md_ file. Be sure to add your **names**, **your student numbers** and **your e-mails**.

Day two is beginning.

### Day 2, Phase 1: Chronological info about the movies

Let's continue to expand the class.

- [ ] Define a new method called **releases** that receives a _genre_ argument with a default of **None**. If **None** is selected, the class should create a pandas dataframe with how many movies per year were released in total. Using _genre_ should filter only for the movies of that type.
- [ ] Make a second page for the streamlit app you are developping. It is going to be used for chronological info. Plot the output of the previous computed dataframe there i na **bar plot**. There should be an input in the streamlit app for the genre. It is OK to limit the genres into just 5-10 different ones, for time's sake.
- [ ] Define a new class mehtod called **ages**. It should receive a single argument of either 'Y', 'M', with 'Y' as default'. If 'Y', for year, is selected, you should compute in a dataframe how many births happend per year. If 'M', for Month, is selected, you should do same for Month of the Year. Please notice it is not Year-Month, but just Month. Someone born in **January 1920** should count towards the same bin as **January 2000**. If the user selects something else, default to Year.
- [ ] In the second page of your app, plot this info below the previous plot. Make a drop down to select the corresponding options.

### Day 2, Phase 2: Classification

- [ ] Make a third page for your app. In this page you are going to use a local LLM like we've seen in class to classify text. Choose a small model from [ollama](www.ollama.com) and add Documentation to your README on this prerequisite.
- [ ]$\times 3$ (_3 points_) In the third page of the app, include a button labeled **"Shuffle"** and three text boxes. In one box, you should print a random movie title and its summary. In the second box, print the genres for that movie contained in the database. Just the genres, not the dictionary itself. In the third box, you are going to print the genre classification your local LLM decided is has. Try to make your LLM to print only the genres. You will definetely need to configure your prompt to produce good results. Welcome to the world of [prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering)! If you are struggling with this part, please contact me.
- [ ] When the latter process runs, ask the LLM again if the genres it identified are contained in the list from the database. Congratulations, you most likely are now doing your **first AI pipeline**.Think and deploy of a way to identify a positive or negative answer.

Remember, when the button is pressed, you should select another random movie.  
It is OK if the Shuffle button does not work or is blocked during the thought process of the LLM.  
**You are not optimising for speed** (yet): it is OK if this process takes some time.  

### Day 2, Phase 3: Cleaning up

- [ ] Add a 'requirements.txt' file to your git repo with all the packages you used. This file will be used to generate an environment where your code will be ran. Remember to make it OS independent. Add instructions to README.md on how to install the packages. Write a small essay at the the end of your README.md on how you think the text classification of this project could help with the [UN's SDGs](https://sdgs.un.org/goals).

---
## Grading

Between the two parts, there are 20 gradable items in both Part 1 and 2. Every [] is 1 point out of 20.

<div class="alert alert-danger">
    <b> REMEMBER: IT IS OK TO PROTOTYPE CODE IN NOTEBOOKS OR OTHER FILES </b>
    <br>
    <b> The final delivery of the project is the app. </b>
    <br>
    <b> We will only consider contents in your "master" repository before the end of the deadline.</b>
</div>
