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
    # **Lexicon-based approaches: Lexical sophistication**

    Intuitively, it makes sense that some texts are easier to read / understand than others. Compare the language in a book written for a child to the manual for operating a microwave - there are noticeable differences in the quality of the words and syntax used in these types of texts. These differences can be found across all types of text categories and genres.

    One way to think about these differences is to consider them in terms of the relative *sophistication* of the words in a text (i.e., the lexical sophistication). The term *sophistication* is a bit opaque, but certainly has something to do with a combination of text difficulty and style.

    However, there is no single measure of lexical sophistication. In this notebook we explore some of these measures, and understand how they are used to analyse texts. The general method we adopt here is to develop lexical profiles of texts: quantitative descriptions of the quality of the words (or syntax) in a text. Information such as the total number of types and tokens are basic building blocks of a lexical profile.

    We can further develop lexical profiles using a lexicon-based approach. These approaches are similar in that they use external dictionaries (or lexicons) of information about words. For example, there might be a lexicon of easy words and difficult words. We could use this dictionary to profile a text by calculating the proportion of tokens in the text that fall into the easy category or the difficult category, resulting in a difficulty score for the text.

    Let us look at some of the resources which exist for lexical sophistication.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import requests
    import polars as pl
    import nltk
    from nltk.corpus import gutenberg

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'gutenberg'])
    return gutenberg, nltk, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Using external lexicons / dictionaries for lexical profiles**

    I have gathered some lexicons and stored them in the course repository so that we can download and use them in these notebooks. Most of the lexicons are basically lists of words with associated values, scores, ratings, and so on. For example, they might look like this:

    |word |value|
    |--|--|
    |w1|2|
    |w2|4|
    |w3|9|
    |...|...|
    |w100|.5|

    To make things easier, I create a helper function which reads in the lexicon and converts it into a Python dictionary, where each word is a key and its rating is the value. Here is the function:
    """)
    return


@app.cell
def _(requests):
    def get_word_rating_resource(url):
      '''helper function to get lexical resources
      resources are stored as .txt files in the form of Word\tValue\n
      '''
      # read the raw text and split on newlines
      raw = requests.get(url).text.split('\n')

      # create an empty dictionary to store the ratings
      ratings = {}

      for line in raw:
        # split each line on the tab character
        pair = line.split('\t')
        # some lines are empty or incomplete, so only keep lines with a word AND a value
        if len(pair) == 2:
          ratings[pair[0]] = round(float(pair[1]), 3)

      return ratings

    return (get_word_rating_resource,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have the helper function loaded, we can start looking at some resources. In what follows, I describe the basic logic of each lexicon and also point you to the relevant sources if you would like to learn more. All of the resources I have here are for English, although some of these authors also provide data in other languages - you'll need to search that up yourself if you're interested in similar lexicons for languages other than English.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **General word frequency values**

    Word frequency refers to how frequently a word appears in general usage. One simplistic analysis one can make is to associate less frequent words with more difficult vocabulary. There are a lot of different frequency lists out there. The resource I will give you here are the [SUBTLEXus frequency measures.](https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus)

    These frequency measures are taken from a large corpus of subtitles in American television and movies. Using this method, the authors have created frequency lists for a variety of different languages, which you can explore on their website.

    I have only included the Log10WF, (base 10 logarithmic word frequency), which is a normalised measure of frequency that takes into account the logarithmic distribution of words in corpora (remember Zipf's law from the frequency notebook!). A higher value means that the word is more frequent. Also, keep in mind this data includes both capitalised and lowercased versions of some words – this was because the authors wanted to take proper names into account.

    You would want to use frequency for any comparison of vocabulary between texts in English. For example, you could compute the average frequency of the words in a text. In general, words which are *less* frequent are considered to be *more* sophisticated, but this is not an absolute relationship.

    ## How are these values different from `FreqDist`?

    Note that these frequency values are *different* than calculating the frequency of the words in your corpus / texts. The frequency values from SUBTLEXus are gathered from larger corpora of text data, and thus represent the *general* frequency of a word. When we count the frequency of words in a single text with `FreqDist`, we are counting the specific and localised frequency within that text.
    """)
    return


