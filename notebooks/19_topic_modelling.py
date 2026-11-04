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
    #### Other tutorials on this topic

    [scikit-learn: Latent Dirichlet Allocation](https://scikit-learn.org/stable/modules/decomposition.html#latentdirichletallocation)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Topic modelling: finding groups of words across documents**

    In the tf-idf notebook, we found the words that make *one* document distinctive when compared to all the other documents in a corpus. Topic modelling turns this around a bit. Instead of looking at what makes one document different, a topic model looks for groups of words which tend to occur *together* across lots of different documents.

    For example, if the words *school*, *students*, and *teachers* keep showing up in the same documents, a topic model would put them together into a group. We might look at that group and call it an "education" topic.

    The topic model we will use is called **Latent Dirichlet Allocation (LDA)**. The maths behind LDA is quite complicated, so we will not calculate it by hand like we did with tf-idf. But the basic idea is:

    - each **topic** is a list of words, with some words more important to the topic than others
    - each **document** is a mixture of topics (e.g., a news article might be 50% politics, 30% sport, and 20% something else)

    Crucially, the model is never told what the topics are! It only sees which words occur in which documents, and it tries to find groups of words that explain those patterns. It is then up to *us* to look at the groups of words and decide what (if anything) they mean.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import polars as pl
    import nltk
    from nltk import FreqDist
    from nltk.corpus import brown
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation

    # download the NLTK resources for this notebook
    nltk.download(['brown'])
    return CountVectorizer, FreqDist, LatentDirichletAllocation, brown, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Getting the data**

    Topic models work best with lots of documents, so we will use the 500 documents in the Brown corpus. Each document in Brown has its own file ID, and each file ID belongs to one of the 15 categories (genres) of Brown.
    """)
    return


@app.cell
def _(brown):
    brown_files = brown.fileids()

    # how many documents?
    len(brown_files)
    return (brown_files,)


@app.cell
def _(brown_files):
    # the first few file IDs
    brown_files[:10]
    return


@app.cell
def _(brown):
    # which category does the first document belong to?
    brown.categories(fileids = 'ca01')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Like in the tf-idf notebook, we will make one string per document, keeping only alphabetic words and lowercasing them. This might take a few seconds.
    """)
    return


@app.cell
def _(brown, brown_files):
    brown_documents = []

    for brown_file in brown_files:
      file_words = [word.lower() for word in brown.words(brown_file) if word.isalpha()]
      brown_documents.append(' '.join(file_words))

    len(brown_documents)
    return (brown_documents,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Counting words with scikit-learn**

    LDA works with simple word counts rather than tf-idf scores. scikit-learn has a function called `CountVectorizer()` which works just like the `TfidfVectorizer()` from the tf-idf notebook, except that it gives us the raw counts of each word in each document.

    We will also give `CountVectorizer()` a few arguments to remove some of the words we don't want:

    - `stop_words = 'english'` removes a built-in list of English function words such as *the*, *and*, and *of*. Otherwise, every topic would be full of these words!
    - `max_df = 0.5` removes words which appear in more than 50% of the documents (just like we did with tf-idf)
    - `min_df = 5` removes words which appear in fewer than 5 documents. Very rare words can't really help us find words that occur together across lots of documents.
    """)
    return


@app.cell
def _(CountVectorizer, brown_documents):
    # create the vectorizer (it turns text into word counts)
    brown_vectorizer = CountVectorizer(stop_words = 'english', max_df = 0.5, min_df = 5)

    # get the counts
    brown_counts = brown_vectorizer.fit_transform(brown_documents)

    # get the words (the columns)
    brown_words = brown_vectorizer.get_feature_names_out()

    # rows are documents, columns are words
    brown_counts.shape
    return brown_counts, brown_words


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Fitting the topic model**

    Now we can create the topic model. There are two important arguments:

    - `n_components` is the number of topics we want the model to find. *We* have to decide this, the model can't figure it out for us! Let's start with 10 topics.
    - `random_state` makes sure that we get the same results each time. LDA starts with a random guess and then improves it, so without `random_state` you would get slightly different topics every time you run the model. The number itself does not matter, it just needs to stay the same.

    If you want to change the number of topics later, just change the number in the cell below and marimo will re-run the cells that depend on it.
    """)
    return


@app.cell
def _():
    number_of_topics = 10
    return (number_of_topics,)


