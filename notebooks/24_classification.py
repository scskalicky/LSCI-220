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
    #### Relevant NLTK Book sections

    [NLTK Book, Chapter 6, Sections 1 and 3](https://www.nltk.org/book/ch06.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Classification: teaching a computer to sort texts**

    Many NLP tasks involve sorting texts into categories. Is this email spam or not spam? Is this review positive or negative? Was this text written by a human or a computer? Is this review real or satirical? Sorting things into categories like this is called **classification**, and a program that does it is called a **classifier**.

    In this notebook, we will build two classifiers which try to sort sentences from the Brown corpus into two categories: **news** and **romance**. We will stay at the level of *ideas* rather than maths: what a classifier needs, how it learns, and how we can tell whether it is any good.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Supervised vs unsupervised learning**

    In the topic modelling notebook, we gave the computer a pile of documents and asked it to find groups of words, without telling it anything about the documents. The model was never told which documents were news, which were fiction, and so on. It had to find patterns on its own, and then we had to decide what the patterns meant by assigning labels to the topics. This approach to machine learning is called **unsupervised** learning.

    An alternative approach is **supervised** learning. In this case, we give the computer a set of examples where we already know the right answer (known as the **label**), such as sentences which we know are from news or romance genres. The computer is given a set of **features** and then locates which features seem to pattern with different labels. The algorithm then uses those patterns to guess the labels of new examples it has never seen before. Because we "supervise" the learning by providing the right answers, this is called **supervised** learning.


    Here are the key terms for classification:

    - **label**: the category we want to predict (here, `news` or `romance`)
    - **features**: the information about each example that the classifier can use to make its decision. In this course, features are always **linguistic features**
    - **training**: showing the classifier lots of examples, with their labels, so it can learn which clues go with which label
    - **predicting**: asking the trained classifier to guess the label of a new example
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import random
    import polars as pl
    import nltk
    from nltk import FreqDist
    from nltk.corpus import brown
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, confusion_matrix
    from sklearn.preprocessing import StandardScaler

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'brown'])
    return (
        FreqDist,
        LogisticRegression,
        StandardScaler,
        accuracy_score,
        brown,
        confusion_matrix,
        nltk,
        pl,
        random,
        train_test_split,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Getting the data**

    We need examples with labels. We will use sentences from two categories of the Brown corpus: news and romance. I take a random sample of 3,000 sentences from each category, and I use `random.seed()` so that we all get the same sample.

    Then I put all of the sentences into one list, where each item is a tuple of `(sentence, label)`, and shuffle the list so that the news and romance sentences are mixed together.

    First I make a helper function to check if the sentence has enough words (otherwise some sentences have quotes or only like 1 or 2 words.)
    """)
    return


@app.cell
def _(brown, random):
    random.seed(220)

    # make sure there are words!
    def has_words(sentence):
      # make sure there are at least three alphabetic words
      words = [word for word in sentence if word.isalpha()]
      return len(words) > 2

    # random sample 3000 sentences from each category
    news_sentences = random.sample([sent for sent in brown.sents(categories = 'news') if has_words(sent)], 3000)
    romance_sentences = random.sample([sent for sent in brown.sents(categories = 'romance') if has_words(sent)], 3000)


    # put them together as (sentence, label) tuples
    labelled_sentences = []
    for news_sentence in news_sentences:
      labelled_sentences.append((news_sentence, 'news'))
    for romance_sentence in romance_sentences:
      labelled_sentences.append((romance_sentence, 'romance'))

    # mix them up
    random.shuffle(labelled_sentences)

    len(labelled_sentences)
    return (labelled_sentences,)


@app.cell
def _(labelled_sentences):
    # what do the examples look like?
    for (example_sentence, example_label) in labelled_sentences[:5]:
      print(example_label, ' '.join(example_sentence))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **The baseline**

    Before we build anything, we need to know how to measure the success of our classifier. In this case, that's kind of easy because our data has exactly half news and half romance sentences. So if our classifier just guessed `news` for every single sentence, it would be right 50% of the time, without learning anything at all!

    This is called the **baseline**. A classifier is only useful if it does *better* than the baseline. Always ask "compared to what?" when someone tells you how accurate a classifier is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Classifier 1: Naive Bayes, with words as features (NLTK)**

    Our first classifier follows the example in Chapter 6 of the NLTK book. The features (clues) will be the words in each sentence. For each of the 1000 most frequent words in our data, the feature records whether or not the sentence contains that word. So, in this sense, we are asking whether particular word choices can help us "learn" the different labels.

    First, let's find the 1000 most frequent words in the entire set of sentences. Not surprisingly, they are function words.
    """)
    return


