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
    # **In-class: word frequencies**

    Today's plan:

    1. Review: frequency distributions with `nltk.FreqDist()`
    2. Activities: a live frequency panel, Zipf's law, and raw vs normalised frequencies
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import matplotlib.pyplot as plt
    import polars as pl
    import nltk
    from nltk import FreqDist
    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['punkt_tab', 'stopwords', 'genesis', 'state_union'])
    from nltk.corpus import stopwords
    from nltk.corpus import state_union

    english_stopwords = stopwords.words('english')
    return FreqDist, english_stopwords, nltk, pl, plt, state_union


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: word frequencies - key points**

    - Word frequencies are a distribution of the number of times words occur in your text/data
      - High frequency words: occur a lot in your text
      - Low frequency words: occur very few times in your text
    - a small number of words will contribute to a relatively higher proportion of the total words (Zipfian distribution)
    - Note! These are frequencies specific to your data. Later we will look at generalised corpus frequencies from large data sets.

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _():
    # create a list of words
    colours = ['blue', 'blue', 'yellow', 'black']
    return (colours,)


@app.cell
def _(FreqDist, colours):
    # the result is a dictionary with keys (words) and values (frequencies)
    colour_fdist = FreqDist(colours)
    colour_fdist
    return (colour_fdist,)


@app.cell
def _(colour_fdist):
    # look up a specific value
    colour_fdist['blue']
    return


@app.cell
def _(colour_fdist):
    colour_fdist['orange']
    return


@app.cell
def _(FreqDist):
    # You can run a frequency distribution on a raw string, which gives us the frequency of characters
    kia_ora_fdist = FreqDist('kia ora koutou')
    kia_ora_fdist.most_common()
    return (kia_ora_fdist,)


@app.cell
def _(kia_ora_fdist):
    # types, tokens, and hapaxes
    print(f"types (B): {kia_ora_fdist.B()}")
    print(f"tokens (N): {kia_ora_fdist.N()}")
    print(f"hapaxes: {kia_ora_fdist.hapaxes()}")
    return


