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
    # **Sentiment Analysis**

    In its most basic form, sentiment analysis tries to measure the overall positivity and negativity from the tone of a text, with the idea that you are able to capture the opinion and/or mood of the author(s). You might also see this referred to as *valence* or *polarity*. The classic examples of sentiment analysis usually discuss how one can use sentiment analysis to detect overall negative versus positive tone in movie or product reviews.

    A lot of sentiment analysis libraries are rule-based, which means that the creator of the resources has spent time trying to program the best set of rules to analyse language for these features. And some are purely lexicon-based, which means they contain a dictionary of words mapped to sentiment values (just like the lexicons in the lexical sophistication notebook).

    ## Where does sentiment come from?

    Where does one obtain measures of positivity and negativity? In many cases the sentiment ratings are obtained from human perceptions of how positive or negative individual words are in isolation. These lexicons or wordlists will include high frequency content words (in particular adjectives, which should make sense), and store them in a manner where each word has a "score" indicating how positive or negative it is. These scores differ in how they are calculated - for instance someone could rate a word from 0 to 1, with 0 being negative and 1 being positive. Or one could use a Likert scale from 1 negative to 7 positive, or one could gather votes for whether a word is negative or positive from a variety of people and then let the feature with the most votes "win." The point is, there are a few different approaches to capturing these perceptions.

    ## Who is giving these ratings?

    Crowdsourcing is one method, where researchers can hire people on platforms such as Amazon Mechanical Turk to provide ratings for words. This allows for rapid and cheap data annotation (in fact Amazon Mechanical Turk has been called "artificial artificial intelligence" because so many annotation tasks were originally farmed out to workers on that platform). In this way, we can view the most simple form of sentiment analysis as a lexical resource, similar to the names corpus, the concreteness ratings, and a variety of other things we have already explored.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import io
    import zipfile
    import requests
    import polars as pl
    import nltk
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'vader_lexicon'])
    return SentimentIntensityAnalyzer, io, nltk, pl, requests, zipfile


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # AFINN Sentiment Lexicon

    Many sentiment lexicons are lists of words with scores. For example, I downloaded the [AFINN Sentiment Lexicon](http://www2.imm.dtu.dk/pubdb/pubs/6010-full.html). Inside the folder are three files: an older version of the list, a newer version of the list, and a README file explaining the resource. Here is the description from the README file:

    *AFINN is a list of English words rated for valence with an integer between minus five (negative) and plus five (positive). The words have been manually labeled by Finn Årup Nielsen in 2009-2011. The file is tab-separated. There are two versions.*

    *AFINN-111: Newest version with 2477 words and phrases.*

    *AFINN-96: 1468 unique words and phrases on 1480 lines. Note that there are 1480 lines, as some words are listed twice. The word list in not entirely in alphabetic ordering.*

    Let's play with the AFINN lexicon. I'll use the `requests` library to ask for the file via a URL.
    """)
    return


@app.cell
def _(requests):
    # save the URL as a string to a variable
    afinn_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/AFINN-111.txt'

    # call the url and ask for the .text
    AFINN = requests.get(afinn_url).text
    return (AFINN,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the AFINN file - it's literally a single string containing a word then a rating, but it also has the `\t` and `\n` characters in there, which mean TAB and NEWLINE, respectively.
    """)
    return


@app.cell
def _(AFINN):
    # just reading in AFINN gives us this, explore the first 500 characters
    AFINN[:500]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is the same structure as the lexicons in the lexical sophistication notebook: one word and one rating on each line, separated by a tab. So we can turn it into a dictionary in the same way. We split the text on newlines, then split each line on the tab character, and add the word and its rating to a dictionary. The ratings are whole numbers, so I convert them using `int()`.
    """)
    return


@app.cell
def _(AFINN):
    afinn_dict = {}

    for line in AFINN.split('\n'):
      pair = line.split('\t')
      # only keep lines with a word AND a rating
      if len(pair) == 2:
        afinn_dict[pair[0]] = int(pair[1])
    return (afinn_dict,)


@app.cell
def _(afinn_dict):
    # it works!
    afinn_dict['happy']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now start thinking about the values associated with the words. Remember, the author of AFINN has told us that words range from -5 (negative) to +5 (positive). Look at the examples I've chosen, do their ratings make sense to you? Also, the word "banana" is not in the lexicon – think about it for a second – does that make sense? What polarity would *you* assign to the word banana?
    """)
    return


