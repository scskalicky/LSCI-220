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
    # **In-class: strings**

    Today's plan:

    1. Getting comfortable with marimo
    2. Review: strings, what they are and how to make them
    3. Activities: how Python "sees" strings
    4. Critical reflection
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **marimo - key concepts**

    - running a cell: click ▶ at the top right of a cell, or click in the cell and press Shift + Enter
    - adding a cell: hover over the top or bottom edge of a cell and click **+**
    - cells **react** to each other: when you change a variable, every cell that uses it runs again
    - each variable can only be created in **one** cell
    - making a new notebook of your own

    Run the next two cells. Then change `greeting` to something else and run its cell again. What happens to the cell below it?
    """)
    return


@app.cell
def _():
    greeting = 'kia ora'
    return (greeting,)


@app.cell
def _(greeting):
    # this cell uses greeting, so it re-runs whenever greeting changes
    greeting.upper()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the code below, type `greeting = 'hello'` into it. Run it. What does marimo tell you?
    """)
    return


@app.cell
def _():
    # use this code cell.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"What just happened?": mo.md(r'''
    - `greeting` already exists in another cell, so marimo won't let a second cell create it
    - this is how marimo keeps track of which cells depend on which: every variable has exactly one "home" cell
    - to fix it, choose a new name (e.g. `greeting2`), or change the original cell instead
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: strings - key concepts**

    - what are "strings"?
    - how do we create/manipulate strings in Python?
    - what are delimiters?

    Before running each cell below, predict what the output will be. Were you right?
    """)
    return


@app.cell
def _():
    # a string can be a sentence
    'something in the way'
    return


@app.cell
def _():
    # or seemingly nothing

    '      '
    return


@app.cell
def _():
    # or something that looks like numbers

    '1234'
    return


@app.cell
def _():
    1234
    return


app._unparsable_cell(
    r"""
    # importance of matching delimiters
    'hello world"
    """,
    name="_"
)


@app.cell
def _():
    # double outside, single inside
    "jerry looked at the camera and said: 'that's a shame'"
    return


@app.cell
def _():
    # single outside, double inside
    'i am afraid i am not fully "aware" of the situation'
    return


@app.cell
def _():
    # escaping with \ tells Python to "ignore" the quote as a delimiter

    # the apostrophe in it's is ignored as a delimiter

    'the knight looked down, then said "it\'s just a flesh wound!"'
    return


@app.cell
def _():
    # how can I save a string as a variable?
    mydata = 'this is a string'
    mynumber = 1
    return (mydata,)


@app.cell
def _(mydata):
    # how can I access the string stored to a variable?

    print(mydata)
    return


@app.cell
def _(mydata):
    # how can I manipulate the string? (e.g., lowercase it, uppercase it)

    mydata.upper()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using `len()` and `type()`
    """)
    return


@app.cell
def _():
    len('hello world')
    return


@app.cell
def _():
    type('1234')
    return


@app.cell
def _():
    type(1234)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Adding and multiplying strings:
    """)
    return


@app.cell
def _():
    'hello' + ' ' + 'world!'
    return


@app.cell
def _():
    'b' + 'r'*10
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Strings are sequences of characters

    Look at what is printed out - what is included in this sequence?
    """)
    return


@app.cell
def _():
    # a python list comprehension to return each value of a sequence:

    [c for c in '"strings are sequences of characters!"']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: string inspector**

    Type any string into the box below and press Enter. The cell after it shows you how Python sees your string.

    Some things to try:

    - only spaces
    - `1234`
    - an emoji 😀
    - a word with a macron, like `kākā`
    - two words joined with a hyphen
    - a full sentence with punctuation
    """)
    return


@app.cell
def _(mo):
    # a text box to type a string into
    inspect_box = mo.ui.text(value='kia ora koutou!', label='your string:', full_width=True)
    inspect_box
    return (inspect_box,)


@app.cell
def _(inspect_box):
    # how does Python see the string in the box?
    inspected = inspect_box.value

    print(f"the string:     '{inspected}'")
    print(f"type:           {type(inspected)}")
    print(f"length:         {len(inspected)}")
    print(f"characters:     {[c for c in inspected]}")
    print(f"uppercase:      {inspected.upper()}")
    print(f"split:          {inspected.split()}")
    print(f"number of 'words' after .split(): {len(inspected.split())}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Activity: same to you, different to Python?**

    Type a string into each box below. To a person, the two strings might look the same. Does Python agree?

    Try:

    - `hello` and `hello ` (with a space at the end)
    - `Hello` and `hello`
    - `cant` and `can't`
    - `1234` and `1,234`
    """)
    return


@app.cell
def _(mo):
    # two text boxes, side by side
    string_a = mo.ui.text(value='hello', label='string A:')
    string_b = mo.ui.text(value='hello ', label='string B:')
    mo.hstack([string_a, string_b], justify='start')
    return string_a, string_b


@app.cell
def _(string_a, string_b):
    print(f"A: '{string_a.value}'  ({len(string_a.value)} characters)")
    print(f"B: '{string_b.value}'  ({len(string_b.value)} characters)")
    print(f"Does Python think they are the same? {string_a.value == string_b.value}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    # **Critical reflection**

    1. What differences exist between computational and human representations of strings? Find the pair of strings that look most alike to a person, but that Python treats as different.
    2. Which of the differences you found should "count" when we analyse language? For example, should `Hello` and `hello` be the same word? What about `resume` and `résumé`? Who gets to decide?
    3. A string stores the characters of a text. What does it leave out about language as people actually use it?
    """), kind='info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - to Python, a string is just a sequence of characters, and every character counts: spaces, punctuation, capital letters, accents
    - people ignore a lot of this (a trailing space, a capital at the start of a sentence), and Python ignores none of it
    - sometimes a small difference matters (`resume` vs `résumé` are different words), and sometimes it doesn't (`Hello` vs `hello`): deciding which depends on the question being asked
    - so before we can count *words*, we have to make decisions about which differences matter (this is the start of tokenisation)
    - a string leaves out a lot: speech, intonation, gesture, who is speaking and to whom, and the context that tells us what an utterance means
    - Is there anything else you noticed?
    ''')})
    return


if __name__ == "__main__":
    app.run()
