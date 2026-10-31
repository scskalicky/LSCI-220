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
    # LSCI 220: setup check

    This notebook checks that everything you need for LSCI 220 is working on your computer.

    Scroll to the bottom. A green **"All checks passed"** box means you're set up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Python and marimo
    """)
    return


@app.cell
def _(mo):
    import sys
    python_version = sys.version.split()[0]
    mo.md(f"Python version: **{python_version}** &nbsp;&nbsp; marimo version: **{mo.__version__}**")
    return (python_version,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. NLTK and the internet
    """)
    return


@app.cell
def _():
    import nltk

    # download the NLTK data used in this notebook
    nltk.download(['punkt_tab', 'stopwords', 'averaged_perceptron_tagger_eng', 'brown'])
    return (nltk,)


@app.cell
def _():
    # read a text from the course GitHub repository
    import requests
    url = 'https://raw.githubusercontent.com/scskalicky/LING-226-vuw/main/sample-texts/tmoom.txt'
    meat = requests.get(url).text
    print(meat[:200])
    return (meat,)


@app.cell
def _(meat, nltk):
    # split the text into tokens
    tokens = nltk.word_tokenize(meat.lower())
    len(tokens)
    return (tokens,)


@app.cell
def _(nltk, tokens):
    # remove punctuation and stopwords
    from nltk.corpus import stopwords
    stop = stopwords.words('english')
    content_words = [word for word in tokens if word.isalpha() and word not in stop]
    content_words[:15]
    return (content_words,)


@app.cell
def _(nltk):
    # part-of-speech tags
    tags = nltk.pos_tag(nltk.word_tokenize('They are made out of meat.'))
    tags
    return (tags,)


@app.cell
def _(nltk):
    # a built-in corpus: the Brown corpus (about one million words)
    from nltk.corpus import brown
    brown_count = len(brown.words())
    brown_count
    return (brown_count,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Tables and plots
    """)
    return


@app.cell
def _(content_words, nltk):
    # a table of the most frequent content words
    import polars as pl
    freq = nltk.FreqDist(content_words)
    freq_table = pl.DataFrame(freq.most_common(10), schema=['word', 'count'], orient='row')
    freq_table
    return freq, freq_table


@app.cell
def _(freq):
    # a bar chart of the same words
    import matplotlib.pyplot as plt
    words = [word for word, count in freq.most_common(10)]
    counts = [count for word, count in freq.most_common(10)]
    plt.figure(figsize=(7, 3))
    plt.bar(words, counts)
    plt.xticks(rotation=45)
    plt.ylabel('count')
    chart = plt.gca()
    chart
    return (chart,)


@app.cell(hide_code=True)
def _(brown_count, chart, freq_table, mo, python_version, tags):
    mo.callout(
        mo.md(f"""
        ## ✅ All checks passed

        Python {python_version}, NLTK and its data, the internet connection, tables and plots are all working.
        """),
        kind="success",
    )
    return


if __name__ == "__main__":
    app.run()
