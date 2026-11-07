# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.25.2",
#     "nltk==3.10.4",
#     "matplotlib==3.11.2",
#     "polars==2.1.0",
#     "requests==2.34.2",
#     "scikit-learn==1.9.1",
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
    # **In-class: topic modelling**

    Today's plan:

    1. Review: word counts, topics, and topic mixtures
    2. Activities: naming the topics, choosing the number of topics, and changing the random seed
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import matplotlib.pyplot as plt
    import polars as pl
    import nltk
    from nltk import FreqDist
    from nltk.corpus import brown
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['brown'])
    return CountVectorizer, FreqDist, LatentDirichletAllocation, brown, pl, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: topic modelling - key concepts**

    - `CountVectorizer()` turns a list of documents into a table of word counts (rows are documents, columns are words)
    - a **topic** is a list of words, with some words more important to the topic than others
    - each **document** is a mixture of topics
    - the model is never told what the topics are: *we* decide what they mean

    For the rest of today we need the Brown documents and their word counts, just like in the topic modelling notebook. This might take a few seconds.
    """)
    return


@app.cell
def _(CountVectorizer, brown):
    brown_files = brown.fileids()

    brown_documents = []
    for brown_file in brown_files:
      file_words = [word.lower() for word in brown.words(brown_file) if word.isalpha()]
      brown_documents.append(' '.join(file_words))

    brown_vectorizer = CountVectorizer(stop_words = 'english', max_df = 0.5, min_df = 5)
    brown_counts = brown_vectorizer.fit_transform(brown_documents)
    brown_words = brown_vectorizer.get_feature_names_out()
    return brown_counts, brown_files, brown_words


@app.cell
def _(FreqDist, LatentDirichletAllocation, brown_counts, brown_words):
    def top_topic_words(topic_scores, n = 10):
      # pair each word with its score for this topic, and keep the top n words
      return [word for (word, score) in FreqDist(dict(zip(brown_words, topic_scores))).most_common(n)]

    # fit a model with 10 topics
    brown_lda = LatentDirichletAllocation(n_components = 10, random_state = 220)
    brown_lda.fit(brown_counts)
    document_topics = brown_lda.transform(brown_counts)
    return brown_lda, document_topics, top_topic_words


@app.cell
def _(document_topics):
    # what do the topic proportions of the first document add up to?
    sum(document_topics[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One last prediction, which we will come back to in the final activity: if we fit the same model again with a different `random_state`, will we get the same topics?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Review answers": mo.md(r'''
    - `stop_words = 'english'` removes *the* and *and*, which leaves 5 words: *cat, cats, dog, dogs, sat*. So the table has 3 rows (documents) and 5 columns (words)
    - notice that *cat* and *cats* are different columns: `CountVectorizer()` does not know they are the same word
    - the topic proportions of a document always add up to 1 (sometimes 0.9999999 because of rounding)
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: name the topics**

    Here are the top 10 words for each of the 10 topics. Discuss what each topic might be about, and type a name for each topic in the boxes below. If you can't name a topic, leave it blank or call it "mystery"!
    """)
    return


@app.cell
def _(brown_lda, top_topic_words):
    for topic_number, topic_scores in enumerate(brown_lda.components_):
      print(topic_number, top_topic_words(topic_scores))
    return


@app.cell
def _(mo):
    topic_names = mo.ui.array([mo.ui.text(placeholder = 'topic ' + str(number), label = 'topic ' + str(number) + ':') for number in range(10)])
    topic_names
    return (topic_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now choose a document to see its mixture of topics, using *your* names. The category of the document is shown above the chart. Do your topic names make sense for that kind of writing?
    """)
    return


@app.cell
def _(brown_files, mo):
    mixture_choice = mo.ui.dropdown(options = brown_files, value = 'ca01', label = 'document:')
    mixture_choice
    return (mixture_choice,)


@app.cell
def _(brown, brown_files, document_topics, mixture_choice, plt, topic_names):
    # use the typed name, or 'topic n' if the box is empty
    chart_labels = []
    for number, name in enumerate(topic_names.value):
      if name == '':
        chart_labels.append('topic ' + str(number))
      else:
        chart_labels.append(name)

    mixture_proportions = document_topics[brown_files.index(mixture_choice.value)]

    fig1, ax1 = plt.subplots(figsize = (10, 4))
    ax1.bar(chart_labels, mixture_proportions)
    ax1.set_ylabel('proportion of the document')
    ax1.set_title(mixture_choice.value + ' (' + brown.categories(fileids = mixture_choice.value)[0] + ')')
    plt.xticks(rotation = 45, ha = 'right')
    fig1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - `ca01` is a news article. Which topics is it made of?
    - Try documents from other categories: `cj07` (learned), `cp01` (romance), `cd01` (religion), `cr01` (humour). Which documents are mostly one topic, and which are a mix?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: how many topics?**

    In the topic modelling notebook, we had to choose the number of topics ourselves. Choose a number below, and the model will be fitted again (this takes a few seconds). The table shows how many documents in each Brown category have each topic as their strongest topic.
    """)
    return


