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
    # **In-class: lexical sophistication and readability**

    Today's plan:

    1. Review: lexicons, coverage, and readability formulas
    2. Activities: a lexical profile explorer, a rewrite challenge, and a word lookup
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import requests
    import polars as pl
    import nltk
    from nltk.corpus import cmudict
    nltk.download(['punkt_tab', 'cmudict'])
    return cmudict, nltk, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, let's load the four lexicons from the lexical sophistication notebook. This might take a few seconds.
    """)
    return


@app.cell
def _(requests):
    def get_word_rating_resource(url):
      # read the raw text and split on newlines
      raw = requests.get(url).text.split('\n')

      ratings = {}
      for line in raw:
        pair = line.split('\t')
        # only keep lines with a word AND a value
        if len(pair) == 2:
          ratings[pair[0]] = round(float(pair[1]), 3)
      return ratings

    resources = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/'

    lexicons = {
      'frequency': get_word_rating_resource(resources + 'subtlxus_frequency.txt'),
      'age of acquisition': get_word_rating_resource(resources + 'AoA_Brysbart.txt'),
      'concreteness': get_word_rating_resource(resources + 'concreteness.txt'),
      'semantic diversity': get_word_rating_resource(resources + 'semantic_diversity.txt'),
    }
    return (lexicons,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: lexicons, coverage, and readability - key concepts**

    - a **lexicon** is a dictionary of words with ratings (frequency, age of acquisition, concreteness, semantic diversity)
    - a text's **profile** is the average rating of its words
    - **coverage** is the proportion of words in the text which are in the lexicon
    - **readability formulas** combine counts of words, sentences, and syllables

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _(lexicons):
    # are these the same key?
    print('These' in lexicons['frequency'])
    print('these' in lexicons['frequency'])
    return


@app.cell
def _():
    # what is the average of no ratings at all?
    no_ratings = []
    sum(no_ratings) / len(no_ratings)
    return


@app.cell
def _(lexicons):
    # which lexicon has a rating for 'pretzels'? What about 'pretzel'?
    for lexicon_name in lexicons:
      print(lexicon_name, 'pretzels' in lexicons[lexicon_name], 'pretzel' in lexicons[lexicon_name])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Review answers": mo.md(r'''
    - Python dictionaries are case-sensitive, so `These` and `these` are different keys. The frequency lexicon has some capitalised words (for names), but not `These`. This is why we lowercase texts before looking up their words
    - dividing by the length of an empty list gives a `ZeroDivisionError`. In the lexical sophistication notebook, we fixed this with an `if` statement that returns `None` when there are no ratings
    - some lexicons only have the base form of a word (*pretzel*), not the inflected forms (*pretzels*), so the same text can have very different coverage in different lexicons
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here are the functions we need for today, rolled together from the lexical sophistication and readability notebooks. You don't need to read them in detail, but make sure you know what each one gives back:

    - `lexicon_profile(text, lexicon)` gives back the average rating, the coverage, and the list of words which were *not* in the lexicon
    - `readability(text)` gives back the Flesch Reading Ease, Flesch-Kincaid Grade Level, and Gunning Fog scores
    - `full_profile(text)` uses both functions to make a table with every measure for a text
    """)
    return


@app.cell
def _(nltk):
    def clean_tokens(text):
      # lowercase and tokenise, keeping only alphabetic tokens
      return [token for token in nltk.word_tokenize(text.lower()) if token.isalpha()]

    def lexicon_profile(text, lexicon):
      tokens = clean_tokens(text)
      ratings = []
      missing = []
      for token in tokens:
        if token in lexicon:
          ratings.append(lexicon[token])
        else:
          missing.append(token)

      # avoid dividing by zero
      if len(ratings) == 0:
        return None, 0, missing

      average = round(sum(ratings) / len(ratings), 2)
      coverage = round(len(ratings) / len(tokens), 2)
      return average, coverage, missing

    return clean_tokens, lexicon_profile


