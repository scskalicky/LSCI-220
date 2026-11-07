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
    # **In-class: parts of speech**

    Today's plan:

    1. Review: POS tags, what they mean, and how they are stored
    2. Activities: tag profiles, breaking the tagger, and a tag explorer
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import requests
    import matplotlib.pyplot as plt
    import polars as pl
    import nltk
    from nltk import FreqDist
    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['punkt_tab', 'averaged_perceptron_tagger_eng', 'tagsets_json', 'universal_tagset', 'genesis', 'brown'])
    return FreqDist, nltk, pl, plt, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: part of speech tags - key concepts**

    - what they are
    - how to obtain them
    - how they are stored (as `(word, tag)` tuples)

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _(nltk):
    # obtaining part of speech tags is relatively easy
    nltk.pos_tag(nltk.word_tokenize('the blarg'))
    return


@app.cell
def _(nltk):
    # but what do they mean?!
    nltk.help.upenn_tagset('NNP')
    return


@app.cell
def _(nltk):
    # look up a specific tag
    nltk.help.upenn_tagset('JJ')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Tagset: https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html

    ## POS tags are tuples

    A tuple is the `()` data container that is like a list but is immutable (it can't be changed once it's made).
    """)
    return


@app.cell
def _(nltk):
    for pair in nltk.pos_tag(nltk.word_tokenize('colourless green ideas sleep furiously')):
      print(f'the full thing is {pair}')
      print(f'get the first part: {pair[0]}')
      print(f'get the second part: {pair[1]}', end = '\n\n')
    return


@app.cell
def _(nltk):
    # what will happen if we give it a string instead of a list of tokens?
    nltk.pos_tag('colourless green ideas sleep furiously')
    return


@app.cell
def _(nltk):
    # what is going on here?
    nltk.pos_tag(['cat', 'comb', 'asdf', 'bbbbb'])
    return


@app.cell
def _(nltk):
    # and here? (focus on comb)
    nltk.pos_tag(nltk.word_tokenize('the woman had a comb. they will comb her hair.'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: tag profiles**

    In the self-study notebook, we used POS tags to compare the lexical density of a TV script and a speech. Let's go further, and compare the whole **part of speech profile** of two texts: what percentage of each text is nouns, verbs, pronouns, and so on?

    To make the profiles easy to compare, we'll use the simpler **universal tagset**, which has just 12 broad tags:

    | tag | meaning | examples |
    |---|---|---|
    | `NOUN` | nouns | *salad, Jerry* |
    | `VERB` | verbs | *went, is* |
    | `ADJ` | adjectives | *big, green* |
    | `ADV` | adverbs | *really, now* |
    | `PRON` | pronouns | *I, they, it* |
    | `DET` | determiners and articles | *the, a, this* |
    | `ADP` | prepositions (adpositions) | *in, of, to* |
    | `CONJ` | conjunctions | *and, but* |
    | `PRT` | particles | *up, not, 's* |
    | `NUM` | numbers | *two, 1965* |
    | `X` | other (foreign words, typos) | |
    | `.` | punctuation | |

    First, the texts (the first 50,000 tokens of each):
    """)
    return


