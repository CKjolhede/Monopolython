# MONOPOLYTHON

## Overview

- Monopolython is a command line interface application that is a smaller version of the commonly known Monopoly™ board game. This application is a meant to be a demonstration of how object relational mapping should be done using Sqlite3 and Python.

---

## Introduction

Monopoloython utilizes the command line interface(cli) as the access point for user interaction.  Unlike a graphical user interface (GUI), the CLI relies on text inputs and typically uses minimal graphics and sound as part of the user interation. As is typical of CLI applications, the use of the mouse is virtually absent.

This program relies upon a python interpreter and pip files to manage the virtual environment. Monopolython takes advantage of a handful of python libraries and modules to facilitate its functions. 

Monopolython relies heavily upon Sqlite3 for its database interfacing and management. Monopolython takes advantage of the tools provided through the installed packages Rich and Pick to augment the graphical organization, presentation, and enhanced interactive features not found in native python libraries.  I have imported the python libraries:   time, os, random, ipdb, and sqlite3 as each offers tools that enable a more comfortable user experience. Primarily the libraries I've imported help manage the navigation of application menus in a way that makes them easier to read and assist in the speed in which information is presented to the user.



Take a look at the directory structure:

```console
.
├── Pipfile
├── Pipfile.lock
├── README.md
└── lib
    ├── models
    │   ├── __init__.py
    │   └── game.py
    │   └── game_space.py
    │   └── player.py
    │   └── space.py
    ├── cli.py
    ├── debug.py
    └── setup_helper.py
    └── monopolython.db
```


---

## Generating Your Environment

upon installation of the program, users must first setup the virtual environment by running
following commands:
```console
pipenv install
pipenv shell
```
### *** a migrate.py file exists to reinitiate the database and its tables if necessary ***
---

## Database Organization and Relationships

![Schema] (./lib/assets/Monopolython(3).png)
4 tables reside within the database to organize and store game data for both during game_setup
and synchronous data storage and retrieval during game play.

![alt text](<lib/assets/Monopolython (3).png>) 

This diagram dipicts the One to Many relationships between the Games table and both the Players and Game_spaces tables.   

The Spaces table is a unique table that is static. It is the root source of game information that exists for every game encounter.

The CLI menus are designed to offer users a small number of options to navigate their way through the game experience.  Starting with the game setup, the diagram below offers a roadmap of the flow of the program throughout the beginning of the game.

![alt text](lib/assets/gameboard2.jpg)



