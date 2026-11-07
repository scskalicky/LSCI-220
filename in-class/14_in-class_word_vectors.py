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
    # **In-class: word vectors and meaning**

    Today's plan:

    1. Review: vectors, cosine similarity, analogies, and WordNet
    2. Activities: a similarity explorer, an analogy machine, and a bias probe
    3. Critical reflection
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
    import gensim.downloader
    from sklearn.decomposition import PCA
    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['punkt_tab', 'state_union', 'wordnet'])
    return PCA, Word2Vec, gensim, nltk, pl, plt, state_union


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    First, let's load the GloVe vectors from the word vectors notebook (this will be quick if you have already downloaded them), and train a small word2vec model on the State of the Union speeches.
    """)
    return


@app.cell
def _(Word2Vec, gensim, nltk, state_union):
    glove = gensim.downloader.load('glove-wiki-gigaword-50')

    # a small word2vec model of the State of the Union speeches
    speeches = []
    for fileid in state_union.fileids():
      speeches.append([word.lower() for word in nltk.word_tokenize(state_union.raw(fileid)) if word.isalpha()])

    su_w2v = Word2Vec(sentences = speeches, vector_size = 50, epochs = 10, window = 5, min_count = 10, seed = 220, workers = 1)
    return glove, su_w2v


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: word vectors - key concepts**

    - a **word vector** is a list of numbers which represents how a word is used
    - words used in similar contexts get similar vectors, which we measure with **cosine similarity** (from -1 to 1)
    - we can add and subtract vectors to make **analogies**
    - **WordNet** relations were made by people; vectors are *learned* from a corpus

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _(glove):
    # how many numbers are in each GloVe vector?
    len(glove['kiwi'])
    return


@app.cell
def _(glove):
    # what does a vector look like?
    glove['kiwi']
    return


@app.cell
def _(glove):
    # which pair is the most similar?
    print('cat and dog:', glove.similarity('cat', 'dog'))
    print('cat and kitten:', glove.similarity('cat', 'kitten'))
    print('cat and banana:', glove.similarity('cat', 'banana'))
    return


@app.cell
def _(glove):
    # hot and cold are opposites. Will their similarity be high or low?
    glove.similarity('hot', 'cold')
    return


@app.cell
def _(glove):
    # walked - walk + swim = ?
    glove.most_similar(positive = ['walked', 'swim'], negative = ['walk'], topn = 3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Review answers": mo.md(r'''
    - every word in these GloVe vectors has 50 numbers
    - *cat* and *dog* are actually more similar than *cat* and *kitten*! *Cat* and *dog* appear in very similar contexts (pets, vets, food), and are mentioned together a lot
    - *hot* and *cold* get a high similarity, because opposites are used in very similar contexts (*the water was hot / cold*); WordNet, on the other hand, records them as antonyms
    - the vectors have learned something about past tense: *walked* is to *walk* as *swam* is to *swim*
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: similarity explorer**

    Type a word to see its 10 most similar words in two different sets of vectors:

    - the **GloVe** vectors, trained on about 6 billion words of Wikipedia and news
    - our small **State of the Union** word2vec model, trained on about 350,000 words of presidential speeches

    What *kinds* of similar words do you get? Synonyms? Opposites? Words from the same topic? Words that appear in the same phrases?
    """)
    return


@app.cell
def _(mo):
    similar_word = mo.ui.text(value = 'freedom', label = 'word:')
    similar_word
    return (similar_word,)


