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
    # **Word Probabilities and ngram models**
    The application of word probabilities we are concerned about here has to do with *predicting* which word will come next given any one particular sequence of words.

    As you have hopefully come to learn, language is largely patterned, and corpora are very useful for finding and analysing these patterns. The word probabilities discussed in this notebook will also exploit the patterned nature of language. However, the word probabilities are going to be a bit different in that they use frequency statistics and chained probabilities to predict words.

    ## **N-grams**
    You have seen reference made to the term `n-grams` in the collocations notebook. As a reminder, a single word can also be called a `unigram`, a pair of words can be called a `bigram`, three is a `trigram`, and so on. So the "n" in `n-gram` can be any sequence of words of any length long (e.g., you could have a 100-gram). However, think about our work with corpus patterns - most of them are not this large! As it turns out, bigrams and trigrams end up being very helpful for predicting future words.

    There are two other books which have informed this notebook. One is called [*Language and Computers*](https://www.wiley.com/en-us/Language+and+Computers-p-9781405183055), and the other is called [*Speech and Language Processing*](https://web.stanford.edu/~jurafsky/slp3/).

    When discussing word probabilities, both texts use a similar approach to describing how n-gram models are used in NLP (*L&C*, pp. 26-28; *SLP*, pp. 29-35). Each uses an uncompleted sentence to make the same point -- you probably have a really good guess for which words come after other certain words. (*L&C* uses the example "I dreamed I saw the knights in...", whereas *SLP* uses "Please turn your homework...").

    But, why do **you** have that knowledge, as a human? What does this say about the brain and language – is our language knowledge a series of statistical connections? Is the brain a computer? Keep this question in the back of your mind while you read on and complete this notebook.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import requests
    import nltk
    from nltk import FreqDist
    from nltk.corpus import state_union

    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'state_union'])
    return FreqDist, nltk, requests, state_union


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Word probabilities for single tokens**

    You have already calculated some probabilities in this course: in the collocations notebook, PMI compared the probability of a bigram with the probability of each of its words, and Delta P asked how likely one word was given another word. In the classification notebook, Naive Bayes also used probabilities to choose a label. In this notebook we will look at probabilities more closely, and use them to *predict* words. Let's start small, with a refresher on how to calculate probabilities and the notation that goes with them.

    $P(A)$ is a shorthand for representing the probability (or likelihood) that something (`A`) will occur. For word probabilities, we can think of this as telling us how likely a single token will occur in some larger context, such as the likelihood of randomly drawing a particular token from a document. Because in this scenario we assume all tokens would have an equally likely chance of being selected, we can rely on a fairly simple method for calculating our probability: counting.

    If we want to predict the probability of randomly selecting a single token from a document we only have two possible outcomes: the randomly selected token either *is* or *is not* our target token. So, the probability of choosing any one token is based on the total number of tokens in the document/space we are searching. If I had a sentence of four different tokens, each token would have a 25% probability of being randomly chosen. Once we start repeating the same token in a text, the chances of randomly selecting tokens of that type increase.

    We can apply this calculation to an entire text, keeping in mind the distinction between types and tokens. To calculate this, we count how many tokens for our target occur in the document/space, and divide that by the total space we are sampling from (i.e., the total number of tokens in a document).

    Therefore, the probability of choosing a word ( $P(A)$ ) is directly linked to the overall frequency of the tokens representing that word in a document.

    For example, if the word `pretzels` occurs 100 times in a 1000 word document, the probability of choosing a random token from the document and that token being `pretzels` would be 100/1000, which is 0.1, or 10%.

    So the $P(A)$ for this example says there is a 10% likelihood to encounter the token `pretzels` if we randomly sampled one token from this hypothetical document.

    Of course, that's not very useful yet. We want to make predictions about the presence of one token in light of *other* tokens. So, we need to modify the approach to take this information into account.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Changing the search space to other words**

    We can calculate the probability for a word occurring after *other* words by changing a word's search space to be specific patterns of tokens (rather than an entire document). In the example above, our search space was every possible word in the document, which does not take into account any other information about where the word occurs.

    However if we predefine a smaller context for a search space, such as a smaller sequence of tokens, we can then divide by only the number of times that sequence appears (rather than the size of an entire document).

    Say for instance we wanted to know the probability of the word `"thirsty"` appearing after the words `"these pretzels are making me"`:

    > $P(\text{"thirsty"}|\text{"these pretzels are making me"})$

    To get this prediction, we need to count the total instances of the complete sentence `"these pretzels are making me thirsty"` (instead of counting the total number of times `thirsty` appears).

    If I search for the phrase "`these pretzels are making me thirsty`" in Google, I get 69,500 hits (at least, when I did that search in the past...). Let's pretend that's the total frequency of the phrase in a corpus.

    We could then calculate the probability of `"thirsty"` appearing in this context by dividing by the total number of times the phrase occurs with *any* word, not just `"thirsty"`. In Google, I previously got 7,080,000 results for the phrase `"these pretzels are making me"` followed by any word (including "thirsty").

    We then divide the frequency of the phrase with our *target* word by the frequency of the phrase followed by *any* word. In this case it would be `69500/7080000`, which is slightly less than 1%. That might not seem like a lot, but a 1% predictive chance is likely a lot higher than any other word which can fit into that slot (and is aided by the frequency of this phrase being associated with a Seinfeld episode).
    """)
    return


@app.cell
def _():
    69500/7080000
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Issues with using full sentences as contexts**

    As is pointed out by the authors of *SLP*, this method brings with it a few challenges. Language is creative and even similar sentences might be phrased in slightly different ways, leading to a lot of different possible sentences that need to be counted. Language corpora cannot be guaranteed to contain all of these creative examples, and thus prediction will suffer. (Moreover, using Google like I did is not really a good method because we are not really sampling from a corpus of language – I mainly used it to represent the concept).

    The only reason my sentence above was so frequent is because it is a well known quote from *Seinfeld* and has apparently been repeated many, many times on the internet!

    The solution to address this challenge is to avoid trying to calculate the probability of a word based on the entire sentence context, but instead calculate the individual probabilities of `n-grams` in a sentence, and then multiply these probabilities together as they appear in sentences. This means we want to calculate the combined probability of `"thirsty"` coming after `"me"`, as well as the probability of `"me"` coming after the word `"making"`, and so on. This smaller combined probability approximates using the entire sentence context.

    In other words, this approach makes an assumption that the probabilities associated with the prior 1-2 words of a word are predictive enough to stand in for longer sentence contexts - which *SLP* explains is a **Markov assumption**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Conditional probabilities and n-grams**
    So, how can we go about doing this? Now we are more interested in how to predict a word *given a prior word context* that is limited to just one or two words. Let's just stick with one word for now.

    We need to expand our probability notation to include the likelihood of something occurring when something *else* also occurs. This is the exact same as what we have done above, except we are changing our contexts of counting. Let's also add to our notation for probabilities.

    $P(A|B)$ is a shorthand for representing the probability (or likelihood) that something (A) will occur **if** something else occurs (B). This is called the [`conditional probability`](http://www.stat.yale.edu/Courses/1997-98/101/condprob.htm). If you clicked that link and read the examples (or remember from prior courses / reading), you'll see that conditional probability is just more counting and then some division.

    In this approach, our *condition* is the appearance of a prior word, and we want to see how strongly that condition is associated with the occurrence of our target word.

    For predicting a probability on a conditional event (such as word A occurring after word B), we divide the total count of the event occurring (such as word A occurring after word B) by the total number of times the event *could* occur (such as the word B occurring before another word) – this is what I did above with the pretzels example, except now we are looking at individual words rather than full sentences.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Let's calculate a conditional probability**

    *SLP* gives the following formula to calculate the conditional probability of word co-occurrence:

    $$
    P(W_n|W_{n-1}) = \frac{c(W_{n-1}W_n)}{c(W_{n-1})}
    $$

    Here is what the symbols mean:

    $W$ = the given word

    $n$ = the index or identity of a word (think of it like a Python list index)

    $W_{n-1}$ = the word occurring one index *before* the word we want to predict

    $c$ = the frequency count

    Let's break the formula down using the example of `"these pretzels"`. If we wanted to predict the likelihood of `"pretzels"` coming after the word `"these"`, the notation is thus:

    $$
    P(\text{"pretzels"}|\text{"these"}) = \frac{c(\text{"these pretzels"})}{c(\text{"these"})}
    $$

    Hypothetically, if in a particular search space the bigram `"these pretzels"` occurred 20 times and `"these"` occurred 128 times, then:

    $$
    P(\text{"pretzels"} | \text{"these"}) = \frac{20}{128} = .156
    $$

    Our definition above says we should divide the total count of our target bigram (`these pretzels`) by the total number of times the prior word (`these`) could occur before *any word*, including our target word. So technically this value should be the number of bigrams involving the first word. As is pointed out by *SLP*, however, we can use the simple frequency of the word before our target word as the denominator.

     **[SLP](https://web.stanford.edu/~jurafsky/slp3/3.pdf) says "the reader should take a moment to be convinced by this" (p. 32)**

    Are you? Think...can the total frequency of the number of times word B (`these`) potentially occurs before any other word ever be different than the total number of times word B occurs on its own?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **A longer example**
    Let's work with more data and start writing some functions to calculate these probabilities for an input text.

    Consider the following sentence:

    >`"these pretzels are making me thirsty! They are also making me tired! I love pretzels because they make me thirsty!"`

    Let's now consider the probabilities of the word `"thirsty"`. In our sentence, `"thirsty"` occurs two times, and both times after the word `"me"`. We also see that `"me"` occurs three times, two times before `"thirsty"` but also one time before `"tired"`. Let's calculate some basic probabilities for these words.

    ### **Calculate single word probabilities**

    We can write some quick code to:

    1. Count the total number of words
    2. Count the frequency of the words we are interested in (`"thirsty," "tired,"` and `"me"`)
    """)
    return


