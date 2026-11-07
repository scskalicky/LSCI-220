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
    #### Relevant NLTK Book sections

    [NLTK Book, Chapter 2, Section 2.4](https://www.nltk.org/book/ch02.html#generating-random-text-with-bigrams)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Generating Text from Bigrams**

    This notebook is intended to prompt you to think about how text generation programs might work using nothing more than frequency counts. Chapter 2 of the NLTK book has a section which shows how to use bigrams as a way to generate text. In the word probabilities notebook, we used bigrams to calculate how likely a word is to come after another word. Now we will turn that around, and use the bigrams to *choose* the next word.

    The first thing you need to do is create a list of bigrams. Let's use the Marine Biologist episode from *Seinfeld*.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import re
    import random
    import requests
    import nltk
    from nltk import FreqDist
    from collections import defaultdict

    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab'])
    return FreqDist, defaultdict, nltk, random, re, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I load the text, lowercase it, and make the bigrams.
    """)
    return


@app.cell
def _(nltk, requests):
    mb = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/marine_biologist.txt').text

    mb_bigrams = list(nltk.bigrams(nltk.word_tokenize(mb.lower())))

    mb_bigrams[:5]
    return mb, mb_bigrams


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Which words come next?**

    To generate text, we need to know, for every word, which words come *after* it and how often. We can store this in a `defaultdict` (remember the defaultdict notebook!) where:

    - each key is a word
    - each value is a `FreqDist` of the words which come after that word

    Using `defaultdict(FreqDist)` means that the first time we see a word, it automatically gets an empty `FreqDist`, so we can start counting straight away. We loop through the bigrams, and for each pair `(w1, w2)`, we add 1 to the count of `w2` in the `FreqDist` for `w1`.

    I put this in a function, so that we can use it on other texts later.
    """)
    return


@app.cell
def _(FreqDist, defaultdict):
    def next_word_model(bigrams):
      # each word gets a FreqDist of the words which come after it
      next_words = defaultdict(FreqDist)
      for (w1, w2) in bigrams:
        next_words[w1][w2] += 1
      return next_words

    return (next_word_model,)


@app.cell
def _(mb_bigrams, next_word_model):
    # now "train" themodel on the marine biologist script
    mb_model = next_word_model(mb_bigrams)
    return (mb_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Looking up a single word gives us a frequency distribution of the words which came after it:
    """)
    return


@app.cell
def _(mb_model):
    # the words which came after 'whale', and how often
    mb_model['whale'].most_common()
    return


@app.cell
def _(mb_model):
    # the most frequent words after 'jerry'
    mb_model['jerry'].most_common(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Version 1: always choose the most frequent next word**

    Here is a function based on the code from the NLTK book. There are three arguments to the function:

    1. `model` - our dictionary of next words
    2. `word` - a seed word (the first word)
    3. `num` - a number controlling the total amount of words to generate, with a default value of 15

    The function will loop for as many times as specified by `num`. In the loop, the function prints the provided value for the `word` argument.

    Then, the value of `word` is overwritten with another word. How is that word selected? The function looks up the `FreqDist` of next words for the current word, and asks for the word with the highest frequency. This is what the `.max()` does. That word then becomes the new target word to find the *next* word. And this repeats for as many times as specified.

    I also added a check: if a word has *no* next words (e.g., it was the very last word of the text), the function stops early, rather than crashing.
    """)
    return


@app.function
def generate_model(model, word, num = 15):
  for i in range(num):
    print(word, end = ' ')
    # stop if this word never had a next word
    if len(model[word]) == 0:
      break
    word = model[word].max()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ok, let's try the function with two different seed words.

    How effective is it?
    """)
    return


@app.cell
def _(mb_model):
    generate_model(mb_model, 'well')
    return


@app.cell
def _(mb_model):
    generate_model(mb_model, 'jerry')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It seems pretty good at first, but when we start asking for longer texts, the model just repeats itself. This is a problem with the function in that words will get stuck in loops.

    But, this tiny little model contains the same basic idea that other generative text AI models use - predicting the next word based on information about the likelihood of all the other possible words.
    """)
    return