@app.cell
def _(nltk, requests):
    # the texts to explore, as lists of tokens
    big_salad_text = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/big_salad.txt').text

    explorer_texts = {
      'Genesis': list(nltk.corpus.genesis.words('english-kjv.txt'))[:50000],
      'Big Salad (Seinfeld scripts)': nltk.word_tokenize(big_salad_text)[:50000],
      'Brown: news': list(nltk.corpus.brown.words(categories = 'news'))[:50000],
      'Brown: romance': list(nltk.corpus.brown.words(categories = 'romance'))[:50000],
    }
    return (explorer_texts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Choose two texts to compare. Each text is tagged (using its first 20,000 tokens, to keep things quick), punctuation is left out, and then `FreqDist()` counts the tags. Because the texts have different numbers of words, the counts are turned into **percentages**, just like normalising in the frequency session.
    """)
    return


@app.cell
def _(explorer_texts, mo):
    profile_choice_a = mo.ui.dropdown(options = list(explorer_texts.keys()), value = 'Big Salad (Seinfeld scripts)', label = 'text A:')
    profile_choice_b = mo.ui.dropdown(options = list(explorer_texts.keys()), value = 'Brown: news', label = 'text B:')
    mo.hstack([profile_choice_a, profile_choice_b], justify = 'start')
    return profile_choice_a, profile_choice_b


@app.cell
def _(FreqDist, explorer_texts, nltk, pl, profile_choice_a, profile_choice_b):
    # tag each text with the universal tagset, leaving out punctuation (the '.' tag)
    profile_tagged_a = [(word, tag) for (word, tag) in nltk.pos_tag(explorer_texts[profile_choice_a.value][:20000], tagset = 'universal') if tag != '.']
    profile_tagged_b = [(word, tag) for (word, tag) in nltk.pos_tag(explorer_texts[profile_choice_b.value][:20000], tagset = 'universal') if tag != '.']

    # count the tags in each text
    profile_fdist_a = FreqDist([tag for (word, tag) in profile_tagged_a])
    profile_fdist_b = FreqDist([tag for (word, tag) in profile_tagged_b])

    # the tags, from most to least frequent in text A
    profile_tags = [tag for (tag, count) in profile_fdist_a.most_common()]

    # the percentage of each text that has each tag
    profile_pct_a = [round(profile_fdist_a[tag] / profile_fdist_a.N() * 100, 1) for tag in profile_tags]
    profile_pct_b = [round(profile_fdist_b[tag] / profile_fdist_b.N() * 100, 1) for tag in profile_tags]

    pl.DataFrame({
      'tag': profile_tags,
      profile_choice_a.value + ' (%)': profile_pct_a,
      profile_choice_b.value + ' (%)': profile_pct_b,
    })
    return profile_pct_a, profile_pct_b, profile_tags


@app.cell
def _(
    plt,
    profile_choice_a,
    profile_choice_b,
    profile_pct_a,
    profile_pct_b,
    profile_tags,
):
    # the two profiles side by side, as a bar chart
    profile_positions = range(len(profile_tags))

    fig1, ax1 = plt.subplots(figsize = (10, 4))
    ax1.bar([position - 0.2 for position in profile_positions], profile_pct_a, width = 0.4, label = profile_choice_a.value)
    ax1.bar([position + 0.2 for position in profile_positions], profile_pct_b, width = 0.4, label = profile_choice_b.value)
    ax1.set_xticks(profile_positions, profile_tags)
    ax1.set_ylabel('% of words')
    ax1.legend()
    fig1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - Big Salad vs Brown news. Which has more pronouns and verbs? Which has more nouns, determiners and prepositions? Why might conversation and news writing differ in these ways?
    - Genesis vs Brown romance. Both tell stories: are their profiles similar?
    - Brown news vs Brown romance. Can you tell the genres apart from their profiles alone?
    - Big Salad has a surprisingly high share of nouns for a conversation. Remember the speaker labels from the self-study notebook: how might they be affecting this profile?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - conversation (the Seinfeld scripts) usually has more pronouns, verbs and adverbs: people talk about themselves and each other, in short clauses
    - news writing usually has more nouns, determiners and prepositions: it packs information into long noun phrases (*the new tax policy of the state government*)
    - this is the same pattern as lexical density, seen in more detail: a whole profile can distinguish genres that a single number can't
    - remember that all of these percentages depend on the tagger, which makes more mistakes on some texts than others
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: break the tagger**

    Type the sentences below into the box, one at a time. Where does the tagger go wrong, and why do you think it makes that mistake?

    - `The old man the boat.` (*man* is a verb here: the old people crew the boat)
    - `The horse raced past the barn fell.` (the horse *that was* raced past the barn fell)
    - `Time flies like an arrow; fruit flies like a banana.`
    - `Buffalo buffalo Buffalo buffalo buffalo buffalo Buffalo buffalo.`
    - `I saw her duck.`
    - a sentence with made-up words, like `The glorp snorked a wibbly frunt.`
    - a sentence in another language

    Can you find a sentence of your own that breaks it?
    """)
    return


@app.cell
def _(mo):
    sentence_box = mo.ui.text_area(value = 'The old man the boat.', label = 'sentence:', full_width = True)
    sentence_box
    return (sentence_box,)


