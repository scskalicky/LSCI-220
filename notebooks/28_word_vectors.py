# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo==0.25.2",
#     "nltk==3.10.4",
#     "matplotlib==3.11.2",
#     "polars==2.1.0",
#     "requests==2.34.2",
#     "scikit-learn==1.9.1",
#     "gensim==4.4.0",
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
    # **Word Vectors**

    You might not have any idea what someone means by the term word `vectors` or word `embeddings`, but such technology can no longer be escaped. What we will cover in this notebook is a method to represent word relationships in a new way, one which has eventually formed the backbone of generative AI technology such as ChatGPT.

    Now, we are not going to be training ChatGPT models, but we are going to look at how to model the distributional patterns of words using algorithms which generate word vectors. This helps capture more semantic relationships. One of these algorithms is called `word2vec`. What is so great about it? Like bigrams, Word2Vec leverages co-occurrences, but it does so over larger windows (not just one preceding word). So, rather than calculating raw probabilities of word occurrences, word2vec considers how words influence the probabilities of other words, and then groups similar words together based on those probabilities. It does so by assigning words not just one score, but tens or hundreds of scores which represent how the words function in a bunch of different contexts. These scores are the vectors, which can be mapped to a multidimensional space. Then, the distance among these scores can be compared in the space to find similar / different words.

    It's okay if that explanation doesn't make immediate sense to you. The point is that we can learn how to use this algorithm to train our very own vector models on our texts. Then we can find which words are most similar to other words in texts. To do so, we will use a library called [`gensim`](https://radimrehurek.com/gensim/).

    Remember Firth from the collocations notebook: "You shall know a word by the company it keeps." Word vectors take this idea very seriously! Unlike WordNet, where people decided how words are related, word vectors *learn* how words are related from the contexts they are used in.

    Let's use the `state_union` corpus in `nltk` to learn how to train and use a model.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import matplotlib.pyplot as plt
    import polars as pl
    import nltk
    from nltk.corpus import state_union
    from nltk.corpus import wordnet as wn
    from gensim.models import Word2Vec
    from gensim.models.fasttext import FastText
    import gensim.downloader
    from sklearn.decomposition import PCA

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'state_union', 'wordnet'])
    return FastText, PCA, Word2Vec, gensim, nltk, pl, plt, state_union, wn


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We need to convert our data into a list of tokenized "sentences", although the term "sentence" is a bit vague here. A sentence could be a paragraph or an entire document. Below I will convert each State of the Union text into a single tokenized list, resulting in a list of lists (which is what the gensim Word2Vec function will expect as input).

    I will also lower case the words and remove any numbers and punctuation.
    """)
    return


@app.cell
def _(nltk, state_union):
    # create output containers, plus corpus size for info
    state_union_combined = []
    corpus_size = 0

    # loop through the file ids then tokenize and add to list
    for fileid in state_union.fileids():
      speech = state_union.raw(fileid)
      speech_words = [word.lower() for word in nltk.word_tokenize(speech) if word.isalpha()]
      state_union_combined.append(speech_words)
      # add current size to total size
      corpus_size += len(speech_words)

    # how many words in the corpus?
    corpus_size
    return (state_union_combined,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **state union word2vec model**

    To fit a `word2vec` model, we choose the text, plus the `vector_size`, `epochs`, `window`, and `min_count`.

    The default vector size is 100, which means each word in the text will have 100 values or vectors (these are the values used to represent the word in the multidimensional space). I will lower this to 50 because of our relatively small corpus. `window` represents the size of the text spans the algorithm will use (i.e., it looks at each sequential 5-word context). `min_count` means a word must occur at least that many times, 5 is the default but I will increase that to ten.

    `epochs` represents the number of re-trainings to do, which can help when you have small data. I ask for 10 epochs here as a means to obtain a more stable model.

    Like topic modelling, word2vec starts with random values and then improves them, so you would get slightly different results each time. To make sure we all get the same results, I set `seed = 220` and `workers = 1` (using only one worker means the training always happens in the same order).

    These parameters are not set in stone, and usually require some tweaking or adjustment based on the size of the corpus. So, feel free to play around with them.

    Our state union corpus is pretty small (only about 350k words), but we will still be able to find some interesting associations among words.
    """)
    return


