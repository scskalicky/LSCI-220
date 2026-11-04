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

    [NLTK Book, Chapter 1, Section 3.3](https://www.nltk.org/book/ch01.html#bigrams_index_term)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **“You shall know a word by the company it keeps"**

    [Firth](https://en.wikipedia.org/wiki/John_Rupert_Firth)

    This quote embodies the concept of *collocational meaning* — the idea that the true meaning of words is only realised when words are used in the context of *other* words.

    Here is a dictionary definition of collocation (Oxford Languages):

    > **collocation** (*Linguistics*): the habitual juxtaposition of a particular word with another word or words with a frequency greater than chance.

    Note how the linguistic definition includes an additional qualification about habitual co-occurrence. Collocations are not just words which occur next to another word, they are words which co-occur *non-randomly* - at a rate higher than chance.

    How do we know which words occur non-randomly or not? Think of the corpora that you've already seen thus far — large corpora such as Brown (and much, much larger than Brown) allow us to mine not just frequently occurring single words, but also frequently occurring word pairs, triplets, and even longer segments. Statistical measures of word co-occurrence probabilities provide insight into natural language and are also responsible for the ever-increasing accuracy of automatic NLP algorithms used today.

    Statistical knowledge of collocations is not just present in corpora, but is also a function of becoming proficient in a language. This [Wikipedia article](https://en.wikipedia.org/wiki/English_collocations) contains a decent explanation of some collocations in English. Consider these examples, which show how some word pairs seem natural / correct, whereas others do not:

    | Natural English | Unnatural English |
    |---|---|
    | the fast train | the quick train |
    | fast food | quick food |
    | a quick shower | a fast shower |
    | a quick meal | a fast meal |

    Note that none of the word combinations in the "unnatural English" column are ungrammatical, rather it's just that they seem to be odd combinations particularly when compared to the versions in the "natural English" column. Collocations are extracted from large corpora of language and are thought to reflect language use, which is in turn reflected by our interpretation of which of these collocations seems right and which seem odd.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Bigrams vs. collocations

    As was shown above, collocations are defined as words which are statistically more likely to occur with each other when compared to other words. Collocations can stretch beyond two words, to three, four, or more word partners.

    A related but crucially different term is the term **bigrams**. In NLP, the term `bigram` means a sequence of two tokens, and technically can mean *any pair of adjacent words in a text*. The more general terminology is `n-grams`, where the `n` can stand for any number. So you can have bigrams (two words), trigrams (three words), and so on. You may find that sometimes people conflate `collocation` with `ngram`, but what they probably are referring to are unusually frequent n-grams when compared to other n-grams, especially when taking into account individual word frequencies.

    Simply put, the relationship between collocations and bigrams is that all collocations are bigrams (or, more accurately, n-grams), but not all n-grams are collocations. In order to be upgraded from n-gram to collocation, it must be shown that the n-gram occurs more frequently than would be allowed by chance.

    So, collocations are defined based on statistical co-occurrence frequencies: collocations are thus two or more words which are more likely to occur with one another when compared to other words, controlled for each word's individual word frequency.

    ### locating bigrams and collocations in text

    How can we locate bigrams or collocations in a text? Bigrams (and other n-grams) can be found using a `for loop` and functions like `enumerate`. Collocations are a bit trickier and require obtaining measures of probability and other statistical associations.

    However, NLTK has two functions which calculate these values for us — `bigrams` and `collocations`. Let's start with `bigrams`
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import math
    import requests
    import polars as pl
    import nltk
    from nltk import FreqDist
    from nltk.text import Text
    from nltk.collocations import BigramCollocationFinder
    from nltk.metrics import BigramAssocMeasures
    from nltk.tokenize import MWETokenizer

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'averaged_perceptron_tagger_eng', 'webtext', 'gutenberg', 'brown', 'universal_tagset'])
    return (
        BigramAssocMeasures,
        BigramCollocationFinder,
        FreqDist,
        MWETokenizer,
        Text,
        math,
        nltk,
        pl,
        requests,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **using `nltk.bigrams()`**

    The function to create bigrams in NLTK is relatively straightforward. We just need to call the function on a tokenized text and the function will return a list of all the bigrams in the text (sequentially). If we do not provide tokens, we would instead obtain the bigrams of characters in a string!
    """)
    return


@app.cell
def _(nltk):
    # create a sample sentence
    great_quote = 'we live in a society!'

    # use nltk bigrams (wrapping it in list() provides us with the output right away)
    list(nltk.bigrams(nltk.word_tokenize(great_quote)))
    return (great_quote,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You should be able to inspect the output and get an idea for what's going on. This function is simply starting with the first token in the list, making a pair with the second token, then moving on to the second token, making a pair with the third token, and so on. We can conceptualise how this works with a pseudo formula:

    First we would loop through a sentence:

    > `for n:m in a sentence (where n = the first token and m = the final token)`

    Then we would iterate ahead by one and add that to the current loop value

    > `output = (n, n1), (n1, n2), (n2, n3) ... (m-1, m)`

    Is it that simple, can we produce the bigrams in the same way that the NLTK module has? One excellent function which can help us with this is `enumerate()`!

    Check out the code below - you can see that it was relatively easy to get the same basic functionality from NLTK with our own code. Take a moment to study what I've had to do in order to prevent index errors.
    """)
    return


@app.function
# use enumerate to make bigrams by asking for adjacent words until we get to the end of the sentence.
def bootleg_bigram(tokens):
  for i, word in enumerate(tokens):
    if i != len(tokens)-1: # what is the role of this line?
      print((tokens[i], tokens[i + 1]))


@app.cell
def _(great_quote, nltk):
    # Test out bootleg_bigram on the same text.
    bootleg_bigram(nltk.word_tokenize(great_quote))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    Spend some time using `nltk.bigrams()` on some text/strings. Make sure you understand what it is doing, and also compare the output to the `bootleg_bigram()` function.
    """)
    return


@app.cell
def _():
    # play with nltk.bigrams() here.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Bigrams and Parts of Speech**

    If we annotate the bigrams in a text with part of speech tags, we can start to obtain patterns that reflect the grammar of a language.

    Let's use `nltk.bigrams()` on a set of part of speech tagged tokens — this will create a set of `((word, tag) , (word, tag))` pairs.
    """)
    return