@app.cell
def _(get_word_rating_resource):
    # load in frequency values
    freq_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/subtlxus_frequency.txt'
    freq_dict = get_word_rating_resource(freq_url)
    return (freq_dict,)


@app.cell
def _(freq_dict):
    # one of the most frequent words in the English language
    freq_dict['the']
    return


@app.cell
def _(freq_dict):
    # what about some lower frequency words?
    # (.477 is the lowest value in this resource)
    freq_dict['Tyrannosaur']
    return


@app.cell
def _(freq_dict):
    # try some more words
    freq_targets = ['cabbage', 'Klondike', 'sconce', 'Yes', 'car', 'think']

    for freq_target in freq_targets:
      if freq_target in freq_dict:
        print(f'Word frequency for {freq_target} is {freq_dict[freq_target]}')
      else:
        print(f'Sorry, {freq_target} not found')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **calculating a frequency profile**

    To calculate a frequency profile, we simply need to expand the loop used in the previous cell into a function. Below I create a simple function which can be used for different texts and dictionaries.
    """)
    return


@app.cell
def _(nltk):
    def calculate_metric(text, dictionary):
      # create empty output container
      metric = []

      # tokenize the text (and any other preprocessing you might need)
      tokens = nltk.word_tokenize(text)

      # check if token is in dictionary and append to metric output if so
      for token in tokens:
        if token in dictionary:
          metric.append(dictionary[token])
      return metric

    return (calculate_metric,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This function can be passed a string and dictionary to obtain their general frequency values. For example:
    """)
    return


@app.cell
def _(calculate_metric, freq_dict):
    calculate_metric('these pretzels are making me thirsty!', freq_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can average these resulting frequencies to get an average word frequency for the text:
    """)
    return


@app.cell
def _(calculate_metric, freq_dict):
    # obtain an average frequency
    frequencies = calculate_metric('these pretzels are making me thirsty!', freq_dict)
    sum(frequencies) / len(frequencies)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You could include this in an analysis as a measure of the overall complexity or sophistication of vocabulary, but keep in mind it is only one dimension of this feature. You would also want to report the *coverage* of this resource - which is a measure of how many words in your text were included/excluded in this lexicon. We will come back to coverage below.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Age of acquisition ratings**

    Age of acquisition (AoA) is another measure of vocabulary complexity and sophistication. Unlike general word frequency which is an objective measure from corpora, the AoA values represent the average age where native English speakers think they first learned a particular word. These values were gathered via surveys.

    A lower AoA means that, on average, people believed they learned those words earlier in life. Words that are learned earlier in life (i.e., as children) are logically words which are more frequent, more concrete, and therefore less sophisticated.

    You [can read the paper which gathered these ratings for more information here.](https://link.springer.com/article/10.3758/s13428-012-0210-4)

    Let's look at how to load in and use AoA values:
    """)
    return


@app.cell
def _(get_word_rating_resource):
    # read in aoa data
    aoa_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/AoA_Brysbart.txt'
    aoa_dict = get_word_rating_resource(aoa_url)
    return (aoa_dict,)


@app.cell
def _(aoa_dict):
    # which words do people say they learned, on average, after 20 years of age?
    for aoa_word in aoa_dict:
      if aoa_dict[aoa_word] > 20:
        print(aoa_word, aoa_dict[aoa_word])
    return


