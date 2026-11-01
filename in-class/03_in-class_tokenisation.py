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
    # **Tokenisation and preprocessing**

    - what counts as a "word"?
    - what does `.split()` get wrong?
    - how do our preprocessing choices change the results?

    Today's plan:

    1. Review: `.split()`, tokenizers and preprocessing
    2. Activity: a preprocessing control panel, with three prompts
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import re
    import nltk
    nltk.download(['punkt_tab', 'stopwords'])
    from nltk.corpus import stopwords
    from nltk.tokenize import RegexpTokenizer

    english_stopwords = stopwords.words('english')
    word_tokenizer = RegexpTokenizer(r'\w+')
    return RegexpTokenizer, english_stopwords, nltk, re, word_tokenizer


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: the most basic way to tokenise a string, `.split()`**

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _():
    "and isn't it ironic"
    return


@app.cell
def _():
    # are these words?
    "and isn't it ironic".split()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The default behaviour of `.split()` assumes that spaces are a stable word boundary.
    """)
    return


@app.cell
def _():
    # what are two issues with this output?

    'what an open-ended problem this is!'.split()
    return


@app.cell
def _():
    # hmm, what's happening here?

    '大家好'.split()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can split on any character - the default is to split on spaces.
    """)
    return


@app.cell
def _():
    'prying.open.my.third.eye'.split('.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Review: tokenizers and preprocessing**

    From the self-study notebook: **preprocessing** means the steps we take to prepare a text before analysing it, such as lowercasing, removing punctuation, and removing stopwords. A **tokenizer** splits a text into tokens.

    Predict the output of each cell before you run it.
    """)
    return


@app.cell
def _(nltk):
    # how does nltk split a contraction?
    nltk.word_tokenize("I can't even.")
    return


@app.cell
def _(re):
    # what happens to the contraction if we remove punctuation first?
    re.sub(r'[^\w\s]', '', "I can't even.")
    return


@app.cell
def _(english_stopwords):
    # is 'not' a stopword?
    'not' in english_stopwords
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: preprocessing control panel**

    Type or paste a text into the box, then switch the preprocessing steps on and off and choose a tokenizer. The results update as you go.

    The panel applies the steps in this order:

    1. lowercase the text
    2. remove punctuation (using `re.sub(r'[^\w\s]', '', text)`)
    3. tokenise
    4. remove stopwords

    Use the panel below to work through these three prompts.

    **Prompt 1: the order of steps.** Is the order above the best order? What would change if we removed punctuation *after* tokenising?

    **Prompt 2: break the tokenizer.** Come up with strings that you think will trip up a tokenizer, and paste them into the panel. Some ideas to get started:

    - contractions: `I can't believe you won't`
    - hyphens: `a well-known state-of-the-art tool`
    - abbreviations: `Dr. Smith arrived at 3 p.m.`
    - a URL or an email address
    - emoji: `that was great 😂😂`
    - a language without spaces: `大家好`

    For each one: which tokenizer does best? Is there a "right" answer?

    **Prompt 3: stopwords and TTR.** Copy the text below into the panel, then switch **remove stopwords** on and off. What happens to the number of tokens, and to TTR? Can you still understand the text without its stopwords? What does this tell us about what stopwords *are*, and what removing them does to lexical diversity?

    ```
    Irony is a juxtaposition of what, on the surface, appears to be the case with what is actually or expected to be the case. Originally a rhetorical device and literary technique, irony has also come to assume a metaphysical significance with implications for one's attitude towards life. The concept originated in ancient Greece, where it described a dramatic character who pretended to be less intelligent than he actually was in order to outwit boastful opponents.
    ```
    """)
    return


@app.cell
def _(mo):
    # the controls for the panel
    panel_text_box = mo.ui.text_area(value='The past, the present, and the future walked into a bar. It was tense.', label='your text:', full_width=True)
    lowercase_check = mo.ui.checkbox(label='lowercase')
    punct_check = mo.ui.checkbox(label='remove punctuation')
    stopword_check = mo.ui.checkbox(label='remove stopwords')
    tokenizer_choice = mo.ui.radio(options=['.split()', 'nltk.word_tokenize()', "RegexpTokenizer(r'\\w+')"], value='.split()', label='tokenizer:')

    mo.vstack([panel_text_box, mo.hstack([lowercase_check, punct_check, stopword_check], justify='start'), tokenizer_choice])
    return (
        lowercase_check,
        panel_text_box,
        punct_check,
        stopword_check,
        tokenizer_choice,
    )


