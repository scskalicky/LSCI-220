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
    #### Other tutorials on this topic

    [scikit-learn: tf-idf term weighting](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **tf-idf: finding distinctive words**

    Counting words can tell us a lot, but you have probably noticed by now that the most frequent words in almost any English text are the same: *the*, *I*, *you*, *to*, *a*, and so on. These words are frequent everywhere, so they don't tell us very much about what makes one text different from another.

    What if we wanted to find the words that are *characteristic* of a particular text? For example, which words make one Seinfeld episode different from all of the other Seinfeld episodes? A word that is frequent in one episode but rare in the others is probably telling us something about that episode.

    This is the idea behind **tf-idf**, which stands for **term frequency - inverse document frequency**. tf-idf gives each word in a document a score which goes up when the word is frequent in that document, and goes down when the word appears in lots of other documents too. In this notebook we will calculate tf-idf by hand, and then see how to do the same thing using a library called `scikit-learn`.
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
    from nltk.text import Text
    from nltk.corpus import gutenberg
    from sklearn.feature_extraction.text import TfidfVectorizer

    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'gutenberg'])
    return (
        FreqDist,
        Text,
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
    # **Getting the data**

    We will use the Seinfeld scripts again, using the same `download_corpus()` function from the corpora notebook. Each episode is its own file, which means each episode can be treated as its own *document*.
    """)
    return


@app.cell
def _(io, requests, zipfile):
    def download_corpus(url, folder):
      # download the zip file
      response = requests.get(url)

      # open the downloaded data as a zip file
      zip_file = zipfile.ZipFile(io.BytesIO(response.content))

      # unzip everything into the folder
      zip_file.extractall(folder)

      # give back the name of the folder, so we can use it later
      return folder

    # download and unzip the Seinfeld scripts into a folder called 'seinfeld'
    seinfeld_folder = download_corpus('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/seinfeld.zip', 'seinfeld')
    return (seinfeld_folder,)


@app.cell
def _(glob, seinfeld_folder):
    # glob to grab the filenames (sorted so they are in alphabetical order)
    filenames = sorted(glob(seinfeld_folder + '/*.txt'))

    filenames
    return (filenames,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's normalise the text a bit by lowercasing and removing punctuation, using the same `pre_process()` function from the collocations notebook:
    """)
    return


@app.function
def pre_process(x, lower = True, remove_punc = True):

  if lower == True:
    # x will not be lowercase unless lower == True (the default)
    x = x.lower()

  if remove_punc == True:
    # this variable won't be declared unless remove_punc == True (the default)
    punctuation = '.;"!\'[]{}:><-_?,'
    # this join and list comprehension won't trigger unless remove_punc == True
    x = ''.join([char for char in x if char not in punctuation])
  return x


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can loop through the files and store the tokens of each episode in a dictionary. The keys will be the episode names, and the values will be the list of tokens for that episode.

    I use `os.path.basename()` to get just the name of the file without the folder, and then use `.replace()` to remove the `_cleaned.txt` at the end of each filename.
    """)
    return


@app.cell
def _(filenames, nltk, os):
    # create an empty dictionary to store the tokens of each episode
    episode_tokens = {}

    for episode_file in filenames:
      # turn 'seinfeld/THE JUNIOR MINT_cleaned.txt' into 'the junior mint'
      episode_name = os.path.basename(episode_file).replace('_cleaned.txt', '').lower()

      # read the file, clean it, and tokenise it
      with open(episode_file, encoding = 'utf-8') as f:
        episode_text = f.read()
      episode_tokens[episode_name] = nltk.word_tokenize(pre_process(episode_text))

    # what are the keys of our dictionary?
    list(episode_tokens)
    return (episode_tokens,)


@app.cell
def _(episode_tokens):
    # how many episodes (i.e., documents) do we have?
    number_of_episodes = len(episode_tokens)
    number_of_episodes
    return (number_of_episodes,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **The problem with raw frequency**

    Let's look at the most frequent words in a few episodes. What do you notice?
    """)
    return


@app.cell
def _(FreqDist, episode_tokens):
    FreqDist(episode_tokens['the junior mint']).most_common(10)
    return


@app.cell
def _(FreqDist, episode_tokens):
    FreqDist(episode_tokens['the pez dispenser']).most_common(10)
    return