@app.cell
def _(aoa_dict):
    # loop through some words to see varying AoAs
    aoa_targets = ['cabbage', 'sconce', 'car', 'think', 'no']

    for aoa_target in aoa_targets:
      if aoa_target in aoa_dict:
        print(f'Age of acquisition for {aoa_target} is {aoa_dict[aoa_target]}')
      else:
        print(f'Sorry, {aoa_target} not found')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **calculating an age of acquisition profile**

    And use the `calculate_metric` function to get average AoA values for a sample text
    """)
    return


@app.cell
def _(aoa_dict, calculate_metric):
    aoas = calculate_metric("these pretzels are making me thirsty!", aoa_dict)
    # notice that we don't have AoA values for all words
    aoas
    return (aoas,)


@app.cell
def _(aoas):
    sum(aoas) / len(aoas)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Word Concreteness ratings**

    Word concreteness is a subjective measure of how abstract or concrete the concept associated with a lexical item is. From this view, people perceive words not necessarily as only concrete or only abstract, but rather slide along a scale. For example, the meaning of the noun "tree" is more concrete than the meaning of the noun "peace." The word concreteness list includes mostly single word items but also some compound, two word items. Like Age of Acquisition, this list of concreteness values was also collected using survey methods.

    In general, words which are more concrete are more frequent and easier to learn, suggesting that language which is more concrete may be less complex. But this is not a hard and fast rule. Concreteness, AoA, and frequency are three measures you might want to consider together when investigating anything related to vocabulary complexity.

    This resource is a list of average concreteness ratings for 40,000 English words. [You can find the paper here.](https://link.springer.com/article/10.3758/s13428-013-0403-5)

    Annotators from Amazon Mechanical Turk were asked to rate how concrete a word was on a scale of 1-5, with a 1 meaning abstract and a 5 meaning concrete.
    """)
    return


@app.cell
def _(get_word_rating_resource):
    # create concreteness dictionary
    concrete_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/concreteness.txt'
    concrete_dict = get_word_rating_resource(concrete_url)
    return (concrete_dict,)


@app.cell
def _(concrete_dict):
    # you can now access mean concreteness ratings
    for concrete_word in concrete_dict:
      # I put a lot of conditions here just to limit the output. there are a LOT of words in here :)
      if concrete_dict[concrete_word] == 5 and ' ' not in concrete_word and len(concrete_word) > 10:
        print(concrete_word, concrete_dict[concrete_word])
    return


@app.cell
def _(concrete_dict):
    # cycle through some concreteness values
    concrete_targets = ['cabbage', 'sconce', 'car', 'think', 'no']

    for concrete_target in concrete_targets:
      if concrete_target in concrete_dict:
        print(f'Average concreteness for {concrete_target} is {concrete_dict[concrete_target]}')
      else:
        print(f'Sorry, {concrete_target} not found')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### **calculating a concreteness profile**
    """)
    return


@app.cell
def _(calculate_metric, concrete_dict):
    concreteness = calculate_metric("these pretzels are making me thirsty!", concrete_dict)
    # again, not every word has a value in this resource
    concreteness
    return (concreteness,)


@app.cell
def _(concreteness):
    sum(concreteness) / len(concreteness)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Semantic diversity ratings**

    This lexicon is a computationally derived measure of word ambiguity. The authors analysed 1000-word spans (i.e. different slices of texts each 1000 words in length) from the British National Corpus and calculated the probability of any one particular word appearing in the spans. A word which has a higher likelihood of appearing in more spans will be more semantically diverse, meaning it can have more polysemous meanings and senses.

    A word with lower ratings means it should have a more specific meaning, and is thus arguably more sophisticated or complicated than a word which can be used in many different contexts.

    [You can read the paper here.](https://link.springer.com/article/10.3758%2Fs13428-012-0278-x)
    """)
    return


@app.cell
def _(get_word_rating_resource):
    semd_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/semantic_diversity.txt'
    semd_dict = get_word_rating_resource(semd_url)
    return (semd_dict,)


@app.cell
def _(semd_dict):
    # what are some of the most restricted words in terms of the contexts they can appear in?
    for semd_word in semd_dict:
      if semd_dict[semd_word] < 0.2:
        print(semd_word)
    return