@app.cell
def _(
    english_stopwords,
    lowercase_check,
    mo,
    nltk,
    panel_text_box,
    punct_check,
    re,
    stopword_check,
    tokenizer_choice,
    word_tokenizer,
):
    # apply the chosen steps, in order
    panel_text = panel_text_box.value

    if lowercase_check.value:
      panel_text = panel_text.lower()

    if punct_check.value:
      panel_text = re.sub(r'[^\w\s]', '', panel_text)

    if tokenizer_choice.value == '.split()':
      panel_tokens = panel_text.split()
    elif tokenizer_choice.value == 'nltk.word_tokenize()':
      panel_tokens = nltk.word_tokenize(panel_text)
    else:
      panel_tokens = word_tokenizer.tokenize(panel_text)

    if stopword_check.value:
      panel_tokens = [token for token in panel_tokens if token.lower() not in english_stopwords]

    # show the raw text and the tokens side by side
    mo.hstack([
      mo.md(f"**Raw text**\n\n{panel_text_box.value}"),
      mo.md(f"**Tokens:** {len(panel_tokens)} &nbsp; **Types:** {len(set(panel_tokens))} &nbsp; **TTR:** {round(len(set(panel_tokens)) / len(panel_tokens), 3)}\n\n`{panel_tokens}`"),
    ], widths=[1, 2])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({
      "Notes: prompt 1 (the order of steps)": mo.md(r'''
    - removing punctuation *before* tokenising turns `can't` into `cant`, and `nltk.word_tokenize()` can no longer split it into `ca` + `n't`
    - removing punctuation *after* tokenising (e.g. dropping tokens that aren't `.isalnum()`) keeps `ca` but throws away `n't`
    '''),
      "Notes: prompt 2 (break the tokenizer)": mo.md(r'''
    - every tokenizer is a set of decisions about what a word is, and each one gets some cases "wrong"
    - `nltk.word_tokenize()` splits contractions (`ca` + `n't`); `RegexpTokenizer(r'\w+')` splits them differently (`can` + `t`) and also splits hyphenated words
    - removing punctuation *before* tokenising turns `can't` into `cant`: the order of steps matters
    - none of them can split `大家好`, because they all rely on spaces or punctuation
        - this is two words: 大家 + 好
    '''),
      "Notes: prompt 3 (stopwords and TTR)": mo.md(r'''
    - stopwords are the most frequent, mostly grammatical words, and they make up a large share of the tokens in any text
    - they are also the words that repeat the most, so removing them **raises** TTR
    - so TTR with and without stopwords are measuring slightly different things, and you need to say which one you used
    '''),
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    # **Critical reflection**

    1. The panel applies its steps in a fixed order. Which order would you choose? Does the "right" order depend on what you are trying to find out?
    2. Every tokenizer you tried made different decisions about what a word is. If two studies analysed the same text with different tokenizers, could you compare their results?
    3. Removing stopwords throws away words that are assumed to carry little meaning. When might those words be exactly what you are interested in?
    4. None of the tokenizers could split `大家好`. What does that suggest about who these tools were built for, and what happens to languages they weren't built for?
    """), kind='info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - there is no single right order: removing punctuation before tokenising turns `can't` into `cant`, which is fine for some questions and a problem for others; the order should follow from the research question
    - results from different tokenizers aren't directly comparable, because the tokens themselves are different; this is why studies need to report their preprocessing
    - stopwords can be the point: negation (`not`) matters for sentiment, pronouns (`I`, `we`, `they`) matter for studying identity and style, and function words are some of the best clues to who wrote a text
    - most NLP tools were built for English and other languages that put spaces between words; languages that don't, or that have fewer resources, get worse results or need their own tools
    ''')})
    return


if __name__ == "__main__":
    app.run()
