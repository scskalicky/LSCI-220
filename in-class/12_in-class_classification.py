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
    # **In-class: classifying satire**

    Today's plan:

    1. Review: baselines, training and test sets, and z-scores
    2. Activities: build your own satire detector, and fool the classifier
    3. Critical reflection
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import io
    import os
    import zipfile
    import requests
    import polars as pl
    import nltk
    from glob import glob
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    nltk.download(['punkt_tab', 'vader_lexicon'])
    return (
        LogisticRegression,
        SentimentIntensityAnalyzer,
        StandardScaler,
        confusion_matrix,
        glob,
        io,
        nltk,
        os,
        pl,
        requests,
        train_test_split,
        zipfile,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Review: classification - key concepts**

    - a classifier learns which **features** go with which **label**, from examples where we already know the label (supervised learning)
    - we train on the **training set**, and check how good the classifier is on the **test set**, which it has never seen
    - the **baseline** is the accuracy we would get without learning anything
    - **z-scores** put features on the same scale, so that their weights can be compared

    Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _():
    # we have 375 satirical reviews and 375 normal reviews.
    # what accuracy would we get if we always guessed 'satire'?
    375 / (375 + 375)
    return


@app.cell
def _():
    # a classifier gets these scores. What is going on?
    training_accuracy = 1.0
    test_accuracy = 0.88

    training_accuracy - test_accuracy
    return


@app.cell
def _(StandardScaler):
    # three scores, and their z-scores. Which z-score belongs to the average score?
    tiny_scaler = StandardScaler()
    tiny_scaler.fit_transform([[2], [4], [6]])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Review answers": mo.md(r'''
    - the data is exactly half satire and half normal, so always guessing one label gives 50%: this is our baseline
    - a classifier that does much better on its training data than on its test data has **overfitted**: it has partly memorised the training examples instead of learning patterns which work on new examples (the 88% is the number to report!)
    - the average score (4) gets a z-score of 0; the other scores are 1.22 standard deviations above and below the average
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Getting the data**

    We use the Amazon reviews from the sentiment notebook. For each review, the file name tells us the star rating and the label (e.g., `001-5-satire.txt` is review 1, 5 stars, satire).
    """)
    return


@app.cell
def _(glob, io, os, requests, zipfile):
    resources = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/'

    def download_corpus(url, folder):
      # download the zip file and unzip everything into the folder
      response = requests.get(url)
      zip_file = zipfile.ZipFile(io.BytesIO(response.content))
      zip_file.extractall(folder)
      return folder

    reviews_folder = download_corpus(resources + 'amazon%20reviews.zip', 'amazon reviews')

    review_texts = []
    review_stars = []
    review_labels = []

    for review_file in sorted(glob(reviews_folder + '/*.txt')):
      # e.g., ['001', '5', 'satire']
      name_parts = os.path.basename(review_file).replace('.txt', '').split('-')
      # skip any file which doesn't have a star rating in its name
      if len(name_parts) == 3 and name_parts[1].isdigit():
        with open(review_file, encoding = 'utf-8') as review_handle:
          review_texts.append(review_handle.read())
        review_stars.append(int(name_parts[1]))
        review_labels.append(name_parts[2])

    len(review_texts)
    return resources, review_labels, review_stars, review_texts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Lexicon features**

    Now we load the lexicons from the lexical sophistication and sentiment notebooks, and write a function which describes each review with a set of features. This cell might take a little while to run.
    """)
    return


@app.cell
def _(SentimentIntensityAnalyzer, requests, resources):
    def get_word_rating_resource(url):
      ratings = {}
      for line in requests.get(url).text.split('\n'):
        pair = line.split('\t')
        if len(pair) == 2:
          ratings[pair[0]] = float(pair[1])
      return ratings

    afinn_dict = get_word_rating_resource(resources + 'AFINN-111.txt')
    aoa_dict = get_word_rating_resource(resources + 'AoA_Brysbart.txt')
    concrete_dict = get_word_rating_resource(resources + 'concreteness.txt')
    freq_dict = get_word_rating_resource(resources + 'subtlxus_frequency.txt')

    vader = SentimentIntensityAnalyzer()
    return afinn_dict, aoa_dict, concrete_dict, freq_dict, vader