@app.cell
def _(afinn_dict):
    # we can now look up words in the dictionary to get their ratings
    test_words = ['ironic', 'tired', 'happy', 'banana', 'alive', 'hurt']

    # loop through words, check if in dict, if so, print word and rating
    for test_word in test_words:
      if test_word in afinn_dict:
        print(test_word, afinn_dict[test_word])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you were to loop through the dictionary and search for words with a rating of negative 5, you will find some words which are offensive and vulgar. Of course, we have to remain somewhat dispassionate here, because we would expect these words to exist in natural language and thus attempt to account for them in any analysis of natural language. I'll leave it to you to write and execute such a loop, but fair warning you will see some words which might offend you.

    ```
    # print words with -5 or 5 as a rating
    for word in afinn_dict:
      if afinn_dict[word] == 5 or afinn_dict[word] == -5:
        print(word, afinn_dict[word])
    ```

    Instead, I'll pick out some of the less offensive words (at least, I think so!) and show you what counts as fully negative or fully positive. There are actually fewer than 20 words with such extreme ratings.
    """)
    return


@app.cell
def _(afinn_dict):
    # these words have a -5 or +5 rating
    extreme_words = ['bastard', 'twat', 'superb', 'thrilled']

    for extreme_word in extreme_words:
      print(extreme_word, afinn_dict[extreme_word])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Using the AFINN sentiment scores

    Let's see how one could use this resource, and whether or not the output makes sense.

    Let's start with two extremely different sentences which we would expect to be very negative or very positive.
    """)
    return


@app.cell
def _():
    positive_sentence = 'That meal was excellent.'
    negative_sentence = 'That meal was awful.'
    return negative_sentence, positive_sentence


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's write a function which will look up the sentiment of each word in the sentence, and then average those values. This should give us the average sentiment for each sentence. The function also calculates the **coverage** (the proportion of tokens which were found in the lexicon), just like in the lexical sophistication notebook.

    The function has a second argument, `sentiment_dict`, so that we can use it with *any* sentiment lexicon, not just AFINN. And remember the division by zero problem from the lexical sophistication notebook? If none of the words are in the lexicon, the function returns `None` instead of crashing.
    """)
    return


@app.cell
def _(nltk):
    def sentiment_lookup(text, sentiment_dict):
      '''calculates average sentiment and coverage for a given string'''

      # tokenise a lower-cased version of our text
      tokens = nltk.word_tokenize(text.lower())

      # initialise empty output to store sentiment ratings
      output = []

      for token in tokens:
        # first check if the token is even in the dictionary
        if token in sentiment_dict:
          # add the rating to the output if so
          output.append(sentiment_dict[token])

      # avoid dividing by zero if no words were in the dictionary
      if len(output) == 0:
        return None, 0

      # we calculate the average sentiment of the text from all the values in our output
      average_sentiment = round(sum(output) / len(output), 2)

      # coverage: how many of the tokens were actually used in the calculation?
      coverage = round(len(output) / len(tokens), 2)

      return average_sentiment, coverage

    return (sentiment_lookup,)


@app.cell
def _(afinn_dict, positive_sentence, sentiment_lookup):
    # calculate the average & coverage of the positive sentence
    sentiment_lookup(positive_sentence, afinn_dict)
    return


@app.cell
def _(afinn_dict, negative_sentence, sentiment_lookup):
    # calculate the average & coverage of the negative sentence
    sentiment_lookup(negative_sentence, afinn_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Seems to be working, however, you probably have realised that these "average" values are actually only taking sentiment from one word in each sentence. The function skips the words `that meal was` because none of those words were in `afinn_dict`. This is an issue related to **coverage** – the performance of a parser or lexical resource is largely dependent upon how much of the text can actually be analysed. In the two examples above, our resource only provided coverage over 20% of each text.

    Keep in mind, punctuation is still counted in those tokens, so our coverage will also be slightly different depending upon how we deal with punctuation.

    Let's see what happens if we combine our sentences. If we join our sentences (with a space in between), we see that the calculations are still based on the same 2 words, this is still 20% of the text, but our text's sentiment is now 0. This is because the -3 rating of `awful` and the +3 rating of `excellent` are summing to zero.

    So, in this sense, a "neutral" text is simply a text which does not have a strong tendency towards positive or negative, but we can clearly see that there exists both positive and negative sentiment in the text!
    """)
    return