@app.cell
def _(FreqDist, labelled_sentences):
    all_words = FreqDist([word.lower() for (sentence, label) in labelled_sentences for word in sentence if word.isalpha()])

    top_words = [word for (word, count) in all_words.most_common(1000)]

    top_words[:25]
    return (top_words,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we write a **feature extractor**: a function which takes a sentence and returns its features. NLTK wants the features as a dictionary, where each key is the name of a feature and each value is the value of that feature. For example, `{'contains(president)': True, 'contains(eyes)': False, ...}`.

    So, essentially, this feature extractor is detecting the presence/absence of words (i.e., features) in each sentence, which can then be used to "learn" where features are (and are not), in turn giving us patterns associated with either category.
    """)
    return


@app.cell
def _(top_words):
    def sentence_word_features(sentence):
      # the set of (lowercased) words in this sentence
      sentence_words = set([word.lower() for word in sentence])

      # does the sentence contain each of the top words?
      features = {}
      for word in top_words:
        features['contains(' + word + ')'] = word in sentence_words
      return features

    return (sentence_word_features,)


@app.cell
def _(labelled_sentences, sentence_word_features):
    # the features for the first sentence (just the first 10, there are 1000 in total!)
    list(sentence_word_features(labelled_sentences[0][0]).items())[:10]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Training and test sets**

    If we want to know how good our classifier is, we can't test it on the same sentences it learned from. That would be like giving students the exact exam questions to practise with, and then marking them on those same questions: the "learning" is just repeating the correct answers.

    So in this sort of research it is common to split the data into two parts:

    - the **training set**, which the classifier learns from (here, 80% of the sentences)
    - the **test set**, which we hide from the classifier until the end, and use to check how well it does on sentences it has never seen (the other 20%)

    Because we already shuffled our sentences, we can just use the first 4800 for training and the last 1200 for testing.

    I use `nb` to stand for Naive Bayes.
    """)
    return


@app.cell
def _(labelled_sentences, sentence_word_features):
    # turn every sentence into (features, label)
    word_feature_sets = [(sentence_word_features(sentence), label) for (sentence, label) in labelled_sentences]

    nb_train = word_feature_sets[:4800]
    nb_test = word_feature_sets[4800:]

    print(len(nb_train), 'training examples')
    print(len(nb_test), 'test examples')
    return nb_test, nb_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **How does Naive Bayes work?**

    Naive Bayes gets its name from its two parts:

    - **Bayes**: it uses Bayes’ rule (named after Thomas Bayes), which lets us work backwards. From the training data, the classifier counts how often a word appears in each category (e.g., how often *president* appears in the news genre). Bayes’ rule (which is a way to calculate probability) turns that around into what we actually want to know: how likely a sentence is to be news, given that it contains president.

    - **Naive**: the classifier is naive because it assumes every clue is independent of every other clue. For example, it assumes that seeing united tells you nothing about whether you’ll see states. This is an overly simplistic view of language, but it keeps the calculation simple.

    Here's an explanation of what it does:

    1. During training, it counts how often each feature value (e.g., `contains(president) = True`) appears with each label. For example, the word *president* might appear in lots of news sentences, but hardly any romance sentences.
    2. When it sees a new sentence, it looks at all of the clues in that sentence, and adds up how much each clue points towards `news` or `romance`.
    3. It chooses the label with the most evidence.

    It is called "naive" because it treats every clue as if it had nothing to do with the other clues (e.g., it doesn't know that *united* and *states* often appear together). This is obviously not true of language, but the classifier often works surprisingly well anyway!

    Let's train it. This might take a few seconds.
    """)
    return


@app.cell
def _(nb_train, nltk):
    # first train it on our training set of data
    nb_classifier = nltk.NaiveBayesClassifier.train(nb_train)
    return (nb_classifier,)


@app.cell
def _(nb_classifier, nb_test, nltk):
    # then point the TRAINED classifier to the test data 
    nltk.classify.accuracy(nb_classifier, nb_test)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We obtain 0.835, or 83.5% accuracy in predicting whether a sentence in the test set belongs to news or romance genres. That's much better than the 50% baseline, meaning that the classifier has "learned" how to associate certain words with certain genres. This is **machine learning** in a nutshell.

    We should be curious about more than the accuracy, such as which clues did the classifier find most useful? NLTK's `show_most_informative_features()` tells us. The ratio on the right shows how much more likely the clue is with one label than with the other. For example, `33.8 : 1.0` means the clue was about 28 times more likely to appear with that label.
    """)
    return


