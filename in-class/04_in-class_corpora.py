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
    # **In-class: corpora**

    Today's plan:

    1. Review: NLTK corpora, using the State of the Union corpus
    2. Activities: exploring speeches, testing a hypothesis, and looking at concordance lines
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import os
    import matplotlib.pyplot as plt
    import polars as pl
    import nltk
    nltk.download(['state_union', 'punkt_tab'])
    from nltk.corpus import state_union
    from nltk.corpus import PlaintextCorpusReader
    from nltk.text import Text

    # allow NLTK to read corpora from the current folder
    nltk.data.path.append('.')
    return PlaintextCorpusReader, Text, os, pl, plt, state_union


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: NLTK corpora - key concepts**

    - what a corpus is: texts plus metadata
    - `.words()`, `.raw()` and `.sents()`
    - `.fileids()` and using file ids to pick out texts

    Let's quickly practise using just ONE corpus - `state_union`. Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _(state_union):
    # what even is this thing
    state_union
    return


@app.cell
def _(state_union):
    # tokens are stored as .words()
    state_union.words()
    return


@app.cell
def _(state_union):
    # the entire string is stored as .raw()
    state_union.raw()[:250]
    return


@app.cell
def _(state_union):
    # it even has sentences!
    state_union.sents()
    return


@app.cell
def _(state_union):
    # fileids is the metadata/fileid for each text in the corpus
    state_union.fileids()
    return


@app.cell
def _(state_union):
    # they are just another list of strings...
    for speech_id in state_union.fileids():
      if speech_id[0] == '2':
        print(speech_id)
    return


@app.cell
def _(state_union):
    len(state_union.words())
    return


@app.cell
def _(state_union):
    # you use these names as identifiers to get specific files/texts
    state_union.words('1963-Johnson.txt')
    return


@app.cell
def _(state_union):
    len(state_union.words('1963-Johnson.txt'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: speech explorer**

    Pick a speech from the dropdown. The cell below it uses the file id to pull out some information about the speech.
    """)
    return


@app.cell
def _(mo, state_union):
    # a dropdown of every speech in the corpus
    explorer_choice = mo.ui.dropdown(options = state_union.fileids(), value = '2006-GWBush.txt', label = 'speech:')
    explorer_choice
    return (explorer_choice,)


@app.cell
def _(explorer_choice, state_union):
    explorer_id = explorer_choice.value

    # the year is the first four characters of the file id
    print(f"year: {explorer_id[:4]}")

    # the president's name is the rest, without '.txt'
    print(f"president: {explorer_id[5:].replace('.txt', '')}")

    print(f"words: {len(state_union.words(explorer_id))}")
    print(f"sentences: {len(state_union.sents(explorer_id))}")
    print()
    print(state_union.raw(explorer_id)[:600])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look through a few speeches. Which are the longest and shortest? Do some presidents have more than one speech in the same year? (Look at 2001, for example.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: testing a hypothesis**

    Let's say I predict that the use of the word "terror" and its variants increased after September 11, 2001. The corpus has two speeches by George W. Bush from 2001: one from January, and one from September. Let's look at the start of each:
    """)
    return


@app.cell
def _(state_union):
    state_union.raw('2001-GWBush-1.txt')[100:400]
    return


@app.cell
def _(state_union):
    state_union.raw('2001-GWBush-2.txt')[184:500]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How can I find all the words related to "terror"? I will use a simple strategy, `str.startswith()`, to locate any token that starts with the stem `terro` (what other strategies could I take?).

    First, lowercase the words of each speech (keeping only tokens made of letters), then use a list comprehension to keep only the tokens that start with `terro`:
    """)
    return


@app.cell
def _(state_union):
    # lowercase the words of each speech
    pre_tokens = [word.lower() for word in state_union.words('2001-GWBush-1.txt') if word.isalpha()]
    post_tokens = [word.lower() for word in state_union.words('2001-GWBush-2.txt') if word.isalpha()]

    # keep only the tokens that start with 'terro'
    pre_terror = [word for word in pre_tokens if word.startswith('terro')]
    post_terror = [word for word in post_tokens if word.startswith('terro')]
    return post_terror, post_tokens, pre_terror, pre_tokens


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can count the matches with `len()`. Because the two speeches are different lengths, we also divide by the number of words in the speech, and multiply by 1,000, to get the number of matches **per 1,000 words**:
    """)
    return