@app.cell
def _(afinn_dict, negative_sentence, positive_sentence, sentiment_lookup):
    # the positive and negative words cancel each other out
    sentiment_lookup(positive_sentence + ' ' + negative_sentence, afinn_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's look at a larger text to see if adding words helps here.

    This text is a satirical story from *The Civilian*, a New Zealand satirical newspaper.
    """)
    return


@app.cell
def _():
    xmas_threat = '''While Auckland prepares to move to Alert Level 3 on Wednesday,
    New Zealanders in the fun part of the country have been wondering when they might see a drop down to Level 1,
    given the persistent lack of Covid cases since the outbreak.
    But the Government isn't currently considering any such plans,
    and Prime Minister Jacinda Ardern poured cold water on the idea at today's post-Cabinet press conference,
    reiterating that Level 2 may last for “some time”
    and that a move to Level 1 won't be considered for at least as long as there remains
    a threat that organisers decide to go ahead with annual kids' concert Christmas in the Park.
    '''
    return (xmas_threat,)


@app.cell
def _(afinn_dict, sentiment_lookup, xmas_threat):
    sentiment_lookup(xmas_threat, afinn_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ok, so our results are saying that, on average, this text is more negative than positive (because a neutral text would have a rating of 0). At the same time, the entire sentiment of the text is based on only a handful of words — we can check which words those are:
    """)
    return


@app.cell
def _(afinn_dict, nltk, xmas_threat):
    # let's scrutinise the exact words being used for the calculations here.
    for xmas_word in nltk.word_tokenize(xmas_threat.lower()):
      if xmas_word in afinn_dict:
        print(xmas_word, afinn_dict[xmas_word])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Identifying the limitations of a lexicon-based approach

    Ok, so we see that the overall sentiment in that text is dictated by the average sentiment of `alert, fun, drop, lack, threat`. We see the same problem here that occurred above — the sentiment of the text is being driven by a very small number of words.

    While it does make sense that specific words, namely **content** words such as adjectives, adverbs, verbs, and nouns are doing the heavy lifting to colour the overall sentiment of a text, it's a bit frustrating to see so few words being included in the lookup lexicon. This is again a matter of coverage and a limitation of any lexicon-based approach.

    These results also identify a second problem with a lexicon-based approach. Each word is being treated in isolation, without consideration of the words that come before or after. A single word can take on possible different meanings and senses, and knowing which meaning/sense/part of speech is intended relies on knowing how the word is *used* - how it patterns with *other* words (remember Firth from the collocations notebook!). Our sentiment lexicon does not capture this.

    For example, look at that sentence which contains the word `lack`:

    `given the persistent lack of Covid cases since the outbreak.`

    Is this sentence negative? One would think not, a *lack* of COVID cases is probably an overall *good* thing (unless someone doubts the authenticity of such a report, but let's just keep it simple for now). So, while the decontextualised meaning of `lack` is more or less negative (although even that is debatable), we see that it is referring to the lack of *something bad* -- which we might want to reasonably argue is a good thing. This, hopefully, is starting to show you that word-based lexicons must be carefully used and interpreted, because words do not create meaning on their own...their meaning is also dependent upon the ways they are used with other words.

    This further demonstrates the limitations of using a lookup approach like this. That does not mean that this is a terrible approach to use, but rather we must be careful with such an approach. Certain texts will be more suitable for this type of analysis, and parsers with better rules will also help.

    To finalise this point a bit more, also consider the topic of negation in English. Saying that something is *not* good means that it is bad. And saying something is "not bad" usually means that it is at least good, right? The AFINN dictionary cannot take this information into account:
    """)
    return


@app.cell
def _(afinn_dict, sentiment_lookup):
    # something that is not terrible should be good?
    sentiment_lookup('This is not terrible', afinn_dict)
    return


@app.cell
def _(afinn_dict, sentiment_lookup):
    # something that is not superb should be bad?
    sentiment_lookup('this is not superb', afinn_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    How could we resolve this? We could write a new set of rules which looks for negation words before our sentiment words. This sort of approach and the limitations of existing sentiment libraries such as AFINN and many others is what prompted CJ Hutto to make a better rule-based sentiment library named VADER.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sentiment Analysis with VADER

    VADER (Valence Aware Dictionary for sEntiment Reasoning) was created to address the shortcomings with some of the lexicon approaches to sentiment analysis. If you read or even skimmed the paper and other links associated with VADER, you can see the author provides a rationale for why VADER is "better," even though VADER is still rule-based!

    The author of VADER incorporated information from a variety of prior sentiment dictionaries, and then also thought about features such as capitalisation, emoticons, non-standard words, negation, and a variety of other ways that people actually *use* language.

    And, VADER is relatively simple to use in NLTK. We already downloaded the `vader_lexicon` resource at the start of the notebook, so now we create a sentiment analyser and save it to a variable name.
    """)
    return