@app.cell
def _():
    # Create the data
    # triple quote to break lines
    text_input = """these pretzels are making me thirsty
    They are also making me tired
    I love pretzels because they make me thirsty"""

    # split data into separate words
    text_input_words = text_input.split()
    print(text_input_words)

    # total search space
    len(text_input_words)
    return text_input, text_input_words


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we use `FreqDist()` to count the words. Notice that we count the *list of words*, not the original string.
    """)
    return


@app.cell
def _(FreqDist, text_input_words):
    # count every word
    input_fdist = FreqDist(text_input_words)

    # what is the probability of each word, on its own?
    for target_word in ['thirsty', 'tired', 'me']:
      print(f'word: {target_word} | total frequency: {input_fdist[target_word]} | probability: {input_fdist[target_word] / len(text_input_words)}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since we know that `thirsty` occurs twice, both times after `me`, we know there are two instances of our target bigram, `me thirsty`. We know that `me` occurs three times total, twice with `thirsty` and once with `tired`. So:

    $$
    P(\text{"thirsty"}|\text{"me"}) = \frac{c(\text{"me thirsty"})}{c(\text{"me"})} = \frac{2}{3} = .66
    $$

    Within this search space, the word `thirsty` has a 10% chance of occurring overall, but a 66% chance of coming after `me.` With such a small sentence, this isn't very useful. We want to start increasing the search space and looking directly at bigrams.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Calculate bigram probabilities**

    The next step is to expand this program to calculate the bigram probabilities of a text. Our program will take an input text and an input word, and then calculate the probability of that word coming after every word it follows in the text (the **headwords**).

    We already know how to do the counting from the collocations notebook: `FreqDist()` on the words gives us the frequency of each headword, and `FreqDist()` on the bigrams gives us the frequency of each bigram. Then we just need to divide!

    Below, I define a function which:

    1. lowercases and tokenises the text
    2. creates the bigrams, and keeps only the bigrams without punctuation
    3. counts the words and the bigrams with `FreqDist()`
    4. loops through the bigrams which end in our target word, and divides the bigram frequency by the headword frequency
    """)
    return