@app.cell
def _(glove, pl, similar_word, su_w2v):
    target = similar_word.value.lower().strip()

    if target in glove.key_to_index:
      glove_similar = [word for (word, score) in glove.most_similar(target)]
    else:
      glove_similar = ['(not in vocabulary)'] * 10

    if target in su_w2v.wv.key_to_index:
      speech_similar = [word for (word, score) in su_w2v.wv.most_similar(target)]
    else:
      speech_similar = ['(not in vocabulary)'] * 10

    pl.DataFrame({'GloVe': glove_similar, 'State of the Union': speech_similar})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now try making a map of some words. Type a list of words (separated by commas), and the GloVe vectors will be squashed down to two dimensions (using PCA, as in the word vectors notebook). Do words with similar meanings end up close together?
    """)
    return


@app.cell
def _(mo):
    map_words = mo.ui.text(value = 'kiwi, wellington, auckland, rugby, cricket, sheep, cow, beer, wine, coffee, happy, sad, angry', label = 'words to map:', full_width = True)
    map_words
    return (map_words,)


@app.cell
def _(PCA, glove, map_words, mo, plt):
    # keep only the words which are in the GloVe vocabulary
    chosen_map_words = [map_word.strip().lower() for map_word in map_words.value.split(',') if map_word.strip().lower() in glove.key_to_index]
    mo.stop(len(chosen_map_words) < 3, mo.md('**Type at least 3 words that are in the vocabulary!**'))

    map_points = PCA(n_components = 2).fit_transform([glove[map_word] for map_word in chosen_map_words])

    fig1, ax1 = plt.subplots(figsize = (8, 6))
    ax1.scatter([point[0] for point in map_points], [point[1] for point in map_points])
    for map_word, point in zip(chosen_map_words, map_points):
      ax1.annotate(map_word, (point[0], point[1]), xytext = (4, 4), textcoords = 'offset points')
    fig1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Try *kiwi*. Which meaning of *kiwi* do the GloVe vectors know about? What does that tell you about the training data?
    - Try the same word in both models (e.g., *freedom*, *war*, *family*, *money*). Why are the results so different?
    - Which words in your map ended up close together? Were there any surprises?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - each word gets only *one* vector, which mixes together all of its meanings; for *kiwi*, the GloVe vectors mostly learned the sports meaning (*kiwis*, *wallaby*, *proteas*), because that is how the word is mostly used in news
    - the State of the Union model learns how words are used in presidential speeches, so its similar words are about politics and rhetoric; GloVe learns from a much wider (but still particular) range of texts
    - "similar" in vectors can mean many things: synonyms, opposites, co-hyponyms (*cat* and *dog*), or words from the same topic, because all of these appear in similar contexts
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: analogy machine**

    Fill in the boxes to make an analogy: **A** is to **B** as **C** is to **?** The model calculates B - A + C, and shows the 5 closest words.

    Your group's challenge: find analogies that **work**, and analogies that **fail**. Some ideas:

    - capitals: *france : paris :: japan : ?*
    - tenses: *walk : walked :: swim : ?*
    - comparatives: *good : better :: bad : ?*
    - New Zealand: *australia : sydney :: zealand : ?* (why *zealand* and not *new zealand*?)
    """)
    return


@app.cell
def _(mo):
    analogy_a = mo.ui.text(value = 'france', label = 'A:')
    analogy_b = mo.ui.text(value = 'paris', label = 'B:')
    analogy_c = mo.ui.text(value = 'japan', label = 'C:')
    mo.hstack([analogy_a, mo.md('is to'), analogy_b, mo.md('as'), analogy_c, mo.md('is to ?')], justify = 'start')
    return analogy_a, analogy_b, analogy_c