@app.cell
def _(
    afinn_dict,
    aoa_dict,
    concrete_dict,
    freq_dict,
    nltk,
    pl,
    review_stars,
    review_texts,
    vader,
):
    def average_rating(tokens, lexicon):
      ratings = [lexicon[token] for token in tokens if token in lexicon]
      # avoid dividing by zero
      if len(ratings) == 0:
        return 0
      return round(sum(ratings) / len(ratings),3)

    def review_features(text, stars):
      tokens = [token for token in nltk.word_tokenize(text.lower()) if token.isalpha()]
      sentences = nltk.sent_tokenize(text)

      # avoid dividing by zero for empty texts
      if len(tokens) == 0 or len(sentences) == 0:
        tokens = ['']
        sentences = ['']

      return {
        'VADER (sentence average)': round(sum([vader.polarity_scores(sentence)['compound'] for sentence in sentences]) / len(sentences), 3),
        'AFINN average': average_rating(tokens, afinn_dict),
        'age of acquisition': average_rating(tokens, aoa_dict),
        'concreteness': average_rating(tokens, concrete_dict),
        'frequency': average_rating(tokens, freq_dict),
        'review length': len(tokens),
        'average sentence length': round(len(tokens) / len(sentences),3),
        'exclamation marks': round(text.count('!') / len(tokens),3),
        'I / me / my': round(len([token for token in tokens if token in ['i', 'me', 'my', 'mine', 'myself']]) / len(tokens),3),
        'star rating': stars,
      }

    # a table with every feature for every review
    features_table = pl.DataFrame([review_features(text, stars) for text, stars in zip(review_texts, review_stars)])
    feature_options = features_table.columns
    features_table
    return feature_options, features_table, review_features


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We use the same training and test split for everything today, so that the classifiers are compared fairly. Instead of splitting the texts themselves, I split the positions of the reviews (0, 1, 2, ...), and use those positions to pick out the texts, features, and labels.
    """)
    return


@app.cell
def _(review_labels, review_texts, train_test_split):
    train_positions, test_positions = train_test_split(list(range(len(review_texts))), test_size = 0.2, random_state = 220)

    y_train = [review_labels[position] for position in train_positions]
    y_test = [review_labels[position] for position in test_positions]

    print(f'all the train positions are: {train_positions}\n')

    print(len(train_positions), 'training reviews')
    print(len(test_positions), 'test reviews')
    return test_positions, train_positions, y_test, y_train


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: build your own satire detector**

    Choose some features below, and a logistic regression classifier will be trained on them (using z-scores, as in the classification notebook). You'll see its accuracy on the test set, the weights of the features, and a confusion matrix.

    Your group's challenge: get the **highest accuracy** with the **fewest features**.

    - Which single feature works best on its own?
    - Do more features always mean higher accuracy?
    - Should `star rating` be allowed? Is it a *linguistic* feature?
    """)
    return


@app.cell
def _(feature_options, mo):
    chosen_features = mo.ui.multiselect(options = feature_options, value = ['VADER (sentence average)', 'AFINN average'], label = 'features:')
    chosen_features
    return (chosen_features,)


@app.cell
def _(
    LogisticRegression,
    StandardScaler,
    chosen_features,
    features_table,
    mo,
    test_positions,
    train_positions,
    y_test,
    y_train,
):
    # stop here if no features are chosen
    mo.stop(len(chosen_features.value) == 0, mo.md('**Choose at least one feature!**'))

    # only the chosen features, as lists of numbers
    chosen_rows = features_table.select(chosen_features.value).rows()
    lexicon_X_train = [chosen_rows[position] for position in train_positions]
    lexicon_X_test = [chosen_rows[position] for position in test_positions]

    # z-score, using the training data only
    lexicon_scaler = StandardScaler()
    lexicon_scaler.fit(lexicon_X_train)

    # train and test the classifier
    lexicon_classifier = LogisticRegression()
    lexicon_classifier.fit(lexicon_scaler.transform(lexicon_X_train), y_train)
    lexicon_predictions = lexicon_classifier.predict(lexicon_scaler.transform(lexicon_X_test))
    lexicon_accuracy = lexicon_classifier.score(lexicon_scaler.transform(lexicon_X_test), y_test)

    mo.md(f'### test accuracy: {round(lexicon_accuracy * 100, 1)}%')
    return lexicon_classifier, lexicon_predictions, lexicon_scaler