@app.cell
def _(Word2Vec, state_union_combined):
    # train the model using our texts and specific parameters
    su_w2v = Word2Vec(sentences = state_union_combined, vector_size = 50, epochs = 10, window = 5, min_count = 10, seed = 220, workers = 1)
    return (su_w2v,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The model trains relatively fast. Now that we have a trained model, what can we do with it? With these vectors, we can:

    1. query the model to find the most similar words to an input word
    2. find the difference between different words
    3. find words that don't match in a list of other words
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **`.most_similar()`**

    The most useful information we can obtain from a model like this is word similarity metrics. We can ask the model to output a list of the most similar words to an input word. By default, this will produce the top ten most similar words, along with the cosine similarity value. The cosine similarity value will range from -1 to 1. Negative values mean the words mean something very different, positive values mean the words mean something similar, and values near zero indicate no relationship.

    To use `.most_similar()`, we need to access the `.wv` attribute from the model, which stands for word vectors. Below I look up the similarity metrics for several words. What do you think about the output?
    """)
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar('america')
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar('conflict')
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar('peace')
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar('solution')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **`.most_similar(positive, negative)`**

    You can be more specific in your approach to using `.most_similar()`, by supplying not just one word, but several words. You can also specify whether the similarity should be positively or negatively related to some words.

    Compare the difference between asking for only the most similar words to `"money"` against asking for words similar to `"money"` but not similar to `"war"`.
    """)
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar(positive = 'money')
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar(positive = 'money', negative = 'war')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can enter as many words as you like as a list.
    """)
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar(positive = ['citizen', 'taxpayer'])
    return


@app.cell
def _(su_w2v):
    # slight differences here.
    su_w2v.wv.most_similar(positive = ['citizen', 'taxpayer'], negative = ['terrorist'])
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar(positive = ['jobs'])
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar(positive = ['jobs'], negative = ['military'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **`.doesnt_match()`**

    This function takes a list of words and tells you which word is the least similar to the other words. I am not sure how useful this really is, but it is at least fun to play with.
    """)
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.doesnt_match(['war', 'jobs', 'military'])
    return