@app.cell
def _(FreqDist, nltk):
    def bigram_counter(text, target):
      # lowercase and tokenise the text
      tokens = nltk.word_tokenize(text.lower())

      # count the words, and the bigrams which don't include punctuation
      word_fdist = FreqDist(tokens)
      bigram_fdist = FreqDist([(w1, w2) for (w1, w2) in nltk.bigrams(tokens) if w1.isalpha() and w2.isalpha()])

      print(f'total frequency of {target} is {word_fdist[target]} \n')
      print(f'probabilities for bigrams with {target} are:\n')

      # loop through every bigram, and only look at the ones which end in our target word
      for (headword, word) in bigram_fdist:
        if word == target:
          probability = bigram_fdist[(headword, word)] / word_fdist[headword]
          print(f'total frequency of bigram {(headword, word)}: {bigram_fdist[(headword, word)]}')
          print(f'total frequency of headword {headword} is {word_fdist[headword]}')
          # I use .upper() to make the words stand out
          print(f'probability of {target.upper()} after {headword.upper()}: {round(probability, 3)} \n')

    return (bigram_counter,)


@app.cell
def _(bigram_counter, text_input):
    # check it works on our small example
    bigram_counter(text_input, 'thirsty')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's practice our function on Bill Clinton's 2000 State of the Union Address.
    """)
    return


@app.cell
def _(state_union):
    clinton = state_union.raw('2000-Clinton.txt')

    # the first 500 characters
    clinton[:500]
    return (clinton,)


@app.cell
def _(bigram_counter, clinton):
    # let's pick three words to search for. what do you think about their bigram probabilities?
    for clinton_target in ['americans', 'america', 'fellow']:
      bigram_counter(clinton, clinton_target)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Chaining probabilities**
    Our function thus computes target bigrams for any one word and then gives us the probability of that word's occurrence after a particular headword. That's kinda cool, right? We probably should calculate sentence boundaries and maybe do this for each sentence rather than a whole text, but hopefully you get the idea of how this function works now.

    However, let's now think about how we can use this information to predict the probability of a longer string of words using bigram probabilities. We want to be able to predict the overall probability of a word after more than one word, say, to finish a complete sentence (such as the ones given at the start of this notebook).

    As was teased above, we can do this by chaining together the individual bigram probabilities of all the words in a target string that come before a word. This means if we wanted to compute the likelihood of the sentence `'these pretzels are making me thirsty'`, we would calculate:

    $$
    P(\text{"pretzels"}|\text{"these"}) \times P(\text{"are"}|\text{"pretzels"}) \times P(\text{"making"}|\text{"are"}) \times P(\text{"me"}|\text{"making"}) \times P(\text{"thirsty"}|\text{"me"})
    $$

    Can we create a function which will do this? We need to:

    - read in a text and count its words and bigrams (this is our **model**)
    - accept a target phrase
    - for each bigram in the phrase, find the probability of that bigram
    - multiply the bigram probabilities to find the overall probability of the phrase
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Building a bigram model**

    We'll split this into two functions. The first function, `bigram_model()`, does all of the counting one time, and gives back the two frequency distributions. This is our model. The second function, `phrase_probability()`, uses the model to calculate the probability of a phrase. Splitting them up means we don't need to count the whole text again every time we want to look up a new phrase.
    """)
    return


