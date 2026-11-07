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
    #### Relevant NLTK Book Sections

    [NLTK Book, Chapter 1, Section 3.1 and 3.2](https://www.nltk.org/book/ch01.html#frequency_distribution_index_term)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Word Frequencies**

    In this notebook we will learn how to explore a fundamental numerical distribution of language: the relative frequencies of words. Word frequency is a very interesting property of language because it correlates with other constructs, such as word length (shorter words are more frequent) and word difficulty (more complex words are less frequent).

    Moreover, counting the frequency in which words occur with *other* words has proven very insightful for linguistics and NLP. The most basic insight is that words tend to co-occur with other specific words in predictable ways. Corpus linguists call these pairs of words `collocations`, and define them using a variety of different statistical measures. Finding these larger collocational patterns has given strength to functional linguistic theories of grammar such as construction grammar, which argue that both meaning and syntax determine the way a word is used in language.

    Word co-occurrence statistics have also been used to create co-occurrence distributions and early word vector spaces - which have since led to large-scale NLP algorithms and artificial intelligence applications which rely on forward predictions in both processing and production (more on that later!).

    This notebook covers:

    1. frequency distributions with `nltk.FreqDist()`
    2. searching a corpus with frequency
    3. plotting frequency, and Zipf's law
    4. normalising frequency counts, so we can compare texts and corpora of different sizes
    5. range: is a frequent word also a widespread word?
    6. frequency over time

    First, let's load all of the libraries and NLTK resources this notebook uses.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import re
    import requests
    import matplotlib.pyplot as plt
    import nltk
    from nltk import FreqDist

    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'nps_chat', 'brown', 'inaugural', 'gutenberg'])
    return FreqDist, nltk, plt, re, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Frequency distributions**

    The simplest form of a frequency distribution is a count of how many times each word appears in a text. It's worth pausing for a moment and considering how you might construct your own frequency distribution with Python and some text — what might be the steps for doing so? Here is one general approach you could take:

    1. You start a loop over the words in a text (ideally already tokenized)
    2. At the first word, you note down the word and store it in a separate data container, alongside a value representing its frequency (starting with 1)
    3. You then move to the next word and check if the next word already exists in your data container,
          - if it does already exist, you increase its count by 1
          - If it does not exist, you add it to the data container and set an initial count of 1

    Here is what that might look like using pseudocode:

    ```
    output_container = []

    for word in list_of_tokens:
      if word in output_container
        increase count of word + 1
      else
        add word to output_container
        increase count of word + 1
    ```

    Now, what kind of data container would make sense for this? A `list` might be able to work, but this would require some careful indexing and might become a pain. There is another data container better designed for this known as a `dictionary`, which you will learn about in the dictionaries notebook. For now, we can rely on a built-in NLTK function named `FreqDist()`, which creates a dictionary of `value:frequency` pairs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Using `nltk.FreqDist()`**

    We can pass a sequence (e.g., a string, a list, etc) to the `FreqDist()` function and it will count the number of times different values in the sequence occur. For example, we can count the frequency of letters in a word, or the frequency of words in a sentence, and so on.

    Let's look at an example. I create a text, then split the text into tokens using `.split()`.
    """)
    return


@app.cell
def _():
    # define a string containing many characters
    turtles = """teenage mutant ninja turtles
    teenage mutant ninja turtles
    teenage mutant ninja turtles
    heroes in a halfshell, turtle power"""
    return (turtles,)


@app.cell
def _(turtles):
    # split the string into tokens/words using .split()
    turtles_tokens = turtles.split()

    turtles_tokens
    return (turtles_tokens,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have a list of tokens, we pass that list of tokens to the `FreqDist()` function, giving it the variable name `turtle_fdist`:
    """)
    return


@app.cell
def _(FreqDist, turtles_tokens):
    # save the frequency distribution to a variable
    turtle_fdist = FreqDist(turtles_tokens)
    return (turtle_fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the results:
    """)
    return


@app.cell
def _(turtle_fdist):
    # inspect the frequency distribution
    turtle_fdist
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The resulting frequency distribution is a Python data object called a `dictionary` which stores `key:value` pairs. In this case, our keys are the words, and the values are the frequencies.

    We can query a dictionary for specific `key:value` pairs using the following syntax:

    > `dictionary['key']`

    This should look familiar, because it is similar to how one can index characters in strings (e.g., `turtles[1]`) or index words in lists (e.g., `['one', 'two'][0]`)

    So, we can ask the frequency distribution to give us the frequency for a target word. For example, the word `turtles`:
    """)
    return