@app.cell
def _(nb_classifier):
    nb_classifier.show_most_informative_features(15)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Do these clues make sense? Look at the words and think about whether you agree with their designation.

    We can ask the classifier to label new sentences of our own. Remember that it needs the sentence as a list of tokens. Note the last sentence - the classifier only has two choices, news or romance, so we might get some interesting results when we start putting in sentences that don't really belong to either version.
    """)
    return


@app.cell
def _(nb_classifier, nltk, sentence_word_features):
    my_sentences = [
      'The senator announced a new tax plan on Tuesday.',
      'She looked into his eyes and smiled.',
      'The weather was lovely.',
        'This course is about natural language processing'
    ]

    for my_sentence in my_sentences:
      my_features = sentence_word_features(nltk.word_tokenize(my_sentence))
      print(nb_classifier.classify(my_features), ':', my_sentence)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Classifier 2: Logistic regression, with hand-made features (scikit-learn)**

    Our second classifier uses a completely different kind of feature. Instead of words, we will describe each sentence based on different linguistic features.

    1. the length of the sentence, in words
    2. the average length of the words
    3. the proportion of words which are pronouns (e.g., *I*, *she*, *they*)
    4. the proportion of words which start with a capital letter

    These features don't care *which* words are used, only about the *shape* of the sentence. Remember the part of speech profiles from the parts of speech notebook: conversation and fiction used more pronouns, and news used more nouns (and longer words).

    Notice the `if` statement in the function. Our `has_words()` function already removed sentences without enough words, so this should never happen, but it's there just in case: a sentence with no words would give us a division by zero.
    """)
    return


@app.cell
def _():
    pronouns = ['i', 'me', 'my', 'you', 'your', 'he', 'him', 'his', 'she', 'her', 'we', 'us', 'our', 'they', 'them', 'their', 'it']

    def sentence_numbers(sentence):
      # keep only the words (no punctuation)
      words = [word for word in sentence if word.isalpha()]

      # avoid dividing by zero if the sentence has no words
      if len(words) == 0:
        return [0, 0, 0, 0]

      sentence_length = len(words)
      average_word_length = sum([len(word) for word in words]) / len(words)
      pronoun_proportion = len([word for word in words if word.lower() in pronouns]) / len(words)
      capital_proportion = len([word for word in words if word[0].isupper()]) / len(words)

      return [sentence_length, average_word_length, pronoun_proportion, capital_proportion]

    return (sentence_numbers,)


