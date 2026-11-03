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
    #### Relevant NLTK book Sections

    [NLTK Book, Chapter 5, Section 1 and Section 2](https://www.nltk.org/book/ch05.html#parts_of_speech_index_term)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Parts of Speech**

    This notebook discusses a basic lexical property: parts of speech. We have thus far dealt with searching and manipulating text based on the orthographic features of words (i.e., their written forms). That means we have remained focused on the forms of the words (i.e., types and tokens). This has given us the ability to measure basic yet important aspects of texts: length, word frequency, and also some considerations about lexical diversity.

    You probably have some familiarity with how words are classified into different lexical and syntactic categories, such as nouns, verbs, adjectives, pronouns, etc. These categories are called *parts of speech* (POS), and can be used as another source of information which can be exploited during linguistic analysis of texts.

    In NLP it is common to see reference made to POS **Tags**, which are annotations associated with a word to represent more information about that word (i.e., metadata). Just like the base form of words, these tags can be counted and compared, and also provide critical information for building and understanding grammars of languages.

    Let's explore how to tag texts and then use these tags to query information about texts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Using `nltk.pos_tag()`**

    The NLTK library includes a function which will automatically assign part of speech tags to an English text. To use this function, we need to import NLTK and download some additional resources.
    """)
    return


@app.cell
def _():
    # import the libraries for this notebook
    import re
    import requests
    import polars as pl
    import nltk
    from nltk import FreqDist

    # import resources for tokenizing and tagging
    nltk.download(['punkt_tab', 'averaged_perceptron_tagger_eng', 'tagsets_json', 'treebank', 'universal_tagset', 'state_union'])
    return FreqDist, nltk, pl, re, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The NLTK function expects a list of tokens and is used like this:

    > `nltk.pos_tag(tokens)`

    The results will be a list of `(word,tag)` pairs (which are in the form of a `tuple` - another type of Python object.)

    The next three cells demonstrate an example of how to POS tag a text using NLTK:
    """)
    return


@app.cell
def _():
    # step 1: have some text
    rant = "You know, we're living in a society! We're supposed to act in a civilized way."
    return (rant,)


@app.cell
def _(nltk, rant):
    # step 2: tokenize
    rant_tokens = nltk.word_tokenize(rant)
    return (rant_tokens,)


@app.cell
def _(nltk, rant_tokens):
    # step 3: tag
    rant_pos = nltk.pos_tag(rant_tokens)

    # look at the resulting (word, tag) pairs
    [tagged for tagged in rant_pos]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    POS tagging has created a list of tuples of our words, with `(word, tag)` format. The tags are informative and indeed go beyond broader word categories such as NOUN and VERB. For example,

    ```
    VBP = verb, present tense, not 3rd person singular
    ```

    while

    ```
    VBG = verb, present participle or gerund.
    ```

    These tags are from the Penn tagset which is one commonly used set of POS tags. You can run the following cell to see the full list or by [going to this link](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html).

    Take a moment to scroll through these tags and explore their explanations and examples.
    """)
    return


@app.cell
def _(nltk):
    # full list of tags, with definitions and examples
    nltk.help.upenn_tagset()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can also look up one specific tag by supplying the tag as a string to the `help` function:
    """)
    return


@app.cell
def _(nltk):
    # what is the NNP tag?
    nltk.help.upenn_tagset('NNP')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Discussion**

    Part of speech tags help make sense of words in the context of other words. Consider this example from the NLTK book - what is the difference in use for the instances of *refuse* and *permit*?

    Are there any clues provided by the words which come *before* refuse/permit that might help the tagger choose the right part of speech?
    """)
    return


@app.cell
def _(nltk):
    nltk.pos_tag(nltk.word_tokenize("They refuse to permit us to obtain the refuse permit"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can supply our own examples as well — let us compare two uses of the same word "comb":
    """)
    return


@app.cell
def _(nltk):
    # what pos tag does the word "comb" have in this example?
    nltk.pos_tag(nltk.word_tokenize('Quick, comb the desert for droids!'))
    return


