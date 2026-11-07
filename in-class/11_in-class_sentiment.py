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
    # **In-class: sentiment and emotion**

    Today's plan:

    1. Review: lexicon lookups, VADER, and emotion lexicons
    2. Activities: break VADER, can sentiment spot satire?, and emotion profiles
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import io
    import os
    import zipfile
    import requests
    import matplotlib.pyplot as plt
    import polars as pl
    import nltk
    from glob import glob
    from collections import defaultdict
    from nltk import FreqDist
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['punkt_tab', 'vader_lexicon'])
    return (
        FreqDist,
        SentimentIntensityAnalyzer,
        defaultdict,
        glob,
        io,
        nltk,
        os,
        pl,
        plt,
        requests,
        zipfile,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, let's load the lexicons from the sentiment and emotion lexicons notebooks, and create a VADER analyser.
    """)
    return


@app.cell
def _(SentimentIntensityAnalyzer, defaultdict, requests):
    resources = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/'

    # AFINN: word -> rating from -5 to +5
    afinn_dict = {}
    for afinn_line in requests.get(resources + 'AFINN-111.txt').text.split('\n'):
      afinn_pair = afinn_line.split('\t')
      if len(afinn_pair) == 2:
        afinn_dict[afinn_pair[0]] = int(afinn_pair[1])

    # NRC: emotion -> set of words
    nrc_emotion_dict = defaultdict(set)
    for nrc_line in requests.get(resources + 'emotion_lexicon.txt').text.split('\n'):
      nrc_parts = nrc_line.split('\t')
      if len(nrc_parts) == 3 and nrc_parts[2].strip() == '1':
        nrc_emotion_dict[nrc_parts[1]].add(nrc_parts[0])

    # VAD: word -> valence, arousal, dominance
    vad_dict = {}
    for vad_line in requests.get(resources + 'warriner_VAD.txt').text.split('\n')[1:]:
      vad_parts = vad_line.strip().split('\t')
      if len(vad_parts) == 4:
        vad_dict[vad_parts[0]] = {'valence': float(vad_parts[1]), 'arousal': float(vad_parts[2]), 'dominance': float(vad_parts[3])}

    vader = SentimentIntensityAnalyzer()
    return afinn_dict, nrc_emotion_dict, resources, vad_dict, vader


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And here are the functions we need, rolled together from those notebooks:
    """)
    return