@app.cell
def _(clean_tokens, cmudict, nltk):
    cmu = cmudict.dict()

    def count_syllables(word):
      # use the CMU dictionary if we can
      if word in cmu:
        return len([sound for sound in cmu[word][0] if sound[-1].isdigit()])

      # otherwise, count the groups of vowels
      syllables = 0
      previous_char_is_vowel = False
      for char in word:
        if char in 'aeiouy':
          if previous_char_is_vowel == False:
            syllables += 1
          previous_char_is_vowel = True
        else:
          previous_char_is_vowel = False
      return syllables

    def readability(text):
      tokens = clean_tokens(text)
      sentences = nltk.sent_tokenize(text)

      # avoid dividing by zero
      if len(tokens) == 0 or len(sentences) == 0:
        return None, None, None

      syllables = 0
      complex_words = 0
      for token in tokens:
        token_syllables = count_syllables(token)
        syllables += token_syllables
        if token_syllables > 2:
          complex_words += 1

      words_per_sentence = len(tokens) / len(sentences)
      syllables_per_word = syllables / len(tokens)

      reading_ease = round(206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word), 1)
      grade_level = round((0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59, 1)
      fog = round(0.4 * (words_per_sentence + 100 * (complex_words / len(tokens))), 1)
      return reading_ease, grade_level, fog

    return (readability,)


@app.cell
def _(lexicon_profile, lexicons, pl, readability):
    def full_profile(text):
      measures = []
      values = []
      coverages = []

      # the four lexicons
      for lexicon_name in lexicons:
        average, coverage, missing = lexicon_profile(text, lexicons[lexicon_name])
        measures.append(lexicon_name)
        values.append(average)
        coverages.append(coverage)

      # the three readability formulas
      reading_ease, grade_level, fog = readability(text)
      measures = measures + ['Flesch reading ease', 'Flesch-Kincaid grade', 'Gunning Fog']
      values = values + [reading_ease, grade_level, fog]
      coverages = coverages + [None, None, None]

      return pl.DataFrame({'measure': measures, 'value': values, 'coverage': coverages})

    return (full_profile,)


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Reminder: what do the measures mean?": mo.md(r'''
    | measure | higher score means... |
    |---|---|
    | frequency | more frequent words (less sophisticated) |
    | age of acquisition | words learned later in life (more sophisticated) |
    | concreteness | more concrete words (less sophisticated) |
    | semantic diversity | words used in more contexts (less sophisticated) |
    | Flesch reading ease | easier to read |
    | Flesch-Kincaid grade | harder to read (a higher US school grade) |
    | Gunning Fog | harder to read (a higher US school grade) |
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: lexical profile explorer**

    Type or paste any text into the box below to see its full profile. Try a few different kinds of text, for example:

    - a text message or social media post
    - a paragraph from one of the course readings
    - a news story
    - a page from a children's book
    - something you have written for another course

    (The example text in the box is the first sentence of the Wikipedia article on Bayesian statistics.)
    """)
    return


@app.cell
def _(mo):
    explorer_text = mo.ui.text_area(value = 'Bayesian statistics is a theory in the field of statistics based on the Bayesian interpretation of probability, where probability expresses a degree of belief in an event. ', label = 'your text:', full_width = True, rows = 6)
    explorer_text
    return (explorer_text,)


@app.cell
def _(explorer_text, full_profile):
    full_profile(explorer_text.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which words were *not* in each lexicon?
    """)
    return


