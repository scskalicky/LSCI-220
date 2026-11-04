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
    # **Bonus / unused material**

    Sections taken out of the in-class notebooks, parked here in case they're useful later. Each section says where it came from.

    *From: in-class 05 (word frequencies)*
    """)
    return


@app.cell
def _():
    # libraries and data these sections need
    import nltk
    from nltk import FreqDist
    nltk.download(['stopwords', 'genesis', 'state_union'])
    from nltk.corpus import stopwords
    from nltk.corpus import state_union

    english_stopwords = stopwords.words('english')

    senior_files = ['1989-Bush.txt', '1990-Bush.txt', '1991-Bush-1.txt', '1991-Bush-2.txt', '1992-Bush.txt']
    junior_files = ['2001-GWBush-1.txt', '2001-GWBush-2.txt', '2002-GWBush.txt', '2003-GWBush.txt', '2004-GWBush.txt', '2005-GWBush.txt', '2006-GWBush.txt']
    return FreqDist, english_stopwords, junior_files, nltk, senior_files, state_union


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Practice: using `FreqDist` for conditional tests**

    A frequency distribution can be used as a resource to perform conditional tests. Here is a frequency distribution of Genesis (lowercased, letters only).

    How can we:

    - get every entry in the Genesis FreqDist if the word is longer than 5 characters and the frequency is more than 10?
    - get a set of all words that start with 'a' and have a frequency greater than 10?
    - get a list of all words that occur only one time and are longer than 10 characters?
    """)
    return


@app.cell
def _(FreqDist, nltk):
    genesis_fdist = FreqDist([token.lower() for token in nltk.corpus.genesis.words('english-kjv.txt') if token.isalpha()])
    return (genesis_fdist,)


@app.cell
def _(genesis_fdist):
    # start slowly - get all entries in genesis_fdist if they are longer than 5
    [entry for entry in genesis_fdist if len(entry) > 5]
    return


@app.cell
def _(genesis_fdist):
    # how about every entry with frequency greater than 10?
    [entry for entry in genesis_fdist if genesis_fdist[entry] > 10]
    return


@app.cell
def _(genesis_fdist):
    # combine them?
    [entry for entry in genesis_fdist if len(entry) > 5 and genesis_fdist[entry] > 10]
    return


@app.cell
def _():
    # get a set of all words in genesis that start with 'a' and have a frequency greater than 10?
    return


@app.cell
def _():
    # get a list of all words that occur only one time and are longer than 10 characters
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Functions save typing**

    When we compare the same words across lots of speeches, we end up repeating the same code. This is where functions (from the Writing functions notebook) help: we write the steps once, then reuse them.
    """)
    return


@app.cell
def _(FreqDist):
    def word_counter_9000(files, corpus, targets):
      for file in files:
        print(f'\nanalysing {file}')
        tokens = [token.lower() for token in corpus.words(file)]
        fd = FreqDist(tokens)

        for target in targets:
          print(f'frequency of {target}: {fd[target]}, which is {round(fd[target] / fd.N() * 1000000)} per million words')

    return (word_counter_9000,)


@app.cell
def _(senior_files, state_union, word_counter_9000):
    word_counter_9000(senior_files, state_union, ['the', 'freedom', 'americans'])
    return


@app.cell
def _(junior_files, state_union, word_counter_9000):
    word_counter_9000(junior_files, state_union, ['the', 'freedom', 'americans'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **can go crazy and write more functions**

    This one will clean the text and then output the top n most frequent words
    """)
    return


@app.cell
def _(FreqDist, english_stopwords):
    def word_counter_9001(files, corpus, n = 5):
      for file in files:
        print(f'\nanalysing {file}')
        tokens = [token.lower() for token in corpus.words(file) if token.isalnum() and token.lower() not in english_stopwords]
        fd = FreqDist(tokens)

        print(f'top {n} words for {file}:\n{fd.most_common(n)}')

    return (word_counter_9001,)


@app.cell
def _(senior_files, state_union, word_counter_9001):
    word_counter_9001(senior_files, state_union, n = 10)
    return


if __name__ == "__main__":
    app.run()