@app.cell
def _(turtle_fdist):
    # how frequent is "turtles?"
    turtle_fdist['turtles']
    return


@app.cell
def _(turtle_fdist):
    # how frequent is "turtle?"
    turtle_fdist['turtle']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we ask for a word that is *not* in the distribution, we receive an answer of 0, which makes sense.
    """)
    return


@app.cell
def _(turtle_fdist):
    # what happens if we ask for a word not in the dictionary?
    # the NLTK FreqDist gives us a 0 rather than an error, which is handy!
    turtle_fdist['shredder']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **`FreqDist()` functions**

    A `FreqDist()` object comes with some built-in helper functions. For example, we can ask for the most frequent terms from a frequency distribution using the `.most_common()` method. We can specify the number of top results we want by putting a number in the brackets `()` used by `.most_common()`. The code below has a `3` in the brackets, so the function will return the top-three most frequent words in the frequency distribution.
    """)
    return


@app.cell
def _(turtle_fdist):
    # what are the top 3 most frequent words?
    turtle_fdist.most_common(3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also ask for so-called `hapaxes` - words that occur only one time in the distribution:
    """)
    return


@app.cell
def _(turtle_fdist):
    turtle_fdist.hapaxes()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can query the total number of word entries in the distribution using `FreqDist.B()`. In other words, this is the total number of **types** in the text (not tokens!).
    """)
    return


@app.cell
def _(turtle_fdist):
    turtle_fdist.B()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To get the total number of *tokens*, we can use `FreqDist.N()`
    """)
    return


@app.cell
def _(turtle_fdist):
    turtle_fdist.N()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Searching with frequency**

    Let's calculate word frequencies for a larger, more interesting data set: a corpus of online chat messages included with NLTK, called `nps_chat`. We access its tokens using `.words()`, then make a frequency distribution of them.
    """)
    return


@app.cell
def _(FreqDist, nltk):
    # the tokens of the chat corpus
    chat_words = nltk.corpus.nps_chat.words()

    # Now create a FreqDist of the chat corpus
    chat_fdist = FreqDist(chat_words)
    return chat_fdist, chat_words


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What are the 50 most common words in the chat corpus? Examine the output - what do you see? Are there items in the output you did or did not expect? What do you think is happening?
    """)
    return


@app.cell
def _(chat_fdist):
    chat_fdist.most_common(50)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's now look at how people use the phrase "lol" - both the individual frequency and the overall percentage of "lol" in the corpus.

    What do you think about the results? Around 1.5% might seem low, but is actually a rather strong result considering how many possible words *could* be in the corpus.
    """)
    return


@app.cell
def _(chat_fdist):
    # index the value by using the key (in this case, the word we want to check)
    chat_fdist['lol']
    return


@app.cell
def _(chat_fdist, chat_words):
    # divide the frequency of 'lol' by the total length of the corpus, then multiply by 100
    (chat_fdist['lol'] / len(chat_words)) * 100
    return


@app.cell
def _(chat_fdist):
    # note that we can obtain the total tokens using .N() as well.
    (chat_fdist['lol'] / chat_fdist.N()) * 100
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now include word frequency as an additional condition when looking for certain words. Do you recall how `list comprehensions` and conditional `for loops` worked? For example, if we wanted to ask for all words which are three letters long:
    """)
    return


@app.cell
def _(chat_words):
    # this says: give me every word in chat_words but only if the length of the word is equal to 3
    [w for w in chat_words if len(w) == 3]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The output is not very readable, is it? We are getting every single token which is 3 characters long, including repetitions. We can reduce this firstly by wrapping the list comprehension in `set()` so that we get a list of types, rather than tokens.
    """)
    return