@app.cell
def _(nltk, vader):
    def clean_tokens(text):
      # lowercase and tokenise, keeping only alphabetic tokens
      return [token for token in nltk.word_tokenize(text.lower()) if token.isalpha()]

    def sentiment_lookup(text, sentiment_dict):
      # average rating and coverage of the words in a lexicon
      tokens = clean_tokens(text)
      ratings = [sentiment_dict[token] for token in tokens if token in sentiment_dict]
      if len(ratings) == 0:
        return None, 0
      return round(sum(ratings) / len(ratings), 2), round(len(ratings) / len(tokens), 2)

    def vader_label(compound):
      # VADER's guidelines for turning a compound score into a label
      if compound >= 0.05:
        return 'positive'
      elif compound <= -0.05:
        return 'negative'
      else:
        return 'neutral'

    def vader_sentence_average(text):
      # the average compound score of the sentences in a text (better for long texts)
      sentence_scores = [vader.polarity_scores(sentence)['compound'] for sentence in nltk.sent_tokenize(text)]
      if len(sentence_scores) == 0:
        return None
      return round(sum(sentence_scores) / len(sentence_scores), 3)

    def profile_emotions(text, dictionary):
      # the proportion of tokens associated with each emotion
      tokens = clean_tokens(text)
      output = {}
      for emotion in sorted(dictionary):
        if len(tokens) == 0:
          output[emotion] = 0
        else:
          output[emotion] = round(len([token for token in tokens if token in dictionary[emotion]]) / len(tokens), 3)
      return output

    return (
        clean_tokens,
        profile_emotions,
        sentiment_lookup,
        vader_label,
        vader_sentence_average,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: sentiment and emotion - key concepts**

    - **lexicon-based sentiment** (e.g., AFINN) looks up each word and averages the ratings
    - **VADER** also uses a lexicon, but adds rules for negation, intensifiers, capitals, punctuation, and emoticons
    - **emotion lexicons** (e.g., NRC) record which words are *associated* with which emotions

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _(afinn_dict, sentiment_lookup):
    # does AFINN think this is positive or negative?
    sentiment_lookup('I am not happy', afinn_dict)
    return


@app.cell
def _(vader):
    # what about VADER?
    vader.polarity_scores('I am not happy')['compound']
    return


@app.cell
def _(vader):
    # same score or different?
    print(vader.polarity_scores('good')['compound'])
    print(vader.polarity_scores('GOOD!!!')['compound'])
    return


@app.cell
def _(nrc_emotion_dict, profile_emotions):
    # can a text be both joyful and angry?
    profile_emotions('love hate', nrc_emotion_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Review answers": mo.md(r'''
    - AFINN looks up each word on its own, so it only sees *happy* (+3) and says the sentence is positive
    - VADER has a rule for negation, so *not* flips *happy* and the compound score is negative
    - VADER also has rules for capital letters and exclamation marks, which make *GOOD!!!* more positive than *good*
    - the NRC lexicon counts each word on its own, so a text with *love* and *hate* is both joyful and angry (and positive and negative!)
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: break VADER**

    Each line in the box below is treated as a separate sentence. The table shows VADER's compound score and label for each line, along with the AFINN average and coverage.

    Your group's challenge: write sentences which VADER gets **wrong**. Some ideas to try:

    - sarcasm (*Oh great, another Monday.*)
    - slang where a negative word means something positive (*that gig was sick*)
    - New Zealand understatement and slang (*not bad at all*, *yeah nah*)
    - idioms, mixed feelings, and comparisons
    """)
    return


@app.cell
def _(mo):
    break_text = mo.ui.text_area(
      value = 'Oh great, another Monday.\nthat gig was sick\nshe totally killed it\nnot bad at all\nyeah nah\nI could not be happier',
      label = 'one sentence per line:',
      full_width = True,
      rows = 8,
    )
    break_text
    return (break_text,)


@app.cell
def _(afinn_dict, break_text, pl, sentiment_lookup, vader, vader_label):
    break_rows = []

    for break_line in break_text.value.split('\n'):
      if break_line.strip() != '':
        compound = vader.polarity_scores(break_line)['compound']
        afinn_average, afinn_coverage = sentiment_lookup(break_line, afinn_dict)
        break_rows.append({
          'sentence': break_line,
          'VADER compound': compound,
          'VADER label': vader_label(compound),
          'AFINN average': afinn_average,
          'AFINN coverage': afinn_coverage,
        })

    pl.DataFrame(break_rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which kinds of sentences does VADER get wrong? Is there a pattern?
    - Do VADER and AFINN make the same mistakes?
    - What would VADER need to *know* to get these sentences right?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - sarcasm and irony fool VADER because the words are positive but the meaning is negative (or the reverse); VADER has no way of knowing what the speaker really thinks
    - slang meanings (*sick*, *killed it*) are not in the lexicon, so VADER uses the standard (negative) meaning
    - VADER's negation rule can backfire: *I could not be happier* is very positive, but VADER sees *not* + *happier* and makes it negative
    - *yeah nah* means "no(?)" in New Zealand English, but VADER only sees *yeah* as positive; both lexicons were built by and for American English speakers
    - to get these right, a system needs knowledge of context, the speaker, the culture, and how words are used together, not just the words themselves
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: can sentiment spot satire?**

    In the sentiment notebook, we looked at a few of the Amazon reviews, where half are real ("normal") and half are satirical. Now let's look at *all* of them. For each review, we use the average VADER compound score of its sentences, and we also get the star rating and the label from the file name (e.g., `001-5-satire.txt` is review 1, 5 stars, satire).
    """)
    return


@app.cell
def _(io, requests, resources, zipfile):
    def download_corpus(url, folder):
      # download the zip file and unzip everything into the folder
      response = requests.get(url)
      zip_file = zipfile.ZipFile(io.BytesIO(response.content))
      zip_file.extractall(folder)
      return folder

    reviews_folder = download_corpus(resources + 'amazon%20reviews.zip', 'amazon reviews')
    return (reviews_folder,)


@app.cell
def _(glob, os, pl, reviews_folder, vader_sentence_average):
    review_rows = []

    for review_file in sorted(glob(reviews_folder + '/*.txt')):
      review_name = os.path.basename(review_file)
      # e.g., ['001', '5', 'satire']
      name_parts = review_name.replace('.txt', '').split('-')

      # skip any file which doesn't have a star rating in its name
      if len(name_parts) == 3 and name_parts[1].isdigit():
        with open(review_file, encoding = 'utf-8') as review_handle:
          review_text = review_handle.read()
        review_rows.append({
          'review': review_name,
          'stars': int(name_parts[1]),
          'label': name_parts[2],
          'compound': vader_sentence_average(review_text),
        })

    reviews_table = pl.DataFrame(review_rows)
    reviews_table
    return (reviews_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Do the satirical and normal reviews have different sentiment, on average?
    """)
    return


@app.cell
def _(pl, reviews_table):
    reviews_table.group_by('label').agg(pl.col('compound').mean().round(3), pl.len())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What about when we also take the star rating into account? Remember, a satirical 5 star review is "pretending" to be a happy customer:
    """)
    return


@app.cell
def _(pl, reviews_table):
    reviews_table.group_by(['stars', 'label']).agg(pl.col('compound').mean().round(3), pl.len()).sort(['stars', 'label'])
    return


@app.cell
def _(pl, plt, reviews_table):
    # the distribution of scores for each label
    satire_scores = reviews_table.filter(pl.col('label') == 'satire')['compound'].to_list()
    normal_scores = reviews_table.filter(pl.col('label') == 'normal')['compound'].to_list()

    fig1, ax1 = plt.subplots(figsize = (9, 4))
    ax1.hist(normal_scores, bins = 30, alpha = 0.6, label = 'normal')
    ax1.hist(satire_scores, bins = 30, alpha = 0.6, label = 'satire')
    ax1.set_xlabel('average VADER compound score of the sentences')
    ax1.set_ylabel('number of reviews')
    ax1.legend()
    fig1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now read some of the reviews! Choose a review below to see its text and its score. Do the satirical reviews *sound* positive? What gives them away to you, as a human reader?

    (Fair warning: some of the satirical reviews are a bit crude.)
    """)
    return


@app.cell
def _(mo, reviews_table):
    review_choice = mo.ui.dropdown(options = reviews_table['review'].to_list(), value = '001-5-satire.txt', label = 'review:')
    review_choice
    return (review_choice,)


@app.cell
def _(mo, review_choice, reviews_folder, vader_sentence_average):
    with open(reviews_folder + '/' + review_choice.value, encoding = 'utf-8') as chosen_handle:
      chosen_review = chosen_handle.read()

    mo.vstack([
      mo.md(f'**average VADER compound score:** {vader_sentence_average(chosen_review)}'),
      mo.md(chosen_review),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - On average, are satirical reviews more or less positive than normal reviews? Is the difference big enough to tell them apart?
    - Look at the histogram. How much do the two distributions overlap? If you had to guess "satire" or "normal" from the score alone, how often would you be right?
    - What *do* you use as a human reader to spot the satire? Could a computer use any of those clues?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - on average, satirical reviews are less positive than normal reviews with the same star rating, especially for 4 and 5 star reviews: the satire often describes absurd or terrible experiences while pretending to be happy
    - but the distributions overlap a lot, so sentiment on its own would make a lot of mistakes; it might be *one* useful feature among many for a classifier (which is what we will try in the classification in-class notebook)
    - human readers use things like exaggeration, absurd situations, mismatches between the star rating and the content, and knowledge of the world (nobody really needs a banana slicer that badly), most of which are hard to capture with word-level features
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: emotion profiles**

    Choose two texts to compare their emotion profiles (using the NRC lexicon) and their average valence, arousal, and dominance (using the VAD lexicon). If you choose "your own text", type or paste it into the box below the dropdowns.
    """)
    return