@app.cell
def _(FreqDist, episode_tokens):
    FreqDist(episode_tokens['the marine biologist']).most_common(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The lists are quite similar! Function words like *you*, *I*, and *the* are at the top, along with *jerry*, *george*, and *elaine*, which are frequent because the characters' names are used as speaker labels in the scripts. If we only looked at these lists, we would have no idea that one episode involves a junior mint, one involves a pez dispenser, and one involves a whale rescue.

    So we need a way to push down the words that are frequent *everywhere*, and push up the words that are frequent in *this* episode but not in the others. tf-idf does this in two parts:

    - **term frequency (tf)**: how frequent is the word in this document?
    - **inverse document frequency (idf)**: how many documents does the word appear in? The *fewer* documents, the *higher* the idf.

    Then we multiply them together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Term frequency (tf)**

    Term frequency is the easy part. It is the number of times a word appears in a document. Because the episodes are not all the same length, we will normalise the count by dividing by the number of tokens in the episode (just like we did when normalising frequencies in the frequency notebook).
    """)
    return


@app.function
def tf(word, tokens):
  # count the word and divide by the total number of tokens
  return tokens.count(word) / len(tokens)


@app.cell
def _(episode_tokens):
    # what proportion of the junior mint is the word 'the'?
    tf('the', episode_tokens['the junior mint'])
    return


@app.cell
def _(episode_tokens):
    # what about 'mint'?
    tf('mint', episode_tokens['the junior mint'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Document frequency and inverse document frequency (idf)**

    Now we need to know how many documents each word appears in. This is called **document frequency**. Note that we don't care how many times the word appears in each episode, only *whether* it appears in an episode at all.

    A nice way to do this is to loop through each episode, turn its tokens into a `set()` (which removes duplicates, so each word only appears once), and then count each word in the set. I use a `FreqDist` to do the counting, since it works like a dictionary that starts every word at zero.

    In the loop, `document_frequency[word] += 1` adds 1 to the count for that word. `x += 1` is just a shorter way of writing `x = x + 1`.
    """)
    return


@app.cell
def _(FreqDist, episode_tokens):
    # count how many episodes each word appears in
    document_frequency = FreqDist()

    for tokens in episode_tokens.values():
      # set() keeps only one copy of each word
      for word in set(tokens):
        document_frequency[word] += 1
    return (document_frequency,)


@app.cell
def _(document_frequency):
    # 'the' should appear in every episode
    document_frequency['the']
    return


@app.cell
def _(document_frequency):
    # what about 'mint'?
    document_frequency['mint']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The **inverse** document frequency flips this around, so that words which appear in *fewer* documents get a *higher* score. The formula is:

    $$
    \text{idf}(word) = \log\left(\frac{\text{number of documents}}{\text{number of documents containing } word}\right)
    $$

    Why the log? The log squashes the scores so that the difference between appearing in 1 or 2 documents matters more than the difference between appearing in 12 or 13 documents. Just like in the frequency notebook, `math.log()` uses the natural logarithm.

    Think about what happens to a word which appears in *every* document: the fraction becomes $14 / 14 = 1$, and the log of 1 is 0. So words found in every episode will get an idf of 0!
    """)
    return


@app.cell
def _(document_frequency, math, number_of_episodes):
    def idf(word):
      return math.log(number_of_episodes / document_frequency[word])

    return (idf,)


@app.cell
def _(idf):
    # appears in every episode
    idf('the')
    return


@app.cell
def _(idf):
    # appears in only one episode
    idf('mint')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Putting it together: tf-idf**

    The tf-idf score of a word in a document is simply its tf multiplied by its idf:

    $$
    \text{tf-idf}(word, document) = \text{tf}(word, document) \times \text{idf}(word)
    $$

    Let's make a function for this.
    """)
    return


@app.cell
def _(idf):
    def tf_idf(word, tokens):
      return tf(word, tokens) * idf(word)

    return (tf_idf,)


@app.cell
def _(episode_tokens, tf_idf):
    # compare 'the' and 'mint' in the junior mint
    print(tf_idf('the', episode_tokens['the junior mint']))
    print(tf_idf('mint', episode_tokens['the junior mint']))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Even though **the** is much more frequent than **mint** in this episode, its tf-idf score is 0, because it appears in every episode. In contrast, the score for **mint** is 0.008, which is small yet still higher than the score for **the**. Relative differences among words in a corpus is what we are after.

    Now let's calculate the tf-idf score for *every* word in an episode. I loop over the `set()` of the tokens so that we only calculate each word once, and store the `word: score` pairs in a dictionary. Then I put the dictionary into a `FreqDist` so that we can use `.most_common()` to get the highest scores.
    """)
    return


@app.cell
def _(FreqDist, tf_idf):
    def top_tf_idf(tokens, n = 10):
      # calculate tf-idf for each unique word in the document
      scores = {}
      for word in set(tokens):
        scores[word] = tf_idf(word, tokens)
      # FreqDist gives us .most_common() for free
      return FreqDist(scores).most_common(n)

    return (top_tf_idf,)


@app.cell
def _(episode_tokens, top_tf_idf):
    top_tf_idf(episode_tokens['the junior mint'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That looks much better! Now we have words like *mint*, *operation*, *doctor*, and *roy*, which are specific to this episode. Let's put the raw frequency and tf-idf results side by side for a few episodes, using a polars dataframe:
    """)
    return