@app.cell
def _(post_terror, post_tokens, pre_terror, pre_tokens):
    print(f"January 2001: {len(pre_terror)} matches, {round(len(pre_terror) / len(pre_tokens) * 1000, 2)} per 1,000 words")
    print(f"September 2001: {len(post_terror)} matches, {round(len(post_terror) / len(post_tokens) * 1000, 2)} per 1,000 words")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which words did we actually match? `set()` gives us each different word once, and the list method `.count()` tells us how many times a value appears in a list:
    """)
    return


@app.cell
def _(post_terror):
    for terror_form in set(post_terror):
      print(terror_form, post_terror.count(terror_form))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Does this match my hypothesis? Anything else you think should be / could be done?

    (Counting how often *every* word appears in a text is exactly what `nltk.FreqDist()` does, which you will learn about in the frequency notebook.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - the September speech uses *terror* words far more often, even after taking the different lengths into account
    - but the September 2001 speech was an address to Congress after the attacks, not a regular State of the Union, so we are comparing two different kinds of speech
    - the stem `terro` also catches words like *terrorize* and *terrorized*, which may or may not be what we want; a list of target words is another option
    - two speeches is a very small sample: what would we need to show that the *change* lasted?
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Now test your own hypothesis**

    Think of a word (or the start of a word) whose use you think might change over time, or differ between presidents. Some ideas: *econom*, *iraq*, *freedom*, *job*, *tax*, *family*.

    Type the stem in the box, choose some speeches, and see how often it appears in each one, per 1,000 words.
    """)
    return


@app.cell
def _(mo, state_union):
    # a text box for the stem, and a multiselect for the speeches
    stem_box = mo.ui.text(value = 'terro', label = 'stem:')
    speech_choice = mo.ui.multiselect(
      options = state_union.fileids(),
      value = ['2001-GWBush-1.txt', '2001-GWBush-2.txt', '2002-GWBush.txt', '2003-GWBush.txt', '2004-GWBush.txt', '2005-GWBush.txt', '2006-GWBush.txt'],
      label = 'speeches:',
    )
    mo.vstack([stem_box, speech_choice])
    return speech_choice, stem_box


@app.cell
def _(pl, speech_choice, state_union, stem_box):
    # lists to store the results
    hypothesis_speeches = []
    hypothesis_matches = []
    hypothesis_rates = []

    for chosen_speech in speech_choice.value:
      # lowercase the words of the speech, letters only
      speech_tokens = [word.lower() for word in state_union.words(chosen_speech) if word.isalpha()]

      # keep the tokens that start with the stem
      stem_matches = [word for word in speech_tokens if word.startswith(stem_box.value.lower())]

      # save the results
      hypothesis_speeches.append(chosen_speech)
      hypothesis_matches.append(len(stem_matches))
      hypothesis_rates.append(round(len(stem_matches) / len(speech_tokens) * 1000, 2))

    # put the results in a table
    hypothesis_table = pl.DataFrame({
      'speech': hypothesis_speeches,
      'matches': hypothesis_matches,
      'per 1,000 words': hypothesis_rates,
    })

    hypothesis_table
    return hypothesis_rates, hypothesis_speeches


