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
    # **What! is? a. Token?!**

    In this notebook we return to the problem of tokenizing a text and defining what counts as a word. So far we've been doing this with the `.split()` function, which has worked relatively well for us. But there is one issue: splitting on whitespace means that sometimes punctuation is included with our words.

    We will look at several ways of preparing a text before we count anything in it. Keep one question in mind the whole way through: **how does each choice change the numbers we get at the end?**

    First, let's load all of the libraries this notebook uses.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import re
    import string
    import requests
    import polars as pl
    import nltk
    nltk.download(['punkt_tab', 'stopwords'])
    from nltk.corpus import stopwords
    from nltk.tokenize import RegexpTokenizer

    return RegexpTokenizer, nltk, pl, re, requests, stopwords, string


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The problem with `.split()`

    Running `.split()` on the example below will keep commas and exclamation marks as part of the words:
    """)
    return


@app.cell
def _():
    turtles = """teenage mutant ninja turtles,
    teenage mutant ninja turtles,
    teenage mutant ninja turtles,
    heroes in a halfshell, turtle power!"""

    turtles.split()
    return (turtles,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Therefore, we might want to perform some operations on this text *before* we start processing it for linguistic information. These operations will work to normalise and standardise the text to obtain more accurate results. This is called **preprocessing**.

    Preprocessing comes in many options - you could remove just punctuation, or convert everything to lowercase, or remove extra whitespace (with `.strip()`, which you saw in notebook 01), or remove very frequent words, or remove words that are not in the dictionary, or remove words that only occur one time, and so on. Different algorithms and approaches to NLP will all include their own methods and steps for preprocessing, which are tied to the goals of the analysis.

    For now, let's focus on the issue of punctuation in the turtles text.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Removing punctuation

    ## Method 1: a list comprehension

    How could we remove all of the punctuation from a text using what we know so far? We could set up a conditional test which inspects each character in a string, and as long as that character is *not* a punctuation mark, keep it. As a list comprehension, it would look like this:

    ```
    [character for character in string if character not in punctuation]
    ```

    To run this, we need to tell Python what we mean by "punctuation". One way is to define a string containing all the punctuation marks we don't want. We will also lowercase the characters within the same expression.
    """)
    return


@app.cell
def _():
    # define a string containing punctuation we don't like, in this case just commas and exclamation marks
    punct_marks = ',!'
    return (punct_marks,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you run the cell below, you see that the punctuation has been removed, but unfortunately the output is a list of characters, not words!
    """)
    return


@app.cell
def _(punct_marks, turtles):
    # a list comprehension that only keeps characters that aren't in punct_marks
    [character.lower() for character in turtles if character not in punct_marks]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `string.join()`

    We wanted to keep the text as a series of words, not a list of characters. No worries, we can use the handy `.join()` string method to join a list of characters back into one string!

    `.join()` is sort of the bizarre cousin of `.split()`. While `.split()` lets you choose which character to *separate* on, `.join()` lets you choose which character to *join* on. The string you attach to the front of `.join()` is the glue that goes between each item. For example, `''.join()` will join using an empty string, `' '.join()` will join using a space, and `'HELLO'.join()` would join everything with the string `HELLO`.
    """)
    return


@app.cell
def _():
    example_chars = ['n', 'i', 'n', 'j', 'a', ' ', 't', 'u', 'r', 't', 'l', 'e']
    return (example_chars,)


@app.cell
def _(example_chars):
    # join with an empty string
    ''.join(example_chars)
    return


@app.cell
def _(example_chars):
    # join with a space
    ' '.join(example_chars)
    return


@app.cell
def _(example_chars):
    # join with HELLO
    'HELLO'.join(example_chars)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, to glue our cleaned characters back together *without* making any other changes, we wrap the whole list comprehension in `''.join()`:
    """)
    return


@app.cell
def _(punct_marks, turtles):
    turtles_no_punct = ''.join([character.lower() for character in turtles if character not in punct_marks])
    turtles_no_punct
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Typing out every punctuation mark you want removed can be annoying. Python has a ready-made string of (English) punctuation marks in the `string` library, which you could use in place of `punct_marks`:
    """)
    return


