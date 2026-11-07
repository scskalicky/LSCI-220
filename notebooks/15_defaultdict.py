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
    #### Relevant NLTK Book Sections & other readings

    [NLTK Book, Chapter 5, Section 3.1](https://www.nltk.org/book/ch05.html#dictionary_index_term)

    [Geeks for Geeks DefaultDict](https://www.geeksforgeeks.org/defaultdict-in-python/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Doing more with Dictionaries**

    We have already covered dictionaries in general. By now you should see that dictionaries are quite useful for storing linguistic information, which NLTK refers to as mapping from one thing to another (e.g., mapping a POS tag to a word). In this notebook we will return to dictionaries as a refresher, and also learn about extensions to dictionaries used by NLTK.
    """)
    return


@app.cell
def _():
    # download necessary resources for this notebook
    import nltk
    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download('gutenberg')
    return (nltk,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As a reminder, we can manually create a dictionary using a pair of curly braces `{}` or the `dict()` function. Below, I define a dictionary called `pos_dict` where words are keys and POS tags are the values:
    """)
    return


@app.cell
def _():
    # manually create a dictionary
    pos_dict = {}
    pos_dict['colorless'] = 'ADJ'
    return (pos_dict,)


@app.cell
def _(pos_dict):
    # add entries which are word:pos_tag key/value pairs
    pos_dict['ideas'] = 'N'
    pos_dict['sleep'] = 'V'
    pos_dict['furiously'] = 'ADV'
    return


@app.cell
def _(pos_dict):
    # inspect our dictionary
    pos_dict
    return


@app.cell
def _(pos_dict):
    # Using list() will give all the keys, handy as a shortcut
    list(pos_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **using `defaultdict`**

    A `defaultdict` is an extension of Python dictionaries from the `collections` module. Learning how to use `defaultdict` is helpful if you are performing operations where you want automatic values set to keys which do not yet exist in a dictionary.

    First of all, consider what happens when we ask a dictionary for a key that does not exist. I'll create a dictionary with fictional frequency values for two words.
    """)
    return


@app.cell
def _():
    # make a small dictionary with word:frequency key/values
    fake_frequencies = {'the': 1337, 'dog': 42}
    fake_frequencies
    return (fake_frequencies,)


@app.cell
def _(fake_frequencies):
    # everything is fine when I ask for a key already in the dictionary.
    fake_frequencies['the']
    return


@app.cell
def _(fake_frequencies):
    # but if I ask for a key not in the dictionary, we get a key error
    fake_frequencies['ran']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using a `defaultdict` allows us to avoid these errors when looking up values that might not exist. And, by extension, it allows us to think about how this might be useful for things like frequency dictionaries — if a word does not exist in our frequency dictionary, we could assume that it has a frequency of zero. This is exactly what the NLTK `FreqDist` dictionary provides you with.

    Same thing with POS tags or other lexical information — rather than finding out that something is not in the dictionary, it would be preferable to update the dictionary with a value indicating the lack of such information.

    When you create a default dictionary, you can specify the default value (or function) which will trigger if a value does not exist in the dictionary. In the cell below, I import `defaultdict` and then specify the default value for a key not in the dictionary will be an `int`. Because I do not supply any other information about the `int`, the default value will be `0`.

    > **marimo note:** in this notebook, several cells add to a dictionary that was created in an earlier cell (and with a `defaultdict`, even *looking up* a missing key adds it). This works when you run the cells in order. But if you go back and change one of those cells, marimo won't automatically re-run the cells below it, so re-run them yourself.
    """)
    return


@app.cell
def _():
    # import defaultdict
    from collections import defaultdict

    # create a defaultdictionary where default values are `int` of 0.
    frequency = defaultdict(int)

    # add a key/value to the dictionary
    frequency['colorless'] = 4

    # inspect key/value
    frequency['colorless']
    return defaultdict, frequency


@app.cell
def _(frequency):
    # now look up something not in the dictionary
    # the key was not there, so was added with the DEFAULT value of int = 0
    frequency['ideas']
    return


@app.cell
def _():
    # to understand why `int` gives us zero:
    int()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you wanted to set the default value to be a specific number, you can use (`lambda: value`) as the default argument:
    """)
    return


@app.cell
def _(defaultdict):
    # I use an anonymous function (lambda) to set default value to a number that is not zero.
    any_integer = defaultdict(lambda: 1337)

    any_integer['test']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can extend this to other information such as parts of speech. Below, I make a new `defaultdict` called `pos_lists`, and indicate it should have an empty `list` as the default value, and the same process occurs when we look up words not in the dictionary.
    """)
    return


@app.cell
def _(defaultdict):
    # default is an empty list for tag sets
    pos_lists = defaultdict(list)
    # add a key value
    pos_lists['sleep'] = ['NOUN', 'VERB']
    # works as intended
    pos_lists['sleep']
    return (pos_lists,)