@app.cell
def _(requests, resources, reviews_folder):
    emotion_texts = {
      'Mood Ring (Lorde)': requests.get(resources + 'mood_ring.txt').text,
      'The Marine Biologist (Seinfeld)': requests.get(resources + 'marine_biologist.txt').text,
      'banana slicer review (satire)': open(reviews_folder + '/001-5-satire.txt', encoding = 'utf-8').read(),
      'banana slicer review (normal)': open(reviews_folder + '/001-5-normal.txt', encoding = 'utf-8').read(),
    }
    return (emotion_texts,)


@app.cell
def _(emotion_texts, mo):
    emotion_choice_a = mo.ui.dropdown(options = list(emotion_texts.keys()) + ['your own text'], value = 'Mood Ring (Lorde)', label = 'text A:')
    emotion_choice_b = mo.ui.dropdown(options = list(emotion_texts.keys()) + ['your own text'], value = 'The Marine Biologist (Seinfeld)', label = 'text B:')
    own_text = mo.ui.text_area(value = 'I was so excited for the trip, but then the flight was cancelled and I was furious.', label = 'your own text:', full_width = True)
    mo.vstack([mo.hstack([emotion_choice_a, emotion_choice_b], justify = 'start'), own_text])
    return emotion_choice_a, emotion_choice_b, own_text


@app.cell
def _(
    emotion_choice_a,
    emotion_choice_b,
    emotion_texts,
    nrc_emotion_dict,
    own_text,
    plt,
    profile_emotions,
):
    def chosen_text(choice):
      # get the text for a dropdown choice
      if choice == 'your own text':
        return own_text.value
      return emotion_texts[choice]

    text_a = chosen_text(emotion_choice_a.value)
    text_b = chosen_text(emotion_choice_b.value)

    profile_a = profile_emotions(text_a, nrc_emotion_dict)
    profile_b = profile_emotions(text_b, nrc_emotion_dict)
    emotion_names = list(profile_a.keys())

    # the two profiles side by side, as a bar chart
    positions = range(len(emotion_names))
    fig2, ax2 = plt.subplots(figsize = (10, 4))
    ax2.bar([position - 0.2 for position in positions], [profile_a[emotion] for emotion in emotion_names], width = 0.4, label = emotion_choice_a.value)
    ax2.bar([position + 0.2 for position in positions], [profile_b[emotion] for emotion in emotion_names], width = 0.4, label = emotion_choice_b.value)
    ax2.set_xticks(positions, emotion_names, rotation = 45, ha = 'right')
    ax2.set_ylabel('proportion of tokens')
    ax2.legend()
    fig2
    return text_a, text_b