@app.cell
def _(semd_dict):
    # are words with more specific meanings also associated with lower semd?
    semd_targets = ['cabbage', 'sconce', 'car', 'think', 'no', 'the', 'pretentious']

    for semd_target in semd_targets:
      if semd_target in semd_dict:
        print(f'Average semantic diversity for {semd_target} is {semd_dict[semd_target]}')
      else:
        print(f'Sorry, {semd_target} not found')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### **calculating a semantic diversity profile**
    """)
    return


@app.cell
def _(calculate_metric, semd_dict):
    sem_ds = calculate_metric("these pretzels are making me thirsty!", semd_dict)

    sem_ds
    return (sem_ds,)


@app.cell
def _(sem_ds):
    sum(sem_ds) / len(sem_ds)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Coverage**

    All of these lexicons suffer from the same weakness - if a word in a target text is not in the lexicon, then the word will not count towards the profile of the text. Therefore it is important to know the *coverage* of the lexicon for any one text. Coverage is defined as the percentage of words in the target text which are found in the lexicon.

    Let's add a coverage calculation to our profile function. Because we already have a function called `calculate_metric`, I call this one `calculate_metric2`:
    """)
    return


@app.cell
def _(nltk):
    def calculate_metric2(text, dictionary):
      # create empty output container
      metric = []

      # tokenize the text
      tokens = nltk.word_tokenize(text)

      # check if token is in dictionary and append to metric output if so
      for token in tokens:
        if token in dictionary:
          metric.append(dictionary[token])

      # calculate coverage
      coverage = len(metric) / len(tokens)

      # the function now returns two values
      return metric, coverage

    return (calculate_metric2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Try it out on a capitalised version of our sentence. We get 71% coverage, even though every word in the sentence seems like it should be in a list of 60,000 English words!
    """)
    return


@app.cell
def _(calculate_metric2, freq_dict):
    calculate_metric2('These pretzels are making me thirsty!', freq_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What's going on? Let's check which tokens were *not* found in the lexicon:
    """)
    return


@app.cell
def _(freq_dict, nltk):
    [token for token in nltk.word_tokenize('These pretzels are making me thirsty!') if token not in freq_dict]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are two problems here:

    1. `nltk.word_tokenize()` created a punctuation token for `!`, which will never be in the lexicon
    2. `These` has a capital letter. Python dictionaries are case-sensitive, so `These` and `these` are different keys

    So coverage depends on our preprocessing choices (remember the tokenisation notebook!). Let's make a version of the function which lowercases the text and only keeps alphabetic tokens:
    """)
    return


@app.cell
def _(nltk):
    def calculate_metric3(text, dictionary):
      # create empty output container
      metric = []

      # lowercase and tokenize the text, keeping only alphabetic tokens
      tokens = [token for token in nltk.word_tokenize(text.lower()) if token.isalpha()]

      # check if token is in dictionary and append to metric output if so
      for token in tokens:
        if token in dictionary:
          metric.append(dictionary[token])

      # calculate coverage
      coverage = len(metric) / len(tokens)

      return metric, coverage

    return (calculate_metric3,)


@app.cell
def _(calculate_metric3, freq_dict):
    calculate_metric3('These pretzels are making me thirsty!', freq_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Much better! But preprocessing won't solve everything. Look at the coverage of the AoA lexicon for the same sentence:
    """)
    return


@app.cell
def _(aoa_dict, calculate_metric3):
    calculate_metric3('These pretzels are making me thirsty!', aoa_dict)
    return


@app.cell
def _(aoa_dict, nltk):
    [token for token in nltk.word_tokenize('these pretzels are making me thirsty') if token not in aoa_dict]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The AoA lexicon mostly contains the *base forms* of words (e.g., *pretzel*, *make*, *be*), so inflected forms like *pretzels*, *making*, and *are* are not found. Each lexicon was built in a different way, by different people, for different purposes, so each one will have different coverage for the same text.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Avoiding division by zero**

    What happens if *none* of the words in a text are in the lexicon? The `metric` list will be empty, and calculating the average with `sum(metric) / len(metric)` will try to divide by zero, which Python does not allow:
    """)
    return


@app.cell
def _(aoa_dict, calculate_metric3):
    # none of these words are in the lexicon, so the metric list is empty
    empty_metric, empty_coverage = calculate_metric3('blarg zorp', aoa_dict)
    empty_metric
    return (empty_metric,)


@app.cell
def _(empty_metric):
    # this will give us a ZeroDivisionError!
    sum(empty_metric) / len(empty_metric)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This might seem unlikely, but when you calculate metrics for lots of short texts (e.g., sentences or tweets), it happens more often than you'd think! One way to avoid the error is to check the length of the list first, using an `if` statement. If the list is empty, the function returns `None`, which is Python's way of saying "no value". This is better than returning 0, because 0 would be a real (and very misleading!) score.
    """)
    return