@app.cell
def _(chat_words):
    # add set()
    set([w for w in chat_words if len(w) == 3])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you look through that output, you can see that there are a lot of things that look like codes or other non-word stuff, usually in UPPERCASE. We can try removing those using `.islower()`
    """)
    return


@app.cell
def _(chat_words):
    # all tokens which are 3 letters long and all characters are lowercase
    set([w for w in chat_words if len(w) == 3 and w.islower()])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now it's getting more manageable. It's still quite a long list though. Let's add another condition - asking for the same output as the previous code, but this time setting a minimum frequency. We can embed a `FreqDist` as part of the condition.

    Here I include a conditional that the word must have a frequency greater than 100 in the frequency distribution. I also adjust our length so that we let both 3 and 4 letter words appear.
    """)
    return


@app.cell
def _(chat_fdist, chat_words):
    # adding minimum frequency, allow for both 3 and 4 letter words (how else could you write that conditional?)

    # give me the set of all words in chat_words if the word is 3 or 4 letters long, and is lower case, and occurs over 100 times in the fdist
    set([w for w in chat_words if len(w) <= 4 and len(w) >= 3 and w.islower() and chat_fdist[w] > 100])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What do you see in that output? Any words stand out as representative of a chat corpus? What kinds of words do you think you will find using the same criteria but on a different corpus? The point, which was made in the NLTK book regarding the length of words, is that a single line of code with the right tuning can provide relatively precise insight into the nature of a text and/or corpus.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Your Turn**

    Try the same kind of search on a different text. For example, the cell below loads the words of Jane Austen's *Emma* from the Gutenberg corpus.

    Your goal is to try and refine some search patterns to find words which seem to capture the nature of the text. For example, you could think about a minimum frequency and minimum or maximum length, such as I have done with the chat corpus above.
    """)
    return


@app.cell
def _(FreqDist, nltk):
    # the words of Emma, and their frequency distribution
    emma_words = nltk.corpus.gutenberg.words('austen-emma.txt')
    emma_fdist = FreqDist(emma_words)
    return emma_fdist, emma_words


@app.cell
def _(emma_fdist, emma_words):
    # for example...what is this list comprehension doing? what does `set()` do here?

    set([word.lower() for word in emma_words if emma_fdist[word] == 42])
    return


@app.cell
def _():
    # use this code cell to search Emma with frequency!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Plotting frequency**

    Let's explore frequency visually with yet another text: the short story *They're Made Out of Meat*. The following cell loads the text for us.
    """)
    return


@app.cell
def _(requests):
    # load the story from the internet as a string
    tmoom_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/tmoom.txt'
    tmoom = requests.get(tmoom_url).text
    return (tmoom,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's remove punctuation and lowercase the text. I'll use the regex method.
    """)
    return


@app.cell
def _(re, tmoom):
    # remove punctuation and lowercase the text
    tmoom_cleaned = re.sub(r'[^\w\s]', '', tmoom.lower())
    return (tmoom_cleaned,)


@app.cell
def _(nltk, tmoom_cleaned):
    # about 780 tokens
    tmoom_tokens = nltk.word_tokenize(tmoom_cleaned)
    len(tmoom_tokens)
    return (tmoom_tokens,)


@app.cell
def _(tmoom_tokens):
    # of about 300 types
    tmoom_types = set(tmoom_tokens)
    len(tmoom_types)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that I've cleaned the text up a bit, time to run a frequency distribution on it:
    """)
    return


@app.cell
def _(FreqDist, tmoom_tokens):
    tmoom_fdist = FreqDist(tmoom_tokens)
    return (tmoom_fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since we are concerned with frequency, it's interesting to first see how many words only occur one time in the text:
    """)
    return


@app.cell
def _(tmoom_fdist):
    # hapaxes shows us words with a frequency of 1
    tmoom_fdist.hapaxes()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's look at the top ten most frequent words:
    """)
    return