@app.cell
def _(hypothesis_rates, hypothesis_speeches, plt, stem_box):
    # a bar chart of the results
    fig1, ax1 = plt.subplots(figsize = (10, 4))
    ax1.bar(hypothesis_speeches, hypothesis_rates, color = '#6d8e7d', width = .5)
    ax1.set_ylabel('per 1,000 words')
    ax1.set_title(f"words starting with '{stem_box.value}'")
    ax1.tick_params(axis = 'x', labelrotation = 90)
    fig1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: concordance lines**

    Counting tells us *how often* a word is used, but not how it is *used*. A **concordance** shows every place a word occurs, with the words around it. (You looked at concordances in more depth in the concordances notebook.)

    To get concordance lines, we wrap the words of a speech in NLTK's `Text()`. Choose a word and a speech below.
    """)
    return


@app.cell
def _(mo, state_union):
    # create the marimo controls for us. 
    concordance_word = mo.ui.text(value = 'terrorists', label = 'word:')
    concordance_speech = mo.ui.dropdown(options = state_union.fileids(), value = '2001-GWBush-2.txt', label = 'speech:')
    mo.hstack([concordance_word, concordance_speech], justify = 'start')
    return concordance_speech, concordance_word


@app.cell
def _(Text, concordance_speech, concordance_word, state_union):
    # lowercase the words, then wrap them in Text() and show the concordance lines
    concordance_text = Text([word.lower() for word in state_union.words(concordance_speech.value)])
    concordance_text.concordance(concordance_word.value.lower(), width = 100)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look up the word from your hypothesis. Is it used the way you expected? Would the concordance lines change your interpretation of the numbers?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Optional: making a tiny corpus**

    (if time...)

    To make your own corpus, you need your own `.txt` files in a folder. The cell below makes three short "texts" and saves them as files in a folder called `mini_corpus` (you'll learn how writing files works in the writing data to file notebook - normally you would already have your `.txt` files).
    """)
    return


@app.cell
def _(os):
    # create 3 "texts"
    mini_texts = {
      'text1.txt': 'Kinda like a cloud I was up way up in the sky. And I was feeling some feelings you wouldn\'t believe. Sometimes I don\'t believe them myself and I decided I was never coming down.',
      'text2.txt': 'Just then a tiny little dot caught my eye. It was just about too small to see. But I watched it way too long. It was pulling me down',
      'text3.txt': 'I was up above it. I was up above it. I was up above it. I was up above it. Now I\'m down in it',
    }

    # make the folder (exist_ok = True means no error if it already exists)
    mini_folder = 'mini_corpus'
    os.makedirs(mini_folder, exist_ok = True)

    # save each text as a file in the folder
    for mini_name in mini_texts:
      with open(os.path.join(mini_folder, mini_name), 'w') as mini_file:
        mini_file.write(mini_texts[mini_name])
    return (mini_folder,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have some "texts" we can create a corpus using `PlaintextCorpusReader`.
    """)
    return


@app.cell
def _(PlaintextCorpusReader, mini_folder):
    # create our corpus
    down_in_it = PlaintextCorpusReader(root = mini_folder, fileids = ['text1.txt', 'text2.txt', 'text3.txt'])

    # we have our own fileids!!
    down_in_it.fileids()
    return (down_in_it,)


@app.cell
def _(down_in_it):
    # the corpus does tokenization etc for us already
    down_in_it.words('text3.txt')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What if I want to get the TTR of each text?
    """)
    return


@app.cell
def _(down_in_it):
    # do we understand this loop?
    for mini_id in down_in_it.fileids():
      mini_tokens = [token.lower() for token in down_in_it.words(mini_id)]
      print(mini_id, len(set(mini_tokens)) / len(mini_tokens))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. Whose language is in the State of the Union corpus: the presidents', or their speechwriters'? Does it matter for the kinds of questions you might ask?
    2. Your hypothesis test counted words starting with a stem in a handful of speeches. How might your choice of stem, and of speeches, have shaped the result?
    3. The numbers and the concordance lines can tell different stories. When would you trust a frequency count, and when would you need to read the actual text?
    4. What could this corpus *not* tell you about how American presidents use language?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - State of the Union speeches are written by teams of speechwriters and delivered by the president; they tell us about the language of the office and of political communication more than about any one person's language
    - a stem can catch unrelated words (and miss related ones), and a few speeches may not be typical; changing either can change the conclusion, so it's worth trying more than one version
    - counts tell us *how often*, concordances tell us *how*: a word can become more frequent while being used in a completely different way
    - the corpus contains one genre (formal political speeches); it can't tell us about other genres these people use.
    ''')})
    return


if __name__ == "__main__":
    app.run()