@app.cell
def _(su_w2v):
    # why do you think "america" is the outlier here?
    su_w2v.wv.doesnt_match(['america', 'france', 'germany', 'china'])
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.doesnt_match(['rights', 'constitution', 'freedom', 'taxes'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **fastText**

    Word2Vec is not the only way to train word vectors / embeddings. Another method is called FastText. [This algorithm works a bit differently by breaking down words and considering morphological differences.](https://radimrehurek.com/gensim/auto_examples/tutorials/run_fasttext.html) It is also apparently better at dealing with misspelled words.

    Let's try it out. First we create the model with a vector size of 50. Then, we build the model vocabulary using the same `state_union_combined` object we fed to word2vec above.
    """)
    return


@app.cell
def _(FastText, state_union_combined):
    su_ft = FastText(vector_size = 50, seed = 220, workers = 1)

    # build the vocabulary
    su_ft.build_vocab(corpus_iterable = state_union_combined)
    return (su_ft,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we need to train the model. There are a number of parameters, which we will leave as defaults.
    """)
    return


@app.cell
def _(state_union_combined, su_ft):
    # train the model
    su_ft.train(corpus_iterable = state_union_combined, epochs = su_ft.epochs, total_examples = su_ft.corpus_count, total_words = su_ft.corpus_total_words)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use the model just the same as the word2vec model to explore similarities among words. Compare the output here versus the output for word2vec. The most similar words here are more similar in terms of morphological form. This is because of differences in the algorithms.
    """)
    return


@app.cell
def _(su_ft):
    # fastText vectors
    su_ft.wv.most_similar('america')
    return


@app.cell
def _(su_ft):
    su_ft.wv.most_similar('truth')
    return


@app.cell
def _(su_w2v):
    # word2vec vectors
    su_w2v.wv.most_similar('america')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because FastText builds its vectors from pieces of words, it can even give us a vector for a word it has *never seen*. The word *americanish* never appears in the State of the Union speeches, but FastText can still guess which words it is similar to. What happens if you try this with the word2vec model?
    """)
    return


@app.cell
def _(su_ft):
    # is the word in the training data?
    print('americanish' in su_ft.wv.key_to_index)

    # FastText can still make a guess
    su_ft.wv.most_similar('americanish')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Using pretrained vectors**

    You can also use sets of pretrained vectors which have been trained on much larger data sets. Keep in mind those vectors are intended to show similarity at a generalizable level. One advantage of training on our own data is that we can explore similarity in a specific context.

    One interesting experiment then is to see whether your corpus or texts have different similarity relationships when compared to a larger set of reference vectors.

    `gensim` has [a number of pretrained models you can use](https://github.com/piskvorky/gensim-data#models). Here is the list:
    """)
    return


@app.cell
def _(gensim):
    list(gensim.downloader.info()['models'].keys())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some of these are very large (the Google News vectors are 1.7 GB!). We will use a smaller set called **GloVe**, which was trained on Wikipedia and a large collection of news articles (about 6 billion words). The version we use has 50 values for each word, and is about 66 MB.

    The first time you run the cell below, it will download the vectors (this might take a minute or two). gensim saves them in a folder called `gensim-data` in your home folder, so the next time you run it, it will load much faster.
    """)
    return


@app.cell
def _(gensim):
    # download (the first time) and load the pretrained GloVe vectors
    glove = gensim.downloader.load('glove-wiki-gigaword-50')
    return (glove,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because we have downloaded the vectors directly and not the model, we do not need to use the `.wv.` part. You can see the differences using `type`:
    """)
    return


@app.cell
def _(su_w2v):
    # a model
    type(su_w2v)
    return


@app.cell
def _(su_w2v):
    # keyed vectors
    type(su_w2v.wv)
    return


@app.cell
def _(glove):
    # keyed vectors
    type(glove)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's compare the most similar words to 'america' in the GloVe vectors. I will show the state union vectors again for reference. We can see that we obtain vastly different results. This is a direct result of the different training data used. The GloVe data is larger and has more topics. The State Union corpus is smaller and more homogenous (i.e., it is all speeches from US Presidents).
    """)
    return


@app.cell
def _(glove):
    glove.most_similar('america')
    return


@app.cell
def _(su_w2v):
    su_w2v.wv.most_similar('america')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **So what *is* a vector?**

    You might still be a bit fuzzy about what vectors actually *are*, and that's pretty normal. Let's look at one. A word vector is simply a list of numbers. In our GloVe vectors, every word has 50 numbers:
    """)
    return


@app.cell
def _(glove):
    # the vector for 'cat'
    glove['cat']
    return


@app.cell
def _(glove):
    # how many numbers?
    len(glove['cat'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You have actually seen tables of numbers like this before! In the tf-idf and topic modelling notebooks, scikit-learn turned each document into a row of numbers (one number for each word), and each of those rows is a **vector** for a document. A word vector is the same idea, except that each *word* gets a row of numbers, and the numbers are learned from the contexts the word appears in.

    On their own, these numbers don't mean anything to us (there is no "number 7 = animals"). What matters is how the numbers of one word compare to the numbers of other words. Words which are used in similar contexts end up with similar lists of numbers.

    You can think of each word's vector as an arrow pointing in a particular direction (in a space with 50 dimensions, which is impossible to imagine, so don't try!). **Cosine similarity** measures how much two arrows point in the same direction:

    - arrows pointing in the same direction get a similarity close to 1
    - arrows at right angles get a similarity close to 0
    - arrows pointing in opposite directions get a similarity close to -1
    """)
    return