@app.cell
def _(tmoom_fdist):
    tmoom_fdist.most_common(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's plot the 50 most frequent words, from most to least frequent. We'll use the `matplotlib` library to make the plot. First, we pull the words and their counts out of `.most_common()` into two lists.

    Each item that `.most_common()` gives back is a pair of values in round brackets, like `('the', 72)`. This is called a **tuple**, which is a data container like a list, except that it can't be changed once it's made. In the list comprehension below, `for (word, count) in ...` takes each tuple apart, so that the first value is saved as `word` and the second value is saved as `count`. Then we can keep just the words, or just the counts.

    Then we create the plot using a series of commands to first set the plot data, labels, and other aesthetics. Don't worry too much about this if the plot code is confusing.
    """)
    return


@app.cell
def _(plt, tmoom_fdist):
    # the 50 most frequent words and their counts, as two lists
    tmoom_top_words = [word for (word, count) in tmoom_fdist.most_common(50)]
    tmoom_top_counts = [count for (word, count) in tmoom_fdist.most_common(50)]

    # plot them
    fig1, ax1 = plt.subplots(figsize = (12, 5))
    ax1.plot(tmoom_top_words, tmoom_top_counts)
    ax1.set_xlabel('word')
    ax1.set_ylabel('frequency')
    ax1.tick_params(axis = 'x', labelrotation = 90)
    fig1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the shape of that line: a few words are very frequent, and then frequency takes an absolute nose-dive as we proceed along the x-axis.

    What would the plot look like if we included *every* word, not just the top 50? Let's plot the frequency of every word by its **rank** (1 = most frequent, 2 = second most frequent, and so on):
    """)
    return


@app.cell
def _(plt, tmoom_fdist):
    # the counts of every word, from most to least frequent
    tmoom_all_counts = [count for (word, count) in tmoom_fdist.most_common()]

    # the ranks: 1, 2, 3, ... up to the number of types
    tmoom_ranks = range(1, len(tmoom_all_counts) + 1)

    fig2, ax2 = plt.subplots(figsize = (12, 5))
    ax2.plot(tmoom_ranks, tmoom_all_counts)
    ax2.set_xlabel('rank')
    ax2.set_ylabel('frequency')
    fig2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Do you see where all the hapaxes are? The words with a frequency of 1 form a long flat tail at the bottom of the plot. Compare the number of hapaxes with the number of types: a large share of the types in this text occur only once!

    Let's make a second frequency distribution which leaves out the hapaxes. I loop over the words in `tmoom_fdist`, and only add a word to the new distribution if its frequency is more than 1:
    """)
    return


@app.cell
def _(FreqDist, tmoom_fdist):
    # an empty frequency distribution
    tmoom_fdist_no_hapaxes = FreqDist()

    # copy over every word that occurs more than once
    for tmoom_word in tmoom_fdist:
      if tmoom_fdist[tmoom_word] > 1:
        tmoom_fdist_no_hapaxes[tmoom_word] = tmoom_fdist[tmoom_word]
    return (tmoom_fdist_no_hapaxes,)


@app.cell
def _(tmoom_fdist_no_hapaxes):
    # we can double check that there are no hapaxes left
    tmoom_fdist_no_hapaxes.hapaxes()
    return


@app.cell
def _(tmoom_fdist_no_hapaxes):
    # how many types are left?
    tmoom_fdist_no_hapaxes.B()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Consider how else these plots might change if we removed stopwords or if we took another approach to cleaning the punctuation.

    A frequency distribution will count anything you give it, which means we can apply this same logic to characters as well as tokens. Let's look at the frequency of the letters in the text. I only keep characters which are letters (using `.isalpha()`), which leaves out spaces, newlines and numbers.
    """)
    return


@app.cell
def _(FreqDist, tmoom_cleaned):
    # frequency of every letter in the cleaned text
    tmoom_letter_fdist = FreqDist([character for character in tmoom_cleaned if character.isalpha()])
    return (tmoom_letter_fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's plot the alphabet - what do you think? Does the frequency of these letters make sense?
    """)
    return


@app.cell
def _(plt, tmoom_letter_fdist):
    tmoom_letters = [letter for (letter, count) in tmoom_letter_fdist.most_common()]
    tmoom_letter_counts = [count for (letter, count) in tmoom_letter_fdist.most_common()]

    fig3, ax3 = plt.subplots(figsize = (12, 5))
    ax3.bar(tmoom_letters, tmoom_letter_counts)
    ax3.set_xlabel('letter')
    ax3.set_ylabel('frequency')
    fig3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Zipf's law**

    The shape you saw in the rank plot is one of the most famous patterns in language, known as **Zipf's law**. Zipf's law says that a word's frequency is roughly inversely proportional to its rank:

    - the 2nd most frequent word occurs about 1/2 as often as the most frequent word
    - the 3rd most frequent word occurs about 1/3 as often
    - the 10th most frequent word occurs about 1/10 as often
    - and so on

    This pattern turns up in almost every language and every large corpus. It means a small number of words make up most of any text, while most words are rare.

    Zipf's law is easiest to see with a large corpus. Let's use the whole Brown corpus (about 1 million words), lowercased:
    """)
    return