@app.cell
def _(nltk):
    # and what pos tag does the word "comb" have in this example?
    nltk.pos_tag(nltk.word_tokenize('Where is my comb?'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, adding POS tag information provides more information about a text, which becomes useful for more advanced NLP applications such as information extraction, text prediction, and so on. Because the tags are stored as strings, you can use knowledge of Python to search or filter through the list in order to find specific words associated with specific tags.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    - Explore using `nltk.pos_tag()` on some texts.
    - See if you can understand the different POS tags and what they mean about the words.
    - Can you "break" the tagger or have it produce inaccurate results?
    - The tagger has a rule that if it does not know the tag for a word, it will automatically assign a default POS tag. Can you figure out what this default tag is?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Frequency distributions and POS tags**

    The NLTK book demonstrates how we can use frequency distributions to find the most common words associated with a particular part of speech. They do so by using a [pre-tagged corpus](https://catalog.ldc.upenn.edu/LDC99T42) comprised of articles from the *Wall Street Journal*. The corpus is tagged with Penn Treebank tags, but here we ask NLTK to convert them to the simpler [universal tag set](https://universaldependencies.org/u/pos/), which has fewer, broader tags (such as `NOUN`, `VERB` and `ADJ`).

    We can access this corpus through NLTK.
    """)
    return


@app.cell
def _(nltk):
    # load in Penn Treebank corpus using universal pos tags (they are simpler)
    wsj = nltk.corpus.treebank.tagged_words(tagset = 'universal')
    wsj
    return (wsj,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The corpus is tagged, so if we use `nltk.FreqDist()`, we will get a frequency distribution of `(word, tag)` pairs.
    """)
    return


@app.cell
def _(nltk, wsj):
    # create a frequency distribution of the pairs
    word_tag_fd = nltk.FreqDist(wsj)

    # not surprisingly, the most common pairs are punctuation and function words.
    word_tag_fd.most_common(10)
    return (word_tag_fd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can then run a conditional test on the frequency distribution to find the most common words of a certain part of speech category, such as finding the most common verbs.

    To do so, we run a list comprehension with a conditional test over the results of the frequency distribution. Note that in the loop we specify the `((word, tag),freq)` nature of each item being iterated over.
    """)
    return


@app.cell
def _(word_tag_fd):
    # ask for just verbs (leaving most_common empty means it prints all of the words)
    # I included a slice to 25 just so it doesn't spam the screen
    [word for ((word, tag), freq) in word_tag_fd.most_common() if tag == 'VERB'][:25]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Words with more than one part of speech**

    Finding the most common verbs is interesting, but we can also flip the question around: for one word, which parts of speech does it appear as, and how often?

    We can answer this with a list comprehension and `FreqDist()`. The list comprehension goes through every `(word, tag)` pair in the corpus, and keeps the tag whenever the word is the one we are interested in. Then `FreqDist()` counts the tags.

    Because we will do this for several words, let's put it in a function:
    """)
    return


@app.cell
def _(FreqDist, wsj):
    def tag_counts(target_word):
      # count the tags that target_word appears with in the WSJ corpus
      return FreqDist([tag for (word, tag) in wsj if word == target_word])

    return (tag_counts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This part is really cool – you can see that words are not always used with just one part of speech tag.

    Yield is used as both a verb and noun, at a somewhat balanced rate. Cut is used as a verb much more frequently than as a noun.
    """)
    return


@app.cell
def _(tag_counts):
    # you can use .most_common() to sort the tags from most to least frequent
    tag_counts('yield').most_common()
    return


@app.cell
def _(tag_counts):
    tag_counts('cut').most_common()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some words are more restricted to specific parts of speech, these are the so-called function words. What do you think happened with these tags for `the` that are not `det`?
    """)
    return


@app.cell
def _(tag_counts):
    tag_counts('the').most_common()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can obtain the initial treebank pos tagset by loading in the corpus and not specifying that you need the "universal" tagset. The treebank tagset is more detailed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    Spend some time using `tag_counts()` for different words.

    - Which words are more likely to appear in different POS?
    - Which ones are not?
    """)
    return


@app.cell
def _():
    # Look at different POS tags here.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Tagging Big Salad**

    We can easily tag our texts using the `nltk.pos_tag()` function. It becomes another step after tokenising. In the next cell I load the Big Salad script and tokenise it.

    Notice that I do **not** lowercase the text or remove the punctuation first. The tagger was trained on ordinary written text, with capital letters and punctuation, and it uses them as clues (for example, a capital letter in the middle of a sentence suggests a name). We'll see what happens if we take those clues away below.
    """)
    return


@app.cell
def _(nltk, requests):
    # load in the script as one long string
    big_salad_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/big_salad.txt'
    big_salad = requests.get(big_salad_url).text

    # tokenise
    big_salad_tokens = nltk.word_tokenize(big_salad)
    return big_salad, big_salad_tokens


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Then we can tag the text - it takes a little while to run because the text is longer.
    """)
    return


@app.cell
def _(big_salad_tokens, nltk):
    # tag the tokens - takes a little while to run
    big_salad_tagged = nltk.pos_tag(big_salad_tokens)
    return (big_salad_tagged,)


@app.cell
def _(big_salad_tagged):
    # look at first ten token/tag pairs
    big_salad_tagged[:10]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Does preprocessing change the tags?**

    Let's tag the script a second time, but this time lowercase it and remove the punctuation first, like we did in the tokenisation notebook.
    """)
    return