@app.cell
def _(nltk):
    # tag a sentence
    rant = "You know, we're living in a society! We're supposed to act in a civilized way."
    rant_pos = nltk.pos_tag(nltk.word_tokenize(rant))

    # create bigrams of the pos tagged sentence
    rant_bigrams = list(nltk.bigrams(rant_pos))

    # inspect the bigrams
    rant_bigrams
    return (rant_bigrams,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have the part of speech information included with our tokens, we can shift our search patterns away from the orthographic forms of words to instead the part of speech of words. This allows us to find more abstract patterns in language associated with word *categories* rather than with the forms of words themselves.

    For instance, let's look for all words in our example which come before nouns. This requires a bit of indexing, because we are looping through pairs set within a single tuple

    ```
    ((word, tag), (word, tag))
    ```

    So to access the word in the first pair, we would first index the larger tuple using `[0]` to get the first `(word, tag)` pair, then index that pair using `[0]` to get the first part of `(word, tag)`, which would be the word. This is demonstrated in the next code cell
    """)
    return


@app.cell
def _(rant_bigrams):
    for tagged_bigram in rant_bigrams:
      print(tagged_bigram[0][0]) # index the first nested tuple, then index that tuple's first value
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Another strategy would be to follow the NLTK book's guide and set the tuple pair as the iterator, allowing you to index the tuple in a more transparent way.

    ```
    [a for (a,b) in bigrams]
    ```
    """)
    return


@app.cell
def _(rant_bigrams):
    # you can select the first pair of each pair
    [a for (a, b) in rant_bigrams]
    return


@app.cell
def _(rant_bigrams):
    # or the second
    [b for (a,b) in rant_bigrams]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's steal the example from NLTK and find all the words which precede nouns in this example. Do the results make sense?
    """)
    return


@app.cell
def _(rant_bigrams):
    noun_preceders = [a for (a, b) in rant_bigrams if b[1] == 'NN']
    noun_preceders
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    What do you notice about the words which come before nouns?

    - Apply the strategy above to a longer text of your choice
    - Do you find the same words appearing in front of nouns? What patterns are you noticing?
    - Do the findings make sense in terms of what you know about nouns?
    """)
    return