@app.cell
def _(FreqDist, nltk):
    # frequency distribution of the whole Brown corpus, lowercased and punctuation removed
    brown_fdist = FreqDist([word.lower() for word in nltk.corpus.brown.words() if word.isalpha()])

    # the 10 most frequent words
    brown_fdist.most_common(10)
    return (brown_fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compare the counts above with what Zipf's law predicts. If the most frequent word occurs about 70,000 times, Zipf's law predicts the 2nd word occurs about 35,000 times, and the 10th about 7,000 times. How close is it?

    The cell below plots the frequency of every word by its rank (blue), alongside the frequency that Zipf's law predicts (orange: the most frequent word's count divided by the rank). The left plot shows only the 30 most frequent words, on normal axes, so you can compare each word with its prediction. The right plot shows every word in Brown (about 50,000 types) on **log** axes (base 10), where each step along an axis is 10 times bigger than the last. On log axes, Zipf's law becomes a straight line.
    """)
    return


@app.cell
def _(brown_fdist, plt):
    # the counts of every word in Brown, from most to least frequent, and their ranks
    brown_counts = [count for (word, count) in brown_fdist.most_common()]
    brown_ranks = range(1, len(brown_counts) + 1)

    # Zipf's law prediction: the top count divided by each rank
    zipf_predicted = [brown_counts[0] / rank for rank in brown_ranks]

    fig4, (ax4a, ax4b) = plt.subplots(1, 2, figsize = (12, 5))

    # normal axes, top 30 words only
    brown_top_words = [word for (word, count) in brown_fdist.most_common(30)]
    ax4a.plot(brown_top_words, brown_counts[:30], marker = 'o', label = 'Brown', color = 'red')
    ax4a.plot(brown_top_words, zipf_predicted[:30], marker = 'x', label = "Zipf's law")
    ax4a.set_xlabel('word (in rank order)')
    ax4a.set_ylabel('frequency')
    ax4a.tick_params(axis = 'x', labelrotation = 90)
    ax4a.legend()

    # log axes
    ax4b.plot(brown_ranks, brown_counts, label = 'Brown', color = 'red')
    ax4b.plot(brown_ranks, zipf_predicted, label = "Zipf's law")
    ax4b.set_xscale('log')
    ax4b.set_yscale('log')
    ax4b.set_xlabel('rank (log scale)')
    ax4b.set_ylabel('frequency (log scale)')
    ax4b.legend()

    fig4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Where does Brown follow Zipf's law closely, and where does it drift away? What does Zipf's law suggest about how much of a text you could understand if you only knew the 1,000 most frequent words?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Comparing frequency distributions**

    So far we've looked at one text at a time. Now we begin to compare frequencies of items across different datasets. Let's begin with some very simple examples.

    Create two lists which represent two conditions: condition a and condition b.

    The lists each contain tokens of colour, and we can see that while both lists have the same number of tokens (five), they differ in terms of the distributions of those tokens. Specifically, `condition_a` has yellow twice, and blue three times, while `condition_b` has one yellow, three blue, and one red.
    """)
    return


@app.cell
def _():
    # make our conditions
    condition_a = ['yellow', 'yellow', 'blue', 'blue', 'blue']
    condition_b = ['yellow', 'blue', 'blue', 'blue', 'red']
    return condition_a, condition_b


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can combine these conditions into a single list to count the frequencies of the colours:
    """)
    return


@app.cell
def _(condition_a, condition_b):
    # combine the conditions
    combined_conditions = condition_a + condition_b

    # now everything is in one list
    combined_conditions
    return (combined_conditions,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we ask for a `FreqDist()` of the combined conditions, we get an impression of frequency among these three colours:
    """)
    return