@app.cell
def _(nltk, pl, sentence_box):
    # tag the sentence, and show each word and its tag in a table
    sentence_tagged = nltk.pos_tag(nltk.word_tokenize(sentence_box.value))

    pl.DataFrame({
      'word': [word for (word, tag) in sentence_tagged],
      'tag': [tag for (word, tag) in sentence_tagged],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Don't know what a tag means? Type it in the box below.
    """)
    return


@app.cell
def _(mo):
    tag_lookup = mo.ui.text(value = 'NN', label = 'tag:')
    tag_lookup
    return (tag_lookup,)


@app.cell
def _(nltk, tag_lookup):
    nltk.help.upenn_tagset(tag_lookup.value)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - the tagger picks the most likely tag for each word given its neighbours, based on the patterns in the text it was trained on (news articles)
    - garden path sentences trick it the same way they trick people at first: *man* is usually a noun, and *raced* after *the horse* is usually the main verb
    - for made-up words it guesses from clues like word endings (*-ed* suggests a past tense verb, *-y* an adjective) and position in the sentence
    - *I saw her duck* is ambiguous even for people: the tagger has to choose one reading
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: tag explorer**

    Which words appear most often with a particular tag? Choose a text and a tag below. (This uses the full 50,000 tokens of each text, so tagging takes a few seconds.)
    """)
    return


@app.cell
def _(explorer_texts, mo):
    explorer_text_choice = mo.ui.dropdown(options = list(explorer_texts.keys()), value = 'Genesis', label = 'text:')
    explorer_tag_choice = mo.ui.dropdown(options = ['NN', 'NNS', 'NNP', 'VB', 'VBD', 'VBG', 'VBN', 'VBZ', 'JJ', 'RB', 'PRP', 'IN', 'DT', 'MD', 'UH'], value = 'NNP', label = 'tag:')
    mo.hstack([explorer_text_choice, explorer_tag_choice], justify = 'start')
    return explorer_tag_choice, explorer_text_choice


@app.cell
def _(explorer_text_choice, explorer_texts, nltk):
    # tag the chosen text (this takes a few seconds)
    explorer_tagged = nltk.pos_tag(explorer_texts[explorer_text_choice.value])
    return (explorer_tagged,)


@app.cell
def _(FreqDist, explorer_tag_choice, explorer_tagged, pl):
    # the words with the chosen tag
    tag_words = [word for (word, tag) in explorer_tagged if tag == explorer_tag_choice.value]
    tag_fdist = FreqDist(tag_words)

    print(f"{len(tag_words)} of {len(explorer_tagged)} tokens are tagged {explorer_tag_choice.value} ({round(len(tag_words) / len(explorer_tagged) * 100, 1)}%)")

    pl.DataFrame({
      'word': [word for (word, count) in tag_fdist.most_common(20)],
      'frequency': [count for (word, count) in tag_fdist.most_common(20)],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - `NNP` (proper nouns) in each text. Who and what are the texts about? Are all the "proper nouns" really names?
    - `UH` (interjections) in Big Salad vs Brown news. What does that tell you about the two kinds of text?
    - `MD` (modal verbs) in Genesis vs Brown romance.
    - `VBD` (past tense verbs). Which texts tell stories?
    - Look for mistakes: words with a tag they shouldn't have.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"How could we do this for every tag at once?": mo.md(r'''
    Instead of picking one tag at a time, we can make a dictionary with one `FreqDist` for every tag in a text:

    ```python
    # first, the set of all the tags in the text
    tags = set([tag for (word, tag) in explorer_tagged])

    # then a FreqDist of the words for each tag
    words_by_tag = dict()
    for each_tag in tags:
      words_by_tag[each_tag] = FreqDist([word for (word, tag) in explorer_tagged if tag == each_tag])

    # now we can look up any tag
    words_by_tag['NN'].most_common(10)
    ```
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. The NLTK tagger was trained on news articles from the *Wall Street Journal*. What happens when we use it on scripts, the Bible, chat, or other varieties of English? Did you see any evidence of this in the tag explorer?
    2. Who decided what the categories are? Would a different tagset (e.g., the simpler universal tagset, with `NOUN`, `VERB`, `ADJ` ...) change what you can find out?
    3. A tagger that is 97% accurate still gets about 3 in every 100 words wrong. How many errors is that in a 10,000-word text? Which of the measures we've looked at (e.g., lexical density, counts of nouns or verbs) would those errors flow into?
    4. Two texts can have different tag profiles because they really use language differently, or because the tagger handles one of them better. How could you tell which?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - a tagger learns from the text it was trained on: news writing has few interjections, little dialogue and modern spelling, so scripts, older texts (like the King James Bible) and chat all produce more errors
    - tagsets are decisions made by people for particular purposes; a coarser tagset hides distinctions (past vs present tense) but can be more reliable, and results with different tagsets aren't directly comparable
    - 3% of 10,000 words is about 300 errors, and they aren't random: rare words, names and unusual constructions are mis-tagged most often, so any measure built on tags inherits those errors
    - to check whether a difference is real, look at the actual words behind the tags (e.g., with the tag explorer), and check a sample of the tags by hand
    ''')})
    return


if __name__ == "__main__":
    app.run()