@app.cell
def _(FreqDist, nltk):
    def bigram_model(text):
      '''count the words and bigrams in a text'''
      # lowercase and tokenise the text
      tokens = nltk.word_tokenize(text.lower())

      # count the words, and the bigrams which don't include punctuation
      word_fdist = FreqDist(tokens)
      bigram_fdist = FreqDist([(w1, w2) for (w1, w2) in nltk.bigrams(tokens) if w1.isalpha() and w2.isalpha()])

      # the function gives back both frequency distributions
      return word_fdist, bigram_fdist

    return (bigram_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The second function takes the model and a target phrase. It makes the bigrams of the phrase, and multiplies their probabilities together. I also print each bigram and its probability, so that you can see the calculation.

    What happens if a bigram is *not* in the model? A `FreqDist` gives a count of 0 for anything it hasn't seen, so the probability of that bigram is 0. And remember what happens if we multiply by 0? The whole phrase gets a probability of zero. This makes sense, because it reflects that the phrase is *not* in the reference model. (I also check that the headword is in the model, because otherwise we would be dividing by zero!)
    """)
    return


@app.cell
def _(nltk):
    def phrase_probability(model, target):
      '''calculate chained probabilities of a target phrase from a bigram model'''
      word_fdist, bigram_fdist = model

      # create bigrams of our target phrase
      target_tokens = nltk.word_tokenize(target.lower())
      target_bigrams = list(nltk.bigrams(target_tokens))

      # start with a probability of 1, then keep multiplying
      probability = 1
      for (headword, word) in target_bigrams:
        # avoid dividing by zero if the headword is not in the model
        if word_fdist[headword] == 0:
          bigram_probability = 0
        else:
          bigram_probability = bigram_fdist[(headword, word)] / word_fdist[headword]
        print(f'P({word} | {headword}) = {round(bigram_probability, 4)}')
        probability = probability * bigram_probability

      print(f'probability of phrase "{target}" is {probability}')

    return (phrase_probability,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That might be a lot to take in - so let's see if it works with some toy examples. Consider the following sentence context. Looking at it we know that the probability of the phrase "making me thirsty" should be 100% because there is only one sequence of words which occurs using these words:
    """)
    return


@app.cell
def _():
    pretzels = 'these pretzels are making me thirsty'
    return (pretzels,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To start, we would write the chained probability as:

    $$
    P(\text{"me"}|\text{"making"}) \times P(\text{"thirsty"} | \text{"me"})
    $$

    The probabilities are defined as proportions of counts:

    $$
    \frac{c(\text{'making me'})}{c(\text{'making'})} \times \frac{c(\text{'me thirsty'})}{c(\text{'me'})}
    $$

    Each bigram and unigram only occur one time, so we have:

    $$
    \frac{1}{1} \times \frac{1}{1} = 1
    $$

    Confirm with our functions:
    """)
    return


@app.cell
def _(bigram_model, phrase_probability, pretzels):
    phrase_probability(bigram_model(pretzels), 'making me thirsty')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That was a silly example - now let's look at a larger context:
    """)
    return