@app.cell
def _(pos_lists):
    # a word not in the dictionary is updated to default value (an empty list)
    pos_lists['green']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For something like parts of speech, we might actually want to have a default POS tag instead of an empty list. Again we can use the `lambda` function to supply a default POS tag.
    """)
    return


@app.cell
def _(defaultdict):
    # tell defaultdict that the default POS tag is "NOUN"
    pos_noun_default = defaultdict(lambda: 'NOUN')

    pos_noun_default['colorless'] = 'ADJ'
    pos_noun_default['colorless']
    return (pos_noun_default,)


@app.cell
def _(pos_noun_default):
    # if an entry doesn't exist it is added to the dictionary
    # there are other ways to do this using the basic dictionary type as well
    pos_noun_default['blog']
    return


@app.cell
def _(pos_noun_default):
    # look at the dictionary now - 'blog' was added with the default tag of NOUN
    pos_noun_default.items()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Recall that `nltk.pos_tag()` will tag things as a noun by default, and that `FreqDist()` will give frequencies of zero for unknown words. Now you can understand a little bit more about how they go about doing this!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Tagging unknown words**

    Now, instead of supplying a default tag such as "NOUN" (which could be dangerous), NLTK shows how labels such as "unknown" can be used to tag words which are "out of vocabulary."

    Below, we read in *Alice in Wonderland* from the Gutenberg data built into NLTK. We access the `.words` of the book to get the tokenized list, and then create a frequency distribution of those words using `nltk.FreqDist()`.
    """)
    return


@app.cell
def _(nltk):
    # create a frequency distribution of all the words from alice in wonderland
    alice = nltk.corpus.gutenberg.words('carroll-alice.txt')
    alice_vocab = nltk.FreqDist(alice)

    # take a peek at some of the most common words
    alice_vocab.most_common(100)[90:100]
    return alice, alice_vocab


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the next code cell, we use a `list comprehension` to extract the most frequent 1000 words. We only retain the words in the loop.
    """)
    return


@app.cell
def _(alice_vocab):
    # gather the most frequent 1000 tokens
    alice_top_1000 = [word for (word, frequency) in alice_vocab.most_common(1000)]
    alice_top_1000[90:100]
    return (alice_top_1000,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we will create a default dictionary in which the default tag will be 'UNK' for unknown.
    """)
    return


@app.cell
def _(defaultdict):
    # create default dict with a default string of "UNK" if not in the dict.
    alice_known = defaultdict(lambda: 'UNK')
    return (alice_known,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will then add our top 1000 words to the dictionary, and in doing so, will make both the key and the value the word. We do so using a for loop which loops over each word and sets that word as the key and the value.

    Why are we doing this? We are simulating a list of "known" words. Any word which has itself as the value is considered "known."
    """)
    return


@app.cell
def _(alice_known, alice_top_1000):
    # add each word from top 1000 as itself to the dictionary
    for v in alice_top_1000:
      alice_known[v] = v
    return


@app.cell
def _(alice_known):
    # make sure you understand what is going on here.
    list(alice_known.items())[90:100]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we can perform a `list comprehension` which loops over all of the words in the book (contained in the variable `alice`). This will simulate reading the book one word at a time.

    The list comprehension is asking for the value of each word from our default dictionary `alice_known`. Remember, we've already added the top 1000 words to this dictionary, so if they are checked, they will return themselves.

    For the words in `alice` which are *not* in `alice_known`, the default dictionary will return our unknown tag "UNK".

    The end result is a list of tokens the same length as `alice`, but any word not in the top 1000 most frequent words will be replaced with "UNK".
    """)
    return


@app.cell
def _(alice, alice_known):
    # create a new vocab which then looks at all the words in alice (not just the top 1000)
    alice_complete = [alice_known[v] for v in alice]

    # anything not already in the top 1000 words gets assigned to UNK
    alice_complete[:100]
    return (alice_complete,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can compare the two versions - because the words `Lewis` and `Carroll` were not in the top 1000 most frequent words, they are replaced with `UNK`
    """)
    return


@app.cell
def _(alice, alice_complete):
    # extract just the first 10 real words from each version
    first_10_raw = ' '.join([v for v in alice[1:11]])
    first_10_processed = ' '.join([v for v in alice_complete[1:11]])

    # print them for comparison
    print(f'Original version:\n {first_10_raw} \n Processed version:\n {first_10_processed}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can confirm the two lists of tokens are the same length (i.e., have the same number of words):
    """)
    return


@app.cell
def _(alice):
    len(alice)
    return


@app.cell
def _(alice_complete):
    len(alice_complete)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, in the end, this was a really convoluted method which replaced all of the words in the book that are *not* in the top 1000 most frequent words with the tag "UNK".

    You are probably wondering, why might we ever want to do something like this? It of course depends on the goals of your analysis. Extracting the most-frequent 1000 words from a text may in turn include a good portion of the text. In fact, if we ask that question about our text here, we can see that the 1000 most-frequent words account for over 90% of all the words in the book.
    """)
    return


@app.cell
def _(alice, alice_top_1000):
    # all words that are in the top 1000 most frequent words
    in_vocab = [w for w in alice if w in alice_top_1000]

    # all those that are not
    out_vocab = [w for w in alice if w not in alice_top_1000]
    return in_vocab, out_vocab


@app.cell
def _(alice, in_vocab):
    # calculate proportion based on total words for top 1000
    len(in_vocab) / len(alice) * 100
    return


@app.cell
def _(alice, out_vocab):
    # same for those without
    len(out_vocab) / len(alice) * 100
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What we have done by looking at the top 1000 most frequent words is reduced the search space for any task or procedure we might want to perform on this text. The NLTK book points out that a procedure such as this can help with Part of Speech tagging, because it means a tagger would not need to consider any word tagged with "UNK" and thus increase accuracy and performance.

    We can also use such information and compare the top 1000-most frequent words in this text to other texts and/or word lists as a way to assess topics or similarity between two texts, or assess the overall difficulty of the vocabulary by comparing this list to lists of word frequency built on even larger corpora.
    """)
    return


if __name__ == "__main__":
    app.run()