@app.cell
def _(LatentDirichletAllocation, brown_counts, number_of_topics):
    brown_lda = LatentDirichletAllocation(n_components = number_of_topics, random_state = 220)

    # fit the model to our word counts
    brown_lda.fit(brown_counts)
    return (brown_lda,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The box above is how scikit-learn displays a fitted model. Click on **Parameters** to see all of the settings the model used: the ones we chose (`n_components` and `random_state`) are highlighted, and everything else is a default value that we didn't change.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **What are the topics?**

    The model stores the importance of each word to each topic in `.components_`. Each row is a topic, and each column is a word (in the same order as `brown_words`).

    To get the top words for each topic, we can use the same trick as in the tf-idf notebook: `zip()` the words together with the scores, and put them into a `FreqDist` so that we can use `.most_common()`.
    """)
    return


@app.cell
def _(FreqDist, brown_words):
    def top_topic_words(topic_scores, n = 12):
      # pair each word with its score for this topic
      return [word for (word, score) in FreqDist(dict(zip(brown_words, topic_scores))).most_common(n)]

    return (top_topic_words,)


@app.cell
def _(brown_lda, top_topic_words):
    # create a dictionary of the topic words
    brown_topic_words = {}

    for topic_number, topic_scores in enumerate(brown_lda.components_):
        brown_topic_words[topic_number] = top_topic_words(topic_scores)
        # print them here for easy inspection
        print(topic_number, brown_topic_words[topic_number])

    return (brown_topic_words,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    - Look at the words in each topic. Can you give each topic a name? (e.g., "education", "science")
    - Which topics are easy to name, and which ones are a bit of a mess?
    - Some of the topics are not really about a *subject* at all. Look for a topic with words like *got*, *went*, and *looked*. What kind of writing do you think this topic comes from?
    """)
    return


@app.cell
def _():
    # use this code cell to explore the topics!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Documents as mixtures of topics**

    Remember that each document is a *mixture* of topics. We can use `.transform()` to get the topic mixture of each document. The result is a table where each row is a document and each column is a topic. The numbers are proportions, so each row adds up to 1.
    """)
    return


@app.cell
def _(brown_counts, brown_lda):
    document_topics = brown_lda.transform(brown_counts)

    document_topics.shape
    return (document_topics,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's look at the topic mixture of the first document, `ca01`, which is a news article. I put the results in a polars dataframe to make them easier to read, and round the proportions to 2 decimal places.
    """)
    return


@app.cell
def _(document_topics, number_of_topics, pl):
    pl.DataFrame({
      'topic': list(range(number_of_topics)),
      'proportion': [round(proportion, 2) for proportion in document_topics[0]]
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Which topics make up most of this document? Look back at the top words for those topics. Do they make sense for a news article?

    You can look at other documents by changing the number in `document_topics[0]`. The number is the position of the document in `brown_files`, so `document_topics[300]` would be `brown_files[300]`.
    """)
    return


@app.cell
def _(brown, brown_files):
    # which document is number 300, and what category is it?
    print(brown_files[300], brown.categories(fileids = brown_files[300]))
    return


@app.cell
def _():
    # use this code cell to look at the topic mixture of other documents!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Do the topics match the Brown categories?**

    The model was never told about the 15 categories in Brown. So, an interesting question is whether the topics the model found line up with the categories at all. As a reminder, here are the ten topics that emerged from the data. Again, remember that it is up to us to make sense of what the topic "is".
    """)
    return


@app.cell
def _(brown_topic_words):
    # print the topics and their words again
    for k in brown_topic_words:
        print(k, brown_topic_words[k])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To find out which of these ten topics is the strongest for any genre, let's find the *strongest* topic for each document (the topic with the highest proportion) and compare it to the document's category. I use `max()` to find the highest proportion, and `.index()` to find its position in the list, which is the topic number.

    The first results show us that the strongest topic for some "news" documents is topic 9 (check the keywords for 9 above, does that make sense?). This isn't always the case though - you'll need to click around in the dataframe to see beyond the first results. In fact, across all of the news documents, topic 4 is actually the strongest topic more often than topic 9.
    """)
    return


@app.cell
def _(brown, brown_files, document_topics, pl):
    document_categories = []
    strongest_topics = []

    for document_number, document_file in enumerate(brown_files):
      # the category of this document
      document_categories.append(brown.categories(fileids = document_file)[0])

      # the topic with the highest proportion
      proportions = list(document_topics[document_number])
      strongest_topics.append(proportions.index(max(proportions)))

    topic_table = pl.DataFrame({'category': document_categories, 'strongest topic': strongest_topics})
    topic_table
    return (topic_table,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can count how many documents in each category have each topic as their strongest topic. I use `group_by()` and `.len()` to do the counting, and then `.pivot()` to turn the result into a table with one row per category and one column per topic.

    What do you see? Well, for 28 of the 29 adventure documents, the strongest topic is topic 7 (check the topic 7 words above!)
    """)
    return


@app.cell
def _(topic_table):
    topic_counts = topic_table.group_by(['category', 'strongest topic']).len()

    topic_counts.pivot(on = 'strongest topic', index = 'category', values = 'len', sort_columns = True).fill_null(0).sort('category')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    - Which categories are dominated by a single topic? Which categories are spread across lots of topics?
    - Do the categories which share a topic make sense? (e.g., which categories share the topic with *got*, *went*, and *looked*?)
    - Change `number_of_topics` to 5, and then to 20. How do the topics change? Are they easier or harder to name?
    - The model finds groups of words, but *we* decide what the topics mean. What problems could this cause if someone used a topic model to make claims about a corpus?
    """)
    return


@app.cell
def _():
    # use this code cell to explore the topic model!
    return


if __name__ == "__main__":
    app.run()