@app.cell
def _(string):
    string.punctuation
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Method 2: a regular expression

    Another way is to use a regular expression, which you met in the regex notebook. The `re.sub()` function substitutes a pattern in a string with something else:

    `re.sub(pattern, replacement, string)`

    You are telling `re.sub()` to replace THIS with THAT over THERE. If the replacement is an empty string, the pattern is effectively removed from the string. For example:
    """)
    return


@app.cell
def _(re):
    # remove all the 'a' from the string 'banana'
    re.sub(pattern = 'a', repl = '', string = 'banana')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To remove more than one punctuation mark, we put them inside square brackets, which means "any of these characters":
    """)
    return


@app.cell
def _(re, turtles):
    # remove any comma or exclamation mark
    re.sub(pattern = '[,!]', repl = '', string = turtles)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is a more general pattern which removes *all* punctuation:

    ```
    [^\w\s]
    ```

    - `\w` matches any word character: a letter (in any alphabet, including letters with macrons and accents), a digit, or an underscore
    - `\s` matches any whitespace character (spaces, tabs, newlines)
    - the `^` inside square brackets means *anything but* these characters

    So, with a bit of reverse logic, this pattern says "replace anything that is *not* a word character or whitespace with nothing", which cleans out the punctuation. Remember this pattern and come back to copy it when you need to remove punctuation in the future!
    """)
    return


@app.cell
def _(re, turtles):
    # an easy way to remove punctuation from a string
    re.sub(r'[^\w\s]', '', turtles)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Using NLTK to tokenize

    Now we know how to clean a text so that `.split()` returns a tidier set of tokens. But what if we want to *retain* punctuation? Punctuation could tell us something about the syntax of a sentence or the tone of a piece of writing, and it helps us find the boundaries between words and sentences.

    NLTK has two tokenizer functions which improve on `.split()`: `nltk.word_tokenize()` and `nltk.sent_tokenize()`. They convert raw strings into word tokens or sentences, respectively. (They use a resource called `punkt_tab`, which we downloaded at the top of the notebook.)

    Compare the difference between using `.split()` and `nltk.word_tokenize()`:
    """)
    return


@app.cell
def _(nltk):
    pretzels = 'These pretzels are making me thirsty!'

    pretzels_split = pretzels.split()
    pretzels_nltk = nltk.word_tokenize(pretzels)

    print(f"Using .split(): \n{pretzels_split}\n\nUsing nltk: \n{pretzels_nltk}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The NLTK tokenizer has treated the punctuation as a separate token. It does this using a set of rules as well as some splitting. This makes sense for punctuation which occurs after words, such as commas, full stops and exclamation marks.

    What's going on in the cell below?
    """)
    return


@app.cell
def _(nltk):
    # What is different about these tokens?
    nltk.word_tokenize("I can't even.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The word "can't" was split into two tokens: `ca` and `n't`! Why? "Can't" stands for *two* words, "can" and "not", and the tokenizer has rules for splitting contractions. These rules come from the Penn Treebank, a famous collection of tagged English text, which splits off the "n't" part of a contraction as its own token. So "don't" becomes `do` + `n't`, and "can't" becomes `ca` + `n't`.

    Using `.split()`, on the other hand, would keep "can't" as a single word. And removing the punctuation *before* tokenizing turns "can't" into "cant", which is a different word with its own meaning:
    """)
    return