@app.cell
def _(kia_ora_fdist):
    # how could you get the TTR from a FreqDist?
    kia_ora_fdist.B() / kia_ora_fdist.N()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: live frequency panel**

    Choose a text (or type your own), then switch the preprocessing steps on and off, and choose whether to count words or characters. The table, numbers and chart update as you go.

    The texts are:

    - **Drummer speech:** a short speech from *The Expanse*
    - **Genesis:** the Book of Genesis (King James version)
    - **State of the Union 2006:** George W. Bush's 2006 speech
    - **my own text:** whatever you type in the text box
    """)
    return


@app.cell
def _(nltk, state_union):
    drummer = """
    Oye! Beltalowda!
    Listen up. This is your captain. And this is your ship. This is your moment.
    You may think that you're scared, but you're not. That isn't fear, that's your sharpness, that's your power.
    We are Belters. Nothing in the void is foreign to us. The place we go, is the place we belong. This is no different.
    No one has more right to this. None more prepared. Inyalowda go through the ring, call it their own, but a Belta opened it!
    We are the Belt! We are strong, we are sharp, and we don't feel fear! This moment belong to us! For Beltalowda!
    """

    # the raw text of each option
    panel_texts = {
      'Drummer speech': drummer,
      'Genesis': nltk.corpus.genesis.raw('english-kjv.txt'),
      'State of the Union 2006': state_union.raw('2006-GWBush.txt'),
    }
    return (panel_texts,)


@app.cell
def _(mo):
    # the controls for the panel
    text_choice = mo.ui.dropdown(options = ['Drummer speech', 'Genesis', 'State of the Union 2006', 'my own text'], value = 'Drummer speech', label = 'text:')
    own_text_box = mo.ui.text_area(value = 'type your own text here', label = 'my own text:', full_width = True)
    unit_choice = mo.ui.radio(options = ['words', 'characters'], value = 'words', label = 'count:')
    lowercase_check = mo.ui.checkbox(label = 'lowercase')
    punct_check = mo.ui.checkbox(label = 'remove punctuation')
    stopword_check = mo.ui.checkbox(label = 'remove stopwords (words only)')
    top_n_slider = mo.ui.slider(start = 5, stop = 50, step = 5, value = 20, label = 'how many to show:', show_value = True)

    mo.vstack([
      mo.hstack([text_choice, unit_choice], justify = 'start'),
      own_text_box,
      mo.hstack([lowercase_check, punct_check, stopword_check], justify = 'start'),
      top_n_slider,
    ])
    return (
        lowercase_check,
        own_text_box,
        punct_check,
        stopword_check,
        text_choice,
        top_n_slider,
        unit_choice,
    )


@app.cell
def _(
    FreqDist,
    english_stopwords,
    lowercase_check,
    nltk,
    own_text_box,
    panel_texts,
    punct_check,
    stopword_check,
    text_choice,
    unit_choice,
):
    # get the chosen text
    if text_choice.value == 'my own text':
      panel_text = own_text_box.value
    else:
      panel_text = panel_texts[text_choice.value]

    if lowercase_check.value:
      panel_text = panel_text.lower()

    # make the list of units to count
    if unit_choice.value == 'characters':
      # every character except spaces and newlines
      panel_units = [character for character in panel_text if not character.isspace()]
      if punct_check.value:
        panel_units = [character for character in panel_units if character.isalnum()]
    else:
      panel_units = nltk.word_tokenize(panel_text)
      if punct_check.value:
        panel_units = [token for token in panel_units if token.isalnum()]
      if stopword_check.value:
        panel_units = [token for token in panel_units if token.lower() not in english_stopwords]

    # the frequency distribution
    panel_fdist = FreqDist(panel_units)

    print(f"tokens (N): {panel_fdist.N()}")
    print(f"types (B): {panel_fdist.B()}")
    print(f"hapaxes: {len(panel_fdist.hapaxes())}")
    print(f"TTR: {round(panel_fdist.B() / panel_fdist.N(), 3)}")
    return (panel_fdist,)


@app.cell
def _(panel_fdist, pl, top_n_slider):
    # the most frequent items, as a table
    pl.DataFrame({
      'item': [item for (item, count) in panel_fdist.most_common(top_n_slider.value)],
      'frequency': [count for (item, count) in panel_fdist.most_common(top_n_slider.value)],
    })
    return


@app.cell
def _(panel_fdist, plt, top_n_slider):
    # the most frequent items, as a bar chart
    panel_items = [item for (item, count) in panel_fdist.most_common(top_n_slider.value)]
    panel_counts = [count for (item, count) in panel_fdist.most_common(top_n_slider.value)]

    fig1, ax1 = plt.subplots(figsize = (10, 4))
    ax1.bar(panel_items, panel_counts, color = '#6d8e7d')
    ax1.set_ylabel('frequency')
    ax1.tick_params(axis = 'x', labelrotation = 90)
    fig1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - Genesis, words, no preprocessing. What are the most frequent "words"? What happens when you remove punctuation? Lowercase? Remove stopwords?
    - The Drummer speech, characters, lowercased. Does the order of the letters match your intuition about English?
    - Compare the top words of Genesis and the State of the Union speech, with stopwords removed. What do the top words tell you about each text?
    - What share of the types are hapaxes in each text?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: is it Zipfian?**

    Zipf's law says a word's frequency is roughly inversely proportional to its rank (the 2nd most frequent word occurs about 1/2 as often as the most frequent, the 3rd about 1/3, and so on). On log-log axes, Zipf's law is a straight line.

    The plot below uses whatever text and settings you chose in the panel above (shown again here). Does a short text follow Zipf's law as well as a long one? What happens when you remove stopwords?
    """)
    return


@app.cell
def _(
    lowercase_check,
    mo,
    punct_check,
    stopword_check,
    text_choice,
    unit_choice,
):
    # the same controls as above - linked so changing one changes the other
    mo.vstack([
      mo.hstack([text_choice, unit_choice], justify = 'start'),
      mo.hstack([lowercase_check, punct_check, stopword_check], justify = 'start'),
    ])
    return


