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
    # **In-class: language models**

    Today's plan:

    1. Review: conditional probabilities, chained probabilities, and generating text
    2. Activities: build your own autocomplete, a generation playground, and which sounds more natural?
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import random
    import requests
    import polars as pl
    import nltk
    from nltk import FreqDist
    from collections import defaultdict
    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['punkt_tab', 'state_union', 'brown', 'gutenberg'])
    return FreqDist, defaultdict, nltk, pl, random, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: language models - key concepts**

    - the **conditional probability** of a word given the previous word is $P(w_2 | w_1) = \frac{c(w_1 w_2)}{c(w_1)}$
    - the probability of a phrase is the probability of each bigram in it, **chained** (multiplied) together
    - to **generate** text, we keep choosing a next word, based on the words which followed the current word in the training text

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _(FreqDist, nltk):
    review_tokens = 'these pretzels are making me thirsty they are also making me tired i love pretzels because they make me thirsty'.split()
    review_words = FreqDist(review_tokens)
    review_bigrams = FreqDist(nltk.bigrams(review_tokens))

    # what is P(thirsty | me)?
    review_bigrams[('me', 'thirsty')] / review_words['me']
    return review_bigrams, review_words


@app.cell
def _(review_bigrams, review_words):
    # what is P(making | are) x P(me | making) x P(tired | me)?
    (review_bigrams[('are', 'making')] / review_words['are']) * (review_bigrams[('making', 'me')] / review_words['making']) * (review_bigrams[('me', 'tired')] / review_words['me'])
    return


@app.cell
def _(review_bigrams, review_words):
    # what is P(hungry | me)?
    review_bigrams[('me', 'hungry')] / review_words['me']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Review answers": mo.md(r'''
    - *me* occurs 3 times, and *me thirsty* occurs 2 times, so P(*thirsty* | *me*) = 2/3 = 0.67
    - *are* is followed by *making* 1 out of 2 times, *making* is always followed by *me* (2/2), and *me* is followed by *tired* 1 out of 3 times: 0.5 x 1 x 0.33 = 0.17
    - *me hungry* never occurs in the text, so its probability is 0, and so is the probability of any phrase which contains it
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **The models**

    For today's activities, we will train bigram models on four different corpora:

    - the **Big Salad** (Seinfeld scripts)
    - every **State of the Union** speech in NLTK
    - the **news** category of Brown
    - three **Jane Austen** novels from Gutenberg

    For each corpus, the `train_model()` function counts the words and makes a dictionary of the words which come after each word (just like in the word probabilities and generating text notebooks). To keep things simple, it lowercases everything and only keeps alphabetic words. This cell might take a little while to run.
    """)
    return


@app.cell
def _(FreqDist, defaultdict, nltk, requests):
    def train_model(tokens):
      # lowercase and keep only alphabetic words
      words = [token.lower() for token in tokens if token.isalpha()]

      # each word gets a FreqDist of the words which come after it
      next_words = defaultdict(FreqDist)
      for (w1, w2) in nltk.bigrams(words):
        next_words[w1][w2] += 1
      return next_words

    big_salad = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/big_salad.txt').text

    models = {
      'Big Salad (Seinfeld)': train_model(nltk.word_tokenize(big_salad)),
      'State of the Union': train_model(nltk.corpus.state_union.words()),
      'Brown news': train_model(nltk.corpus.brown.words(categories = 'news')),
      'Jane Austen': train_model(nltk.corpus.gutenberg.words('austen-emma.txt') + nltk.corpus.gutenberg.words('austen-persuasion.txt') + nltk.corpus.gutenberg.words('austen-sense.txt')),
    }
    return (models,)


@app.function
def next_word_probability(model, w1, w2):
  # P(w2 | w1): how often w2 came after w1, out of all the words which came after w1
  if model[w1].N() == 0:
    return 0
  return model[w1][w2] / model[w1].N()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: build your own autocomplete**

    Type the start of a sentence, and choose a model. The table shows the 10 most likely next words, based on the *last* word you typed. This is basically how the autocomplete on your phone works (although your phone's model is much bigger, and also learns from what *you* type!).

    Then play **follow the suggestion**: add the top suggestion to your sentence, and keep going. Where does the sentence end up in each model?
    """)
    return