@app.cell
def _():
    # use this code cell to look at the words before nouns in a longer text!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **using `.collocations()`**

    The NLTK `.collocations()` function will give us the bigrams which are unusually frequent when also considering the frequency of the individual words in the bigrams. Under the hood, NLTK ranks the bigrams using a statistic called the **log-likelihood ratio**, which compares how often two words occur together with how often we would expect them to if they were independent. We will calculate a simpler measure of association ourselves later in this notebook.

    Unlike `nltk.bigrams()`, the `.collocations()` function is a method specific to NLTK `Text` objects. We can make a `Text` from the words of any corpus. Let's make two: the script of *Monty Python and the Holy Grail* (from NLTK's `webtext` corpus), and G. K. Chesterton's novel *The Man Who Was Thursday* (from the Gutenberg corpus).
    """)
    return


@app.cell
def _(Text, nltk):
    # make Text objects from the words of two corpora
    holy_grail = Text(nltk.corpus.webtext.words('grail.txt'))
    thursday = Text(nltk.corpus.gutenberg.words('chesterton-thursday.txt'))
    return holy_grail, thursday


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The output of `.collocations()` will be a series of bigrams separated by semicolons `;`

    So let's look at the collocations for each text. The collocations for *Holy Grail* include `BLACK KNIGHT` and `clop clop`. The collocations for *Thursday* include `old gentleman` and `Scotland Yard`.

    - What do you think it is about the text which is creating these collocations?
    - Do you think these same collocations would be found in the other texts?
    - What might this tell us about the power of using collocations / ngrams if we wanted to predict where documents came from (e.g., guessing the genre, guessing the author)?
    """)
    return


@app.cell
def _(holy_grail):
    # what are the collocations of Holy Grail?
    holy_grail.collocations()
    return


@app.cell
def _(thursday):
    # examine the collocations of The Man Who Was Thursday.
    # What do you know about this book, without having read it?
    thursday.collocations()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The default number of collocations returned is 20, but you can ask for more
    """)
    return


@app.cell
def _(thursday):
    thursday.collocations(num = 50)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There is also a `window_size` argument, which by default is 2, meaning that it only looks for adjacent collocations. Increasing this number will increase the span that collocations can occur in, loosening the restrictions and allowing for words to appear between the collocates. [This post has a good example.](https://github.com/nltk/nltk/issues/907)

    Notice how the collocations change when we adjust the window size:
    """)
    return


@app.cell
def _(holy_grail):
    holy_grail.collocations(num = 5, window_size = 2)
    return


@app.cell
def _(holy_grail):
    holy_grail.collocations(num = 5, window_size = 3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **big salad bigram strength**

    Remember that collocations are bigrams which like each other very much. The presence of one word in the bigram is a strong cue for the presence of the other word. Said differently, the calculations for what makes a bigram a collocation (or just a sequence of two words) will take into account the frequency of the words in a collocation when compared to the overall frequency of the words outside of the collocation.

    So collocations are really strong bigrams.

    Can we determine the strength of bigrams using a combination of `FreqDist` and `bigrams`?

    Let us find out by using a text file with over 100 Seinfeld scripts in it (Big Salad):
    """)
    return


@app.cell
def _(requests):
    # load the Big Salad from the course repository
    big_salad = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/big_salad.txt').text
    return (big_salad,)


@app.cell
def _(big_salad):
    # Look at a random quote
    big_salad[1300:1360]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's go ahead and normalise the text a bit:

    - remove punctuation
    - lowercase the text
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


@app.cell
def _(big_salad):
    big_salad_cleaned = pre_process(big_salad)
    return (big_salad_cleaned,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use `nltk.word_tokenize()` to create word tokens:
    """)
    return


@app.cell
def _(big_salad_cleaned, nltk):
    # tokenize
    big_salad_tokens = nltk.word_tokenize(big_salad_cleaned)
    return (big_salad_tokens,)


@app.cell
def _(big_salad_tokens):
    #how many tokens?
    len(big_salad_tokens)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And then create the list of bigrams in the text:
    """)
    return


@app.cell
def _(big_salad_tokens, nltk):
    # create the bigrams- wrapping in list to get the data right away
    big_salad_bigrams = list(nltk.bigrams(big_salad_tokens))
    return (big_salad_bigrams,)


@app.cell
def _(big_salad_bigrams):
    big_salad_bigrams[:17]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have a single list of bigrams, we can use `FreqDist()` to create a frequency distribution of the bigrams.
    """)
    return