@app.cell
def _(SentimentIntensityAnalyzer):
    # create a vader sentiment analyser and save it to the variable `vader`
    vader = SentimentIntensityAnalyzer()
    return (vader,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We are interested primarily in two things from the `vader` object:

    - `lexicon`
    - `polarity_scores`

    Let's peek at the `lexicon` part of this. It's another dictionary with valence ratings for individual words.
    """)
    return


@app.cell
def _(vader):
    # the lexicon is a dictionary!
    type(vader.lexicon)
    return


@app.cell
def _(vader):
    # words have valence measures just like the AFINN dictionary.
    vader.lexicon['irony']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, we could simply use this lexicon in the same way that we did for AFINN above. Because our `sentiment_lookup()` function can take any dictionary, we can give it the VADER lexicon instead. Let's check out how well this VADER dictionary does on our xmas threat text, and compare it to AFINN.
    """)
    return


@app.cell
def _(afinn_dict, sentiment_lookup, xmas_threat):
    # using AFINN lexicon
    sentiment_lookup(xmas_threat, afinn_dict)
    return


@app.cell
def _(sentiment_lookup, vader, xmas_threat):
    # using VADER lexicon
    sentiment_lookup(xmas_threat, vader.lexicon)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Interesting! Both dictionaries have the same coverage, but we get different scores (although both are negative). Let's again scrutinise what words are contributing here.
    """)
    return


@app.cell
def _(afinn_dict, nltk, xmas_threat):
    # afinn
    for afinn_word in nltk.word_tokenize(xmas_threat.lower()):
      if afinn_word in afinn_dict:
        print(afinn_word, afinn_dict[afinn_word])
    return


@app.cell
def _(nltk, vader, xmas_threat):
    # vader
    for vader_word in nltk.word_tokenize(xmas_threat.lower()):
      if vader_word in vader.lexicon:
        print(vader_word, vader.lexicon[vader_word])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Welp, looks like they are *the exact same words*, but the values are different. This is because VADER was initially created by looking up the previous sentiment dictionaries and tweaking the values based on an assessment of prior dictionaries and lexical resources as well as human annotation. So the hard-coded sentiments in VADER are "better" in some regard. But that's not the only improvement VADER has made. There are a number of additional rules that VADER considers in order to consider the ways words are being used to calculate their sentiment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## VADER is more than a lookup dictionary

    Above I used VADER as a lookup dictionary the exact same way as AFINN. But, VADER is more than a lookup dictionary. VADER also has a bunch of other rules which are part of its scoring algorithm that take into account the contexts words appear in. You can scan the [rules here](https://www.nltk.org/_modules/nltk/sentiment/vader.html). You'll see certain rules, such as declaring certain words as intensifiers and also taking negation into account.

    To get the *real* polarity scores, you use the main VADER function, `polarity_scores`, to obtain sentiment scores that have taken these additional rules into account. The function will return a set of values: `neg`, `neu`, `pos`, and `compound`.

    VADER takes into account various punctuation and capitalisation features, which means we actually want to pass raw strings to VADER.

    > `vader.polarity_scores('string input')`
    """)
    return


@app.cell
def _(vader):
    vader.polarity_scores("You can't beat Wellington on a good day.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Consider how two additions change the ratings (an intensifier and an exclamation point):
    """)
    return


@app.cell
def _(vader):
    vader.polarity_scores("You can't friggen beat Wellington on a good day!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Understanding VADER output

    The output in the examples above have a "negative" score, a "neutral" score, and a "positive" score. For both texts, the negative score is 0, the neutral score is the highest, and the positive score is about .3. This suggests both versions of the statement are not negative, but more neutral or positive. However, the value we *really* care about is the "compound" score which takes into account a variety of extra rules the author of VADER has incorporated into the program. You can find the scoring system [here](https://github.com/cjhutto/vaderSentiment#about-the-scoring), which says that:

    "*The compound score is computed by summing the valence scores of each word in the lexicon, adjusted according to the rules, and then normalized to be between -1 (most extreme negative) and +1 (most extreme positive). This is the most useful metric if you want a single unidimensional measure of sentiment for a given sentence. Calling it a 'normalized, weighted composite score' is accurate.*"

    The following guidelines apply to the compound score:

    * positive sentiment: compound score >= 0.05
    * neutral sentiment: (compound score > -0.05) and (compound score < 0.05)
    * negative sentiment: compound score <= -0.05

    So, the above sentiment is best seen in the compound scores for the sentences of .44/.49, suggesting they are both overall positive. Do you agree?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## VADER and negation

    We saw above that the inclusion of the word `friggen` and the use of an exclamation mark enhanced the positivity of the sentence. Another thing VADER takes into account is negation:
    """)
    return