@app.cell
def _(FreqDist, combined_conditions):
    # combined frequency distribution
    color_fdist = FreqDist(combined_conditions)
    color_fdist
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    However we have no way of knowing whether any one colour "likes" one condition over the other, or whether these colours occur equally among our conditions. So we could run a frequency distribution on each condition, separately:
    """)
    return


@app.cell
def _(FreqDist, condition_a):
    # Frequency Distribution of condition a
    condition_a_fdist = FreqDist(condition_a)
    condition_a_fdist
    return


@app.cell
def _(FreqDist, condition_b):
    # Frequency distribution of condition b
    condition_b_fdist = FreqDist(condition_b)
    condition_b_fdist
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can compare the output and see that the two different conditions have different amounts of each colour. This works fine for now, but only because we have the same number of items in each condition. In reality, your texts and corpora will all be of different lengths. We need to start worrying about normalisation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Normalising frequency counts**

    (Note that *normalising* means something different here than in the tokenisation and preprocessing notebook. There, we normalised the *text*, by lowercasing it and removing punctuation, so that different versions of the same word are counted together. Here, we normalise the *counts*, so that we can compare texts and corpora of different sizes.)

    Most corpora have a different total number of words. Let's invent an extreme example and pretend that Corpus A has 1000 words and Corpus B has 100 words. How could we interpret the following counts?

    |Corpus|Word|Raw Frequency|
    |--|--|--|
    |A|Blue|10|
    |B|Blue|5|

    On its face, the frequency of "Blue" in Corpus A is twice as much as Corpus B. However, Corpus A has 10 times as many tokens as Corpus B, and thus many more chances for words to occur. We actually cannot make a clear comparison about whether the word Blue occurs more frequently in Corpus A or Corpus B. We need to somehow normalise this frequency between the two corpora.

    An easy way is to divide the raw frequency of the word by the total size of the corpus. This provides us with a percentage of occurrence, rather than a raw frequency.

    In this example, the table would become:

    |Corpus|Word|Raw Frequency| Freq %|
    |--|--|--|--|
    |A|Blue|10|10/1000 = 0.01 = 1%|
    |B|Blue|5|5/100 = 0.05 = 5% |

    Ah...we now reach a very different conclusion! The word Blue occurs only 1% of the time in Corpus A, whereas it occurs 5% of the time in Corpus B. From this data, we might now conclude that, ***on average***, Blue occurs more frequently in Corpus B when compared to Corpus A.

    ### Per million words

    Percentages work well for very frequent words, but most words are rare, so their percentages are tiny and hard to read (e.g., 0.00031%). Corpus linguists therefore usually report frequency per some normalised standard, such as **per million words**: divide the raw frequency by the corpus size, then multiply by 1,000,000 instead of 100.

    $$
    \text{frequency per million} = \frac{\text{raw frequency}}{\text{number of tokens}} \times 1{,}000{,}000
    $$
    """)
    return


@app.cell
def _():
    # Blue in Corpus A and Corpus B, per million words
    print(f"Corpus A: {10 / 1000 * 1000000} per million")
    print(f"Corpus B: {5 / 100 * 1000000} per million")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's try this out using the Brown corpus. The corpus contains different categories of genres, and we might want to compare the distribution of a particular word (or words) across these genres. First let's look at the categories.
    """)
    return


@app.cell
def _():
    from nltk.corpus import brown

    # here are all the categories in brown:
    brown.categories()
    return (brown,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As a reminder, we can access the tokenised text using the `.words()` method and specifying the category:
    """)
    return


@app.cell
def _(brown):
    brown.words(categories = 'romance')[:10]
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So what could we do if we wanted to create a frequency distribution of the words for each of the categories in the Brown corpus? We could manually save a FreqDist for each category, but that would be a lot of typing.

    Instead, let's loop through the categories and store the results in a dictionary (you'll learn more about dictionaries in the dictionaries notebook). In the cell below, do you see how the names of the categories are used to loop through the Brown corpus but also create the name of each key in the dictionary?
    """)
    return


@app.cell
def _(FreqDist, brown):
    # initialise an empty dictionary
    fdist_dict = {}

    # now create a frequency distribution of each category, and save in the dictionary
    for category in brown.categories():
      fdist_dict[category] = FreqDist(brown.words(categories = category))
    return (fdist_dict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Confirm the keys are the different categories:
    """)
    return


