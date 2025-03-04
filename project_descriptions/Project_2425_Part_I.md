# Welcome to project RAG-TAG
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

### Day 1, Phase 1

- One of you will create a github repository (it does not matter who). __THE NAME OF THE REPOSITORY MUST BE "Group_XX" where XX is the number of your group! If you are group 3, then XX must be 03. Always use two digits and an underscore!__
- Initialize the repo with a README.md file, a proper license, and a .gitignore for the programming language you will use. The README.md file __MUST__ have your emails in a way that it is possible to copy and paste it into an email.
- The one who created the repository will then give __Maintainer__ permissions to the rest of the group. Check under "Project Information" > "Members".
- [ ] Every element of the group clones the repository to their own laptops.

### Day 1, Phase 2

- [ ] The class you decide the create for the project has finally been named after a brief internal fight and is __PEP8 compliant, like the entire project__.

The class will have several methods, which you will __not__ develop in the master branch.  
Document everything!  
Make your calls compliant with __pydantic__ and __static type checking__ when appliable.

- [ ] During the _init_ method, your class must download the data file into a __downloads/__ directory in the root directory of the project (main project directory). If the data file already exists, the method will not download it again.
- [ ] The _init_ method must also unzip the files.
- [ ] The _init_ method must also read the datasets into corresponding pandas dataframes which become attributes for your class.

## Day 1, Phase 3

- [ ] Develop a first method for your class called __movie_type__ that accepts a single int parameter "N" with a default value of 10. If N is not an integer, raise an Exception. It should calculate a pandas dataframe with columns "Movie_Type" of the "N" most common types of movies and how many times they show up in the database. 
- [ ] Develop a second method called __actor_count__. This method calculates a pandas dataframe with a histogram of "number of actors" vs "movie counts".
- [ ] Develop a third method called __actor_distributions__ that receives as arguments a string called "gender", two floats: "max_height" and "min_height", and a bool called "plot", with default False. If "gender" is not a string of if the hieghts are not numerical values, an exception must be raised. If the variable "plot" is True, this method should do a plot in matplotlib of the height distributions. The "gender" variable should accept "All" or the distinct non-missing values in the dataset. Do you think the heights should have a special check?
- [ ] Make a test with pytest (I want to just run _pytest_ in the main directory and perform the tests) where you test if the error handling the first and third methods are working properly.

### Day 1, Phase 4

- [ ] Make a Streamlit App where you import your __Class__ and plot the contents of each method in a plot.
        * It should plot an histogram of the __movie_type__ method and the app must have a field where to select the value of N.
        * It should plot a second histogram with the result of method __actor_count__.
        * It should plot the distribution or distributions of the third method. Add a dropdown to select "gender" and two input fields for the heights in the app. 

**If you feel lost about what story to tell, don't hesitate to contact me.**

<div class="alert alert-info">
    <b> REMEMBER: The first delivery is until March 2 23:59:59 and it is not graded. It is used as course correction. The delivery is the git repo link on moodle. </b>
</div>


<div class="alert alert-info">
    <b> REMEMBER: IT IS OK TO PROTOTYPE CODE IN NOTEBOOKS, BUT THE CLASS MUST BE IN A SINGLE .py FILE! </b>
    <br>
    <b> Prototyping notebooks must have their own separate directory.</b>
    <br>
    <b> We will only consider contents in your "master" repository.</b>
</div>

<div class="alert alert-warning">
    <b>When in doubt, ask.</b>
</div>