@app.cell
def _(mo, models):
    autocomplete_text = mo.ui.text(value = 'do you know', label = 'start of a sentence:', full_width = True)
    autocomplete_model = mo.ui.dropdown(options = list(models.keys()), value = 'Big Salad (Seinfeld)', label = 'model:')
    mo.vstack([autocomplete_text, autocomplete_model])
    return autocomplete_model, autocomplete_text


@app.cell
def _(autocomplete_model, autocomplete_text, mo, models, pl):
    # the last word of the sentence
    typed_words = autocomplete_text.value.lower().split()
    mo.stop(len(typed_words) == 0, mo.md('**Type something!**'))
    last_word = typed_words[-1]

    chosen_model = models[autocomplete_model.value]
    suggestions = chosen_model[last_word].most_common(10)

    mo.vstack([
      mo.md(f'**most likely words after "{last_word}":**'),
      pl.DataFrame({
        'next word': [next_word for (next_word, count) in suggestions],
        'probability': [round(next_word_probability(chosen_model, last_word, next_word), 3) for (next_word, count) in suggestions],
      }),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Try the same sentence start in all four models. How do the suggestions differ? Why?
    - Which model gives the most "useful" suggestions for writing a text message? For writing an essay?
    - What happens when the last word is a word the model has never seen?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - each model only knows the words and patterns in its training corpus, so the same start gives conversational suggestions in Seinfeld, political ones in the State of the Union, and 19th century ones in Austen
    - a model trained on the kind of text you want to write will give better suggestions; this is why phone keyboards learn from the user
    - if the last word was never seen in training, the model has no suggestions at all; and because the model only looks at the *last* word, it ignores everything else you typed (*what are you* and *how are you* give the same suggestions!)
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: generation playground**

    Choose a model, a seed word, and a way of choosing the next word:

    - **most frequent**: always choose the most frequent next word (version 1 in the generating text notebook)
    - **random**: choose any next word at random (version 2)
    - **top-k**: choose at random from the *k* most frequent next words (version 3)
    - **weighted**: choose in proportion to how often each word came next (version 4)

    Click the button to generate new text. Then play **guess the corpus**: one person generates some text without showing which model they used, and the rest of the group guesses which corpus it came from.
    """)
    return


@app.cell
def _(mo, models):
    generate_model_choice = mo.ui.dropdown(options = list(models.keys()), value = 'Big Salad (Seinfeld)', label = 'model:')
    generate_seed = mo.ui.text(value = 'the', label = 'seed word:')
    generate_method = mo.ui.dropdown(options = ['most frequent', 'random', 'top-k', 'weighted'], value = 'weighted', label = 'method:')
    generate_length = mo.ui.slider(start = 5, stop = 50, value = 20, label = 'number of words:')
    generate_k = mo.ui.slider(start = 1, stop = 20, value = 5, label = 'k (for top-k):')
    generate_button = mo.ui.run_button(label = 'generate!')
    mo.vstack([generate_model_choice, generate_seed, generate_method, generate_length, generate_k, generate_button])
    return (
        generate_button,
        generate_k,
        generate_length,
        generate_method,
        generate_model_choice,
        generate_seed,
    )


@app.cell
def _(random):
    def generate(model, word, num, method, k):
      output = []
      for i in range(num):
        output.append(word)
        # stop if this word never had a next word
        if model[word].N() == 0:
          break
        if method == 'most frequent':
          word = model[word].max()
        elif method == 'random':
          word = random.choice(list(model[word]))
        elif method == 'top-k':
          word = random.choice([next_word for (next_word, count) in model[word].most_common(k)])
        else:
          word = random.choices(list(model[word].keys()), weights = list(model[word].values()))[0]
      return ' '.join(output)

    return (generate,)


@app.cell
def _(
    generate,
    generate_button,
    generate_k,
    generate_length,
    generate_method,
    generate_model_choice,
    generate_seed,
    mo,
    models,
):
    mo.stop(not generate_button.value, mo.md('*Click the button to generate some text.*'))

    generated = generate(models[generate_model_choice.value], generate_seed.value.lower().strip(), generate_length.value, generate_method.value, generate_k.value)
    mo.md(f'### {generated}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - Which method gives the most realistic text? Which gives the most interesting text?
    - How easy was it to guess the corpus? What gave it away?
    - Did the generated text ever *say* something true, or meaningful? Did the model *mean* it?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - *most frequent* quickly gets stuck in loops, *random* is gibberish, and *top-k* and *weighted* are usually the most realistic; real language models use methods like top-k and weighted sampling (with a "temperature" setting)
    - the corpus is usually easy to guess from the vocabulary (names, topics, old-fashioned words), even when the grammar is a mess
    - any meaning in the generated text comes from the training texts and from *us* as readers: the model only knows which words tend to follow which
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: which sounds more natural?**

    Write two versions of the same idea, and see which one the model thinks is more likely. For example:

    - *strong tea* vs *powerful tea* (remember the natural vs unnatural English activity from the collocations session! You might find that both get 0...)
    - a normal sentence vs the same words in a different order
    - a common phrase vs a creative or unusual phrase

    Does the model agree with your intuitions?
    """)
    return


@app.cell
def _(mo, models):
    natural_model = mo.ui.dropdown(options = list(models.keys()), value = 'Big Salad (Seinfeld)', label = 'model:')
    phrase1 = mo.ui.text(value = 'i want to go home', label = 'phrase 1:', full_width = True)
    phrase2 = mo.ui.text(value = 'i want to go house', label = 'phrase 2:', full_width = True)
    mo.vstack([natural_model, phrase1, phrase2])
    return natural_model, phrase1, phrase2


@app.cell
def _(models, natural_model, nltk, phrase1, phrase2, pl):
    def phrase_probability(model, phrase):
      # multiply the probability of each bigram in the phrase
      phrase_words = phrase.lower().split()
      probability = 1
      unseen = []
      for (w1, w2) in nltk.bigrams(phrase_words):
        bigram_probability = next_word_probability(model, w1, w2)
        if bigram_probability == 0:
          unseen.append(w1 + ' ' + w2)
        probability = probability * bigram_probability
      return probability, unseen

    natural_results = []
    for chosen_phrase in [phrase1.value, phrase2.value]:
      phrase_result, unseen_bigrams = phrase_probability(models[natural_model.value], chosen_phrase)
      natural_results.append({'phrase': chosen_phrase, 'probability': phrase_result, 'unseen bigrams': ', '.join(unseen_bigrams)})

    pl.DataFrame(natural_results)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Some things to think about:

    - When did the model agree with your intuitions? When did it disagree?
    - How often did you get a probability of 0? What does an "unseen bigram" tell you?
    - Is a phrase with a probability of 0 *wrong*? Is a phrase with a high probability *good*?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - the model often agrees with our intuitions for common phrases, because natural phrases are frequent ones
    - but any creative, new, or rare phrase quickly gets a probability of 0, because even one unseen bigram makes the whole phrase impossible; real models use smoothing so that unseen phrases get a small probability instead
    - probability is not the same as correctness or quality: rare phrases can be perfectly good (poetry, jokes, new ideas), and frequent phrases can be clichés
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. In Searle's "Chinese Room", someone who doesn't know Chinese follows rules to give perfect Chinese answers. Is our language model like the person in the room? Is predicting the next word the same as understanding?
    2. The same algorithm sounded like Seinfeld or like a president, depending on the training data. What does that mean for large language models which are trained on huge amounts of text from the internet?
    3. Our models give a probability of zero to anything new, but language is creative. What would a model trained only on the past miss about the future?
    4. Large language models are based on the same idea of predicting the next word, at a much larger scale. If a model can produce fluent text that is wrong, how should we decide what to trust?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - the model manipulates word patterns without any connection to what the words refer to; whether a much bigger model (with much better patterns) *understands* is still debated, and it depends on what we mean by understanding
    - a model reproduces the language, topics, opinions, and biases of its training data; internet text over-represents some people, languages, and views, and under-represents others
    - a model trained on past text will be worse at new words, new events, and new ways of speaking, and it may treat unusual (but perfectly fine) language as unlikely or wrong
    - fluency comes from frequent patterns, not from checking facts, so fluent text can be confidently wrong; claims from a language model should be checked against reliable sources
    ''')})
    return


if __name__ == "__main__":
    app.run()