@app.cell
def _(analogy_a, analogy_b, analogy_c, glove, mo, pl):
    analogy_words = [analogy_a.value.lower().strip(), analogy_b.value.lower().strip(), analogy_c.value.lower().strip()]
    missing_words = [analogy_word for analogy_word in analogy_words if analogy_word not in glove.key_to_index]
    mo.stop(len(missing_words) > 0, mo.md(f'**Not in the vocabulary:** {", ".join(missing_words)}'))

    # B - A + C
    analogy_results = glove.most_similar(positive = [analogy_words[1], analogy_words[2]], negative = [analogy_words[0]], topn = 5)

    pl.DataFrame({
      'answer': [word for (word, score) in analogy_results],
      'similarity': [round(score, 3) for (word, score) in analogy_results],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which kinds of analogies work best? Which kinds fail?
    - When an analogy fails, is the answer completely wrong, or "nearly" right?
    - Remember that `.most_similar()` never gives back the input words. Does that make the analogies look better than they really are?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - analogies about very regular, frequent relationships (capitals, tenses, plurals, comparatives) tend to work best, because these relationships appear consistently in the training data
    - analogies about less frequent or less consistent relationships often give a related word (from the right topic), but not the right answer
    - because the input words are excluded, the "answer" is often the nearest word to C that isn't C itself; studies have found that many analogies only "work" because of this rule
    - GloVe treats each token separately, so multi-word names like *new zealand* are split into *new* and *zealand*
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: bias probe**

    In the word vectors notebook, we saw that analogies can reveal stereotypes. Here is another way to look for bias: for each word in a list, we calculate how much more similar it is to *she* than to *he*.

    - a **positive** score means the word is closer to *she*
    - a **negative** score means the word is closer to *he*
    - a score near **zero** means the word is about equally close to both

    The box starts with a list of jobs. Try other lists too, such as adjectives (*emotional, strong, smart, beautiful*), hobbies, or sports.
    """)
    return


@app.cell
def _(mo):
    bias_words = mo.ui.text(value = 'nurse, receptionist, homemaker, librarian, teacher, doctor, pilot, scientist, programmer, engineer, ceo, secretary', label = 'words:', full_width = True)
    bias_words
    return (bias_words,)


@app.cell
def _(bias_words, glove, mo, plt):
    chosen_bias_words = [bias_word.strip().lower() for bias_word in bias_words.value.split(',') if bias_word.strip().lower() in glove.key_to_index]
    mo.stop(len(chosen_bias_words) == 0, mo.md('**Type some words that are in the vocabulary!**'))

    # similarity to 'she' minus similarity to 'he'
    bias_scores = [float(glove.similarity(bias_word, 'she') - glove.similarity(bias_word, 'he')) for bias_word in chosen_bias_words]

    fig2, ax2 = plt.subplots(figsize = (9, 5))
    ax2.barh(chosen_bias_words, bias_scores)
    ax2.axvline(0, color = 'black', linewidth = 1)
    ax2.set_xlabel('closer to "he"  <---------->  closer to "she"')
    fig2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which words are closest to *she*? Which are closest to *he*? Do these match stereotypes?
    - Look at *secretary*. Why might it be closer to *he*? (Hint: think about the other meanings of *secretary* in the news.)
    - The vectors learned these patterns from real texts. Does that make the vectors "right"? What could happen if a company used them to sort job applications?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - jobs like *nurse*, *receptionist*, and *homemaker* come out much closer to *she*, and jobs like *engineer* and *ceo* closer to *he*: the vectors have learned stereotypes from how these words are used in the texts
    - *secretary* is closer to *he* because in news text it is often used for *Secretary of State* or *Secretary of Defence*, which are mostly men in the training data: one vector mixes all of a word's meanings
    - the vectors accurately reflect patterns in the training texts, but those patterns reflect past and present inequalities; systems built on them (e.g., ranking job applicants or search results) can repeat and amplify those inequalities
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. Word vectors learn meaning from "the company a word keeps" (Firth). WordNet's meanings were decided by people. What can each approach capture that the other can't?
    2. The vectors learned stereotypes from the texts they were trained on. Whose responsibility is it to deal with this: the people who wrote the texts, the people who trained the vectors, or the people who use them?
    3. Each word gets a single vector, which mixes all of its meanings together (*kiwi*, *secretary*). What problems might this cause?
    4. Large language models use vectors for every word they read and write. If the vectors carry biases, what might that mean for the text that chatbots produce?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - vectors capture usage, topic, and association, and can be learned for any corpus and any word that appears often enough; WordNet captures precise, hand-checked relations (synonyms, antonyms, hierarchies) but only for the words and senses its creators included, and it can't learn new ones
    - bias can come from the texts, from the choice of which texts to train on, and from how the vectors are used; there are methods to "debias" vectors, but they only remove some kinds of bias, so the people using the vectors still need to test for it
    - a single vector for each word blurs different senses together, so the similarity of a word depends on which of its meanings is most common in the training data (and this can differ between, e.g., New Zealand and American English)
    - the vectors inside modern language models are more sophisticated (they change depending on the context), but they are still learned from text, so the patterns, including the biases, in that text can show up in what chatbots write
    ''')})
    return


if __name__ == "__main__":
    app.run()
