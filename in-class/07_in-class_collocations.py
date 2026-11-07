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
    # **In-class: collocations**

    Today's plan:

    1. Review: bigrams, collocations, and measures of association
    2. Activities: a collocation explorer, frequency vs PMI vs Delta P, natural vs unnatural English, and multiword expressions
    3. Critical reflection
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
    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['punkt_tab', 'webtext', 'gutenberg', 'brown'])
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
    # **Review: bigrams and collocations - key concepts**

    - a **bigram** is any pair of adjacent tokens
    - a **collocation** is a pair of words which occur together more often than we would expect by chance
    - measures of association (PMI, Delta P) compare how often two words occur together with how often each word occurs on its own

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _(nltk):
    # how many bigrams will there be?
    list(nltk.bigrams(['we', 'live', 'in', 'a', 'society']))
    return


@app.cell
def _(nltk):
    # what happens if we give it a string instead of a list of tokens?
    list(nltk.bigrams('cat'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the next prediction, we need the Big Salad, cleaned and tokenised the same way as in the collocations notebook, plus the `pmi()` function:
    """)
    return


@app.cell
def _(FreqDist, nltk, requests):
    # load the Big Salad from the course repository
    big_salad = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/big_salad.txt').text

    def pre_process(x):
      # lowercase and remove punctuation
      x = x.lower()
      punctuation = '.;"!\'[]{}:><-_?,'
      return ''.join([char for char in x if char not in punctuation])

    # tokens, bigrams, and their frequencies
    big_salad_tokens = nltk.word_tokenize(pre_process(big_salad))
    big_salad_bigrams = list(nltk.bigrams(big_salad_tokens))
    big_salad_fdist = FreqDist(big_salad_tokens)
    big_salad_bigram_fdist = FreqDist(big_salad_bigrams)
    return (
        big_salad,
        big_salad_bigram_fdist,
        big_salad_bigrams,
        big_salad_fdist,
        big_salad_tokens,
    )


@app.cell
def _(
    big_salad_bigram_fdist,
    big_salad_bigrams,
    big_salad_fdist,
    big_salad_tokens,
    math,
):
    def pmi(w1, w2):
      # the probability of the bigram, and of each word on its own
      p_bigram = big_salad_bigram_fdist[(w1, w2)] / len(big_salad_bigrams)
      p_w1 = big_salad_fdist[w1] / len(big_salad_tokens)
      p_w2 = big_salad_fdist[w2] / len(big_salad_tokens)
      return math.log2(p_bigram / (p_w1 * p_w2))

    return (pmi,)


@app.cell
def _(big_salad_bigram_fdist):
    # which bigram is more frequent?
    print(big_salad_bigram_fdist[('you', 'know')])
    print(big_salad_bigram_fdist[('new', 'york')])
    return


@app.cell
def _(pmi):
    # which bigram has the higher PMI? Why?
    print(pmi('you', 'know'))
    print(pmi('new', 'york'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Review answers": mo.md(r'''
    - 5 tokens give 4 bigrams: there is always one fewer bigram than tokens
    - a string gives bigrams of *characters*: `('c', 'a'), ('a', 't')`
    - *you know* is far more frequent than *new york*, but *new york* has a much higher PMI (about 10.3 vs 3.8): *new* and *york* are rare on their own, so seeing them together is very surprising, whereas *you* and *know* are both so frequent that we would expect to see them together quite often by chance
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: collocation explorer**

    Choose a text and look at its collocations. Can you guess what the text is about from its collocations alone? What happens when you make the window bigger?

    (These texts are not cleaned, so watch out for capital letters and punctuation.)
    """)
    return


@app.cell
def _(Text, big_salad, nltk):
    # the texts to explore, as NLTK Text objects
    collocation_texts = {
      'Monty Python and the Holy Grail': Text(nltk.corpus.webtext.words('grail.txt')),
      'The Man Who Was Thursday': Text(nltk.corpus.gutenberg.words('chesterton-thursday.txt')),
      'Moby Dick': Text(nltk.corpus.gutenberg.words('melville-moby_dick.txt')),
      'Big Salad (Seinfeld scripts)': Text(nltk.word_tokenize(big_salad)),
    }
    return (collocation_texts,)


@app.cell
def _(collocation_texts, mo):
    collocation_choice = mo.ui.dropdown(options = list(collocation_texts.keys()), value = 'Monty Python and the Holy Grail', label = 'text:')
    collocation_number = mo.ui.slider(start = 5, stop = 50, step = 5, value = 20, label = 'number of collocations:')
    collocation_window = mo.ui.slider(start = 2, stop = 6, value = 2, label = 'window size:')
    mo.vstack([collocation_choice, collocation_number, collocation_window])
    return collocation_choice, collocation_number, collocation_window


@app.cell
def _(
    collocation_choice,
    collocation_number,
    collocation_texts,
    collocation_window,
):
    # .collocation_list() gives the collocations as a list of pairs
    collocation_texts[collocation_choice.value].collocation_list(num = collocation_number.value, window_size = collocation_window.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - Which collocations are names? Which are phrases? Which are something else entirely?
    - Look at the Big Salad. Why are so many of the collocations things like `('KRAMER', 'Yeah')`? (Think about the speaker labels.)
    - Increase the window size for *Holy Grail*. Why do pairs like `('saw', 'saw')` and `('squeak', 'squeak')` move up?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: frequency vs PMI vs Delta P**

    Type a word below to see every word which comes straight after it in the Big Salad. For each bigram, the table shows:

    - **frequency**: how many times the bigram occurs
    - **PMI**: how much more often the bigram occurs than we would expect by chance
    - **Delta P forward**: how much the first word predicts the second word
    - **Delta P backward**: how much the second word predicts the first word

    Click on a column name to sort the table by that column. Use the slider to hide bigrams which are very rare.
    """)
    return


@app.cell
def _(big_salad_bigram_fdist, big_salad_bigrams, big_salad_fdist):
    def delta_p(w1, w2):
      # the counts we need
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
def _(mo):
    association_word = mo.ui.text(value = 'you', label = 'first word:')
    association_minimum = mo.ui.slider(start = 1, stop = 20, value = 3, label = 'minimum frequency:')
    mo.vstack([association_word, association_minimum])
    return association_minimum, association_word


@app.cell
def _(
    association_minimum,
    association_word,
    big_salad_bigram_fdist,
    delta_p,
    pl,
    pmi,
):
    # find every bigram which starts with the chosen word
    association_rows = []

    for (first, second), pair_count in big_salad_bigram_fdist.items():
      if first == association_word.value.lower() and pair_count >= association_minimum.value:
        forward, backward = delta_p(first, second)
        association_rows.append({
          'bigram': first + ' ' + second,
          'frequency': pair_count,
          'PMI': round(pmi(first, second), 2),
          'Delta P forward': round(forward, 3),
          'Delta P backward': round(backward, 3),
        })

    pl.DataFrame(association_rows).sort('frequency', descending = True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - Start with *you*. Sort by frequency, then by PMI. Which bigrams are at the top of each? Why are they so different?
    - Move the minimum frequency down to 1. What happens to the top of the PMI column?
    - Try *new*, *ice*, and *the*. When is Delta P backward much bigger than Delta P forward? What does that tell you?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Formulas and notes on the measures": mo.md(r'''
    $$
    \text{PMI}(w_1, w_2) = \log_2\left(\frac{P(w_1, w_2)}{P(w_1) \times P(w_2)}\right)
    $$

    $$
    \Delta P_{forward} = P(w_2 \mid w_1) - P(w_2 \mid \text{not } w_1)
    $$

    $$
    \Delta P_{backward} = P(w_1 \mid w_2) - P(w_1 \mid \text{not } w_2)
    $$

    - PMI overrates rare pairs: if two words each occur once, and occur together that one time, they get a very high PMI, even though one occurrence tells us almost nothing. This is why we use a minimum frequency
    - Delta P is directional: in the Big Salad, *york* almost always comes after *new* (Delta P backward is close to 1), but *new* can be followed by lots of other words (*new car*, *new girlfriend*), so Delta P forward is much lower
    - NLTK's `.collocations()` uses yet another measure (the log-likelihood ratio), so its rankings won't match PMI exactly
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: natural vs unnatural English**

    Remember the table at the start of the collocations notebook: *fast food* sounds natural, but *quick food* sounds odd. Let's test some adjective + noun pairs against a corpus.

    Type two adjectives that mean similar things, and a list of nouns separated by commas. The table counts how many times each adjective + noun pair occurs in the Brown corpus.
    """)
    return


@app.cell
def _(FreqDist, nltk):
    # lowercase all of the words in Brown, and count the bigrams
    brown_words = [word.lower() for word in nltk.corpus.brown.words()]
    brown_bigram_fdist = FreqDist(nltk.bigrams(brown_words))
    return (brown_bigram_fdist,)


@app.cell
def _(mo):
    adjective1 = mo.ui.text(value = 'big', label = 'adjective 1:')
    adjective2 = mo.ui.text(value = 'large', label = 'adjective 2:')
    noun_list = mo.ui.text(value = 'man, house, car, number, amount, part, city, area', label = 'nouns:', full_width = True)
    mo.vstack([mo.hstack([adjective1, adjective2], justify = 'start'), noun_list])
    return adjective1, adjective2, noun_list


@app.cell
def _(adjective1, adjective2, brown_bigram_fdist, noun_list, pl):
    # split the nouns on commas and remove any spaces
    chosen_nouns = [noun.strip().lower() for noun in noun_list.value.split(',')]

    pl.DataFrame({
      'noun': chosen_nouns,
      adjective1.value: [brown_bigram_fdist[(adjective1.value.lower(), noun)] for noun in chosen_nouns],
      adjective2.value: [brown_bigram_fdist[(adjective2.value.lower(), noun)] for noun in chosen_nouns],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - *strong* vs *powerful*, with *tea, wind, argument, man, engine, coffee*
    - *quick* vs *fast*, with *look, glance, car, food, train, shower*
    - your own pairs! Do the counts match your intuitions about what sounds natural?
    - What do you notice about how many of the counts are 0? What does that tell you about the size of Brown?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: multiword expressions**

    At the end of the collocations notebook we asked: if *New York* is really one unit of meaning, should it be one token? And how would we decide which expressions to join?

    One option is to let a collocation measure suggest the candidates. Below are the 30 bigrams in the Big Salad with the highest PMI (only counting bigrams which occur at least 10 times). Choose which ones you think should be joined into a single token, and see what happens to the text.
    """)
    return


@app.cell
def _(BigramAssocMeasures, BigramCollocationFinder, big_salad_tokens, mo):
    # find the bigrams with the highest PMI, ignoring rare bigrams
    mwe_finder = BigramCollocationFinder.from_words(big_salad_tokens)
    mwe_finder.apply_freq_filter(10)
    mwe_candidates = [w1 + ' ' + w2 for (w1, w2) in mwe_finder.nbest(BigramAssocMeasures.pmi, 30)]

    mwe_choice = mo.ui.multiselect(options = mwe_candidates, value = ['ice cream', 'heart attack', 'marble rye'], label = 'join these expressions:')
    mwe_choice
    return (mwe_choice,)


@app.cell
def _(MWETokenizer, big_salad_tokens, mwe_choice, pl):
    # a tokenizer which joins the chosen expressions with an underscore
    mwe_tokenizer = MWETokenizer([tuple(expression.split()) for expression in mwe_choice.value], separator = '_')
    mwe_tokens = mwe_tokenizer.tokenize(big_salad_tokens)

    # compare the text before and after joining
    pl.DataFrame({
      'version': ['before', 'after'],
      'tokens': [len(big_salad_tokens), len(mwe_tokens)],
      'types': [len(set(big_salad_tokens)), len(set(mwe_tokens))],
      'TTR': [round(len(set(big_salad_tokens)) / len(big_salad_tokens), 4), round(len(set(mwe_tokens)) / len(mwe_tokens), 4)],
    })
    return (mwe_tokens,)


@app.cell
def _(FreqDist, mwe_tokens):
    # how often does each joined expression occur?
    FreqDist([token for token in mwe_tokens if '_' in token]).most_common()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - Which of the candidates are real multiword expressions? Which are names? Which are just two words that happen to appear together a lot in Seinfeld?
    - Join more expressions. Why does the number of types go *up* even though the number of tokens goes down?
    - If you had to choose expressions to join for *every* text, not just the Big Salad, how would you do it?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Multiword expression notes": mo.md(r'''
    - joining expressions reduces the number of tokens (two tokens become one), but can increase the number of types, because *new_york* is a new type while *new* and *york* usually still occur elsewhere
    - the PMI candidates mix multiword expressions (*ice cream*, *heart attack*), names (*keith hernandez*, *marisa tomei*) and things which are frequent only because of the plot (*marble rye*, *puffy shirt*)
    - there's no perfect way to choose: common options are a list made by hand, a dictionary of multiword expressions, or a collocation measure with a frequency cut-off, and each gives different results
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. Collocations tell us what is "natural" *in the corpus they came from*. If a computer learned what counts as natural English from Seinfeld scripts, or from American writing in the 1960s (Brown), what would it think sounds natural or odd?
    2. Whose English ends up counting as "natural"? What might happen to varieties of English that are not well represented in the corpora we use?
    3. PMI, Delta P, and log-likelihood can all give different answers about which words "belong together". If different measures disagree, which one is right?
    4. Deciding which multiword expressions to join changes the tokens, and so it changes every count and measure built on those tokens. Who should make these decisions, and how should they be reported?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - a corpus is a sample of language from particular people, places, times and genres; collocations learned from it reflect that sample, not "English" in general
    - varieties which are under-represented (e.g., New Zealand English, or the English of second language users) can end up looking "unnatural" simply because they aren't in the data, and tools built on the data (autocomplete, grammar checkers, language models) can then treat them as errors
    - the measures answer different questions (surprise, prediction, statistical evidence), so there isn't one right answer: the choice should depend on the question you are asking, and be reported
    - tokenisation decisions like joining multiword expressions are usually invisible in the final results, but they change everything downstream, so they need to be stated clearly
    ''')})
    return


if __name__ == "__main__":
    app.run()