@app.cell
def _(FreqDist, episode_tokens, pl, top_tf_idf):
    def compare_top_words(episode, n = 10):
      tokens = episode_tokens[episode]
      return pl.DataFrame({
        'raw frequency': [word for (word, count) in FreqDist(tokens).most_common(n)],
        'tf-idf': [word for (word, score) in top_tf_idf(tokens, n)]
      })

    return (compare_top_words,)


@app.cell
def _(compare_top_words):
    compare_top_words('the pez dispenser')
    return


@app.cell
def _(compare_top_words):
    compare_top_words('the marine biologist')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Do you see the difference? In the raw frequency column we see the words that are simply frequent in this episode (and probably in every other episode too). In the tf-idf column, we see the words that are frequent in this episode when compared with all the other episodes in the corpus.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Using concordance lines to check the numbers**

    tf-idf can tell us that a word is distinctive in a document, but not *why*. Some of the words at the top of the tf-idf lists are names of characters who only appear in one episode, others are words related to the plot, and others might be there for reasons that are less obvious. This is where concordance lines from the concordances notebook come in handy, since they let us go back to the text and check.

    For example, why is *roy* so distinctive in the junior mint?
    """)
    return


@app.cell
def _(Text, episode_tokens):
    # make an NLTK Text so we can use .concordance()
    junior_mint_text = Text(episode_tokens['the junior mint'])

    junior_mint_text.concordance('roy')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And why is marine important in marine biologist?
    """)
    return


@app.cell
def _(Text, episode_tokens):
    # make an NLTK Text so we can use .concordance()
    marine_biologist_text = Text(episode_tokens['the marine biologist'])

    marine_biologist_text.concordance('marine')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    - Use `compare_top_words()` on a few other episodes. Can you guess what the episode is about from the tf-idf words alone?
    - Pick a word from one of the tf-idf lists that you're not sure about, and look at its concordance lines. Why is it distinctive?
    - What *kinds* of words tend to get the highest tf-idf scores? Is that what you would want if you were trying to figure out what an episode is about?
    """)
    return


@app.cell
def _():
    # use this code cell to explore tf-idf in the other episodes!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Comparing two episodes**

    Use the dropdowns below to compare the tf-idf words of any two episodes.
    """)
    return


@app.cell
def _(episode_tokens, mo):
    episode_choice1 = mo.ui.dropdown(options = list(episode_tokens), value = 'the junior mint', label = 'first episode')
    episode_choice2 = mo.ui.dropdown(options = list(episode_tokens), value = 'the parking garage', label = 'second episode')

    mo.hstack([episode_choice1, episode_choice2])
    return episode_choice1, episode_choice2