@app.cell
def _(big_salad, nltk, re):
    # lowercase and remove punctuation, then tokenise and tag
    big_salad_cleaned = re.sub(r'[^\w\s]', '', big_salad.lower())
    big_salad_cleaned_tagged = nltk.pos_tag(nltk.word_tokenize(big_salad_cleaned))
    return (big_salad_cleaned_tagged,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's count the tags in each version. `NNP` is the Penn tag for a proper noun (a name), such as *Jerry* or *Elaine*. What happens to it?
    """)
    return


@app.cell
def _(FreqDist, big_salad_cleaned_tagged, big_salad_tagged):
    # count the tags in each version
    raw_tag_fdist = FreqDist([tag for (word, tag) in big_salad_tagged])
    cleaned_tag_fdist = FreqDist([tag for (word, tag) in big_salad_cleaned_tagged])

    print(f"NNP tags in the original text: {raw_tag_fdist['NNP']}")
    print(f"NNP tags in the lowercased, cleaned text: {cleaned_tag_fdist['NNP']}")
    return cleaned_tag_fdist, raw_tag_fdist


@app.cell
def _(cleaned_tag_fdist, raw_tag_fdist):
    # the ten most common tags in each version
    print(raw_tag_fdist.most_common(10))
    print(cleaned_tag_fdist.most_common(10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Preprocessing changes what the tagger sees, so it changes the tags. Just like in the tokenisation notebook, the **order** of the steps matters: if you want POS tags, tag first, and then lowercase or remove punctuation afterwards if you need to.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Frequent word/tag pairs**

    Let's go back to the original tagged script, and create a FreqDist of the token/tag pairs to locate some frequent and infrequent combinations

    (note that I excluded punctuation in the list comprehension)
    """)
    return


@app.cell
def _(big_salad_tagged, nltk):
    big_salad_tagged_fdist = nltk.FreqDist([pair for pair in big_salad_tagged if pair[1].isalpha()])
    return (big_salad_tagged_fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the top ten most frequent word/tag pairs. Do these make sense?
    """)
    return


@app.cell
def _(big_salad_tagged_fdist):
    # top ten most frequent word/tag pairs.
    big_salad_tagged_fdist.most_common(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Recall that the `.hapaxes()` function gives you things which occur only one time. Look at the results - remember that these are not tokens which occur only one time, but instead token + tag combinations that occur only one time. This might be a way to find mistagged tokens, or tokens which are spelled wrong and/or idiosyncratically.
    """)
    return


@app.cell
def _(big_salad_tagged_fdist):
    big_salad_tagged_fdist.hapaxes()[:20]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Lexical density**

    POS tags let us measure things about a text that we couldn't measure from word forms alone. One example is **lexical density**: the proportion of the words in a text that are *content words* (nouns, verbs, adjectives and adverbs), rather than *function words* (determiners, prepositions, pronouns, conjunctions, and so on).

    $$
    \text{lexical density} = \frac{\text{number of content words}}{\text{number of words}}
    $$

    A text with a high lexical density packs a lot of information into its words (think of a news report or an academic article), while a text with a low lexical density has more of the "glue" words that hold sentences together (think of casual conversation).

    With Penn tags, all the noun tags start with `NN`, all the verb tags with `VB`, adjectives with `JJ` and adverbs with `RB`. So we can find content words by checking the first two letters of each tag. The function below only counts tokens made of letters (using `.isalpha()`), so that punctuation is not counted as a word.
    """)
    return


@app.function
def lexical_density(tagged_tokens):
  # keep only the tokens that are words (no punctuation or numbers)
  words = [(word, tag) for (word, tag) in tagged_tokens if word.isalpha()]

  # keep only the content words: tags starting with NN, VB, JJ or RB
  content_words = [(word, tag) for (word, tag) in words if tag[:2] in ['NN', 'VB', 'JJ', 'RB']]

  return len(content_words) / len(words)


@app.cell
def _(big_salad_tagged):
    # lexical density of the Big Salad script
    lexical_density(big_salad_tagged)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's compare the script with a very different kind of text: George W. Bush's 2006 State of the Union speech.
    """)
    return