@app.cell
def _(panel_fdist, plt, text_choice):
    # frequency by rank, with Zipf's prediction
    zipf_counts = [count for (item, count) in panel_fdist.most_common()]
    zipf_ranks = range(1, len(zipf_counts) + 1)
    zipf_predicted = [zipf_counts[0] / rank for rank in zipf_ranks]

    fig2, ax2 = plt.subplots(figsize = (6, 5))
    ax2.plot(zipf_ranks, zipf_counts, label = text_choice.value)
    ax2.plot(zipf_ranks, zipf_predicted, label = "Zipf's law")
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_xlabel('rank (log scale)')
    ax2.set_ylabel('frequency (log scale)')
    ax2.legend()
    fig2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: raw vs normalised frequencies**

    Let's compare the State of the Union speeches of George H. W. Bush (Bush senior) and George W. Bush (Bush junior).
    """)
    return


@app.cell
def _(FreqDist, state_union):
    senior_files = ['1989-Bush.txt', '1990-Bush.txt', '1991-Bush-1.txt', '1991-Bush-2.txt', '1992-Bush.txt']
    junior_files = ['2001-GWBush-1.txt', '2001-GWBush-2.txt', '2002-GWBush.txt', '2003-GWBush.txt', '2004-GWBush.txt', '2005-GWBush.txt', '2006-GWBush.txt']

    # one frequency distribution for each president, lowercased
    senior_fdist = FreqDist([token.lower() for token in state_union.words(senior_files)])
    junior_fdist = FreqDist([token.lower() for token in state_union.words(junior_files)])

    print(f"Bush senior: {senior_fdist.N()} tokens")
    print(f"Bush junior: {junior_fdist.N()} tokens")
    return junior_fdist, junior_files, senior_fdist, senior_files


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The two presidents' corpora are different sizes, so raw counts aren't directly comparable. Type some words (separated by commas) into the box, and switch between **raw counts** and **per million words**.

    Can you find a word where the conclusion *flips* when you normalise? (Hint: look for a word whose raw counts are fairly close for the two presidents, then check which corpus is bigger.)
    """)
    return


@app.cell
def _(mo):
    target_box = mo.ui.text(value = 'the, freedom, americans, must, will, terror', label = 'words:', full_width = True)
    count_choice = mo.ui.radio(options = ['raw counts', 'per million words'], value = 'raw counts', label = 'show:')
    mo.vstack([target_box, count_choice])
    return count_choice, target_box


@app.cell
def _(count_choice, junior_fdist, pl, senior_fdist, target_box):
    # split the box into a list of words
    target_words = [word.strip().lower() for word in target_box.value.split(',')]

    # raw counts or per million, for each president
    if count_choice.value == 'raw counts':
      senior_values = [senior_fdist[word] for word in target_words]
      junior_values = [junior_fdist[word] for word in target_words]
    else:
      senior_values = [round(senior_fdist[word] / senior_fdist.N() * 1000000) for word in target_words]
      junior_values = [round(junior_fdist[word] / junior_fdist.N() * 1000000) for word in target_words]

    pl.DataFrame({
      'word': target_words,
      'Bush senior': senior_values,
      'Bush junior': junior_values,
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. Is the most frequent word in a text the most *important* word? What does the top-10 list of a text actually tell you, and what doesn't it tell you?
    2. Which preprocessing choices changed the top-10 lists the most? If two researchers made different choices, could they compare their results?
    3. Normalising lets us compare corpora of different sizes. What does a normalised frequency still hide? (Think back to range in the self-study notebook.)
    4. These are frequencies specific to *your* data. How might the Bush senior vs junior comparison change if we used a different set of speeches, or a different kind of text?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - the most frequent words are almost always function words and punctuation; even after removing stopwords, frequency tells us what a text talks about a lot, not what matters most in it
    - lowercasing, punctuation and stopwords can all reorder the top-10 list; results based on different preprocessing aren't directly comparable, which is why studies need to report their steps
    - a normalised frequency is an average across the whole corpus: it hides whether a word is spread evenly or packed into one or two texts (range and dispersion)
    - frequencies describe the data they come from: five speeches by one president are a small, particular sample, and a different selection (or a different genre) could change the comparison
    ''')})
    return


if __name__ == "__main__":
    app.run()