@app.cell
def _(episode_choice1, episode_choice2, episode_tokens, pl, top_tf_idf):
    pl.DataFrame({
      episode_choice1.value: [word for (word, score) in top_tf_idf(episode_tokens[episode_choice1.value], 15)],
      episode_choice2.value: [word for (word, score) in top_tf_idf(episode_tokens[episode_choice2.value], 15)]
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **tf-idf with scikit-learn**

    Calculating tf-idf by hand is a great way to understand what it is doing, but in practice people normally use a library. [scikit-learn](https://scikit-learn.org/) is a popular Python library for machine learning and NLP, and it has a function called `TfidfVectorizer()` that does all of the above in one go.

    `TfidfVectorizer()` expects a list of *strings*, one string per document. So let's join our tokens back together into one string for each episode:
    """)
    return


@app.cell
def _(episode_tokens):
    # the episode names, in the same order as the documents
    episode_names = list(episode_tokens)

    # one string per episode
    episode_documents = [' '.join(episode_tokens[episode]) for episode in episode_names]
    return episode_documents, episode_names


@app.cell
def _(episode_documents):
    # just a string now
    episode_documents[0][:85]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we create the vectorizer and use `.fit_transform()` on our documents. This does the counting and the calculating in one step.
    """)
    return


@app.cell
def _(TfidfVectorizer, episode_documents):
    # create the object to do the word
    seinfeld_vectorizer = TfidfVectorizer()

    # create a new thing from the worker
    seinfeld_tfidf = seinfeld_vectorizer.fit_transform(episode_documents)

    # rows are episodes, columns are words
    seinfeld_tfidf.shape
    return seinfeld_tfidf, seinfeld_vectorizer


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The result is a big table (a *matrix*) where each row is an episode and each column is a word. Each cell in the table is the tf-idf score of that word in that episode. We can get the words for each column using `.get_feature_names_out()`:
    """)
    return


@app.cell
def _(seinfeld_vectorizer):
    seinfeld_words = seinfeld_vectorizer.get_feature_names_out()

    # look at a few of the words (the columns)
    seinfeld_words[1000:1010]
    return (seinfeld_words,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To get the top words for an episode, we grab the row for that episode, `zip()` the words together with the scores, and put them into a `FreqDist` like before. The `.toarray()` is needed to turn the row into a normal list of numbers.
    """)
    return


@app.cell
def _(FreqDist):
    def top_sklearn(matrix, words, row_number, n = 10):
      # get the scores for one row (i.e., one document)
      scores = matrix[row_number].toarray()[0]
      # pair each word with its score
      return FreqDist(dict(zip(words, scores))).most_common(n)

    return (top_sklearn,)


@app.cell
def _(episode_names, seinfeld_tfidf, seinfeld_words, top_sklearn):
    # which row is the junior mint?
    # (.index() gives the position of an item in a list)
    junior_mint_row = episode_names.index('the junior mint')

    top_sklearn(seinfeld_tfidf, seinfeld_words, junior_mint_row)
    return (junior_mint_row,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Wait, what? *jerry*, *you*, and *the* are back at the top! This is because scikit-learn calculates idf a little bit differently from us:

    $$
    \text{idf}(word) = \log\left(\frac{1 + \text{number of documents}}{1 + \text{number of documents containing } word}\right) + 1
    $$

    The `+ 1` at the end means that words which appear in every document get an idf of 1 instead of 0, so they are not completely removed. With only 14 episodes, very frequent words like *the* can still win. (The `1 +` inside the fraction is there to avoid dividing by zero.)

    scikit-learn also does a few other things differently: it uses its own tokeniser (which ignores one-letter words like *i* and *a*), and it normalises the scores for each document so that the numbers are not directly comparable with ours.

    One way to get closer to our results is to use the `max_df` argument, which tells the vectorizer to ignore words that appear in more than a certain proportion of the documents. Setting `max_df = 0.9` means ignore any word that appears in more than 90% of the episodes:
    """)
    return


@app.cell
def _(TfidfVectorizer, episode_documents, junior_mint_row, top_sklearn):
    seinfeld_vectorizer2 = TfidfVectorizer(max_df = 0.9)
    seinfeld_tfidf2 = seinfeld_vectorizer2.fit_transform(episode_documents)
    seinfeld_words2 = seinfeld_vectorizer2.get_feature_names_out()

    top_sklearn(seinfeld_tfidf2, seinfeld_words2, junior_mint_row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That looks much more like our results. The order is not exactly the same, but the same kinds of words are at the top.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **tf-idf in Gutenberg**

    Now that we have scikit-learn doing the work, it's easy to try tf-idf on other data. Let's treat each *book* in NLTK's Gutenberg corpus as a document, and see which words are most distinctive of each book.

    First we make one string per book, keeping only alphabetic words and lowercasing them:
    """)
    return


@app.cell
def _(gutenberg):
    # a list of all the book names
    gutenberg_books = gutenberg.fileids()

    # create an empty placeholder (a list)
    gutenberg_documents = []

    # loop and add the lowercased words in there, keeping only alpha words
    for book in gutenberg_books:
      book_words = [word.lower() for word in gutenberg.words(book) if word.isalpha()]
      gutenberg_documents.append(' '.join(book_words))

    # how many books?
    len(gutenberg_documents)
    return gutenberg_books, gutenberg_documents


@app.cell
def _(TfidfVectorizer, gutenberg_books, gutenberg_documents, top_sklearn):
    # create a vectorizer tool
    gutenberg_vectorizer = TfidfVectorizer(max_df = 0.9)

    # run tf-idf and create the scores.
    gutenberg_tfidf = gutenberg_vectorizer.fit_transform(gutenberg_documents)
    gutenberg_words = gutenberg_vectorizer.get_feature_names_out()

    # print the top 8 words for each book
    # note how we loop over the existing list to get the file names - what else could we do?
    for row_number, gutenberg_book in enumerate(gutenberg_books):
      book_top = [word for (word, score) in top_sklearn(gutenberg_tfidf, gutenberg_words, row_number, 8)]
      print(gutenberg_book, book_top)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    - Look at the top words for each book. Which books have lots of character names, and which have other kinds of words (like *thou* and *thee*)? Why do you think that is?
    - Look at the three Shakespeare plays. What are words like *ham*, *macb*, and *bru*? (Hint: think about the speaker labels in the Seinfeld scripts.)
    - Try changing `max_df` to `0.5`. What happens to the words? What about `1.0`?
    - Seinfeld episodes and Gutenberg books are quite different kinds of "documents". How does the choice of what counts as a document change what tf-idf can tell us?
    """)
    return


@app.cell
def _():
    # use this code cell to explore tf-idf in Gutenberg!
    return


if __name__ == "__main__":
    app.run()