@app.cell
def _(labelled_sentences, sentence_numbers):
    # the four features for the first sentence
    print(' '.join(labelled_sentences[0][0]))
    sentence_numbers(labelled_sentences[0][0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Before we train anything, let's check whether these features actually differ between news and romance. I put the features into a polars dataframe, and use `group_by()` to get the average of each feature for each label:
    """)
    return


@app.cell
def _(labelled_sentences, pl, sentence_numbers):
    feature_names = ['sentence length', 'average word length', 'pronoun proportion', 'capital proportion']

    feature_rows = []
    for (row_sentence, row_label) in labelled_sentences:
      numbers = sentence_numbers(row_sentence)
      feature_rows.append({
        'label': row_label,
        'sentence length': numbers[0],
        'average word length': numbers[1],
        'pronoun proportion': numbers[2],
        'capital proportion': numbers[3],
      })

    feature_table = pl.DataFrame(feature_rows)
    feature_table.group_by('label').mean()
    return (feature_names,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The averages are different, so these features should give the classifier some useful clues. But remember that these are *averages*: plenty of individual news sentences will look like romance sentences, and the other way around.

    ## **Training and test sets (again)**

    scikit-learn wants the features as a list of lists of numbers (one list of 4 numbers for each sentence), and the labels as a separate list. scikit-learn also has a function called `train_test_split()` which shuffles and splits the data for us. Here I also split the original sentences, so that we can look at them later.

    (By tradition, the features are called `X` and the labels are called `y`.)
    """)
    return


@app.cell
def _(labelled_sentences, sentence_numbers, train_test_split):
    # get our features for each sentence
    number_features = [sentence_numbers(sentence) for (sentence, label) in labelled_sentences]

    # split the labels and sentences into two different lists
    labels = [label for (sentence, label) in labelled_sentences]
    sentences = [sentence for (sentence, label) in labelled_sentences]

    # split everything into 80% training and 20% test
    X_train, X_test, y_train, y_test, sentences_train, sentences_test = train_test_split(number_features, labels, sentences, test_size = 0.2, random_state = 220)

    print(len(X_train), 'training examples')
    print(len(X_test), 'test examples')
    return X_test, X_train, sentences_test, y_test, y_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Putting the features on the same scale**

    Our four features are measured on very different scales. Sentence length can be anything from 3 to over 100 words, whereas pronoun proportion and capital proportion can only go from 0 to 1. This makes the weights hard to compare: a feature measured with small numbers needs a big weight to make any difference, and a feature measured with big numbers only needs a small weight.

    So before training the classifier, we **z-score** the features. A z-score shows how far a value is from the average, measured in *standard deviations*. A z-score of 0 means the value is exactly average, a z-score of 1 means it is one standard deviation above average, and a z-score of -1 means it is one standard deviation below average.

    If you don't understand this, just know that it puts all of the features on the same scale so that we can compare them directly. Imagine you had to compare one student's score on a test marked out of 10 with another student's score on a test marked out of 100: you would need to put both scores on the same scale before you could say who did better. z-scores do this by asking "how unusual is this score, compared to everyone else's?"

    scikit-learn's `StandardScaler()` does the z-scoring for us. Notice that the scaler only learns the averages and standard deviations from the **training set**. The test set is supposed to be data the classifier has never seen, so we don't let it influence anything, not even the averages! We then use the training averages to z-score both sets.
    """)
    return


@app.cell
def _(StandardScaler, X_test, X_train):
    # learn the averages and standard deviations from the training data only
    scaler = StandardScaler()
    scaler.fit(X_train)

    # z-score both the training and test data
    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # the first sentence, before and after z-scoring
    print('before:', X_train[0])
    print('after:', X_train_scaled[0].round(2))
    return X_test_scaled, X_train_scaled


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **How does logistic regression work?**

    Logistic regression is a different algorithm when compared to Naive Bayes. A regression shows how much each feature matters, which we can use to make predictions. Compare this to Naive Bayes, which counted how often each feature appeared with each category, one feature at a time, and then found a winner. Logistic regression instead learns a **weight** for each feature, and it learns all of the weights *at the same time*, adjusting them together until they separate the categories as well as possible. Because the weights are learned together, they take each other into account (e.g., if two features carry the same information, the weight can be shared between them, rather than counted twice). To make a prediction, logistic regression multiplies each feature by its weight, adds them all up, and uses the total to choose the most likely category.

    For example, it might learn that a high proportion of pronouns is a strong clue for `romance`, and that a high proportion of capital letters is a clue for `news`. To make a prediction, it combines the four features using these weights, and decides which label is more likely.

    Let's train it:
    """)
    return