@app.cell
def _(vader):
    # happy is being negated, so it should be negative
    vader.polarity_scores('I am not happy')
    return


@app.cell
def _(vader):
    # no negation, so happy should be positive.
    vader.polarity_scores('I am happy')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Just to remind you, look how poorly the AFINN dictionary performs using basic look up and averaging. It says this sentence is *positive* because it is naively looking at the word `happy` and not considering the surrounding words. Clearly, VADER is providing a better understanding of the sentiment in the sentence.
    """)
    return


@app.cell
def _(afinn_dict, sentiment_lookup):
    # compare the "negated" sentence with AFINN
    sentiment_lookup('I am not happy', afinn_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## VADER and emoticons

    VADER also has some support for parsing the sentiment of emoticons (what we called them before they became emoji). Look how the frowny face makes the word "Thanks" neutral, whereas the happy face makes "Thanks" more positive than just "Thanks" alone.
    """)
    return


@app.cell
def _(vader):
    # explore how emoticons are parsed by VADER
    thanks = ['Thanks', 'Thanks :(',  'Thanks :)']

    for thank in thanks:
      print(f'Score for {thank} is: {vader.polarity_scores(thank)}')
    return


@app.cell
def _(vader):
    # basically, the emoticons are just more words with their own valence
    emoticons = [':)', ':(', ':D']
    for emoticon in emoticons:
      print(emoticon, vader.lexicon[emoticon])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## VADER and sarcasm

    So VADER can handle negation, intensifiers, punctuation, and emoticons. What about sarcasm? Each of the sentences below would normally be said by someone who is *not* happy. What does VADER think?
    """)
    return


@app.cell
def _(vader):
    sarcastic_sentences = [
      'Oh great, another Monday.',
      'I just love waiting on hold for an hour.',
      'Wow, what a fantastic idea to cancel the bus.',
      'Thanks a lot for nothing.',
    ]

    for sarcastic_sentence in sarcastic_sentences:
      print(sarcastic_sentence, vader.polarity_scores(sarcastic_sentence)['compound'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    VADER says all of these are positive! The positive words (*great*, *love*, *fantastic*, *thanks*) are doing all of the work, because VADER has no way of knowing that the speaker means the *opposite* of what they are saying. Understanding sarcasm requires knowing about the context, the speaker, and what they probably think about Mondays, waiting on hold, and cancelled buses - none of which is in the words themselves.

    This is a well-known problem for sentiment analysis, and more generally for any method that works at the level of words. Non-literal language (sarcasm, irony, satire, humour, metaphor) is where these methods tend to break down.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Sentiment and satire

    We can see a similar problem with satire. Satirical text is far more complex in meaning, with hidden and subtle critiques that might use irony - but we actually do not have a good idea how it will look with sentiment.

    In the course repository there is a corpus of Amazon product reviews, where half of the reviews are real ("normal") and half of the reviews are satirical. Each file name tells us whether the review is normal or satirical (and how many stars the reviewer gave the product).

    Let's download the reviews using the same `download_corpus()` function from the corpora notebook, and look at a few:
    """)
    return


@app.cell
def _(io, requests, zipfile):
    def download_corpus(url, folder):
      # download the zip file and unzip everything into the folder
      response = requests.get(url)
      zip_file = zipfile.ZipFile(io.BytesIO(response.content))
      zip_file.extractall(folder)
      return folder

    reviews_folder = download_corpus('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/amazon%20reviews.zip', 'amazon reviews')
    return (reviews_folder,)


