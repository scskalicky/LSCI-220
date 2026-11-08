# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.25.2",
#     "nltk==3.10.4",
#     "matplotlib==3.11.2",
#     "polars==2.1.0",
#     "requests==2.34.2",
# ]
# ///

import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Get your feet wet and start using some Python.

    Python has a reputation among some people for being "easy" because the code almost looks like you can just type what you want. An older [XKCD](https://xkcd.com/) comic tried to make this point (although it was when Python 2.x was being used!). You might not immediately get parts of this comic, but come back later in the course and you might!

    > <img src = "https://imgs.xkcd.com/comics/python.png" height = 500>

    Anyhow, let's put Python's reputation to the test and dive right into some basics and start using it.

    In this section, there are some code cells which you do not need to modify.

    1. Look at each cell and try to understand it without running the code cell. What do you think will happen when you run the code cell?
    2. Run the code cell (click the ▶ button at the top right of the cell, or click in the cell and press Shift + Enter) to check your prediction. Were you right?
    """)
    return


@app.cell
def _():
    print("Soda Onion")
    return


@app.cell
def _():
    name = "Soda Onion"
    print(name)
    return (name,)


@app.cell
def _(name):
    len(name)
    return


@app.cell
def _(name):
    for letter in name:
      print(letter)
    return


@app.cell
def _(name):
    [letter for letter in name]
    return


@app.cell
def _(name):
    [letter for letter in reversed(name)]
    return


@app.cell
def _():
    # approximate 2025 figures
    NZ_Pop = 5330000

    World_Pop = 8230000000

    NZ_perc = (NZ_Pop / World_Pop) * 100

    NZ_perc
    return


@app.cell
def _():
    anthem_te_reo = "E Ihowa Atua,\nO ngā iwi mātou rā,\nāta whakarongo na;\nMe aroha noa.\nKia hua ko te pai;\nKia tau tō atawhai;\nManaakitia mai\nAotearoa"
    anthem_english = "God of nations at thy feet,\nIn the bonds of love we meet.\nHear our voices, we entreat\nGod defend our free land.\nGuard Pacific's triple star\nFrom the shafts of strife and war,\nMake her praises heard afar,\nGod defend New Zealand."
    print(anthem_te_reo + "\n\n" + anthem_english)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Values and Variables

    The code cells above contained a range of Python *values* which were saved to different *variables*. Values are the basic pieces of information or data that Python works with.

    A value can be a number, a piece of text, or other things, such as containers. Here are some of the examples used in the code cells above

    Variable | Value | Type
    ------|------|------
    `name`|"Soda Onion"|text
    `NZ_Pop`|5330000|number

    The *type* of a value is actually more specific than the table above suggests. For example, numbers are classified into integers (whole numbers) or floats (decimals). And text is classified as a `string` (more on this later).

    You can check the `type` of a value in Python by using the `type()` function. See below, the `type` for each value will be shown in the output. Knowing the type of a value is useful when performing operations on text versus numbers.
    """)
    return


@app.cell
def _():
    # int = integer
    type(42)
    return


@app.cell
def _():
    # float = decimal
    type(4.2)
    return


@app.cell
def _():
    # str = text
    type('forty-two')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What’s the big deal with variables?
    - a value that isn't saved to a variable can't be used again later
    - variables will persist in memory (so you can use and reuse them)
    - variables can be updated based on other actions

    ### Assigning values to a variable
    To assign a value to a variable, we use the `=` sign and the following syntax:

    > `variable_name = value`

    ### Rules for variable names
    - Do not start with numbers
    - Do not use special characters (e.g., #, @), but underscores are fine (e.g., `nz_pop`)
    - Names are case-sensitive, so `name` and `Name` are different variables
    - Do not use Python keywords (e.g., `is`, `True`, `False`)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    1. Below, use the empty code cell and save some text to a variable. Give your variable a descriptive name.

    To add a cell, hover your mouse over the top or bottom edge of a cell and click the **+** button that appears.

    To save text to a variable, use this syntax:

    > `variable_name = "text"`

    Make sure that your string is surrounded by balanced quote marks, just like the example! (this means, if you use a double quote on the left side, you need a double quote on the right side)!

    2. Then, in another new code cell, use the `print()` function to print the value of your variable to the console. Use this syntax:

    > `print(variable)`

    > **Note:** in marimo, each variable name can only be created in one cell. If you see an error saying a variable is defined in multiple cells, choose a new name for it.
    """)
    return


@app.cell
def _():
    # use this code cell to create your variable and print it!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Strings

    As you saw above, we are using the word `string` to represent text. You might wonder, why not just call it `text` or `words`? The reason provides us with our first glimpse into the difference between how humans and computers "see" language. For humans, we see groups of letters and (depending on the language) spaces to form words. However, for Python, strings are defined as a **sequence of characters**.

    The word `string` represents the idea that text data is fundamentally a *sequence* - a string of characters with a start and an end. A string can be any arbitrary size long - from 0 to a million (or more!) characters long.

    There are other types of sequences in Python, so a string is a specific type of sequence, one which contains characters representing written language.

    This can be a bit tricky at first because we are also using letters and words to write the actual Python code. This is one reason why strings are surrounded by quote marks - in order to distinguish them from other values as well as from the actual Python code.

    ### Creating strings

    To create a string, we need to surround the text data in quote marks. These quotes are called `delimiters` and are how you determine the start and end of a string. Crucially, the delimiter on each end must match:

      - ' + ' (single quotes)
      - " + " (double quotes)
      - ''' + ''' (triple quotes)

    What happens when you don't have matching delimiters? Run the code cells below and compare the output.
    """)
    return