@app.cell
def _(nltk):
    # tag the speech (it is already tokenised by the corpus)
    speech_tagged = nltk.pos_tag(nltk.corpus.state_union.words('2006-GWBush.txt'))

    lexical_density(speech_tagged)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which text has the higher lexical density? Does that match what you would expect from a TV script and a political speech?

    > **Think about it:** our function counts every word with a `VB` tag as a content word. But words like *is*, *have* and *do* also get `VB` tags, even when they are auxiliary verbs (e.g., *I **have** eaten*), which are really function words. How might this affect the results? What else does our definition of "content word" depend on?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Speaker labels**

    A TV script has something that most texts don't: **speaker labels**. Look at the start of the Big Salad script below. Every line begins with the name of the character who is speaking.
    """)
    return


@app.cell
def _(big_salad):
    # the first 300 characters of the script
    print(big_salad[:300])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Those names aren't words that anyone *says*, but the tagger tags them anyway (mostly as proper nouns, `NNP`), so our function counts them as content words.

    Let's find the speaker labels. In this script, each label is the first word of a line, written in capital letters. The cell below goes through every line of the script, and keeps the first word of the line if it is all uppercase. Using `set()` gives us each label once.
    """)
    return


@app.cell
def _(big_salad):
    # the first word of every line, if it is in capital letters
    speaker_labels = set([line.split()[0] for line in big_salad.split('\n') if line.split() and line.split()[0].isupper()])

    speaker_labels
    return (speaker_labels,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can make a version of the tagged script without the speaker labels, and compare the lexical density of the two versions:
    """)
    return


@app.cell
def _(big_salad_tagged, speaker_labels):
    # remove every token that is a speaker label
    big_salad_no_labels = [(word, tag) for (word, tag) in big_salad_tagged if word not in speaker_labels]

    print(f"tokens with speaker labels:    {len(big_salad_tagged)}")
    print(f"tokens without speaker labels: {len(big_salad_no_labels)}")
    print()
    print(f"lexical density with speaker labels:    {lexical_density(big_salad_tagged)}")
    print(f"lexical density without speaker labels: {lexical_density(big_salad_no_labels)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How much did the lexical density change? How does the version without speaker labels compare to the State of the Union speech now?

    Nothing about the language in the script changed: only what we counted as part of the "text". When you calculate a measure on a corpus, it's worth checking what is actually in the files (labels, headers, page numbers, stage directions...), because the measure will count all of it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Word length, frequency, and part of speech**

    At the start of the frequency notebook, we said that word frequency correlates with other properties of words, such as word length (shorter words are more frequent) and part of speech. Now that we have POS tags, we can test this, and see how it relates to part of speech.

    Let's use the WSJ corpus again. First, we make a frequency distribution of the (lowercased) words, keeping only tokens made of letters:
    """)
    return


@app.cell
def _(FreqDist, wsj):
    # frequency of every lowercased word in WSJ
    wsj_fdist = FreqDist([word.lower() for (word, tag) in wsj if word.isalpha()])
    return (wsj_fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we want the most common tag for each word. We make a FreqDist of `(word, tag)` pairs, then go through it from the most to the least frequent pair, and save the first tag we see for each word in a dictionary. Because we go from most to least frequent, the first tag we see for a word is its most common tag.
    """)
    return


@app.cell
def _(FreqDist, wsj):
    # frequency of every lowercased (word, tag) pair
    wsj_pair_fdist = FreqDist([(word.lower(), tag) for (word, tag) in wsj if word.isalpha()])

    # a dictionary of each word's most common tag
    main_tag = {}
    for (pair, count) in wsj_pair_fdist.most_common():
      word_type = pair[0]
      pair_tag = pair[1]
      if word_type not in main_tag:
        main_tag[word_type] = pair_tag
    return (main_tag,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can put all of this into a table with `polars` (you saw `pl.DataFrame()` at the end of the tokenisation notebook). Each row is one word type, with its length, its frequency, and its most common tag:
    """)
    return