@app.cell
def _(mo):
    topic_number_choice = mo.ui.dropdown(options = ['5', '10', '15', '20'], value = '5', label = 'number of topics:')
    topic_number_choice
    return (topic_number_choice,)


@app.cell
def _(
    LatentDirichletAllocation,
    brown_counts,
    top_topic_words,
    topic_number_choice,
):
    # fit a new model with the chosen number of topics
    choice_lda = LatentDirichletAllocation(n_components = int(topic_number_choice.value), random_state = 220)
    choice_lda.fit(brown_counts)

    for choice_number, choice_scores in enumerate(choice_lda.components_):
      print(choice_number, top_topic_words(choice_scores, 8))
    return (choice_lda,)


@app.cell
def _(brown, brown_counts, brown_files, choice_lda, pl):
    # the strongest topic for each document
    choice_topics = choice_lda.transform(brown_counts)
    choice_strongest = []
    for choice_proportions in choice_topics:
      proportions_list = list(choice_proportions)
      choice_strongest.append(proportions_list.index(max(proportions_list)))

    choice_table = pl.DataFrame({
      'category': [brown.categories(fileids = choice_file)[0] for choice_file in brown_files],
      'strongest topic': choice_strongest,
    })

    choice_table.group_by(['category', 'strongest topic']).len().pivot(on = 'strongest topic', index = 'category', values = 'len', sort_columns = True).fill_null(0).sort('category')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - With 5 topics, which categories end up sharing a topic? Do those categories have anything in common?
    - With 20 topics, are the topics easier or harder to name? Do any topics only show up in one or two documents?
    - Which number of topics would you choose? How would you justify that choice to someone else?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - with few topics, the model has to lump things together, so the topics are broad (e.g., all of the fiction categories share one "narrative" topic)
    - with more topics, the topics get more specific, but some become hard to interpret, or only describe a handful of documents
    - there is no single "right" number of topics: researchers often try several, and choose the one that gives topics they can interpret, which is itself a human judgement
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: same data, different seed**

    Back in the review, you predicted whether a different `random_state` would give the same topics. Let's find out! The table below shows the topics from two models with exactly the same data and settings (10 topics). The only difference is the `random_state`.
    """)
    return


@app.cell
def _(mo):
    seed_choice = mo.ui.number(start = 0, stop = 1000, value = 1, label = 'second random_state:')
    seed_choice
    return (seed_choice,)


@app.cell
def _(
    LatentDirichletAllocation,
    brown_counts,
    brown_lda,
    pl,
    seed_choice,
    top_topic_words,
):
    seed_lda = LatentDirichletAllocation(n_components = 10, random_state = seed_choice.value)
    seed_lda.fit(brown_counts)

    pl.DataFrame({
      'topic': list(range(10)),
      'random_state = 220': [', '.join(top_topic_words(seed_scores, 8)) for seed_scores in brown_lda.components_],
      'random_state = ' + str(seed_choice.value): [', '.join(top_topic_words(seed_scores, 8)) for seed_scores in seed_lda.components_],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to try:

    - Are the topics the same? Are they in the same order?
    - Try to match each topic in the first column with a topic in the second column. Which topics appear in both models? Which only appear in one?
    - Change the second `random_state` a few times. Which topics keep coming back?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - the topic *numbers* are arbitrary: the same topic can be topic 0 in one model and topic 7 in another
    - some topics are stable and come back with almost any seed (e.g., the narrative fiction topic with *got, went, thought, eyes*, a government topic with *state, president, united*, and a religion topic with *church, god, christian*), while others (like education) come and go
    - topics which keep coming back are more trustworthy than topics that only appear with one seed
    - this is why `random_state` should always be reported, and why it's a good idea to check results with more than one seed
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. The model only finds groups of words; *people* decide what the topics are. How might two people name the same topic differently, and when might that matter?
    2. The topics changed with the number of topics and the random seed (and would also change with a different stopword list). If you read a study that used topic modelling, what would you want the authors to report?
    3. Topic models are often used to make claims about large collections of text, such as news coverage or social media posts. What could go wrong if the topics are taken at face value?
    4. Brown is a sample of American writing from 1961. What do its topics tell us about the world of the corpus, and what do they not tell us about the world in general?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - naming a topic is an interpretation: the same list of words could be called "education" or "youth", and the name we choose shapes the story we tell about the corpus
    - results depend on many choices (the documents, preprocessing, stopwords, `min_df` and `max_df`, the number of topics, the random seed), and all of them should be reported so that others can check the results
    - topics can look convincing but be unstable, or mix together things that don't belong together; claims based on them should be checked by reading the actual documents
    - a corpus is a sample of particular writers, places, times and genres: the topics describe what was written in that sample, not what was important in the world
    ''')})
    return


if __name__ == "__main__":
    app.run()