@app.cell
def _(big_salad_bigrams, nltk):
    # create the frequency distribution
    big_salad_bigram_fdist = nltk.FreqDist(big_salad_bigrams)
    return (big_salad_bigram_fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What are the most frequent bigrams in this data?
    """)
    return


@app.cell
def _(big_salad_bigram_fdist):
    big_salad_bigram_fdist.most_common(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The most frequent bigram in this output is `(you, know)`. How strong is the bond between these two words? In order to fully investigate this, we need to compare the individual word frequency against the bigram frequency. So, we could create a frequency distribution of the entire text to obtain single word frequency, and compare that to bigram frequency.
    """)
    return


@app.cell
def _(big_salad_tokens, nltk):
    # create a FreqDist of the entire set of words
    big_salad_fdist = nltk.FreqDist(big_salad_tokens)
    return (big_salad_fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have a frequency distribution of both single words and bigrams, we can compare individual word frequencies against bigram frequencies. One simple way to determine the strength of attraction between two words is the relative proportion of that word occurring with one word compared to all other words - a percentage of co-occurrence.
    """)
    return


@app.cell
def _(big_salad_fdist):
    # the word "you" occurs ~17k times
    big_salad_fdist['you']
    return


@app.cell
def _(big_salad_bigram_fdist):
    # the bigram 'you know' occurs 1777 times
    big_salad_bigram_fdist[('you', 'know')]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So out of the ~17k times the word "you" occurs, 1777 of those times are with the word "know". This means about ~10% of the occurrences of `you` are in this combination, which seems relatively strong.

    Another way to test the strength of this relationship is to find all of the other bigrams that `you` occurs within and then see which proportion of those bigrams are `'you know'` bigrams. How could we do this?  Firstly, we could obtain a set of all the bigrams that start with `you`. We can do this with a conditional that checks the first value of each bigram. We access the first element using an index: `bigram[0]`
    """)
    return


@app.cell
def _(big_salad_bigram_fdist):
    # obtain a set of all bigrams starting with 'you'
    you_bigrams = set([bigram for bigram in big_salad_bigram_fdist if bigram[0] == 'you'])

    you_bigrams
    return (you_bigrams,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **relative probabilities**

    Having obtained this set, we could find how often the second word in the bigram appears with and without the word 'you'. If the word only occurs with 'you', then we might have located a word that strongly likes "you" (and thus might be a collocate).

    To do so, we can divide the frequency of the bigram against the frequency of the second word in the bigram, like this:

    <br>
    $$
    \frac{\text{frequency of (w1, w2)}}{\text{frequency of w2}}
    $$
    <br>

    Let's create a dictionary which stores the probability of every second word in a `you` bigram
    """)
    return


@app.cell
def _(big_salad_bigram_fdist, big_salad_fdist, you_bigrams):
    you_bigram_strengths = dict()

    for bigram in you_bigrams:
      # indexing gets the second word in the you bigrams
      you_bigram_strengths[bigram[1]] = big_salad_bigram_fdist[bigram] / big_salad_fdist[bigram[1]]
    return (you_bigram_strengths,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we have a dictionary of the proportion of times certain words pair with 'you' - let's look at 'know' - the result is about 50% of the time. So, this means that if you see the word `know` in this data, there is a 50% probability the word *before* `know` is `you`! That's pretty high!
    """)
    return


@app.cell
def _(you_bigram_strengths):
    you_bigram_strengths['know']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Pointwise Mutual Information**

    The proportional frequency is useful and highly interpretable. But what about a fancier metric, such as pointwise mutual information scores? This is a common metric in corpus linguistics which can provide us with the strength of association between two words, The calculation is a bit more complex, but is understandable with a bit of effort.

    Firstly, here is the entire formula:

    $$
    \text{PMI}(w_1, w_2) = \log_2 \left( \frac{P(w_1, w_2)}{P(w_1) \cdot P(w_2)} \right)
    $$

    Where:

    - $P(w_1, w_2)$ is the probability of the bigram $(w_1, w_2)$.
    - $P(w_1)$ and $P(w_2)$ are the probabilities of the individual words.

    What does this mean? Focus on the right side of the formula, in the brackets. The $P$ stands for the probability of something. So $P(w1)$ would mean "the probability of word1 occurring in the corpus". This is calculated by dividing the total frequency of a word by the total number of tokens in a text. We know how to do this using a `FreqDist()` and `len()` of a text. Here is the probability of `you` in Big Salad: 3.5%
    """)
    return


@app.cell
def _(big_salad_fdist, big_salad_tokens):
    big_salad_fdist['you'] / len(big_salad_tokens)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we extend this logic about the probability of single words to the probability of bigrams. To find the probability of the bigram 'you know', which is $P(\text{you, know})$, we divide the frequency of that bigram by the total number of bigrams. The probability is very small, less than 1%:
    """)
    return