@app.cell
def _(
    LogisticRegression,
    X_test_scaled,
    X_train_scaled,
    accuracy_score,
    y_test,
    y_train,
):
    # create the classifier
    lr_classifier = LogisticRegression()

    # train it on the (z-scored) training data
    lr_classifier.fit(X_train_scaled, y_train)

    # predict the labels of the (z-scored) test sentences
    lr_predictions = lr_classifier.predict(X_test_scaled)

    # how many predictions were correct?
    accuracy_score(y_test, lr_predictions)
    return lr_classifier, lr_predictions


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Better than the baseline, but not as good as Naive Bayes with words. Remember, Naive Bayes looked at actual words, whereas logistic regression is looking at sentence features. What does this tell you about quality of different linguistic features?

    Anyhow, which features did the logistic regression rely on the most? We can look at the weights in `.coef_`. A positive weight pushes towards `romance`, and a negative weight pushes towards `news` (scikit-learn puts the labels in alphabetical order, and positive weights point to the second one). Bigger numbers (positive or negative) mean the feature matters more.

    Here, pronoun proportion has the largest weight, indicating that more pronouns = more probability of being romance versus news. Does that make sense to you?

    Because we z-scored the features, we can compare the weights directly: each weight shows the effect of a one standard deviation change in that feature. Look at sentence length: without z-scoring, its weight was a tiny -0.05 (because sentences are measured in lots of words), which made it look unimportant. After z-scoring, we can see that it is actually the second most important feature, with longer sentences pointing towards news.
    """)
    return


@app.cell
def _(feature_names, lr_classifier, pl):
    pl.DataFrame({'feature': feature_names, 'weight': [round(weight, 2) for weight in lr_classifier.coef_[0]]})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **What kind of mistakes does it make?**

    Accuracy is just one number. A **confusion matrix** can quantify the nature of the mistakes the classifier makes: how many news sentences it called romance, and how many romance sentences it called news.
    """)
    return


@app.cell
def _(confusion_matrix, lr_predictions, pl, y_test):
    matrix = confusion_matrix(y_test, lr_predictions, labels = ['news', 'romance'])

    pl.DataFrame({
      'true label': ['news', 'romance'],
      'predicted news': [matrix[0][0], matrix[1][0]],
      'predicted romance': [matrix[0][1], matrix[1][1]],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The numbers going diagonally (top left and bottom right) are the correct predictions. The other two numbers are the mistakes. Does the classifier make more mistakes with one label than the other?

    Let's look at some of the sentences it got wrong:
    """)
    return


@app.cell
def _(lr_predictions, sentences_test, y_test):
    mistakes = 0

    for test_sentence, true_label, predicted_label in zip(sentences_test, y_test, lr_predictions):
      if true_label != predicted_label and mistakes < 8:
        print(f'true: {true_label}, predicted: {predicted_label} | ' + ' '.join(test_sentence))
        mistakes += 1
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Why do you think these sentences fooled the classifier? Would *you* have been able to tell which category they came from?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Training accuracy vs test accuracy**

    What happens if we check the classifiers on the sentences they were *trained* on?
    """)
    return


@app.cell
def _(
    X_test_scaled,
    X_train_scaled,
    lr_classifier,
    nb_classifier,
    nb_test,
    nb_train,
    nltk,
    y_test,
    y_train,
):
    print('Naive Bayes, training set:', round(nltk.classify.accuracy(nb_classifier, nb_train), 3))
    print('Naive Bayes, test set:', round(nltk.classify.accuracy(nb_classifier, nb_test), 3))
    print('Logistic regression, training set:', round(lr_classifier.score(X_train_scaled, y_train), 3))
    print('Logistic regression, test set:', round(lr_classifier.score(X_test_scaled, y_test), 3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both classifiers do a bit better on the sentences they have already seen. This is why we always test on a separate test set: the training accuracy makes the classifier look better than it really is. When a classifier does *much* better on its training data than on new data, we say it has **overfitted**: it has memorised the training examples rather than learning patterns that work on new examples.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Wrapping up**

    We built two classifiers which both beat the baseline, using two very different kinds of features:

    - Naive Bayes, with **words** as features, which mostly learned about the *topics* of news and romance
    - logistic regression, with four **sentence level** features

    Remember that a classifier only ever learns about the clues we give it, from the examples we give it. It doesn't understand news or romance; it finds whatever patterns separate the labels in the training data, whether or not those patterns are the ones we were interested in.

    ### **Your Turn**

    - Add a fifth feature to `sentence_numbers()`. You could use something from an earlier notebook, such as the VADER compound score from the sentiment notebook, or the average age of acquisition from the lexical sophistication notebook. Does the accuracy go up?
    - Change the categories to `news` and `editorial`. Why do you think the accuracy changes?
    - Change the number of words in `top_words` (e.g., 100 or 2000). What happens to the Naive Bayes accuracy?
    - A classifier is 85% accurate. Is that good? What would you want to know before deciding?
    """)
    return


@app.cell
def _():
    # use this code cell to explore classification!
    return


if __name__ == "__main__":
    app.run()
