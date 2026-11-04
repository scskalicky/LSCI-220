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
    #### Relevant NLTK Book sections

     [NLTK Book, Chapter 1, Section 2](https://www.nltk.org/book/ch01.html#list_index_term)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Python `lists`

    Lists are another value type in Python. Lists can be thought of as a container for values, and more specifically as a giant bucket which almost anything can be tossed into. This means a list can contain a number of different values,  *and* these values can be of different types, neat!

    The basic structure of a list is that a list is surrounded by square brackets `[]`, and values inside of a list are separated by commas.

    Run through the code cells to see lists with different combinations of values.
    """)
    return


@app.cell
def _():
    # a list of strings
    names = ['Jerry', 'George', 'Elaine', 'Kramer']

    # call the value of the variable
    names
    return


@app.cell
def _():
    # a list of numbers (integers)
    dates = [1982, 1986, 2008, 2012]
    dates
    return


@app.cell
def _():
    # a list containing strings and an integer
    mixed_values = ['Jerry', '5A', 5]
    mixed_values
    return


@app.cell
def _():
    # a list can even contain other lists,
    listception = [['Jerry', 'Elaine'], ['George', 'Kramer']]
    listception
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # List functions

    Just like strings, lists have their own built in functions (or methods). And, we can also use `len()` to count the length of a list.

    > - `len(list)` returns the length of the list (the number of values in a list)
    > - `list.sort()` sorts the list object
    > - `list.append()` adds a value to the end of a list

    *You can find a more complete list of list methods [here](https://www.geeksforgeeks.org/list-methods-in-python/)*
    """)
    return


@app.cell
def _():
    # define a list
    quote = ['colorless', 'green', 'ideas', 'sleep', 'furiously']

    print(quote)
    return (quote,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When we analyse the length of a list, we get a number of the total values in the list. Crucially, we do *not* get the length of the values themselves. So even though each string value in `quote` has a different length, there are a total of 5 words in quote, and hence `len()` will tell us that `quote` is 5 values in length:
    """)
    return


@app.cell
def _(quote):
    # how many values in the list?
    len(quote)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you wanted to know how long the combined string is within `quote`, you could do a variety of different things. Here is just one of many possibilities, using the string method `.join()`. We will learn more about this elsewhere - this here is just for a bit of extra info.
    """)
    return


@app.cell
def _(quote):
    print(' '.join(quote))
    len(' '.join(quote))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Back to list functions!
    """)
    return


@app.cell
def _(quote):
    # the list as it is now
    quote
    return


@app.cell
def _(quote):
    # make a copy of the list, then sort the copy alphabetically
    # (note that .sort() does more than return output - it directly changes the list)
    quote_sorted = quote.copy()
    quote_sorted.sort()
    quote_sorted
    return


@app.cell
def _(quote):
    # make another copy, then add something to the end of it
    quote_added = quote.copy()
    quote_added.append('Chomsky')
    quote_added
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    Create a list or two containing different values and of different types. Make sure to use the square brackets and to separate values in the list using commas.

    Then, play with `len()` and some other list functions in order to get a good sense of how to use them.
    """)
    return


@app.cell
def _():
    # make some lists here!


    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Indexing strings and lists

    Strings and Lists are both sequences of values and are stored in a particular order. This allows us to access specific values at specific locations in these sequences. To do so, we use **indexing** and **slicing**:

    - **indexing** gets a single value from a sequence, e.g. `x[0]`
    - **slicing** gets a range of values from a sequence, e.g. `x[1:4]`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Indexing string characters
    The syntax for doing so uses square brackets, the same as are used to declare lists, so be careful! The difference is that index brackets are placed immediately after the value (or variable name mapped to a value), like this:

    > `value[]`

    In addition to placing the square brackets, you also need to indicate the numerical index you wish to inspect.

    In the example below, I ask for portions of a string sequence located at index 1:
    """)
    return


@app.cell
def _():
    # index a string at location/index 1
    'Melodrama'[1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why did we get "e" instead of "M"? The reason is that in Python, the starting point of a sequence is 0, not 1. So, to get the *first* thing in a sequence, we have to ask for the 0th thing:
    """)
    return


@app.cell
def _():
    'Melodrama'[0]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In actuality, the indexes sit before/after each character in a string, so that instead of being located at any one index, characters are located *between* indexes:

    || | | | | | | | | | | | | | | | | | | |
    ---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
    character||M||e||l||o||d||r||a||m||a
    index     |0||1||2||3||4||5||6||7||8||9|

    When we index a string using a single number, we are technically asking for the value which comes after that index. Also see section 8.4 [here](https://greenteapress.com/thinkpython2/html/thinkpython2009.html#sec95)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Slicing a range of string characters

    To slice a range of values from within a sequence, we can include more information inside the square brackets. Specifically, we can specify a `start` and a `stop`, which are separated by a colon:

    > `value[start:stop]`

    Just as if we were asking for a single index, asking for range will return everything *after* the start index and *before* the stop index. This means you will not get the value which comes after the stop index! Compare the table above with the output below:
    """)
    return


@app.cell
def _():
    # use a start:stop
    'Melodrama'[1:6]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can leave the start or stop blank - doing so defaults to the start or end, depending on which value you leave blank:
    """)
    return


@app.cell
def _():
    # The first half of melodrama
    'Melodrama'[:4]
    return


@app.cell
def _():
    # the second half
    'Melodrama'[4:]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can also use negatives to start from the *end* of a sequence. What is the value `-1` indexing if it provides us with the final character?
    """)
    return


@app.cell
def _():
    # index the last item
    'Melodrama'[-1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why is this output the same as the previous example?
    """)
    return


@app.cell
def _():
    "Melodrama"[-1:]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Perhaps starting at -2 makes this more clear? The index goes from -2 to the end of the string
    """)
    return


@app.cell
def _():
    "Melodrama"[-2:]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why don't we get the full word here? What is the start, and what is the stop?
    """)
    return


@app.cell
def _():
    'Melodrama'[:-1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you try to index a string at a location which does not exist, you will receive an "out of range" error:
    """)
    return


@app.cell
def _():
    'Melodrama'[42]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Indexing single values from lists

    Once you understand how to index and slice strings, many of the same general principles apply to lists.
    """)
    return


@app.cell
def _():
    # create a list
    birbs = ['kiwi', 'kākā', 'tūī', 'kea', 'pīwauwau']
    return (birbs,)


@app.cell
def _(birbs):
    # find the first bird
    birbs[0]
    return


@app.cell
def _(birbs):
    # who won bird of the year in 2022?
    birbs[-1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Slicing ranges of values from lists

    The same principles apply to lists for ranged slices as well
    """)
    return


@app.cell
def _(birbs):
    # give everything up until index 2
    birbs[:2]
    return


@app.cell
def _(birbs):
    # give everything from index 2 to the end of the list
    birbs[2:]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Your Turn**

    - create some strings and lists, and practice indexing them!
    - note down any remaining errors or problems you're having, as well as any questions about how this all works!
    """)
    return


@app.cell
def _():
    # use this code cell to practice indexing and slicing!

    return


if __name__ == "__main__":
    app.run()