@app.cell
def _(reviews_folder):
    # a satirical review of a banana slicer
    with open(reviews_folder + '/001-5-satire.txt', encoding = 'utf-8') as satire_file:
      satire_example = satire_file.read()

    satire_example
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's compare the VADER compound scores of three satirical reviews and three normal reviews. All of these reviewers gave the product 4 or 5 stars (that's the number in the middle of the file name).
    """)
    return


@app.cell
def _(pl, reviews_folder, vader):
    review_files = ['001-5-satire.txt', '010-5-satire.txt', '228-4-satire.txt', '001-5-normal.txt', '010-5-normal.txt', '239-4-normal.txt']

    review_scores = []

    for review_file in review_files:
      with open(reviews_folder + '/' + review_file, encoding = 'utf-8') as review_handle:
        review_text = review_handle.read()
      review_scores.append(vader.polarity_scores(review_text)['compound'])

    pl.DataFrame({'review': review_files, 'compound': review_scores})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The normal reviews are all very positive, which makes sense for 4 and 5 star reviews. But the satirical reviews are all over the place, even though they also gave the products 4 or 5 stars! Could the sentiment of a review help a computer tell satire apart from real reviews? We will come back to this question in the classification notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## VADER and long texts

    VADER was intended to be used on short texts, such as social media posts and other similar types of data. Running VADER on very long texts usually results in poor performance. Look at the compound score for the first normal review, which is over 1,000 words long:
    """)
    return


@app.cell
def _(reviews_folder, vader):
    with open(reviews_folder + '/001-5-normal.txt', encoding = 'utf-8') as long_file:
      long_review = long_file.read()

    print(len(long_review.split()), 'words')
    vader.polarity_scores(long_review)
    return (long_review,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The compound score is almost exactly 1, which is the maximum! This happens because the compound score adds up the sentiment of *all* the words in the text before squashing it between -1 and 1. In a long text, the sum gets so big that almost any text ends up near -1 or 1.

    One way to address this is to split the text into sentences, get the compound score for each sentence, and then average the sentence scores:
    """)
    return


@app.cell
def _(long_review, nltk, vader):
    sentence_scores = []

    for review_sentence in nltk.sent_tokenize(long_review):
      sentence_scores.append(vader.polarity_scores(review_sentence)['compound'])

    # the average sentence score
    round(sum(sentence_scores) / len(sentence_scores), 3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The average sentence is only a little bit positive. Which number do you think describes the review better?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Adding new words to VADER

    Because the VADER lexicon is a Python dictionary, we can update the dictionary if we want to add new words which don't exist in the VADER lexicon.

    Changing the lexicon of our `vader` analyser would change the results of all of the cells above if we ran them again (and marimo would not know to re-run them!). So I make a *second* analyser to play with, called `vader2`. Each analyser has its own copy of the lexicon, so changing `vader2` will not change `vader`.
    """)
    return


@app.cell
def _(SentimentIntensityAnalyzer):
    # a second analyser, so that we can change its lexicon without changing the first one
    vader2 = SentimentIntensityAnalyzer()

    # find a word not in the vader lexicon
    'blarged' in vader2.lexicon
    return (vader2,)


@app.cell
def _(vader2):
    # there is effectively nothing to measure here, 'blarged' was probably identified as neutral because it is not in the dictionary.
    vader2.polarity_scores('I really blarged that one up.')
    return


@app.cell
def _(vader2):
    # let's pretend blarged is negative
    vader2.lexicon['blarged'] = -4

    # our new word is in there with a very negative rating :)
    vader2.polarity_scores('I really blarged that one up.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You could even overwrite the sentiment values for existing words in the dictionary. Maybe we think the word `happy` is actually negative:
    """)
    return


@app.cell
def _(vader, vader2):
    # let's make happy negative!
    vader2.lexicon['happy'] = -2

    # ultimate power over our words!!
    print('vader:', vader.polarity_scores('happy'))
    print('vader2:', vader2.polarity_scores('happy'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **The point**

    Sentiment analysis can be pretty bad when used naively. Averaging single word counts of valence/polarity is probably not a good method, but with larger texts some of that noise might wash out. However, fortunately we have VADER which is a much smarter sentiment tool, even if it is rule-based. But even VADER struggles with sarcasm, satire, and long texts.

    Importantly, VADER will perform its own tokenisation, so we have the luxury of passing raw strings to VADER, rather than needing to preprocess text.

    ### **Your Turn**

    - Write some sentences of your own which you think VADER will get wrong. Why does it get them wrong?
    - Compare the AFINN and VADER lexicons on some of your own texts, or on some of the Brown categories.
    - Look at some more of the Amazon reviews. Do you think sentiment could help a computer tell the satirical reviews apart from the normal reviews?
    """)
    return


@app.cell
def _():
    # use this code cell to explore sentiment!
    return


if __name__ == "__main__":
    app.run()