@app.cell
def _(nltk, re):
    # remove punctuation first, then tokenize
    nltk.word_tokenize(re.sub(r'[^\w\s]', '', "I can't even."))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The point is that the **order** of preprocessing steps is important. Many modern NLP libraries perform preprocessing automatically, and some analyses now don't need any preprocessing at all! It is nonetheless important to understand how your data has been changed in order to use these tools properly.

    ## Method 3: tokenize first, then remove punctuation tokens

    Because `nltk.word_tokenize()` puts punctuation into its own tokens, we can remove punctuation *after* tokenizing by dropping those tokens. The string method `.isalpha()` returns `True` only if **every** character in a string is a letter:
    """)
    return


@app.cell
def _():
    # False because the ! is not a letter
    'hi!'.isalpha()
    return


@app.cell
def _():
    # also False, because '1' is a number, not a letter (so .isalpha() removes numbers too!)
    'hi1'.isalpha()
    return


@app.cell
def _(nltk):
    jp = 'Life, uh, finds a way.'

    # the comma and full stop are their own tokens
    nltk.word_tokenize(jp)
    return (jp,)


@app.cell
def _(jp, nltk):
    # only keep tokens that are made of letters
    [token for token in nltk.word_tokenize(jp) if token.isalpha()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Think about it:** what would happen to the `n't` in "I can't even." if you used `.isalpha()` on its tokens? Try it in the cell below.
    """)
    return


@app.cell
def _():
    # use this code cell to test things out!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Creating sentences with `nltk.sent_tokenize()`

    We can also split a text into sentences using `nltk.sent_tokenize()`. The output is a list of sentences. Before running the cell below, predict: how many sentences are in the turtles text?
    """)
    return


@app.cell
def _(nltk, turtles):
    # all the sentences in turtles
    nltk.sent_tokenize(turtles)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Only one sentence! Even though the song is written over four lines, `sent_tokenize()` does not use newlines to find sentences. It looks for sentence-final punctuation such as full stops, question marks and exclamation marks, and the only one in the song is at the very end ("turtle power!").

    Here is a string with two clear sentences:
    """)
    return


@app.cell
def _(nltk):
    # two sentences, each ending with a full stop
    nltk.sent_tokenize("Give a man a fire and he's warm for a day. Set fire to him and he's warm for the rest of his life.")
    return


@app.cell
def _(nltk):
    # we can see how reliant it is on punctuation: without the first full stop, we get one sentence
    nltk.sent_tokenize("Give a man a fire and he's warm for a day Set fire to him and he's warm for the rest of his life.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Lowercasing

    Let's consider how preprocessing influences a measure we've already explored: lexical diversity. Compare what capitalisation will do to the TTR of these two texts:
    """)
    return


@app.cell
def _():
    # create two texts that only differ based on capitalisation
    version1 = ['Soda', 'soda', 'Onion', 'onion']
    version2 = ['soda', 'soda', 'onion', 'onion']
    return version1, version2


@app.cell
def _(version1, version2):
    # calculate their TTR
    version1_ttr = len(set(version1)) / len(version1)
    version2_ttr = len(set(version2)) / len(version2)
    return version1_ttr, version2_ttr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compare - version 1 has a higher TTR than version 2, even though they are effectively the "same" words:
    """)
    return


@app.cell
def _(version1_ttr):
    version1_ttr
    return


@app.cell
def _(version2_ttr):
    version2_ttr
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We clearly would not want to think that `version1` is more lexically diverse than `version2`, unless we have strong reason to believe the capitalisation results in a fundamentally different word. If we convert all of the tokens to lowercase, we now obtain the same TTR:
    """)
    return


@app.cell
def _(version1, version2):
    # use a list comprehension to lowercase all the tokens
    version1_lower = [token.lower() for token in version1]
    version2_lower = [token.lower() for token in version2]
    return version1_lower, version2_lower


@app.cell
def _(version1_lower, version2_lower):
    # calculate new TTR scores
    version1_lower_ttr = len(set(version1_lower)) / len(version1_lower)
    version2_lower_ttr = len(set(version2_lower)) / len(version2_lower)
    return version1_lower_ttr, version2_lower_ttr


@app.cell
def _(version1_lower_ttr):
    version1_lower_ttr
    return


@app.cell
def _(version2_lower_ttr):
    version2_lower_ttr
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    While this is helpful, we need to be careful. Perhaps in some cases you will want to retain capitalisation. In English, at least, capitalisation signals names and proper nouns (compare "Apple" and "apple"). And in languages which use logographic scripts, such as Chinese and Japanese, lowercasing does not apply at all!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stopwords

    Another form of preprocessing is to remove so-called stopwords. Stopwords are frequently occurring **function** words, such as determiners and articles (e.g., *the*, *an*), prepositions (*over*, *in*, *at*), and so on. Contrast these with content words, such as nouns (e.g., *dog*), verbs (e.g., *run*), and adjectives (e.g., *quick*).

    The logic of removing stopwords is that they contribute very little to the meaning of a text. Stopwords are also not good for distinguishing among texts, because they are so common and used in every text. However, removing stopwords can sometimes be counterproductive, as we'll see below.

    NLTK has a list of English stopwords built in. Let's save it to a variable so we can use it throughout the notebook:
    """)
    return