@app.cell
def _(big_salad_bigram_fdist, big_salad_bigrams):
    big_salad_bigram_fdist[('you', 'know')] / len(big_salad_bigrams)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The only other piece of information we need is the probability of the second word in the bigram: `know`.
    """)
    return


@app.cell
def _(big_salad_fdist, big_salad_tokens):
    big_salad_fdist['know'] / len(big_salad_tokens)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can calculate the PMI. We use the `log2` function from the `math` library (imported at the top of the notebook). Then I copy the raw calculations over and we obtain a PMI of 3.826.
    """)
    return


@app.cell
def _(
    big_salad_bigram_fdist,
    big_salad_bigrams,
    big_salad_fdist,
    big_salad_tokens,
    math,
):
    math.log2((big_salad_bigram_fdist[('you', 'know')] / len(big_salad_bigrams)) / (big_salad_fdist['you'] / len(big_salad_tokens) * (big_salad_fdist['know'] / len(big_salad_tokens))))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is the formula again expressed in terms of the individual probability calculations:

    $$
    \text{PMI}(w_1, w_2) = \log_2 \left( \frac{\text{frequency of } (w_1, w_2)}{\text{total number of bigrams}} \div \left( \frac{\text{frequency of } w_1}{\text{total number of tokens}} \times \frac{\text{frequency of } w_2}{\text{total number of tokens}} \right) \right)
    $$
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now don't worry if that formula still doesn't make complete sense to you. We can use what we know to make a function which calculates PMI.

    We have already made the tokens, the bigrams and both frequency distributions for the Big Salad, so the function can use those directly: we only need to give it the two words. If the bigram doesn't occur in the text at all, the PMI can't be calculated (we can't take the log of zero), so the function checks for that first.
    """)
    return


@app.cell
def _(
    big_salad_bigram_fdist,
    big_salad_bigrams,
    big_salad_fdist,
    big_salad_tokens,
    math,
):
    def pmi(w1, w2):
      """
      calculates the pointwise mutual information of two words in the Big Salad

      Args:
        w1 (str): the first word of bigram.
        w2 (str): the second word of a bigram

      Returns:
        the PMI score for w1 and w2
      """

      # check if the bigram exists in the fdist, end the function if the freq is 0
      if big_salad_bigram_fdist[(w1, w2)] == 0:
        print(f"The bigram ('{w1}', '{w2}') does not exist in the text.")
        return None

      # gather frequencies needed to calculate PMI
      p_bigram = big_salad_bigram_fdist[(w1, w2)] / len(big_salad_bigrams)
      p_w1 = big_salad_fdist[w1] / len(big_salad_tokens)
      p_w2 = big_salad_fdist[w2] / len(big_salad_tokens)

      # calculate the PMI
      return math.log2(p_bigram / (p_w1 * p_w2))

    return (pmi,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that the function is created, we can query the PMI between any two words in a bigram! Let's calculate this for the bigram `you know`. We get the same value as above.
    """)
    return


@app.cell
def _(pmi):
    pmi('you', 'know')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I always like to check my work. Guess what: NLTK has a way to find the pointwise mutual information! We need to first import two things: a collocation finder class and an association measure class:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the `BigramCollocationFinder.from_words()` function to create all of the bigrams and their frequencies. I do so below and save the results to a variable:
    """)
    return


@app.cell
def _(BigramCollocationFinder, big_salad_tokens):
    big_salad_bigram_finder = BigramCollocationFinder.from_words(big_salad_tokens)
    return (big_salad_bigram_finder,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We don't see much by looking at it on its own:
    """)
    return


@app.cell
def _(big_salad_bigram_finder):
    big_salad_bigram_finder
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But we can ask for the entire frequency distribution with `.ngram_fd`
    """)
    return


@app.cell
def _(big_salad_bigram_finder):
    big_salad_bigram_finder.ngram_fd
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also use the `.most_common()` method from the Frequency Distribution:
    """)
    return