@app.cell
def _(mb_model):
    generate_model(mb_model, 'george', num = 50)
    return


@app.cell
def _(mb, nltk):
    # how many tokens in this text?
    len(nltk.word_tokenize(mb))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Maybe we need more data? Let's try it on a larger corpus: the Big Salad. I will lowercase and remove punctuation.
    """)
    return


@app.cell
def _(next_word_model, nltk, re, requests):
    # download and lowercase the text
    big_salad = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/big_salad.txt').text.lower()

    # remove punctuation (anything that is not a word character or a space)
    big_salad = re.sub(r'[^\w\s]', '', big_salad)

    # tokenise, make the bigrams, and make the model
    sf_bigrams = list(nltk.bigrams(nltk.word_tokenize(big_salad)))
    sf_model = next_word_model(sf_bigrams)

    sf_bigrams[:10]
    return (sf_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have a larger text ready to go, let's try the text generation function again:
    """)
    return


@app.cell
def _(sf_model):
    generate_model(sf_model, 'jerry')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We still have the problem identified in the NLTK book - at some point we get stuck in a loop. Why? Because we are always asking for the most frequent bigram pair. The NLTK book suggests randomly sampling from among the available words, rather than taking the most frequent value.

    ## **Version 2: choose any next word at random**

    To randomly choose in Python, we can use the `choice()` function from the `random` library. Here is how it works. Run this cell a few times to see that you get different results each time:
    """)
    return


@app.cell
def _(random):
    # choose one item from this list at random
    random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we can use `choice()` to pick words from the next word distribution as well. Here I loop 10 times to show the range of possible results. Run this cell more than once to get new words.
    """)
    return


@app.cell
def _(random, sf_model):
    # pick one word among the words which come after 'hello'
    for i in range(10):
      print(random.choice(list(sf_model['hello'])))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ok, now we can incorporate `choice()` into the generate text function.
    """)
    return


@app.cell
def _(random):
    def generate_model2(model, word, num = 15):
      for i in range(num):
        print(word, end = ' ')
        if len(model[word]) == 0:
          break
        # randomly choose from all of the possible next words
        word = random.choice(list(model[word]))

    return (generate_model2,)


@app.cell
def _(generate_model2, sf_model):
    generate_model2(sf_model, 'jerry')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The results are pretty interesting and funny - you can run this cell multiple times and get different text each time. But we seem to have gone too far in the other direction. The output is mostly gibberish. This is because words with low frequencies are just as likely to be chosen as words with high frequencies.

    What can be done to address this? One solution might be to force the choice to be made from among the highest frequency options, rather than just the maximum.

    ## **Version 3: choose at random from the top few next words**

    We can use `.most_common()` to get the most frequent next words. For example, here are the five most frequent words that occur after 'jerry':
    """)
    return


@app.cell
def _(sf_model):
    [next_word for (next_word, count) in sf_model['jerry'].most_common(5)]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So now we can choose from this restricted range of high frequency pairs:
    """)
    return


@app.cell
def _(random, sf_model):
    # run this cell a few times to get different results
    random.choice([next_word for (next_word, count) in sf_model['jerry'].most_common(5)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And even if there are not enough words, the program should work. For example, if a word only has 3 next words, `.most_common(5)` just gives us those 3.

    Let's add this functionality to our function. We will add a new argument which allows the user to set the number of top words to choose from, with a default of `5`.

    This approach actually has a name: **top-k sampling**, where *k* is the number of top words to choose from. It is one of the methods that real AI text generators (such as ChatGPT) can use to choose their next word.
    """)
    return