@app.cell
def _(stopwords):
    # save the English stopwords to a variable
    english_stopwords = stopwords.words('english')
    english_stopwords
    return (english_stopwords,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Have a look through the list above - there are a lot of words and pieces of words. We can use this list to remove stopwords with a list comprehension, keeping tokens only if they are *not* in the list.

    In the list comprehension below, I test whether the lowercased version of each token is in the stopwords list. This does not change the original token: it uses the lowercased version only for the test. So I get the best of both worlds - a decision based on a normalised version of the token, while keeping the raw token.
    """)
    return


@app.cell
def _():
    # bring in a quote to use:
    hitchhiker = """Far Out in the uncharted backwaters of the unfashionable end
    of the Western Spiral arm of the galaxy lies a small unregarded yellow sun"""
    return (hitchhiker,)


@app.cell
def _(english_stopwords, hitchhiker, nltk):
    # remove any token for which the lowercased version is in the stopwords list
    [token for token in nltk.word_tokenize(hitchhiker) if token.lower() not in english_stopwords]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What effect has removing stopwords had on the text? Can you still understand it?

    Let's try this out on a longer text, the script of the *Seinfeld* episode "The Marine Biologist":
    """)
    return


@app.cell
def _(requests):
    # load the script from the internet as one long string
    mb_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/marine_biologist.txt'
    mb_raw = requests.get(mb_url).text
    return (mb_raw,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's get an idea of the text. I'll use `nltk.sent_tokenize()` on the script and print out 23 sentences from near the end.

    (The loops in the next few cells use `sent1`, `sent2` and `sent3` as their variable names, because marimo only lets each variable be created in one cell.)
    """)
    return


@app.cell
def _(mb_raw, nltk):
    # 23 sentences from near the end of the text
    for sent1 in nltk.sent_tokenize(mb_raw)[350:373]:
      print(sent1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's see what happens when we remove stopwords. I use `' '.join()` and `nltk.word_tokenize()` inside the loop to split each sentence into tokens, remove the stopwords, and glue the tokens back together.

    What do you think of the output? Can you still understand the 'gist' of the text?
    """)
    return


@app.cell
def _(english_stopwords, mb_raw, nltk):
    for sent2 in nltk.sent_tokenize(mb_raw)[350:373]:
      print(' '.join([token for token in nltk.word_tokenize(sent2) if token.lower() not in english_stopwords]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The logic behind removing "stopwords" is that you could do this for *any* set of words that you want removed from a text. For example, what if I wanted to remove the names of the characters in the script? I could define my own list of stopwords and use those in the test:
    """)
    return


@app.cell
def _():
    # create a list of target names to remove:
    stopnames = ['ELAINE', 'JERRY', 'GEORGE', 'KRAMER', 'DIANE']
    return (stopnames,)


@app.cell
def _(mb_raw, nltk, stopnames):
    # remove the names
    for sent3 in nltk.sent_tokenize(mb_raw)[350:373]:
      print(' '.join([token for token in nltk.word_tokenize(sent3) if token not in stopnames]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## When removing stopwords goes wrong

    Is *not* a stopword? Check below:
    """)
    return


@app.cell
def _(english_stopwords):
    'not' in english_stopwords
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    It is! So is *no*. Now look at what happens to this sentence when we remove stopwords:
    """)
    return


@app.cell
def _(english_stopwords, nltk):
    [token for token in nltk.word_tokenize("This movie was not good.") if token.lower() not in english_stopwords]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The meaning has flipped from negative to positive. If we wanted to know whether a review was positive or negative (something we'll do later in the course with sentiment analysis), removing stopwords would have thrown away the most important word in the sentence. Whether a word "contributes very little to meaning" depends on what you are trying to find out.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Tokenizing with a regex pattern

    At the end of the regex notebook, you saw that NLTK's `RegexpTokenizer` lets us define tokens with a pattern. Here it is again with `\w+`, which means "one or more word characters in a row". Compare its output to `nltk.word_tokenize()` for the same sentence:
    """)
    return