@app.cell
def _():
    pretzels2 = 'these pretzels are making me thirsty! These pretzels are making me tired!'
    return (pretzels2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the same target string, our counts would change, in that `making`, `me`, and `making me` now occur twice each in the entire search space. So the counts to determine probabilities:

    $$
    \frac{c(\text{'making me'})}{c(\text{'making'})} \times \frac{c(\text{'me thirsty'})}{c(\text{'me'})}
    $$

    Will become this:

    $$
    \frac{2}{2} \times \frac{1}{2}
    $$

    Which is:

    $$
    1 \times 0.5 = 0.5 = 50\%
    $$

    We can see our function returns this:
    """)
    return


@app.cell
def _(bigram_model, phrase_probability, pretzels2):
    phrase_probability(bigram_model(pretzels2), 'making me thirsty')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's train a model on the Clinton speech:
    """)
    return


@app.cell
def _(bigram_model, clinton):
    clinton_model = bigram_model(clinton)
    return (clinton_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we've trained our model, we can query it. Holy crap...we've made an n-gram language model!!

    What is the likelihood of the phrase 'my fellow americans' in the Clinton speech?
    """)
    return


@app.cell
def _(clinton_model, phrase_probability):
    phrase_probability(clinton_model, 'my fellow americans')
    return


@app.cell
def _(clinton_model, phrase_probability):
    phrase_probability(clinton_model, 'my fellow romulans')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **The problem with zeros**

    Clinton never said *romulans*, so the whole phrase has a probability of 0. Is that right? The phrase is unlikely, but it's not *impossible* - after all, I just wrote it!

    This is a big problem for n-gram models: any phrase that contains even one bigram the model hasn't seen gets a probability of zero, no matter how normal the rest of the phrase is. And language is creative, so new phrases happen all the time. This means a model needs to be trained on a lot of text to be useful, much larger than a single State of the Union speech.

    Real n-gram models deal with this using **smoothing**: they take a tiny bit of probability away from the bigrams they *have* seen, and share it out among the bigrams they haven't seen. That way, unseen phrases get a very small probability instead of zero. We won't calculate smoothing here, but keep in mind that the zeros are a sign that our model is too small to know about everything.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Longer phrases**

    Let's train a model on a larger text: the Big Salad. This might take a few seconds.
    """)
    return


@app.cell
def _(bigram_model, requests):
    big_salad = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/big_salad.txt').text

    big_salad_model = bigram_model(big_salad)
    return (big_salad_model,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All right. Now, check out what happens to the probability as we expand our ngram into larger and larger phrases. The probability will decrease as we create more and more specific contexts.
    """)
    return


@app.cell
def _(big_salad_model, phrase_probability):
    phrase_probability(big_salad_model, 'you know')
    return


@app.cell
def _(big_salad_model, phrase_probability):
    phrase_probability(big_salad_model, 'you know what')
    return


@app.cell
def _(big_salad_model, phrase_probability):
    phrase_probability(big_salad_model, 'you know what i think')
    return


@app.cell
def _(big_salad_model, phrase_probability):
    phrase_probability(big_salad_model, 'what are you doing')
    return


@app.cell
def _(big_salad_model, phrase_probability):
    phrase_probability(big_salad_model, 'what are you doing here')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You're witnessing a method used to predict upcoming text. We could now take a phrase stem (such as 'please hand your homework...') and then find the words with the highest overall phrase probability, eventually locating 'please hand your homework **in**' as the most likely combination, depending on which model we use. In this way, we could use this as a simplistic text prediction algorithm. (In the generating text notebook, we will use this idea to *generate* text!)

    Thinking back to some of the earlier questions I opened the notebook with about how ***you*** can predict upcoming words. One argument is that your brain contains some form of probabilistic distribution of language patterns, which is why we are so good at predicting upcoming words. Whether this computational approximation using n-grams reflects the same process can't be fully proven (yet), but as language models get larger, and the methods for computing probabilities become more sophisticated, the performance of NLP models and predictive text applications continues to increase and match the way humans can predict.

    ### **Your Turn**

    - Try some phrases of your own with the Big Salad model. Which phrases get a probability of zero? Why?
    - Compare the probability of the same phrase in the Clinton model and the Big Salad model. Why are they so different?
    - Train a model on a different text (e.g., another State of the Union speech, or a Gutenberg book). What kinds of phrases does it think are likely?
    """)
    return


@app.cell
def _():
    # use this code cell to explore word probabilities!
    return


if __name__ == "__main__":
    app.run()
