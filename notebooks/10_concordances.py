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
    #### Relevant NLTK Book sections:

    [NLTK Book, Chapter 1, Section 1.3](https://www.nltk.org/book/ch01.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Concordances: words in context**

    You've already used `.concordance()` in the corpora notebook to see how words like *whale* and *banana* are used in various contexts. This notebook looks at concordances in more depth, along with two related tools from corpus linguistics for seeing words **in context**: finding words that are used in similar contexts, and finding the contexts two words share.

    These tools are also how we check what a number really means. Later in the course, when we find words that are "distinctive" of particular texts, concordance lines are how you find out *why* a word is distinctive.

    First, let's load the libraries and texts for this notebook.
    """)
    return


@app.cell
def _():
    # import the main nltk module and the Text class
    import nltk
    from nltk.text import Text

    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    # download the corpora this notebook uses
    nltk.download(['webtext', 'nps_chat', 'gutenberg'])
    return Text, nltk


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Searching Text**

    Chapter 1 of the NLTK book loads a series of books and corpora which are stored in NLTK as examples (`text1`, `text2`, and so on). These are just the words of NLTK corpora, wrapped in NLTK's `Text()` class, which gives them some extra functions such as `.concordance()`. We can make them ourselves from the corpora we've already met.

    Take a moment to look at the texts below - some are single books and movie scripts, while others are collections of texts. What is the difference between the two? A book is simply a stand-alone book, whereas a corpus is a large collection of text from similar texts/documents, which can be longer or shorter than a single book.
    """)
    return


@app.cell
def _(Text, nltk):
    # the script of Monty Python and the Holy Grail
    holy_grail = Text(nltk.corpus.webtext.words('grail.txt'))

    # a corpus of online chat messages
    chat = Text(nltk.corpus.nps_chat.words())

    # a corpus of personal ads
    personals = Text(nltk.corpus.webtext.words('singles.txt'))

    # Moby Dick
    moby_dick = Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt'))
    return chat, holy_grail, moby_dick, personals


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Concordance Lines

    NLTK starts off with concordances, which is a method that draws from corpus linguistics to analyse the meanings and/or functions of different words in texts. This method is fundamental for performing corpus analysis because a concordance will let you see a single word or patterns of words **in context** of the surrounding words.

    The example in the NLTK book is to search for the word `monstrous` in *Moby Dick*:
    """)
    return


@app.cell
def _(moby_dick):
    moby_dick.concordance('monstrous')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are some other concordance searches based on my own guesses about what you might find in the different texts. Feel free to play around and look for your own words.
    """)
    return


@app.cell
def _(holy_grail):
    # search for "color" in Holy Grail
    holy_grail.concordance('color')
    return


@app.cell
def _(chat):
    # search for "like" in the chat corpus
    chat.concordance('like')
    return


@app.cell
def _(personals):
    # search for 'looking' in the personals corpus
    personals.concordance('looking')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `.concordance()` shows 25 lines by default, each 80 characters wide. You can ask for more lines, or wider lines:
    """)
    return


@app.cell
def _(personals):
    personals.concordance('looking', width = 120, lines = 50)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Comparing words

    What you probably noticed is that words are used in specific ways in different corpora. This relatively simple analysis has thus already told us something about the way language works: context determines the way words are used and understood. Corpus linguistic analysis is thus a crucial way to gain a better understanding of word meanings and language use.

    The `.similar()` and `.common_contexts()` functions from the NLTK texts allow you to find words that are used in the same contexts. This means words which occur before/after the same other words. For example, in the following two sentences the words "truck" and "apple" are similar because they both occur after the word "red":

    - A big red truck
    - A big red apple

    For example, the cell below finds the words used in similar contexts as the word `green` in *Holy Grail*. Then try testing other words (such as `hello`) using the `.similar()` method in different texts. The output that you see represents words that are used in similar contexts as your input word.
    """)
    return


@app.cell
def _(holy_grail):
    # which words occur in the same contexts as 'green' in Monty Python?
    holy_grail.similar('green')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's verify this by looking at the concordance lines for those words...we can see that both `"green"` and `"black"` occur before the word `"knight"`. While interesting, the `.similar()` function is admittedly difficult to use in a meaningful way - we have seen better ways of capturing these relationships with collocations, and will see more later with word probabilities and word vectors.
    """)
    return


@app.cell
def _(holy_grail):
    holy_grail.concordance('green')
    return


@app.cell
def _(holy_grail):
    holy_grail.concordance('black')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `.common_contexts()` method allows you to compare two words in the same text. The NLTK book uses the example of testing `monstrous` and `very` in *Moby Dick*. The NLTK book asks you to pick two words of your own and compare them. If you're like me, you will see that many times you have no results because the words you searched for do not occur in the corpus or do not have any common contexts - this further demonstrates how we can predict the types of words based on our knowledge of the corpus.

    Please note that the two words you are searching for are placed inside a list, separated by a comma.
    """)
    return


@app.cell
def _(holy_grail):
    # test common contexts with 'green' and 'black'
    holy_grail.common_contexts(['green', 'black'])
    return


@app.cell
def _(chat):
    # do hello and goodbye have similar contexts in the chat corpus?
    chat.common_contexts(['hello', 'goodbye'])
    return


@app.cell
def _(chat):
    # what about 'hi' and 'bye' in the chat corpus?
    chat.common_contexts(['hi', 'bye'])
    return


@app.cell
def _(personals):
    # how about "hi" and "bye" in the personals?
    personals.common_contexts(['hi', 'bye'])
    return


@app.cell
def _(moby_dick):
    # these words in moby dick?
    moby_dick.common_contexts(['white', 'whale'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we wanted to make sure the words are actually in a text before running the function, we could use the `in` conditional statement and check the `.vocab()` of the text. `.vocab()` gives the frequency of every word in the text (it's a `FreqDist`, which you'll learn about in the frequency notebook), so you can also use it to look up frequencies!
    """)
    return


@app.cell
def _(chat):
    # check if a word is in the text
    'like' in chat.vocab()
    return


@app.cell
def _(holy_grail):
    'knight' in holy_grail.vocab()
    return


@app.cell
def _(holy_grail):
    # .vocab() is a FreqDist, so we can look up frequencies too
    # (why is this number so small? try 'KNIGHT' instead...)
    holy_grail.vocab()['knight']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    1. Spend a few moments using the `.concordance()` function to search for different words in the texts. See if you can find any interesting examples.

    2. After looking through some concordances, play with the `.similar()` and `.common_contexts()` functions to see if you can find words used in similar contexts.

    3. What can this analysis tell us, if anything, about the nature of the different texts?
    """)
    return


@app.cell
def _():
    # use this code cell to explore concordances!
    return


if __name__ == "__main__":
    app.run()
