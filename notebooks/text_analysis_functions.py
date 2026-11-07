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
    # **Text analysis functions**

    This notebook collects the most useful functions from the course notebooks, in their final form, so that you can use them for your own text analysis. They are organised in the same order as the course.

    **How to use this notebook**

    - Run the first code cell (the imports)
    - Each function has a short description of what goes in and what comes out. Underneath each function is a short example.
    - To use a function in your own notebook, copy the function's cell (and the imports it needs) into your notebook.
    - If you are not sure how a function works, go back to the course notebook it came from (named in each section).
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import io
    import os
    import math
    import zipfile
    import random
    import requests
    import polars as pl
    import nltk
    from glob import glob
    from nltk import FreqDist
    from collections import defaultdict
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from nltk.corpus import cmudict

    nltk.download(['punkt_tab', 'averaged_perceptron_tagger_eng', 'universal_tagset', 'vader_lexicon', 'cmudict'])

    # the course repository, where the texts and lexicons are stored
    resources = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/'
    return (
        FreqDist,
        SentimentIntensityAnalyzer,
        cmudict,
        defaultdict,
        glob,
        io,
        math,
        nltk,
        os,
        pl,
        random,
        requests,
        resources,
        zipfile,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **1. Loading texts**

    *From the writing functions, corpora, and tf-idf notebooks.*
    """)
    return


@app.cell
def _(requests):
    def load_text(url):
      '''
      Download a text file from a URL.
      In: a URL (string). Out: the text (string).
      '''
      return requests.get(url).text

    return (load_text,)


@app.cell
def _(load_text, resources):
    example_text = load_text(resources + 'marine_biologist.txt')
    example_text[:200]
    return (example_text,)


@app.cell
def _(io, requests, zipfile):
    def download_corpus(url, folder):
      '''
      Download a zip file of texts and unzip it into a folder (in the folder that contains this notebook).
      In: a URL to a zip file (string), and a folder name (string). Out: the folder name (string).
      '''
      response = requests.get(url)
      zip_file = zipfile.ZipFile(io.BytesIO(response.content))
      zip_file.extractall(folder)
      return folder

    return (download_corpus,)


@app.cell
def _(glob, os):
    def load_folder(folder):
      '''
      Read every .txt file in a folder.
      In: a folder name (string). Out: a dictionary of {file name: text}.
      '''
      texts = {}
      for filename in sorted(glob(folder + '/*.txt')):
        with open(filename, encoding = 'utf-8') as f:
          texts[os.path.basename(filename)] = f.read()
      return texts

    return (load_folder,)


@app.cell
def _(download_corpus, load_folder, resources):
    seinfeld_texts = load_folder(download_corpus(resources + 'seinfeld.zip', 'seinfeld'))
    list(seinfeld_texts.keys())[:5]
    return (seinfeld_texts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **2. Preprocessing and tokenisation**

    *From the tokenisation and preprocessing, and collocations notebooks.*
    """)
    return


@app.function
def pre_process(text, lower = True, remove_punc = True):
  '''
  Lowercase a text and/or remove punctuation.
  In: a text (string). Out: the cleaned text (string).
  '''
  if lower == True:
    text = text.lower()
  if remove_punc == True:
    punctuation = '.;"!\'[]{}:><-_?,'
    text = ''.join([char for char in text if char not in punctuation])
  return text


@app.cell
def _(nltk):
    def clean_tokens(text):
      '''
      Lowercase and tokenise a text, keeping only alphabetic tokens (no punctuation or numbers).
      In: a text (string). Out: a list of tokens.
      '''
      return [token for token in nltk.word_tokenize(text.lower()) if token.isalpha()]

    return (clean_tokens,)


