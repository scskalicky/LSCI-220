# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.25.2",
#     "nltk==3.10.4",
#     "matplotlib==3.11.2",
#     "polars==2.1.0",
#     "requests==2.34.2",
#     "scikit-learn==1.9.1",
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
    # **In-class: tf-idf**

    Today's plan:

    1. Review: tf, idf, and tf-idf
    2. Activities: guess the episode, what counts as a document, and changing the settings
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import io
    import os
    import math
    import zipfile
    import requests
    import polars as pl
    import nltk
    from glob import glob
    from nltk import FreqDist
    from nltk.corpus import gutenberg
    from sklearn.feature_extraction.text import TfidfVectorizer
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['punkt_tab', 'gutenberg'])
    return (
        FreqDist,
        TfidfVectorizer,
        glob,
        gutenberg,
        io,
        math,
        nltk,
        os,
        pl,
        requests,
        zipfile,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: tf-idf - key concepts**

    - **term frequency (tf)**: how frequent is a word in *this* document?
    - **inverse document frequency (idf)**: how many documents in the *corpus* does the word appear in? The fewer documents, the higher the idf
    - **tf-idf**: tf multiplied by idf, which is high for words that are frequent in this document but rare in the others

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _(math):
    # a word appears in all 14 of 14 episodes. What is its idf?
    math.log(14 / 14)
    return


@app.cell
def _(math):
    # a word appears 9 times in an episode with 2891 tokens, and in only 1 of the 14 episodes.
    # Will its tf-idf be big or small?
    (9 / 2891) * math.log(14 / 1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the rest of today we need the Seinfeld scripts. This time, we will split each line of the scripts into the **speaker** and **what they said**, so that we can build different kinds of documents later on.
    """)
    return


@app.cell
def _(io, requests, zipfile):
    def download_corpus(url, folder):
      # download the zip file and unzip everything into the folder
      response = requests.get(url)
      zip_file = zipfile.ZipFile(io.BytesIO(response.content))
      zip_file.extractall(folder)
      return folder

    seinfeld_folder = download_corpus('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/seinfeld.zip', 'seinfeld')
    return (seinfeld_folder,)


@app.cell
def _(glob, os, seinfeld_folder):
    def pre_process(x):
      # lowercase and remove punctuation
      x = x.lower()
      punctuation = '.;"!\'[]{}:><-_?,'
      return ''.join([char for char in x if char not in punctuation])

    # each line becomes a tuple of (episode, speaker, what they said)
    script_lines = []

    for episode_file in sorted(glob(seinfeld_folder + '/*.txt')):
      episode_name = os.path.basename(episode_file).replace('_cleaned.txt', '').lower()
      with open(episode_file, encoding = 'utf-8') as f:
        for line in f:
            # remove trailing/leading spaces
            line = line.strip()
  
            # skip any line that DOES NOT have a space
            if ' ' in line:
                # the speaker is the first word of the line, and the rest is what they said
                # so SPLIT on whitespace, but only ONCE (' ', 1)
                line_speaker, line_speech = line.split(' ', 1)
                script_lines.append((episode_name, line_speaker, pre_process(line_speech)))

    script_lines[:5]
    return (script_lines,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are the tf-idf functions from the tf-idf notebook, all rolled into one. You give `tf_idf_top_words()` a dictionary of documents (`name: text`), and it gives back the top tf-idf words for every document.
    """)
    return


@app.cell
def _(FreqDist, math, nltk):
    def tf_idf_top_words(documents, n = 10):
      # tokenise every document
      document_tokens = {}
      for name in documents:
        document_tokens[name] = nltk.word_tokenize(documents[name])

      # document frequency: how many documents does each word appear in?
      document_frequency = FreqDist()
      for tokens in document_tokens.values():
        for word in set(tokens):
          document_frequency[word] += 1

      # tf-idf for every word in every document
      number_of_documents = len(document_tokens)
      top_words = {}
      for name, tokens in document_tokens.items():
        counts = FreqDist(tokens)
        scores = {}
        for word in counts:
          tf = counts[word] / len(tokens)
          idf = math.log(number_of_documents / document_frequency[word])
          scores[word] = tf * idf
        top_words[name] = [word for (word, score) in FreqDist(scores).most_common(n)]

      return top_words

    return (tf_idf_top_words,)


@app.cell
def _(script_lines, tf_idf_top_words):
    # one document per episode
    episode_documents = {}
    for (episode, episode_speaker, episode_speech) in script_lines:
      episode_documents[episode] = episode_documents.get(episode, '') + ' ' + episode_speech

    episode_top_words = tf_idf_top_words(episode_documents)
    return episode_documents, episode_top_words


@app.cell
def _(episode_top_words):
    episode_top_words
    return


@app.cell
def _(episode_top_words):
    # 'jerry' is said in every episode. Will it be in the top 10 tf-idf words of any episode?
    [episode for episode in episode_top_words if 'jerry' in episode_top_words[episode]]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: guess the episode**

    Each episode below is one of the 14 Seinfeld episodes, but all you get to see are its top 10 tf-idf words. Maybe you haven't seen any of these episodes (Seinfeld is from the 1990s!), so some of them will be hard to guess. But for some episodes, the title might be all you need: see if you can match the words to one of the titles in the list below. Can you also guess what happens in the episode? Tick the box to check your answer.

    Episode list: *The Boyfriend (parts 1 and 2), The Chinese Restaurant, The Dealership, The Doodle, The English Patient, The Face Painter, The Good Samaritan, The Junior Mint, The Little Kicks, The Marine Biologist, The Parking Garage, The Parking Space, The Pez Dispenser*
    """)
    return


@app.cell
def _(episode_top_words, mo):
    import random

    # shuffle the episodes, using a seed so everyone gets the same order
    shuffled_episodes = list(episode_top_words)
    random.seed(220)
    random.shuffle(shuffled_episodes)

    # give each episode a mystery number, so the names are hidden
    mystery_episodes = {}
    for mystery_number, mystery_episode in enumerate(shuffled_episodes):
      mystery_episodes['mystery episode ' + str(mystery_number + 1)] = mystery_episode

    mystery_choice = mo.ui.dropdown(options = list(mystery_episodes.keys()), value = 'mystery episode 1', label = 'choose an episode:')
    mystery_reveal = mo.ui.checkbox(label = 'reveal the answer')
    mo.vstack([mystery_choice, mystery_reveal])
    return mystery_choice, mystery_episodes, mystery_reveal


@app.cell
def _(episode_top_words, mo, mystery_choice, mystery_episodes, mystery_reveal):
    mystery_name = mystery_episodes[mystery_choice.value]

    mo.vstack([
      mo.md('**top tf-idf words:** ' + ', '.join(episode_top_words[mystery_name])),
      mo.md('**answer:** ' + mystery_name.title()) if mystery_reveal.value else mo.md('')
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which kinds of words give the episode away? Which kinds of words are no help at all?
    - Which episodes could you match to their title from the words alone? Which were impossible without having seen the episode? What does that tell you about how much tf-idf can tell us about a text?
    - Are there any words in the lists you can't explain? How could you find out why they are there? (Hint: concordance lines!)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: what counts as a document?**

    tf-idf finds words that are distinctive of a document *compared to the other documents*. So what happens if we change what counts as a document? Below, the same Seinfeld lines are split up in three different ways:

    - **episodes**: one document per episode (14 documents)
    - **main characters**: everything said by Jerry, George, Elaine, and Kramer, across all the episodes (4 documents)
    - **chunks**: all the lines in order, cut into chunks of 500 words (about 90 documents)
    """)
    return