@app.cell
def _(chosen_features, lexicon_classifier, pl):
    # positive weights point towards satire, negative weights towards normal
    pl.DataFrame({'feature': chosen_features.value, 'weight': [round(weight, 2) for weight in lexicon_classifier.coef_[0]]}).sort('weight')
    return


@app.cell
def _(confusion_matrix, lexicon_predictions, pl, y_test):
    lexicon_matrix = confusion_matrix(y_test, lexicon_predictions, labels = ['normal', 'satire'])

    pl.DataFrame({
      'true label': ['normal', 'satire'],
      'predicted normal': [lexicon_matrix[0][0], lexicon_matrix[1][0]],
      'predicted satire': [lexicon_matrix[0][1], lexicon_matrix[1][1]],
    })
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - on their own, the sentiment features work best (AFINN average gets about 70%, VADER about 65%), followed by the proportion of *I / me / my* (about 61%); some features, like review length and frequency, are no better than the baseline on their own
    - using all of the lexicon features together gets a little over 70%, so more features don't always help much: many of the features carry similar information
    - the weights suggest satirical reviews are less positive, use more *I / me / my* (they tell a story about the "customer"), and use later-acquired, more concrete words
    - star rating is not a linguistic feature, and it only helps because of how this particular dataset was collected; including it would make the classifier less useful for other data
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: fool the classifier**

    Write your own review below, and give it a star rating. The classifier will guess whether it is satire or normal, using the features you chose in the first activity.

    Can you write a satirical review that the classifier thinks is normal? Can you write a real review that it thinks is satire? Try changing the features in the first activity, and see if the guess changes.
    """)
    return


@app.cell
def _(mo):
    my_review = mo.ui.text_area(value = 'I bought this kettle last month. It boils water quickly and is easy to clean. Great value for the price.', label = 'your review:', full_width = True, rows = 5)
    my_stars = mo.ui.slider(start = 1, stop = 5, value = 5, label = 'stars:')
    mo.vstack([my_review, my_stars])
    return my_review, my_stars


@app.cell
def _(
    chosen_features,
    lexicon_classifier,
    lexicon_scaler,
    mo,
    my_review,
    my_stars,
    review_features,
):
    # the lexicon classifier: describe the review with the chosen features
    my_features = review_features(my_review.value, my_stars.value)
    my_lexicon_row = [[my_features[feature] for feature in chosen_features.value]]
    my_lexicon_guess = lexicon_classifier.predict(lexicon_scaler.transform(my_lexicon_row))[0]

    mo.md(f'### the classifier thinks this review is: {my_lexicon_guess}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r'''
    # **Critical reflection**

    1. Our classifier does better than the baseline. Has it learned what satire *is*?
    2. What do you think would happen if we used this classifier on satirical reviews of new products, or on satire from somewhere else (e.g., news satire)?
    3. As a human reader, how do *you* recognise satire? Which of those clues could our features capture, and which could they not?
    4. Satire and humour can be hard for people to recognise too. What does it mean for a classifier to be "right" when people might disagree about whether something is satirical?
    '''), kind = 'info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - a classifier learns whatever patterns separate the labels in its training data, whether or not they are the patterns we care about; our features capture some traces of satire (e.g., less positive sentiment, more storytelling with *I*), but they don't capture what makes something satirical
    - on new products or other kinds of satire (e.g., news satire, which is not written in the first person), the patterns could be quite different, so the classifier would probably do worse
    - people use exaggeration, absurdity, mismatches between tone and content, knowledge of the world, and knowledge of the genre; word counts and lexicon averages only capture traces of these (e.g., less positive sentiment, more storytelling with *I*)
    - the labels in our data came from people, and recognising satire depends on knowledge, culture, and context; a classifier can only be as "right" as the labels it was trained on, and accuracy hides the cases where the labels themselves are debatable
    ''')})
    return


if __name__ == "__main__":
    app.run()
