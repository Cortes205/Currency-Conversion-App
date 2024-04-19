# Currency Conversion App
Interactive command line interface application used to convert currencies with live exchange rates

All currency information is extracted from [here](https://markets.businessinsider.com/currencies) in the section labeled "All Currencies"

## Setup

### Project Folder
Open your computer's terminal and cd to a directory of your choice.

Ensure git is installed on your system, then clone this repository using:

```sh
git clone https://github.com/Cortes205/Currency-Conversion-App.git
```

or you can download it manually as a zipfile.

### Requirements
Ensure python is installed on your system, then download the necessary libraries:

```sh
pip install -r requirements.txt
```

(or)

```sh
pip3 install -r requirements.txt
```

## Usage

### Execute
Open the terminal in the program's directory and ensure you have an internet connection.

To run this program, use the command:

```sh
python main.py
```

(or)

```sh
python3 main.py
```

### Runtime
The four special commands for this program are:

```sh
-q quit
-h help
-r refresh exchange rates
-c display list of currency codes
```
Other than that, this program takes currency codes and dollar amounts as input
and provides a dollar amount in a different currency as output.

### Testing
To test the searching method that I have used, it can be run from the main directory using:

```sh
python tests/test_search.py
```

(or)

```sh
python3 tests/test_search.py
```

As of April 19th, 2024, I have implemented a binary search to find inputted currencies.
I did this as a way of studying for my programming exam and to extend my knowledge.
This algorithm required consideration of many cases and worked with letters as opposed to
integers (the way it was taught in my first year). Nonetheless, this was good practice to better understand binary 
searches for my exam and for the future. 


## About This Project
This project has taught me more about python since it is not a language I use every day.
I as well have learned the basics of webscraping, especially on a complicated website. However,
I am happy with the results as this was my first attempt at such a project.
I hope to one day turn this into a GUI program!

[Linkedin](https://www.linkedin.com/in/cortes205/)
