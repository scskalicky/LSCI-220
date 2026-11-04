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
    ### Other tutorials on this topic

    [Geeks for Geeks Enumerate](https://www.geeksforgeeks.org/enumerate-in-python/)

    [Real Python Zip](https://realpython.com/python-zip-function/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # `enumerate()` for efficient loops, `zip()` for combining

    This notebook describes how to use `enumerate()` as a means to write more flexible for loops. It then covers the `zip()` function to show how to combine things. These are helper functions that you might find useful, but you may also choose to skip this for now.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # `enumerate()`

    `enumerate()` is a handy Python function which lets you declare a `for loop` alongside a counter. This means that you can loop through values *and* the counter of a loop, which can be handy for indexing and doing other tricks.

    To use `enumerate()`, you declare a `for loop` per usual but wrap the sequence you are looping over in `enumerate()`. You also need to declare two *variables*: one for the count of the loop, and one for the values of the for loop.
    """)
    return


@app.cell
def _():
    # define a string to use as an example
    target = 'soda'
    return (target,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the loop below, I print the index variable alongside the character from the target sequence. I print the index variable again just for fun. (The loops in this notebook use numbered variable names, `index1`, `character1`, and so on, because marimo only lets each variable be created in one cell.)
    """)
    return


@app.cell
def _(target):
    # create an enumerate loop
    for index1, character1 in enumerate(target):
      # print the loop counter plus value
      # remember, Python starts at 0
      print(index1, character1, index1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can use this process to do things such as index different locations during a loop.
    """)
    return


@app.cell
def _(target):
    # create an enumerate loop
    for index2, character2 in enumerate(target):
      # use the loop index as a way to index the target at that spot, which is the same result
      print(target[index2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since we have access to the index, we can traverse the sequence starting from that relative position. So if we subtract from or add to the index, we can move left or right.
    """)
    return


@app.cell
def _(target):
    # now print the previous character
    for index3, character3 in enumerate(target):
      # note how the negative index started the sequence at -1
      print(target[index3 - 1], character3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Of course, if we declare an index that is out of range, we will get an error.
    """)
    return


@app.cell
def _(target):
    for index4, character4 in enumerate(target):
      print(target[index4 + 10], character4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Consider how we can use this on a list of tokens to print word pairs:
    """)
    return


@app.cell
def _():
    # use nltk to tokenize
    import nltk
    nltk.download('punkt_tab')

    # create a sentence to work with.
    sentence = nltk.word_tokenize('I overthink your punctuation use. Not my fault, just a thing that my mind do')
    return (sentence,)


@app.cell
def _(sentence):
    # print word pairs
    for index, word in enumerate(sentence):
      # make sure index is not at the end of the sentence
      if index != len(sentence) - 1:
        # I am using the enumerate index to index the structure we are looping over
        print(word, sentence[index + 1])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Knowing about `enumerate()` is handy for looking at word combinations because you may want to iterate before and after words during a loop. Keep this function in mind as we explore bigrams and other ways words pattern together. It might help you when you start making your own functions and analyses!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # `zip()`

    The `zip()` function is a way to combine things from different containers, such as combining two lists into a paired set. The `zip()` function starts by matching the first items in each list, then the second items, and so on. The function works even if the lists are of different lengths - it will stop when it reaches the end of the shortest list.

    Below I create two lists:
    """)
    return


@app.cell
def _():
    te_reo = ["Tāmaki Makaurau", "Te Whanganui-a-Tara", "Ōtautahi"]
    english = ["Auckland", "Wellington", "Christchurch"]
    return english, te_reo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using `zip()` combines them together into a generator object. Basically, this means the data is packed into the generator and waiting for you to access it. You can do this by looping over the generator, using a list comprehension, or just forcing the `zip()` to be a list.
    """)
    return


@app.cell
def _(english, te_reo):
    # on its own, it is a generator
    zip(te_reo, english)
    return


@app.cell
def _(english, te_reo):
    # loop over the zips:
    for pair in zip(te_reo, english):
      print(pair)
    return


@app.cell
def _(english, te_reo):
    # use a list comprehension
    [pair for pair in zip(te_reo, english)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This can be extended to more than two things:
    """)
    return


@app.cell
def _():
    # create three lists
    a = ['a', 'a', 'a']
    b = ['b', 'b', 'b']
    c = ['c', 'c', 'c']

    # combine the lists into new values
    [i for i in zip(a,b,c)]
    return


if __name__ == "__main__":
    app.run()