@app.cell
def _(explorer_text, lexicon_profile, lexicons):
    for missing_lexicon in lexicons:
      missing_average, missing_coverage, missing_words = lexicon_profile(explorer_text.value, lexicons[missing_lexicon])
      print(missing_lexicon, ':', sorted(set(missing_words)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which kinds of text are the most and least sophisticated? Does that match your intuitions?
    - Do the lexicons and the readability formulas agree with each other?
    - Which kinds of words are missing from the lexicons? Does low coverage change how much you trust a score?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - academic texts usually have lower frequency, higher age of acquisition, and lower concreteness than texts like text messages or children's books, and get harder readability scores
    - the measures don't always agree: a text with short sentences but rare words can get an "easy" readability score and a "sophisticated" lexical profile
    - names, numbers written as words, slang, typos, inflected forms, and new words are often missing; when coverage is low, the average is based on only some of the words, which may not be typical of the whole text
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: rewrite challenge**

    Here is a challenge for your group. Start with the plain sentence below, and rewrite it in the second box:

    1. First, make it as **sophisticated** as possible, while keeping the same meaning. Which group can get the highest age of acquisition, or the highest Flesch-Kincaid grade?
    2. Then, make it as **simple** as possible.
    3. Finally, try to **trick** the measures. Can you write something that the formulas say is very easy, but which is actually very hard to understand? Or the other way around?
    """)
    return


@app.cell
def _(mo):
    original_text = mo.ui.text_area(value = 'The dog ran to the park because it wanted to play with the other dogs.', label = 'original:', full_width = True, rows = 4)
    rewritten_text = mo.ui.text_area(value = 'The canine proceeded expeditiously to the recreational area, motivated by a desire to engage in play with its fellow quadrupeds.', label = 'rewrite:', full_width = True, rows = 4)
    mo.hstack([original_text, rewritten_text], widths = 'equal')
    return original_text, rewritten_text


@app.cell
def _(full_profile, original_text, pl, rewritten_text):
    original_profile = full_profile(original_text.value)
    rewritten_profile = full_profile(rewritten_text.value)

    pl.DataFrame({
      'measure': original_profile['measure'],
      'original': original_profile['value'],
      'rewrite': rewritten_profile['value'],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which measures changed the most when you rewrote the sentence? Which hardly changed at all?
    - Is the "sophisticated" version actually *better* writing? Who would find it easier or harder to read?
    - What did you have to do to trick the measures? What does that tell you about what they measure?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - swapping short, common words for long, rare words changes almost everything: frequency goes down, age of acquisition goes up, and the readability formulas go up because of the extra syllables
    - the readability formulas can be tricked by changing sentence length (e.g., lots of very short sentences of difficult words) or by using short words that are hard to understand together (e.g., *what is is, and what is not is not*)
    - "sophisticated" is not the same as "good": the rewrite is harder to read, and most style guides would prefer the original!
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: word lookup**

    Type some words (separated by commas) to look up their ratings in all four lexicons. A blank cell means the word is not in that lexicon.

    The box starts with some New Zealand English words. How well do the lexicons cover them? Can you think of more? Also try finding words where the lexicons seem to disagree, for example a word which is rare, but learned early in life.
    """)
    return


@app.cell
def _(mo):
    lookup_words = mo.ui.text(value = 'jandal, togs, chilly bin, dairy, bach, ute, tramping, gumboots', label = 'words:', full_width = True)
    lookup_words
    return (lookup_words,)


@app.cell
def _(lexicons, lookup_words, pl):
    # split the words on commas and remove any spaces
    chosen_words = [chosen_word.strip().lower() for chosen_word in lookup_words.value.split(',')]

    lookup_table = {'word': chosen_words}
    for lookup_lexicon in lexicons:
      lookup_ratings = []
      for chosen_word in chosen_words:
        if chosen_word in lexicons[lookup_lexicon]:
          lookup_ratings.append(lexicons[lookup_lexicon][chosen_word])
        else:
          lookup_ratings.append(None)
      lookup_table[lookup_lexicon] = lookup_ratings

    pl.DataFrame(lookup_table)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which NZ English words are missing? Which ones are in the lexicons, but probably for a *different* meaning (e.g., *dairy* the shop vs *dairy* the milk products)?
    - If you profiled a text written by a New Zealander, what would happen to its coverage and its scores?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - most of the NZ words (*jandal*, *chilly bin*, *bach*, *gumboots*) are missing from every lexicon, because the lexicons were built from American English (SUBTLEXus, Mechanical Turk workers in the US)
    - some words are present but with a different meaning: *dairy* was most likely rated as milk products, not a corner shop (the raters only saw the word on its own), and *togs* and *ute* only have a frequency rating (from American subtitles, where they are rare)
    - a lexicon's ratings reflect the people and the texts it was built from; for other varieties of English, the coverage drops and the ratings may not mean the same thing
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. Most of these ratings were collected from American adults (often on Amazon Mechanical Turk). Whose sense of "difficult", "concrete", or "learned early" do they represent? What might be different for New Zealanders, children, or second language learners?
    2. If a lexicon only covers half of the words in a text, is that a problem? What are some arguments for when coverage would be too low? Could coverage ever be too high?
    3. Readability formulas are used to assess the right audience for reading, or to ensure that documents (e.g., government forms) are at a low enough reading level for the general public. What could go wrong if they only measure surface features like word and sentence length?
    4. Is a "sophisticated" text the same as a difficult text, or a well-written text? What do these measures actually capture?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - a lexicon reflects the people who rated it and the texts it was built from; other groups may know words earlier or later, find different words concrete, or use words with different meanings
    - low coverage means the score is based on a subset of the words, which are often the most common ones; reporting coverage alongside the score lets readers judge this
    - there's no fixed cut-off for "too low": it depends on *which* words are missing (missing names or function words matter less than missing content words) and on what the score is used for; very high coverage isn't automatically good either, since it can mean the text is made up of the most common words, or that the lexicon includes words with a different meaning from the one in the text
    - readability formulas ignore meaning, background knowledge, word order, and text structure, so a text can be rated "easy" but be confusing (or the reverse); they also may not suit L2 readers, whose difficulties are often different from those of L1 children
    - for documents like government forms, a text can get an "easy" score and still be confusing because of jargon, layout, or concepts the reader doesn't know; and rewriting a text just to hit a target score (e.g., by chopping long sentences into short ones) can make it harder to follow, not easier
    - the measures capture properties of words and sentences, not quality of writing; plain writing can be excellent, and "sophisticated" writing can be hard to read for no good reason
    ''')})
    return


if __name__ == "__main__":
    app.run()