@app.cell
def _(big_salad_bigram_finder):
    big_salad_bigram_finder.ngram_fd.most_common(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And also query the frequency of a specific bigram:
    """)
    return


@app.cell
def _(big_salad_bigram_finder):
    big_salad_bigram_finder.ngram_fd[('you', 'know')]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Anyhow, with this bigram finder, we can use `BigramAssocMeasures` to then calculate association metrics (such as PMI) for any two words:
    """)
    return


@app.cell
def _(BigramAssocMeasures, big_salad_bigram_finder):
    # calculate PMI for 'you know' with NLTK - do we get the same result?
    big_salad_bigram_finder.score_ngram(BigramAssocMeasures.pmi, 'you', 'know')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The results are both 3.826, which verifies our earlier manual calculation.

    But, the number itself is kind of meaningless without something to compare to. Let's compare two other bigrams. Which one do you expect to be the stronger collocation?
    """)
    return


@app.cell
def _(pmi):
    pmi('you', 'maestro')
    return


@app.cell
def _(pmi):
    pmi('you', 'ratted')
    return


@app.cell
def _(pmi):
    # what happens with a bigram that isn't in the text?
    pmi('you', 'yadda')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **PMI loves rare words**

    *You ratted* has a higher PMI than *you know* (about 4.8 vs 3.8), even though *you ratted* occurs only once and *you know* is one of the most common phrases in the whole script. Why?

    Look at the formula again: PMI compares how often the pair occurs with how often we'd *expect* it to occur if the two words were independent. *Ratted* is a rare word, so we'd expect *you ratted* to occur almost never. If it occurs even a couple of times, that's far more than expected, so PMI is high. *Know* is a very common word, so *you know* is expected to occur fairly often anyway.

    This is a well-known property of PMI: it gives very high scores to pairs of rare words, even pairs that only occur once or twice. That's one reason there are many different association measures, and why they often disagree.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Delta P: a directional measure**

    Earlier, we calculated the proportion of times `know` comes after `you` (about 50%). That is a *directional* question: given one word, how likely is the other?

    **Delta P** (written ΔP) builds on that idea. It asks: how much more likely is word 2 when word 1 comes right before it, compared to when word 1 doesn't?

    $$
    \Delta P(w_2 \mid w_1) = P(w_2 \mid w_1) - P(w_2 \mid \text{not } w_1)
    $$

    - $P(w_2 \mid w_1)$: of all the times `w1` occurs, what proportion are followed by `w2`?
    - $P(w_2 \mid \text{not } w_1)$: of all the *other* positions in the text, what proportion are `w2`?

    ΔP ranges from -1 to 1. A value near 0 means `w1` tells us nothing about whether `w2` is coming next; a value near 1 means `w1` is a very strong cue for `w2`.

    Because it's directional, we can also ask it the other way around: how strongly does `w2` predict that `w1` came *before* it?

    $$
    \Delta P(w_1 \mid w_2) = P(w_1 \mid w_2) - P(w_1 \mid \text{not } w_2)
    $$

    The function below calculates both directions, using the same frequency distributions as before. (To keep it simple, it uses each word's total frequency as the number of bigrams starting or ending with that word, which is almost exactly right in a text this long.)
    """)
    return


@app.cell
def _(big_salad_bigram_fdist, big_salad_bigrams, big_salad_fdist):
    def delta_p(w1, w2):
      """calculates Delta P in both directions for the bigram (w1, w2) in the Big Salad"""
      pair_count = big_salad_bigram_fdist[(w1, w2)]
      w1_count = big_salad_fdist[w1]
      w2_count = big_salad_fdist[w2]
      total_bigrams = len(big_salad_bigrams)

      # how much does w1 predict that w2 comes next?
      forward = pair_count / w1_count - (w2_count - pair_count) / (total_bigrams - w1_count)

      # how much does w2 predict that w1 came before it?
      backward = pair_count / w2_count - (w1_count - pair_count) / (total_bigrams - w2_count)

      return forward, backward

    return (delta_p,)