@app.cell
def _(RegexpTokenizer):
    # a tokenizer which treats one or more word characters as a token
    word_tokenizer = RegexpTokenizer(r'\w+')

    word_tokenizer.tokenize("I can't even.")
    return (word_tokenizer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `RegexpTokenizer` gave us `can` and `t`, while `nltk.word_tokenize()` gave us `ca` and `n't`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # One text but many pipelines

    Every choice we've made in this notebook changes the tokens we end up with, and so changes anything we count with those tokens. Let's see how much.

    Below, the Marine Biologist script goes through several different **pipelines** (sequences of preprocessing steps). Each pipeline builds on the one before it, except for the last, which uses `RegexpTokenizer` instead of `nltk.word_tokenize()`.
    """)
    return


@app.cell
def _(english_stopwords, mb_raw, nltk, word_tokenizer):
    # pipeline 1: just .split()
    tokens_split = mb_raw.split()

    # pipeline 2: nltk.word_tokenize() instead
    tokens_nltk = nltk.word_tokenize(mb_raw)

    # pipeline 3: nltk tokens, lowercased
    tokens_lower = [token.lower() for token in tokens_nltk]

    # pipeline 4: lowercased nltk tokens, without punctuation
    tokens_no_punct = [token for token in tokens_lower if token.isalpha()]

    # pipeline 5: lowercased nltk tokens, without punctuation or stopwords
    tokens_no_stop = [token for token in tokens_no_punct if token not in english_stopwords]

    # pipeline 6: RegexpTokenizer on the lowercased text
    tokens_regex = word_tokenizer.tokenize(mb_raw.lower())
    return (
        tokens_lower,
        tokens_nltk,
        tokens_no_punct,
        tokens_no_stop,
        tokens_regex,
        tokens_split,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's put the number of tokens, number of types and TTR for each pipeline into a table. `pl.DataFrame()` (from the `polars` library) makes a table from a set of lists, where each list becomes a column. We'll use tables like this a lot more later in the course.
    """)
    return


@app.cell
def _(
    pl,
    tokens_lower,
    tokens_nltk,
    tokens_no_punct,
    tokens_no_stop,
    tokens_regex,
    tokens_split,
):
    pipeline_names = ['.split()', 'word_tokenize', '+ lowercase', '+ no punctuation', '+ no stopwords', 'RegexpTokenizer (lowercase)']
    pipeline_tokens = [tokens_split, tokens_nltk, tokens_lower, tokens_no_punct, tokens_no_stop, tokens_regex]

    pipeline_table = pl.DataFrame({
      'pipeline': pipeline_names,
      'tokens': [len(tokens) for tokens in pipeline_tokens],
      'types': [len(set(tokens)) for tokens in pipeline_tokens],
      'TTR': [round(len(set(tokens)) / len(tokens), 3) for tokens in pipeline_tokens],
    })

    pipeline_table
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Discussion

    - Which step changes the number of tokens the most? Which changes the number of types the most?
    - Which TTR is the "real" lexical diversity of the Marine Biologist?
    - If you were comparing the vocabulary of two TV scripts, which pipeline would you choose, and why? Would your answer change if you were interested in how characters speak (e.g., their use of punctuation or function words)?
    - Are there any preprocessing steps you think are missing?
    """)
    return


if __name__ == "__main__":
    app.run()