@app.cell
def _(clean_tokens):
    print(pre_process('These pretzels are making me thirsty!'))
    print(clean_tokens('These pretzels are making me thirsty!'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **3. Types, tokens, and lexical diversity**

    *From the types, tokens, and TTR notebook.*
    """)
    return


@app.function
def ttr(tokens):
  '''
  Type-token ratio: the number of types divided by the number of tokens.
  In: a list of tokens. Out: the TTR (number between 0 and 1).
  Remember that TTR goes down as texts get longer, so only compare texts of the same length!
  '''
  if len(tokens) == 0:
    return None
  return len(set(tokens)) / len(tokens)


@app.function
def average_ttr(tokens, window = 100):
  '''
  The average TTR of every chunk of `window` tokens, which can be compared across texts of different lengths.
  In: a list of tokens, and the chunk size. Out: the average TTR.
  '''
  ttrs = []
  for start in range(0, len(tokens) - window + 1, window):
    ttrs.append(ttr(tokens[start:start + window]))
  if len(ttrs) == 0:
    return None
  return sum(ttrs) / len(ttrs)


@app.cell
def _(clean_tokens, example_text):
    example_tokens = clean_tokens(example_text)
    print('TTR:', ttr(example_tokens))
    print('average TTR (100 token chunks):', average_ttr(example_tokens))
    return (example_tokens,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **4. Frequency**

    *From the frequency notebook.*
    """)
    return


@app.function
def per_million(count, total):
  '''
  Normalise a frequency count to a count per million words, so that texts of different lengths can be compared.
  In: a count, and the total number of tokens. Out: the frequency per million words.
  '''
  return count / total * 1000000


@app.cell
def _(FreqDist, pl):
    def frequency_table(tokens, n = 20):
      '''
      The n most frequent words, with their raw and normalised (per million) frequencies.
      In: a list of tokens. Out: a polars dataframe.
      '''
      fdist = FreqDist(tokens)
      top = fdist.most_common(n)
      return pl.DataFrame({
        'word': [word for (word, count) in top],
        'frequency': [count for (word, count) in top],
        'per million': [round(per_million(count, len(tokens)), 1) for (word, count) in top],
      })

    return (frequency_table,)


@app.cell
def _(example_tokens, frequency_table):
    frequency_table(example_tokens, 10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **5. Parts of speech**

    *From the parts of speech notebook.*
    """)
    return


@app.cell
def _(FreqDist, nltk, pl):
    def pos_profile(text):
      '''
      The percentage of words with each part of speech (using the universal tagset), leaving out punctuation.
      In: a text (string). Out: a polars dataframe.
      '''
      tagged = nltk.pos_tag(nltk.word_tokenize(text), tagset = 'universal')
      tags = FreqDist([tag for (word, tag) in tagged if tag != '.'])
      return pl.DataFrame({
        'tag': [tag for (tag, count) in tags.most_common()],
        'percent': [round(count / tags.N() * 100, 1) for (tag, count) in tags.most_common()],
      })

    return (pos_profile,)


@app.cell
def _(nltk):
    def lexical_density(text):
      '''
      The proportion of words which are content words (nouns, verbs, adjectives, adverbs), leaving out punctuation.
      In: a text (string). Out: the lexical density (number between 0 and 1).
      '''
      tagged = nltk.pos_tag(nltk.word_tokenize(text), tagset = 'universal')
      words = [tag for (word, tag) in tagged if tag != '.']
      if len(words) == 0:
        return None
      content = [tag for tag in words if tag in ['NOUN', 'VERB', 'ADJ', 'ADV']]
      return len(content) / len(words)

    return (lexical_density,)


@app.cell
def _(example_text, lexical_density, pos_profile):
    print('lexical density:', lexical_density(example_text))
    pos_profile(example_text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **6. Collocations**

    *From the collocations notebook.*
    """)
    return


@app.cell
def _(FreqDist, math, nltk, pl):
    def collocation_table(tokens, min_frequency = 5):
      '''
      Every bigram which occurs at least min_frequency times, with its frequency, PMI, and Delta P (forward and backward).
      In: a list of tokens. Out: a polars dataframe (click on a column name to sort it).
      '''
      word_fdist = FreqDist(tokens)
      bigrams = list(nltk.bigrams(tokens))
      bigram_fdist = FreqDist(bigrams)
      total = len(bigrams)

      rows = []
      for (w1, w2), pair_count in bigram_fdist.items():
        if pair_count >= min_frequency:
          pmi = math.log2((pair_count / total) / ((word_fdist[w1] / len(tokens)) * (word_fdist[w2] / len(tokens))))
          forward = pair_count / word_fdist[w1] - (word_fdist[w2] - pair_count) / (total - word_fdist[w1])
          backward = pair_count / word_fdist[w2] - (word_fdist[w1] - pair_count) / (total - word_fdist[w2])
          rows.append({'bigram': w1 + ' ' + w2, 'frequency': pair_count, 'PMI': round(pmi, 2), 'Delta P forward': round(forward, 3), 'Delta P backward': round(backward, 3)})

      return pl.DataFrame(rows).sort('PMI', descending = True)

    return (collocation_table,)


@app.cell
def _(collocation_table, example_tokens):
    collocation_table(example_tokens, min_frequency = 3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **7. Comparing documents: tf-idf**

    *From the tf-idf notebook.*
    """)
    return


@app.cell
def _(FreqDist, clean_tokens, math):
    def tf_idf_top_words(documents, n = 10):
      '''
      The words with the highest tf-idf scores in each document.
      In: a dictionary of {document name: text}. Out: a dictionary of {document name: list of top words}.
      '''
      document_tokens = {}
      for name in documents:
        document_tokens[name] = clean_tokens(documents[name])

      # document frequency: how many documents does each word appear in?
      document_frequency = FreqDist()
      for tokens in document_tokens.values():
        for word in set(tokens):
          document_frequency[word] += 1

      top_words = {}
      for name, tokens in document_tokens.items():
        counts = FreqDist(tokens)
        scores = {}
        for word in counts:
          scores[word] = counts[word] / len(tokens) * math.log(len(document_tokens) / document_frequency[word])
        top_words[name] = [word for (word, score) in FreqDist(scores).most_common(n)]
      return top_words

    return (tf_idf_top_words,)


@app.cell
def _(seinfeld_texts, tf_idf_top_words):
    seinfeld_top = tf_idf_top_words(seinfeld_texts, 8)
    seinfeld_top['THE JUNIOR MINT_cleaned.txt']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **8. Lexicons: lexical sophistication and readability**

    *From the lexical sophistication and readability notebooks.*
    """)
    return


@app.cell
def _(requests):
    def get_word_rating_resource(url):
      '''
      Load a lexicon which has one word and one rating on each line, separated by a tab.
      In: a URL (string). Out: a dictionary of {word: rating}.
      Lexicons in the course repository: subtlxus_frequency.txt, AoA_Brysbart.txt, concreteness.txt, semantic_diversity.txt, AFINN-111.txt
      '''
      ratings = {}
      for line in requests.get(url).text.split('\n'):
        pair = line.split('\t')
        if len(pair) == 2:
          ratings[pair[0]] = float(pair[1])
      return ratings

    return (get_word_rating_resource,)


@app.cell
def _(clean_tokens):
    def lexicon_profile(text, lexicon):
      '''
      The average rating of the words in a text, the coverage of the lexicon, and the words which were not in the lexicon.
      In: a text (string), and a lexicon (dictionary). Out: (average, coverage, list of missing words).
      The average is None if no words were in the lexicon.
      '''
      tokens = clean_tokens(text)
      ratings = []
      missing = []
      for token in tokens:
        if token in lexicon:
          ratings.append(lexicon[token])
        else:
          missing.append(token)
      if len(ratings) == 0:
        return None, 0, missing
      return sum(ratings) / len(ratings), len(ratings) / len(tokens), missing

    return (lexicon_profile,)


@app.cell
def _(example_text, get_word_rating_resource, lexicon_profile, resources):
    aoa_lexicon = get_word_rating_resource(resources + 'AoA_Brysbart.txt')

    aoa_average, aoa_coverage, aoa_missing = lexicon_profile(example_text, aoa_lexicon)
    print('average age of acquisition:', aoa_average)
    print('coverage:', aoa_coverage)
    return


@app.cell
def _(cmudict):
    cmu = cmudict.dict()

    def count_syllables(word):
      '''
      Count the syllables in a word, using the CMU dictionary, or counting groups of vowels if the word is not in it.
      In: a word (string). Out: the number of syllables.
      '''
      if word in cmu:
        return len([sound for sound in cmu[word][0] if sound[-1].isdigit()])
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

    return (count_syllables,)


@app.cell
def _(clean_tokens, count_syllables, nltk):
    def readability(text):
      '''
      Flesch Reading Ease (higher = easier), Flesch-Kincaid Grade Level, and Gunning Fog (both higher = harder).
      In: a text (string). Out: (reading ease, grade level, fog).
      '''
      tokens = clean_tokens(text)
      sentences = nltk.sent_tokenize(text)
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

      reading_ease = 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)
      grade_level = (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59
      fog = 0.4 * (words_per_sentence + 100 * (complex_words / len(tokens)))
      return reading_ease, grade_level, fog

    return (readability,)


@app.cell
def _(readability):
    readability('The cat sat on the mat. It was a warm day, and the cat was very happy to be in the sun.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **9. Sentiment and emotion**

    *From the sentiment and emotion lexicons notebooks. For AFINN sentiment, use `get_word_rating_resource()` and `lexicon_profile()` from section 8.*
    """)
    return


@app.cell
def _(SentimentIntensityAnalyzer, nltk):
    vader = SentimentIntensityAnalyzer()

    def vader_score(text):
      '''
      The VADER compound score (from -1 to 1). Best for short texts, such as a sentence or a post.
      In: a text (string). Out: the compound score.
      '''
      return vader.polarity_scores(text)['compound']

    def vader_sentence_average(text):
      '''
      The average VADER compound score of the sentences in a text. Better than vader_score() for long texts.
      In: a text (string). Out: the average compound score.
      '''
      sentence_scores = [vader_score(sentence) for sentence in nltk.sent_tokenize(text)]
      if len(sentence_scores) == 0:
        return None
      return sum(sentence_scores) / len(sentence_scores)

    return vader_score, vader_sentence_average


@app.cell
def _(example_text, vader_score, vader_sentence_average):
    print(vader_score('I am not happy'))
    print(vader_sentence_average(example_text))
    return


@app.cell
def _(clean_tokens, defaultdict, pl, requests, resources):
    def load_nrc_emotions():
      '''
      Load the NRC emotion lexicon from the course repository.
      Out: a dictionary of {emotion: set of words}.
      '''
      emotions = defaultdict(set)
      for line in requests.get(resources + 'emotion_lexicon.txt').text.split('\n'):
        parts = line.split('\t')
        if len(parts) == 3 and parts[2].strip() == '1':
          emotions[parts[1]].add(parts[0])
      return emotions

    def emotion_profile(text, emotions):
      '''
      The proportion of tokens in a text which are associated with each emotion.
      In: a text (string), and the NRC lexicon from load_nrc_emotions(). Out: a polars dataframe.
      '''
      tokens = clean_tokens(text)
      if len(tokens) == 0:
        return None
      return pl.DataFrame({
        'emotion': sorted(emotions),
        'proportion': [round(len([token for token in tokens if token in emotions[emotion]]) / len(tokens), 3) for emotion in sorted(emotions)],
      })

    return emotion_profile, load_nrc_emotions


@app.cell
def _(emotion_profile, example_text, load_nrc_emotions):
    nrc_emotions = load_nrc_emotions()
    emotion_profile(example_text, nrc_emotions)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **10. Language models**

    *From the word probabilities and generating text notebooks.*
    """)
    return


@app.cell
def _(FreqDist, defaultdict, nltk):
    def next_word_model(tokens):
      '''
      For every word, count the words which come after it.
      In: a list of tokens. Out: a dictionary of {word: FreqDist of next words}.
      '''
      next_words = defaultdict(FreqDist)
      for (w1, w2) in nltk.bigrams(tokens):
        next_words[w1][w2] += 1
      return next_words

    return (next_word_model,)


@app.cell
def _(clean_tokens, nltk):
    def phrase_probability(model, phrase):
      '''
      The chained bigram probability of a phrase.
      In: a model from next_word_model(), and a phrase (string). Out: the probability (0 if any bigram is unseen).
      '''
      probability = 1
      for (w1, w2) in nltk.bigrams(clean_tokens(phrase)):
        if model[w1].N() == 0:
          return 0
        probability = probability * (model[w1][w2] / model[w1].N())
      return probability

    return (phrase_probability,)


@app.cell
def _(random):
    def generate_text(model, word, num = 20):
      '''
      Generate text by choosing each next word in proportion to how often it followed the current word.
      In: a model from next_word_model(), a seed word, and the number of words. Out: the generated text (string).
      '''
      output = []
      for i in range(num):
        output.append(word)
        if model[word].N() == 0:
          break
        word = random.choices(list(model[word].keys()), weights = list(model[word].values()))[0]
      return ' '.join(output)

    return (generate_text,)


@app.cell
def _(
    clean_tokens,
    generate_text,
    next_word_model,
    phrase_probability,
    seinfeld_texts,
):
    seinfeld_model = next_word_model(clean_tokens(' '.join(seinfeld_texts.values())))

    print(phrase_probability(seinfeld_model, 'what are you doing'))
    print(generate_text(seinfeld_model, 'jerry'))
    return


if __name__ == "__main__":
    app.run()