@app.cell
def _(
    clean_tokens,
    emotion_choice_a,
    emotion_choice_b,
    pl,
    text_a,
    text_b,
    vad_dict,
):
    # average VAD scores and coverage for each text
    vad_rows = []
    for vad_name, vad_text in [(emotion_choice_a.value, text_a), (emotion_choice_b.value, text_b)]:
      vad_tokens = clean_tokens(vad_text)
      vad_found = [vad_dict[token] for token in vad_tokens if token in vad_dict]
      if len(vad_found) == 0:
        vad_rows.append({'text': vad_name, 'valence': None, 'arousal': None, 'dominance': None, 'coverage': 0})
      else:
        vad_rows.append({
          'text': vad_name,
          'valence': round(sum([scores['valence'] for scores in vad_found]) / len(vad_found), 2),
          'arousal': round(sum([scores['arousal'] for scores in vad_found]) / len(vad_found), 2),
          'dominance': round(sum([scores['dominance'] for scores in vad_found]) / len(vad_found), 2),
          'coverage': round(len(vad_found) / len(vad_tokens), 2),
        })

    pl.DataFrame(vad_rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which words are counting towards each emotion? Choose an emotion to see the most frequent words in each text which are associated with it:
    """)
    return


@app.cell
def _(mo, nrc_emotion_dict):
    emotion_word_choice = mo.ui.dropdown(options = sorted(nrc_emotion_dict.keys()), value = 'fear', label = 'emotion:')
    emotion_word_choice
    return (emotion_word_choice,)


@app.cell
def _(
    FreqDist,
    clean_tokens,
    emotion_choice_a,
    emotion_choice_b,
    emotion_word_choice,
    mo,
    nrc_emotion_dict,
    text_a,
    text_b,
):
    words_a = FreqDist([token for token in clean_tokens(text_a) if token in nrc_emotion_dict[emotion_word_choice.value]]).most_common(15)
    words_b = FreqDist([token for token in clean_tokens(text_b) if token in nrc_emotion_dict[emotion_word_choice.value]]).most_common(15)

    mo.hstack([
      mo.vstack([mo.md(f'**{emotion_choice_a.value}**'), words_a]),
      mo.vstack([mo.md(f'**{emotion_choice_b.value}**'), words_b]),
    ], justify = 'start', gap = 4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which text has the stronger emotion profile? Does that match what you know about the texts?
    - Look at the words counting towards an emotion like `fear` or `anger`. Do they really express that emotion *in these texts*?
    - Try your own text with mixed emotions. Does the profile capture the *change* in feeling (e.g., excited, then furious)?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - the NRC lexicon records whether a word is *associated* with an emotion, not whether the text expresses it: words like *shot* or *bad* count towards fear or anger even in a joke or a positive context
    - the profiles are proportions of *all* tokens, and coverage is low, so differences between texts are often small and based on a handful of words
    - a profile is a summary of the whole text, so it loses the order of emotions: "excited then furious" and "furious then excited" get the same profile
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. AFINN was rated by one person, and VADER's ratings came from a small group of raters in the USA. Whose sense of "positive" and "negative" do these lexicons represent?
    2. Sentiment depends on context, culture, and the speaker. What happens to sarcasm, slang, and New Zealand understatement in a sentiment analysis?
    3. Companies and governments use sentiment analysis to monitor reviews, social media, and public opinion. What could go wrong if the scores are taken at face value?
    4. What is the difference between a word that is *associated* with an emotion and a person who actually *feels* that emotion?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - every lexicon reflects the judgements of the people who made it; other people (from other cultures, age groups, or varieties of English) might rate the same words differently
    - sarcasm, slang, and understatement all depend on shared knowledge between the speaker and listener, which word-level methods don't have; varieties of English that are not well represented in the lexicons will be misread more often
    - scores can be wrong in systematic ways (e.g., sarcastic complaints counted as praise, slang counted as negative), so decisions based on them can be biased against particular groups or styles of writing; it's important to check the actual texts behind the numbers
    - emotion lexicons capture associations between words and emotions in general, but a text can mention fear without being fearful, and a person can feel an emotion without using any of the "right" words
    ''')})
    return


if __name__ == "__main__":
    app.run()