@app.cell
def _(episode_documents, script_lines, tf_idf_top_words):
    # one document per main character
    character_documents = {}
    for (character_episode, character, character_speech) in script_lines:
      if character in ['JERRY', 'GEORGE', 'ELAINE', 'KRAMER']:
        character_documents[character] = character_documents.get(character, '') + ' ' + character_speech

    # chunks of 500 words
    all_words = ' '.join([speech for (episode, speaker, speech) in script_lines]).split()
    chunk_documents = {}
    for start in range(0, len(all_words), 500):
      chunk_documents['chunk ' + str(start // 500 + 1)] = ' '.join(all_words[start:start + 500])

    document_choices = {
      'episodes': tf_idf_top_words(episode_documents),
      'main characters': tf_idf_top_words(character_documents),
      'chunks': tf_idf_top_words(chunk_documents),
    }
    return (document_choices,)


@app.cell
def _(document_choices, mo):
    document_type = mo.ui.dropdown(options = list(document_choices.keys()), value = 'main characters', label = 'what counts as a document?')
    document_type
    return (document_type,)


@app.cell
def _(document_choices, document_type, pl):
    chosen_top_words = document_choices[document_type.value]

    pl.DataFrame({
      'document': list(chosen_top_words.keys()),
      'top tf-idf words': [', '.join(words) for words in chosen_top_words.values()],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Look at the main characters. Based only on their words, what kind of person do you think each character is? What do you think each of them talks about?
    - What kinds of words are distinctive of each *episode*, compared to each *character*?
    - Look at the chunks. Do neighbouring chunks share words? Why? What can chunks tell us that episodes can't?
    - The same text gives very different "distinctive words" depending on how we split it. What does that tell us about tf-idf?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - by episode, the distinctive words are mostly plot words and guest characters (*mint*, *pez*, *roy*), because those are what change from episode to episode
    - by character, the distinctive words come from the storylines each character is part of (e.g., Kramer's *cubans* and *dominicans*), and from how they talk (George's *ho* and *heh*), because the four main characters are in every episode
    - chunks are smaller than episodes, so they pick up individual scenes; neighbouring chunks often come from the same scene or episode, so they share words
    - tf-idf always answers "distinctive *compared to what*?", and the answer changes with the documents and the corpus we choose
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: changing the settings**

    In the tf-idf notebook, we saw that scikit-learn's `TfidfVectorizer()` has a `max_df` setting, which ignores words that appear in more than a certain proportion of documents. There is also a `min_df` setting, which ignores words that appear in fewer than a certain number of documents.

    Choose a Gutenberg book and change the settings. What happens to the top words?
    """)
    return


@app.cell
def _(gutenberg):
    # one string per Gutenberg book
    gutenberg_books = gutenberg.fileids()
    gutenberg_documents = []
    for book in gutenberg_books:
      gutenberg_documents.append(' '.join([word.lower() for word in gutenberg.words(book) if word.isalpha()]))
    return gutenberg_books, gutenberg_documents


@app.cell
def _(gutenberg_books, mo):
    book_choice = mo.ui.dropdown(options = gutenberg_books, value = 'shakespeare-hamlet.txt', label = 'book:')
    max_df_choice = mo.ui.slider(start = 0.1, stop = 1.0, step = 0.1, value = 1.0, label = 'max_df (ignore words in more than this proportion of books):')
    min_df_choice = mo.ui.slider(start = 1, stop = 10, value = 1, label = 'min_df (ignore words in fewer than this many books):')
    mo.vstack([book_choice, max_df_choice, min_df_choice])
    return book_choice, max_df_choice, min_df_choice


@app.cell
def _(
    FreqDist,
    TfidfVectorizer,
    book_choice,
    gutenberg_books,
    gutenberg_documents,
    max_df_choice,
    min_df_choice,
    pl,
):
    settings_vectorizer = TfidfVectorizer(max_df = max_df_choice.value, min_df = min_df_choice.value)
    settings_tfidf = settings_vectorizer.fit_transform(gutenberg_documents)
    settings_words = settings_vectorizer.get_feature_names_out()

    # the scores for the chosen book
    book_scores = settings_tfidf[gutenberg_books.index(book_choice.value)].toarray()[0]
    book_top = FreqDist(dict(zip(settings_words, book_scores))).most_common(15)

    pl.DataFrame({
      'word': [word for (word, score) in book_top],
      'score': [round(score, 3) for (word, score) in book_top],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - Start with `max_df` at 1.0 and `min_df` at 1. What kinds of words are at the top? Now lower `max_df` step by step. When do the function words disappear?
    - Keep lowering `max_df`. What is left at the very bottom?
    - Now raise `min_df`. What happens to the character names? Why?
    - Which settings would you choose if you wanted to know what each book is *about*? Would the same settings work for the Seinfeld episodes?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - with `max_df = 1.0`, words in every book are still included (scikit-learn adds 1 to the idf), so very frequent function words can stay near the top
    - lowering `max_df` removes words that appear in many books, so the function words disappear first, then common content words, until only words from one or two books are left (mostly names)
    - raising `min_df` removes words that appear in only a few books, which removes character names first, since most names only appear in one book
    - there's no single "right" setting: it depends on the question, the documents, and how many documents there are
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. tf-idf finds what is *different* about a document, not what is *important* in it. What might it miss? (e.g., a theme that runs through every episode)
    2. A word is only "distinctive" compared to the other documents in the corpus. Who chooses the corpus, and how could that choice change the results?
    3. Character names often dominate tf-idf results. When is that useful, and when is it just noise?
    4. tf-idf was one of the earliest ways search engines decided which pages best matched a search. What kinds of pages would a ranking like this reward, and what might it hide?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - words that are frequent *everywhere* get low scores, even when they are central to a text (in Seinfeld, the characters' friendship or New York itself)
    - comparing a text to a different corpus gives different distinctive words: a Seinfeld episode compared to other Seinfeld episodes vs compared to news articles would give very different results
    - names are useful if you want to tell documents apart, but they say little about topics or style, so many analyses remove them (or use settings like `min_df`)
    - a tf-idf ranking rewards pages that use the search words often and in a distinctive way, which is easy to game by repeating keywords; it also knows nothing about meaning, so pages that use different words for the same idea can be hidden
    ''')})
    return


if __name__ == "__main__":
    app.run()