@app.function
def average_metric(metric):
  # check if the list is empty before dividing
  if len(metric) == 0:
    return None
  return round(sum(metric) / len(metric), 2)


@app.cell
def _(aoa_dict, calculate_metric3, empty_metric):
    print(average_metric(empty_metric))
    print(average_metric(calculate_metric3('these pretzels are making me thirsty', aoa_dict)[0]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Comparing texts**

    But what we really want to do is create a full profile of more than one text and then compare them. Let's compare some of the books in NLTK's Gutenberg corpus. Two of the books are stories written for children (*Bryant's Stories to Tell to Children* and *The Adventures of Buster Bear*), and the others were written for adults. Which texts do you think will be more sophisticated?

    I'll place the dictionaries and texts into their own dictionaries so we can use the keys as labels:
    """)
    return


@app.cell
def _(aoa_dict, concrete_dict, freq_dict, gutenberg, semd_dict):
    lexical_dictionaries = {
      'frequency': freq_dict,
      'age of acquisition': aoa_dict,
      'concreteness': concrete_dict,
      'semantic diversity': semd_dict,
    }

    # join the words of each book back into a single string
    texts = {
      'Stories to Tell to Children': ' '.join(gutenberg.words('bryant-stories.txt')),
      'The Adventures of Buster Bear': ' '.join(gutenberg.words('burgess-busterbrown.txt')),
      'Emma': ' '.join(gutenberg.words('austen-emma.txt')),
      'Paradise Lost': ' '.join(gutenberg.words('milton-paradise.txt')),
    }
    return lexical_dictionaries, texts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now I loop over the texts and the dictionaries, using `calculate_metric3()` and `average_metric()` for every combination. Each combination becomes one row in a polars dataframe. This might take a few seconds to run.
    """)
    return


@app.cell
def _(calculate_metric3, lexical_dictionaries, pl, texts):
    profile_rows = []

    for text_name in texts:
      for dictionary_name in lexical_dictionaries:
        metric, coverage = calculate_metric3(texts[text_name], lexical_dictionaries[dictionary_name])
        profile_rows.append({
          'text': text_name,
          'lexicon': dictionary_name,
          'average': average_metric(metric),
          'coverage': round(coverage, 2),
        })

    profiles = pl.DataFrame(profile_rows)
    profiles
    return (profiles,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's a bit hard to read. We can use `.pivot()` to put the lexicons in the columns, so each text has one row:
    """)
    return


@app.cell
def _(profiles):
    profiles.pivot(on = 'lexicon', index = 'text', values = 'average')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What do the results tell us? Compared to the books for adults, the children's books have a higher average word frequency (only slightly higher than *Emma*, though), a lower average age of acquisition, and higher average concreteness. If you recall what these variables mean, this suggests that the children's books are *less* lexically sophisticated - which is what we would hope! Do you agree?

    Note that the semantic diversity scores are quite similar for all four books. Not every measure separates every set of texts.

    And don't forget the coverage:
    """)
    return


@app.cell
def _(profiles):
    profiles.pivot(on = 'lexicon', index = 'text', values = 'coverage')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    - The AoA lexicon has much lower coverage than the others. Look at some of the words in these books which are *not* in the AoA lexicon. What kinds of words are they?
    - Choose some other texts (e.g., other Gutenberg books, Brown categories, or the Seinfeld scripts) and compare their profiles. Do the results match your intuitions?
    - The concreteness and AoA ratings come from surveys of (mostly American) adults. Would you expect New Zealanders, children, or second language learners to give the same ratings?
    """)
    return


@app.cell
def _():
    # use this code cell to compare lexical profiles!
    return


if __name__ == "__main__":
    app.run()