@app.cell
def _(main_tag, pl, wsj_fdist):
    # the list of word types
    wsj_types = list(wsj_fdist.keys())

    # a table with one row per word type
    pos_table = pl.DataFrame({
      'word': wsj_types,
      'length': [len(word) for word in wsj_types],
      'frequency': [wsj_fdist[word] for word in wsj_types],
      'tag': [main_tag[word] for word in wsj_types],
    })

    pos_table
    return (pos_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Average word length by part of speech

    Polars can group the rows of a table by the values in one column, and then calculate something for each group. Below, `group_by('tag')` groups the word types by their tag, and `agg()` calculates the average length and the number of word types for each tag. Finally, `sort()` orders the table by average length.

    If you find the polars syntax confusing, don't worry, there are other ways of working with data like this. I just wanted to show you in a somewhat organised way!

    Which parts of speech have the shortest words? The longest? Does that fit with what you know about function and content words?
    """)
    return


@app.cell
def _(pl, pos_table):
    pos_table.group_by('tag').agg(
      pl.col('length').mean().alias('average length'),
      pl.len().alias('number of word types'),
    ).sort('average length')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Is word length correlated with frequency?

    A **correlation** tells us how strongly two measures go up or down together, on a scale from -1 to 1. A negative correlation means that as one goes up, the other goes down.

    Because word frequency is so skewed (remember Zipf's law: a few words are extremely frequent and most are rare), we use a **Spearman** correlation, which compares the *ranks* of the values rather than the values themselves. This stops a handful of extremely frequent words from dominating the result.
    """)
    return


@app.cell
def _(pl, pos_table):
    pos_table.select(pl.corr('length', 'frequency', method = 'spearman'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Is the correlation positive or negative? Strong or weak? Does it support the claim that shorter words are more frequent?

    What might be causing the relationship: is it about length itself, or about the kinds of words (function words vs content words) that tend to be short?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Adding your own tags**

    You can manually tag your own text using a built-in NLTK function, `nltk.tag.str2tuple`. You supply a word and tag in the form of `word/tag`, and the result is a (word, tag) pair. For example, below I add the POS tag "NN" to the word "fly":
    """)
    return


@app.cell
def _(nltk):
    tagged_token = nltk.tag.str2tuple('fly/NN')
    tagged_token
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can then quickly add a number of tags to a text in one go by writing raw strings with word/tag pairs:
    """)
    return


@app.cell
def _(nltk):
    # add tags to a longer text, then tokenize
    raw_text = 'We/PRP live/VBP in/IN a/DT society/NN'

    tokenized_text = nltk.word_tokenize(raw_text)
    tokenized_text
    return (tokenized_text,)


@app.cell
def _(nltk, tokenized_text):
    # now split the tags
    [nltk.tag.str2tuple(w) for w in tokenized_text]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Why would you want to add your own tags?**

    You might wonder what the point of adding your own tags is, especially if you find you are not super confident about which tags should be used for a particular word! One of the reasons NLTK shows this to you is to provide a glimpse into how some corpora come tagged, and how NLTK reads those tags and provides them to you.

    Another potential use is that you could in theory supply any tags you wanted to your text. So, instead of tagging each word with part of speech, you could devise your own coding scheme for other properties of words. For example, if you had an example of speech which mixed two languages, you could tag the language of each word:
    """)
    return


@app.cell
def _():
    # tag words in English/Mandarin
    code_switch = 'Soda/EN is/EN a/EN 很/ZH 乖/ZH 的/ZH 狗/ZH'
    return (code_switch,)


@app.cell
def _(code_switch, nltk):
    # now my text can be searched for "EN" or "ZH"
    [nltk.tag.str2tuple(w) for w in nltk.word_tokenize(code_switch)]
    return


if __name__ == "__main__":
    app.run()