@app.cell
def _(delta_p):
    delta_p('you', 'know')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's put PMI and both directions of Delta P side by side for a few bigrams, in a table:
    """)
    return


@app.cell
def _(big_salad_bigram_fdist, delta_p, pl, pmi):
    # some bigrams to compare
    compare_bigrams = [('you', 'know'), ('you', 'ratted'), ('you', 'maestro'), ('i', 'dont'), ('dont', 'know'), ('new', 'york'), ('the', 'car')]

    pl.DataFrame({
      'bigram': [w1 + ' ' + w2 for (w1, w2) in compare_bigrams],
      'frequency': [big_salad_bigram_fdist[(w1, w2)] for (w1, w2) in compare_bigrams],
      'PMI': [round(pmi(w1, w2), 2) for (w1, w2) in compare_bigrams],
      'Delta P (w1 predicts w2)': [round(delta_p(w1, w2)[0], 3) for (w1, w2) in compare_bigrams],
      'Delta P (w2 predicts w1)': [round(delta_p(w1, w2)[1], 3) for (w1, w2) in compare_bigrams],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the table:

    - Which bigram is the "strongest" collocation according to PMI? According to Delta P?
    - For *you know*, which direction is stronger: does *you* predict *know*, or does *know* predict *you*? Does that make sense?
    - Try adding your own bigrams to the list. Can you find a pair where PMI and Delta P strongly disagree?

    There is no single "correct" measure of collocation strength. Each one captures a different idea of what it means for two words to "go together", so the measure you choose should depend on your question.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Collocations with part of speech filters**

    Look back at the most frequent bigrams in the Big Salad. Many of them are pairs of function words (*of the*, *in a*), which are frequent but not very interesting. One way to find more meaningful collocations is to **filter by part of speech**: for example, only look at adjective + noun pairs.

    The Brown corpus already comes with POS tags, so we don't need to tag it ourselves. We'll ask for the universal tagset, which uses simple tags like `ADJ` and `NOUN`.
    """)
    return


@app.cell
def _(nltk):
    # the tagged words of Brown, with universal tags
    brown_tagged = nltk.corpus.brown.tagged_words(tagset = 'universal')

    # make bigrams of the tagged words
    brown_tagged_bigrams = list(nltk.bigrams(brown_tagged))

    brown_tagged_bigrams[:5]
    return (brown_tagged_bigrams,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now keep only the bigrams where the first word is an adjective and the second is a noun, and count them (lowercased):
    """)
    return


@app.cell
def _(FreqDist, brown_tagged_bigrams):
    # keep (adjective, noun) pairs, lowercased
    adj_noun_pairs = [(pair1[0].lower(), pair2[0].lower()) for (pair1, pair2) in brown_tagged_bigrams if pair1[1] == 'ADJ' and pair2[1] == 'NOUN']

    adj_noun_fdist = FreqDist(adj_noun_pairs)
    adj_noun_fdist.most_common(20)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What kinds of pairs do you see? Do they look more like collocations than the unfiltered bigrams? Try changing the tags (e.g., `'VERB'` followed by `'NOUN'`, or `'NOUN'` followed by `'NOUN'`).
    """)
    return


@app.cell
def _():
    # use this code cell to try other part of speech patterns!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Multiword expressions**

    Some collocations are so strong that they behave like a single word: *New York*, *ice cream*, *kick the bucket*, *by and large*. These are called **multiword expressions**.

    This brings us back to the question from the tokenisation notebook: what is a word? If *New York* is really one unit of meaning, should it be one token?

    NLTK's `MWETokenizer` lets us join chosen multiword expressions into single tokens. You give it a list of expressions (as tuples of words), and it joins them with an underscore:
    """)
    return


@app.cell
def _(MWETokenizer, nltk):
    # a tokenizer which joins these expressions into single tokens
    mwe_tokenizer = MWETokenizer([('new', 'york'), ('ice', 'cream'), ('kick', 'the', 'bucket')], separator = '_')

    mwe_tokens = nltk.word_tokenize('i had ice cream in new york before i nearly did kick the bucket')
    mwe_tokenizer.tokenize(mwe_tokens)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What would joining multiword expressions do to word counts, TTR, or the bigrams we found above? How would you decide which expressions to join? (One option: use a collocation measure to find the strongest candidates!)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Wrapping up**

    Now you have a better idea about how word frequencies can be used to determine the relative probabilities of seeing word pairs occur together. These collocational patterns, or word probabilities, can be extended to larger and larger patterns, which pave the way for more complex and interesting NLP applications!

    A few things to think about:

    - Frequent is not the same as strongly associated: *of the* is very frequent, but is it a collocation?
    - Different measures (PMI, Delta P, log-likelihood) can give different answers. Which should you trust, and how would you decide?
    - How much do the collocations you find depend on the text you use (a TV script vs a novel vs news)?
    """)
    return


if __name__ == "__main__":
    app.run()