app._unparsable_cell(
    r"""
    print('I'm so happy to be here!')
    """,
    name="_"
)


@app.cell
def _():
    print("I'm so happy to be here")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **String Functions**

    Strings have their own things that they can do - *functions* - and are automatically built-in to any string you create or work with in Python. To use these built-in functions, we add a full stop (`.`) to the end of the string (without a space) and then type the name of the function we'd like to use. We also need to include a set of opened and closed brackets after the name of the function - don't worry about this for now!

    Here is an example:
    """)
    return


@app.cell
def _():
    # this is a string by itself:

    "Aotearoa New Zealand"
    return


@app.cell
def _():
    # now add a string function to the end:

    "Aotearoa New Zealand".lower()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the `.lower()` was attached to the end of the string, outside the final delimiter.

    Based on the name of the function and the resulting output, it should be clear that the `.lower()` string function will convert the entire string to lower-cased letters. Neat!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are some other string functions you can use:

    > * `string.upper()` = return an uppercase version of a string
    > * `string.lower()` = return a lowercase version of a string
    > * `string.title()` = return a title case version of a string
    > * `string.strip()` = strip all whitespace from a string
    > * `string.rstrip()` = strip all trailing whitespace from a string
    > * `string.lstrip()` = strip all leading whitespace from a string

    *You can find a more complete list of string methods/functions [here](https://www.geeksforgeeks.org/python-string-methods/)*

    Here are some more examples - take the opportunity to make your own examples and play around with the output.
    """)
    return


@app.cell
def _():
    # Print a lower case version of the string using .lower() 
    print('KIWI'.lower())
    return


@app.cell
def _():
    # Remove the whitespace from the front of a sentence using .lstrip()
    '    look at how the whitespace in front of these words goes away!'.lstrip()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also call the string functions on variable names that have an underlying value that is a string:
    """)
    return


@app.cell
def _():
    # create a variable and assign a string as its values

    VUW = "Te Herenga Waka"
    return (VUW,)


@app.cell
def _(VUW):
    # call the variable name to "see" the value:

    VUW
    return


@app.cell
def _(VUW):
    # use a string function on the variable name

    VUW.upper()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Counting the length of a string

    We can also use the Python function `len()` to count the length of a string. Since a string is a series of characters, `len()` will tell us how many characters are in a string.
    """)
    return


@app.cell
def _():
    # Count the length of a string using len()
    len('kiwi')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why does the following code cell give us 15?
    """)
    return


@app.cell
def _(VUW):
    # works on the variable name too
    len(VUW)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because even though the variable *name* is only three characters long, the underlying *value* is 15 characters long.

    - VUW = 3 characters
    - Te Herenga Waka = 15 characters (including spaces!)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `function()` vs. `.function()`

    Take special note of the differences between functions like `print()` and the string functions like `.upper()`. Both the `print()` and `len()` functions are Python functions that are not attached to a specific type. You can think of them as freely available to be used on all types of variables and values.

    The main difference here is that `len()` and `print()` require putting the variable or value inside the brackets, whereas the other functions require putting the variable or string first and typing the `.function()` afterwards.

    The first kind of function, such as `print()` and `len()` are functions not specific to any one type or class. The second kind, such as `.upper()` are specific to a type (strings), and thus that function can only be used on values of that type. You can think of the `.function()` style as a tail which belongs to a specific animal. Foxes can only use fox tails, and dogs can only use dog tails. Strings can only use string functions, and other types can only use their functions.

    Later on, this distinction becomes fuzzy when we start importing functions from different libraries, because we can use the `.function()` method to call functions from libraries, or import them directly. But the general principle still remains - functions which are specific to *something* (either a type, library, or module) can be called using the `.` notation. You can see this below, where I can import a library (called `math`) and then use the `.fsum()` function to calculate the sum of two numbers.

    In the second cell, I import *just* the function, which makes it available without needing to use the `.` notation. This may be confusing right now, so don't worry if it doesn't make immediate sense! But you'll notice how different strategies for importing influence the way that functions are available in a notebook or a program.
    """)
    return


@app.cell
def _():
    # Import the library and then call a specific function from that library
    import math
    math.fsum([1,2])
    return


@app.cell
def _():
    # Import just the function from the math library
    from math import fsum
    fsum([1,2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    - Create some new code cells below
    - In the code cells, create some strings and try:
      - using different delimiters
      - using different functions on the strings
      - saving the strings to a variable name and then using functions
    """)
    return


@app.cell
def _():
    # use this code cell to test things out!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Strings versus Words**

    Let's return to the idea that strings are not exactly the same as words, phrases, and sentences. Strings might look like sentences or phrases to us, and we can understand the differences between letters, punctuation, and whitespace. But computationally these all count equally as **characters**, and as such a string in Python will be as long as the number of characters.

    For example, note how the length of the following two strings is different, even though the phrase is identical. Can you see why?
    """)
    return


@app.cell
def _():
    # Version 1 - it is 17 characters long
    len('underneath it all')
    return


@app.cell
def _():
    # Version 2 - it is 18 characters long
    len('underneath it all ')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Punctuation also matters, compare these two examples, why is the first version longer than the second?
    """)
    return


@app.cell
def _():
    len("I can't even")
    return


@app.cell
def _():
    len("I cant even")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Discussion

    Consider the way strings are stored computationally.

    - What implications or challenges do you think this might pose for the computational representation of text?

    - Based on your understanding of strings thus far, are there any differences between the following computational representations of text?
      - words versus letters
      - sentences versus words
      - paragraphs versus sentences
      - texts versus paragraphs

    - What remaining questions do you have about variables, strings, and the functions used in this notebook?
    """)
    return


if __name__ == "__main__":
    app.run()