@app.cell
def _(fdist_dict):
    fdist_dict.keys()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can basically do anything we want with this output now. Let's first verify that the sizes of each distribution are indeed different. What do you see in this output? How comparable are the different categories?
    """)
    return


@app.cell
def _(fdist_dict):
    for category1 in fdist_dict:
      print(f"{category1}:\n{fdist_dict[category1].B()} types \t{fdist_dict[category1].N()} tokens\n")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's use the same approach to count the frequency of certain words. For example, how about the word `the`?

    The print statement might be confusing. Note that the fstring is first printing the name of the dictionary key, and then using that same name to access that frequency distribution in the dictionary, before finally asking for the frequency of a single word (in this case, the word "the").

    (The loops in this section use `category1`, `category2` and so on, because marimo only lets each variable be created in one cell.)
    """)
    return


@app.cell
def _(fdist_dict):
    for category2 in fdist_dict:
      print(f"{category2}: {fdist_dict[category2]['the']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can adapt the loop to normalise the frequency by the size of each category. We now see much more comparable distributions, with most categories around 5%. Can you see the two that are higher and lower than ~5%? What might explain these differences?
    """)
    return


@app.cell
def _(fdist_dict):
    print('relative frequency of "the" in Brown categories')
    for category3 in fdist_dict:
      print(f"{category3}: {(fdist_dict[category3]['the'] / fdist_dict[category3].N()) * 100}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now be a bit more selective and ask for specific words in specific categories, similar to what is done in the NLTK Book. We create a list of categories and target words, then write a double loop to compare the frequencies of the words.

    [Modal verbs](https://en.wikipedia.org/wiki/Modal_verb) are auxiliary verbs which provide a level of certainty, possibility, or urgency upon a main verb. In English, these are words such as *must*, *will*, *could*, etc.
    """)
    return


@app.cell
def _():
    # create a list of some Brown genres
    genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']

    # create a list of modals
    modals = ['can', 'could', 'may', 'might', 'must', 'will']
    return genres, modals


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I have a double loop below that first loops through each target word. For each word, the loop then goes through each category, printing 1. the total length of the sub-corpus, 2. the raw frequency of the modal, and 3. the frequency of the modal per million words.

    This should give you a good understanding of why it is important to use normalised frequencies rather than raw counts when comparing. In what instances would relying on raw frequencies lead to a misleading conclusion?
    """)
    return


@app.cell
def _(fdist_dict, genres, modals):
    for modal in modals:
      print(f'information for {modal.upper()}\n')
      for genre in genres:
        print(f'\ttotal tokens in {genre}: {fdist_dict[genre].N()}')
        print(f'\traw frequency for *{modal}* in {genre}: {fdist_dict[genre][modal]}')
        print(f'\tper million words for *{modal}* in {genre}: {round(fdist_dict[genre][modal] / fdist_dict[genre].N() * 1000000)}\n')
      print('='*10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Range: is a frequent word also a widespread word?**

    Frequency tells us how often a word occurs, but not *where* it occurs. Two words can have the same frequency, but one might be spread evenly across a corpus while the other is packed into a few texts or genres.

    Corpus linguists call this **dispersion**. The simplest measure of dispersion is **range**: the number of texts (or categories) in which a word appears at least once.

    The function below calculates the range of a word across the 15 Brown categories, using the frequency distributions in `fdist_dict`:
    """)
    return


@app.cell
def _(fdist_dict):
    def brown_range(word):
      # count how many categories the word appears in
      number_of_categories = 0
      for category in fdist_dict:
        if fdist_dict[category][word] > 0:
          number_of_categories = number_of_categories + 1
      return number_of_categories

    return (brown_range,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's compare two words with almost the same frequency in Brown: *policy* and *true*. First, their total frequencies:
    """)
    return


@app.cell
def _(FreqDist, brown):
    # total frequency of each word in Brown (not lowercased, to match fdist_dict)
    brown_raw_fdist = FreqDist(brown.words())

    print(f"policy: {brown_raw_fdist['policy']}")
    print(f"true:   {brown_raw_fdist['true']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Very similar! Now their range:
    """)
    return


@app.cell
def _(brown_range):
    print(f"policy appears in {brown_range('policy')} of 15 categories")
    print(f"true appears in {brown_range('true')} of 15 categories")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To see *where* each word is, let's print its frequency per million words in every category:
    """)
    return


@app.cell
def _(fdist_dict):
    for category4 in fdist_dict:
      policy_per_million = round(fdist_dict[category4]['policy'] / fdist_dict[category4].N() * 1000000)
      true_per_million = round(fdist_dict[category4]['true'] / fdist_dict[category4].N() * 1000000)
      print(f"{category4}: \t policy {policy_per_million} \t true {true_per_million}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Policy* is concentrated in a few categories (such as government and learned writing), while *true* is spread across all of them. If you were making a list of words that learners of English should know, which of these two would you want, and why? What does this tell you about using frequency alone?

    Try some other words in the cell below. Some to start with: *Kennedy*, *God*, *tax*, *love*.
    """)
    return


