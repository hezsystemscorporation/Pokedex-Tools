
# Pokedex-Tools  
This is the group project of my leadership, written using Python. It provides useful information and insights of Pokémon. 

## Producers  
**Xin HE**, leader of the group, responsible for product design, UI design, data analysis and functions implementation  
**Manlin ZHAO**, responsible for UI Design and Damage Calculator Function  
**Zhibo FENG**, resibonsible for the first version's implementation  
Houze HE, Zisen Feng, Lianghao GONG  

## Project Overview  
### Introduction
As there are lots of players over the world playing Pokémon and more and more new ones joining the large community, it is useful to design tools for them to get the knowledge and insights about the game and the characters. In reply to the needs, we implemented these tools.   
As there are some image of characters missing in our image crawling procedure, you are welcome to upload image to the folder `pokemon_image\<pokemon_name>`. Also as time limits, you are also welcome to make other contributions or give comments about our project.    

### UI Design
For this project, we use `pyside6` to implement our UI designs. We use basic python library to implement basic UIs with functions and then beautify them with `pyside6`. Also **Adobe^®^ XD** is used when designing the UIs.   

### Functions
* **Pokémon Tools Main Page**: 
This page contains the theme of our software and the entries to our functions.   
* **Basic Data reports**: 
This function provides us with the graphic overview of the basic data of Pokémon, a combo box is set to allow users to switch among multiple graphs.   
* **Pokédex**: 
This function provides the players with a way to view the basic data of the Pokémon, Including the data/images and the radar graphs. This allows users to search the Pokémon via their types/abilities and their names.   
* **Damage Calculator**: 
This function allows the user to calculate the damage the Pokémon can cause via the storage information of the damage times of the different types of Pokémon.   

## Key Findings of Our Project
As the generation of Pokémon evolved, or being designed by the game designer, we are trying to find whether the atk or the hp values are increased.   

We tried to build a MLP model to predict the data in the future, but according to the value evaluating the 3 kinds of data selected by the correlation matrix calculated. That mean there are no such relationship among them. But by drawing the correlation matrix, we found the most probably relationship between the data. That is not in the data we selected to generate groups.   

And In the graph we drawn in our experiment, we find no connection or accuracy exists by the 3 data we initially selected, which is probably the data affecting the atk(maybe a little messy). So maybe we will try to find what the relationship of these data in the games like “Genshin Impact” and “Honkai: Star rail” which is charged for play fun or letting the player play harder to play fun.   

Also, with the scatter plots drawn, we can find that there no much Pokémon that is average in the values, that shows that some of the Pokémon is for defense-to defend more attack from the enemies, and some of the Pokémon is for attack-with lower hp value or defense. The Pokémon is generally divided equally in the graph showing the balance in the game. The scatter plots are shown following:   

And in the following distribution chart, we can find that most Pokémon types are equal with normal type and the water type take the most percentage.   

According to the accompanying charts, I observed that-much like in most games-Pokémon are designed with either defensive or offensive archetypes. In this analysis, a substantial number of Pokémon exhibit high defense or hp values, while some display elevated attack or critical‐hit‐related statistics.   

## Requirements
### Environment Requirements   
* Python 3.6 or above

### Installing Dependencies  
Install all required packages:
```bash
pip install -r requirements.txt
```

### requirements.txt  
```text
# pandas for data reading/manipulation
pandas>=1.0.0

# PySide6 for Qt GUI (Widgets, SvgWidgets, Gui, Core, etc.)
PySide6>=6.0.0
```

## How to Run It  
After all the requirements are satisfied, use `python main.py` or simply click `main.py` to run the program.   

## Make a Contribution  
Thank you for considering contributing to this project! There are several ways you can help:

### What you can do?  
1. **Submit Issues or Suggestions**  
* If you find a bug, have a question, or want to propose a new feature, please open an issue on GitHub.  
* Use the issue template (if available) and provide as much detail as possible: steps to reproduce, expected behavior, screenshots, etc.

2. **Fork & Pull Requests**  
* Fork the repository to your own GitHub account.  
* Create a new branch with a descriptive name, e.g. `feature/add-calculator` or `fix/widget-rendering`.  
* Make your changes and ensure everything still works (see “Development Guidelines” below).  
* Commit your code with clear, concise messages (see “Commit Message Style” below).  
* Push your branch to your fork and open a Pull Request (PR) against the `main` branch of this repository.  
* In the PR description, explain what you changed and why. Include screenshots or code snippets if relevant.

3. **Review Process**  
* Once your PR is opened, the project leader or other reviewers will look it over as soon as possible.  
* You may be asked to make adjustments or clarify certain points. Please address review comments promptly.  
* When approved, a project leader (or designated collaborator) will merge your PR.

### Development Guidelines
* **Coding Style**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) conventions where practical, except for indentation:  
* **Use tabs** for indentation (no soft/hard limit on line length).  
* Name variables and functions using `snake_case`; classes with `PascalCase`.  
* Add type hints where appropriate.
*  **Commit Message Style**: First line: short summary (< 50 characters).  Leave a blank line, then write a more detailed description (if needed).  
* **Branch Naming**  
**Features**: `feature/<short-description>`  
**Bug Fixes**: `fix/<short-description>`  
**Documentation**: `docs/<short-description>`
* **Code Reviews**:  
Before submitting a PR, run all existing unit tests to ensure nothing is broken.  
If you add new functionality, include at least one unit test or an example demonstrating usage.   
Document any new public functions or classes in the docstrings (Google or NumPy style).   

## License   
This project is licensed under the [Apache License 2.0](LICENSE).   
See the [LICENSE](LICENSE) file for details on how you may use, distribute, and modify this software.   

## Contact
If you have any questions, feedback, or suggestions, feel free to reach out:
* **Project Leader**: Xin HE (Michael Hertz)
* **Email**: t330026052@mail.uic.edu.cn  or 2430586637@qq.com or hezsystemscorporation@outlook.com