@app.cell
def _(random):
    def generate_model3(model, word, num = 15, k = 5):
      for i in range(num):
        print(word, end = ' ')
        if len(model[word]) == 0:
          break
        # randomly choose from the k most frequent next words
        top_words = [next_word for (next_word, count) in model[word].most_common(k)]
        word = random.choice(top_words)

    return (generate_model3,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Try out the new function - is it better? Yeah, it should be. Is it *good*? Meh?

    Play with the number of top words (`k`) and length of the output to see the different effects it has on the generated text.
    """)
    return


@app.cell
def _(generate_model3, sf_model):
    generate_model3(sf_model, 'well', k = 3)
    return


@app.cell
def _(generate_model3, sf_model):
    generate_model3(sf_model, 'hello', num = 25, k = 5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can see that for this data, a loop occurs when we use a `k` of 1, which would be the same as using `.max()` in the original version.
    """)
    return


@app.cell
def _(generate_model3, sf_model):
    generate_model3(sf_model, 'the', k = 1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So keeping `k` above 1 helps create much more varied text.
    """)
    return


@app.cell
def _(generate_model3, sf_model):
    generate_model3(sf_model, 'hi', num = 30, k = 5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Version 4: choose in proportion to frequency**

    Version 3 still treats the top *k* words as equally likely. But after *jerry*, some words are *much* more common than others. A more realistic approach is to choose each next word **in proportion to how often it occurred**. So if *you* came after *thank* 90% of the time, it would be chosen about 90% of the time, but the other 10% of words would still get a chance.

    The `random.choices()` function (note the `s`!) can do this, using its `weights` argument. The weights are the frequencies of each word. `random.choices()` gives back a list, so I take the first (and only) item with `[0]`.
    """)
    return


@app.cell
def _(random, sf_model):
    # the words after 'thank', and how often they occurred
    thank_words = list(sf_model['thank'].keys())
    thank_counts = list(sf_model['thank'].values())

    print(sf_model['thank'].most_common(5))

    # run this cell a few times: 'you' should be chosen most of the time
    random.choices(thank_words, weights = thank_counts)[0]
    return


@app.cell
def _(random):
    def generate_model4(model, word, num = 15):
      for i in range(num):
        print(word, end = ' ')
        if len(model[word]) == 0:
          break
        # choose the next word in proportion to its frequency
        next_words = list(model[word].keys())
        next_counts = list(model[word].values())
        word = random.choices(next_words, weights = next_counts)[0]

    return (generate_model4,)


@app.cell
def _(generate_model4, sf_model):
    generate_model4(sf_model, 'jerry', num = 30)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is very close to how large language models choose their words. A large language model calculates a probability for every possible next word, and then picks a word in proportion to those probabilities. These models also have a setting called **temperature**: a low temperature makes the most likely words even *more* likely (closer to version 1), and a high temperature makes all of the words more equally likely (closer to version 2).

    ## **The point**

    There are ways to continue tweaking this program to make more realistic text (for example, consider if there were rules about part of speech order!). The point however is to demonstrate that even though it is not perfect, we can start to approximate actual text generation using nothing more than counts of our word pairs. Think about this for a moment - the frequency distributions of our input can be used to create (almost) meaningful output. With more data and more precise counts and algorithms for how certain words go with other words, we can start to grasp the way that more advanced generative artificial intelligence is able to produce meaningful text.

    Our model only ever looks at *one* previous word. Large language models look at thousands of previous words at once, and learn much more complex patterns than bigram counts. But the basic task is the same: predict the next word, again and again.

    ### **Your Turn**

    - Generate text from the Marine Biologist model and the Big Salad model with the same seed word. How does the amount of training data change the output?
    - Try different values of `k` in `generate_model3()`. What value gives the most "realistic" text?
    - Make a model from a different text (e.g., a State of the Union speech, or a Gutenberg book). Can you tell which text a model was trained on from its generated text?
    - The generated text can look like Seinfeld, but the model doesn't know anything about Jerry, George, or New York. Is predicting the next word the same as understanding?
    """)
    return


@app.cell
def _():
    # use this code cell to generate your own text!
    return


if __name__ == "__main__":
    app.run()