@app.cell
def _():
    # use this code cell to find the range of other words!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Frequency over time: inaugural addresses**

    Chapter 2 of the NLTK book looks at how the words *america* and *citizen* change in frequency across the inaugural addresses of US presidents (one occurs every four years). Let's do the same thing using the tools from this notebook.

    First, load in the corpus and look at the file names:
    """)
    return


@app.cell
def _():
    from nltk.corpus import inaugural

    # each file id contains the year and name of the US president
    inaugural.fileids()
    return (inaugural,)


@app.cell
def _(inaugural):
    # remember, raw returns a string from the .txt file.
    # here I pick a set of words from the string to find an interesting quote.
    inaugural.raw('1945-Roosevelt.txt')[1025:1152]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Slicing metadata from filenames

    How can we find out the year of each address? The answer is that the information is included in the filename. Each filename in the inaugural corpus is in this format:

    ```
    YEAR-name.txt
    ```

    Slicing up to 4 on the filename will return the first four characters of the filename, which happens to be the year. So this is a trick that would only work if all the filenames are standardised to follow the same format.
    """)
    return


@app.cell
def _():
    # use this one simple trick to get years!
    '1945-Roosevelt.txt'[:4]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Counting *america* and *citizen*

    The loop below goes through every address. For each one, it:

    1. lowercases the words of the address
    2. counts the words that start with `america` (so *america*, *american*, *americans* all count) and `citizen` (*citizen*, *citizens*, *citizenship*), using `.startswith()`
    3. saves the year, the raw counts, and the counts **per 1,000 words**

    (Inaugural addresses are short, so per 1,000 words gives easier numbers to read than per million.)
    """)
    return


@app.cell
def _(inaugural):
    # lists to store the results
    inaugural_years = []
    america_raw = []
    citizen_raw = []
    america_per_1000 = []
    citizen_per_1000 = []

    for address_id in inaugural.fileids():
      # lowercase the words of this address
      address_words = [word.lower() for word in inaugural.words(address_id)]

      # count the words starting with 'america' and 'citizen'
      america_count = len([word for word in address_words if word.startswith('america')])
      citizen_count = len([word for word in address_words if word.startswith('citizen')])

      # save the year, the raw counts, and the counts per 1,000 words
      inaugural_years.append(int(address_id[:4]))
      america_raw.append(america_count)
      citizen_raw.append(citizen_count)
      america_per_1000.append(america_count / len(address_words) * 1000)
      citizen_per_1000.append(citizen_count / len(address_words) * 1000)
    return (
        america_per_1000,
        america_raw,
        citizen_per_1000,
        citizen_raw,
        inaugural_years,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's plot the raw counts (left) and the counts per 1,000 words (right). What is it the authors of NLTK wanted you to notice about the use of *america* and *citizen* in inaugural addresses over time? Does normalising change the story?
    """)
    return


@app.cell
def _(
    america_per_1000,
    america_raw,
    citizen_per_1000,
    citizen_raw,
    inaugural_years,
    plt,
):
    fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize = (14, 5))

    # raw counts
    ax5a.plot(inaugural_years, america_raw, label = 'america')
    ax5a.plot(inaugural_years, citizen_raw, label = 'citizen')
    ax5a.set_title('raw counts')
    ax5a.set_xlabel('year')
    ax5a.legend()

    # per 1,000 words
    ax5b.plot(inaugural_years, america_per_1000, label = 'america')
    ax5b.plot(inaugural_years, citizen_per_1000, label = 'citizen')
    ax5b.set_title('per 1,000 words')
    ax5b.set_xlabel('year')
    ax5b.legend()

    fig5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Discussion**

    - When are raw counts misleading?
    - Is a frequent word also a widespread one? Why might it matter for a study which one you measure?
    - Zipf's law says most words in any corpus are rare. What does that mean for a researcher trying to study a particular word with a small corpus?
    """)
    return


if __name__ == "__main__":
    app.run()