@app.cell
def _(glove):
    print('dog and cat:', glove.similarity('dog', 'cat'))
    print('dog and car:', glove.similarity('dog', 'car'))
    print('dog and novel:', glove.similarity('dog', 'novel'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Seeing vectors in two dimensions**

    We can't see 50 dimensions, but we can squash the vectors down to just 2 dimensions so that we can plot them. One way to do this is called **PCA** (principal component analysis), which keeps as much of the difference between the vectors as it can. A lot of information gets lost when we squash 50 numbers into 2, so the plot is only a rough picture, but it should show you that words with similar meanings end up close together.
    """)
    return


@app.cell
def _(PCA, glove, plt):
    plot_words = ['dog', 'cat', 'wolf', 'fox', 'beer', 'wine', 'water', 'bread', 'car', 'bicycle', 'truck', 'paris', 'london', 'tokyo']

    # squash the 50 numbers for each word down to 2 numbers
    pca = PCA(n_components = 2)
    points = pca.fit_transform([glove[plot_word] for plot_word in plot_words])

    fig1, ax1 = plt.subplots(figsize = (8, 6))
    ax1.scatter([point[0] for point in points], [point[1] for point in points])
    for plot_word, point in zip(plot_words, points):
      ax1.annotate(plot_word, (point[0], point[1]), xytext = (4, 4), textcoords = 'offset points')
    fig1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Analogies**

    Because the vectors are lists of numbers, we can do maths with them! One famous example is that we can take the vector for *king*, subtract *man*, and add *woman*. Which word is closest to the result?

    In gensim, the words we add go in `positive`, and the words we subtract go in `negative`:
    """)
    return


@app.cell
def _(glove):
    # king - man + woman = ?
    glove.most_similar(positive = ['king', 'woman'], negative = ['man'], topn = 5)
    return


@app.cell
def _(glove):
    # paris - france + japan = ?
    glove.most_similar(positive = ['paris', 'japan'], negative = ['france'], topn = 5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This works because the *difference* between *king* and *queen* is similar to the difference between *man* and *woman*, and the difference between *Paris* and *France* is similar to the difference between *Tokyo* and *Japan*. Nobody told the model these things - it learned them from the way the words are used!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Vectors learn our biases too**

    The vectors learn whatever patterns are in the texts they are trained on. That includes the stereotypes and biases in those texts. Look what happens when we use the same analogy trick with some jobs:
    """)
    return


@app.cell
def _(glove):
    # doctor - man + woman = ?
    glove.most_similar(positive = ['doctor', 'woman'], negative = ['man'], topn = 5)
    return


@app.cell
def _(glove):
    # nurse - woman + man = ?
    glove.most_similar(positive = ['nurse', 'man'], negative = ['woman'], topn = 5)
    return


@app.cell
def _(glove):
    # brilliant - man + woman = ?
    glove.most_similar(positive = ['brilliant', 'woman'], negative = ['man'], topn = 5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The vectors have learned that *doctor* goes with men and *nurse* goes with women. And for *brilliant*, the results shift towards words like *dazzling*, *gorgeous*, and *lively*, which are often used to describe how women look or behave rather than how clever they are. The vectors are not "wrong" about the texts they were trained on - these patterns really are in the news and Wikipedia articles! But when vectors like these are used in real applications (search engines, translation, CV screening, chatbots), they can repeat and even strengthen these stereotypes.

    (It's also worth knowing that analogies are a bit of a trick: `.most_similar()` never gives back any of the input words, so *doctor* can't be the answer to *doctor - man + woman*, even if it's the closest!)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **WordNet vs word vectors**

    In the WordNet notebook, we measured similarity using the paths between words in a hierarchy built by people. Word vectors measure similarity using the contexts that words appear in. Do they agree?

    Below, I compare some pairs of words using WordNet's `path_similarity()` and GloVe's cosine similarity. For WordNet, I have to choose which synset (meaning) of each word to use, so I give the synset names myself (e.g., `whale.n.02` is the animal, but `whale.n.01` would be a very large person!). The vectors don't have this problem (or this option): they only have one vector for each word, which mixes all of its meanings together.
    """)
    return


@app.cell
def _(glove, pl, wn):
    # (word 1, its synset, word 2, its synset)
    word_pairs = [
      ('dog', 'dog.n.01', 'cat', 'cat.n.01'),
      ('beer', 'beer.n.01', 'wine', 'wine.n.01'),
      ('beer', 'beer.n.01', 'water', 'water.n.01'),
      ('beer', 'beer.n.01', 'bread', 'bread.n.01'),
      ('car', 'car.n.01', 'bicycle', 'bicycle.n.01'),
      ('hot', 'hot.a.01', 'cold', 'cold.a.01'),
      ('whale', 'whale.n.02', 'novel', 'novel.n.01'),
    ]

    comparison_rows = []
    for (word1, synset_name1, word2, synset_name2) in word_pairs:
      comparison_rows.append({
        'word 1': word1,
        'word 2': word2,
        'WordNet path similarity': round(wn.synset(synset_name1).path_similarity(wn.synset(synset_name2)), 3),
        'GloVe similarity': round(float(glove.similarity(word1, word2)), 3),
      })

    pl.DataFrame(comparison_rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Where do the two approaches disagree? Look at *beer* and *bread*: WordNet only links them through the very general category *food*, but the vectors know that they are often talked about together (e.g., at meals, or in recipes). And look at *hot* and *cold*: WordNet records them as **antonyms** (opposites), but they get a very high similarity in the vectors! This is because opposites are used in very similar contexts (*the water was hot / cold*), so the vectors can't easily tell them apart.
    """)
    return


@app.cell
def _(wn):
    # WordNet knows that hot and cold are opposites
    wn.synset('hot.a.01').lemmas()[0].antonyms()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Conclusion**

    Training word vectors is a bit more complicated than the other NLP tasks covered so far. But, libraries like `gensim` make it relatively painless to do so. It is very important to explore the output of the model and potentially tune the different parameters until you get something that makes sense.

    There are also other sources of pretrained vectors besides `gensim`, and you can use `gensim` to load in these vectors and use them as you like.

    [There are several blogs and other explanations](https://cloud.google.com/blog/topics/developers-practitioners/meet-ais-multitool-vector-embeddings) out there which may help you understand vectors better. Vectors are now fundamental tools for modern NLP and AI (large language models use vectors for every word they read and write), so gaining an awareness of how they work and how to train them is important.

    Some ideas for how you might want to use these is that you can compare the similarity of target words to different corpora. Seeing the types of words which appear more/less similar to a target word might tell you something about the nature of the meanings in one corpus over another. In this example I compared a general (large) corpus against a small, specific corpus. We found that words associated with "america" in the State Union corpus were more reflective of words used during speeches, which makes sense! The more general GloVe vectors had words more generally related to countries and regions. Creating small word2vec models can tell you something about the way words in your corpus are related to one another.

    ### **Your Turn**

    - Train a word2vec model on a different corpus (e.g., the Big Salad, or the Brown corpus). How do the most similar words change?
    - Try some analogies of your own with the GloVe vectors. Which ones work, and which ones don't?
    - Look for other examples of bias in the GloVe vectors (e.g., nationalities, ages, or names). What do you find?
    - Compare WordNet and the vectors for some pairs of your own. When would you want to use WordNet, and when would you want to use vectors?
    """)
    return


@app.cell
def _():
    # use this code cell to explore word vectors!
    return


if __name__ == "__main__":
    app.run()
