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
    # **Emotional meaning from text data**

    Very similar to word sentiment is the idea that we can capture different emotional tones in a text. The logic is that people use certain words when discussing or expressing certain emotions, therefore counting these so-called emotion words in a text might tell us something about the emotional nature of that text.

    Therefore, emotion-based lexicons are similar to sentiment and other lexicon-based resources. Individual words are categorised for emotions using a variety of methods. In this notebook, we look at how some of these resources can be used.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import requests
    import polars as pl
    import nltk

    import os
    import warnings

    # on molab, hide NLTK's (harmless) warning about the download folder
    if os.path.expanduser('~') == '/home/marimo':
      warnings.filterwarnings('ignore', message = 'NLTK will not authorize')

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab'])
    return nltk, pl, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # The NRC Emotion Lexicon

    This resource is a bit different from some other lexicon dictionaries. Rather than there being a single value associated with each word, this resource is a series of words and whether or not they are associated with a particular emotion. The emotions measured for each word include:

    - anger
    - anticipation
    - disgust
    - fear
    - joy
    - negative
    - positive
    - sadness
    - surprise
    - trust

    The values associated with the words in the dictionary are a 0 or 1 for each of these emotions. A 0 means the word does not have an association, whereas a 1 means it does. So it is binary - either yes or no. With a resource like this, one could tally how many words with these associations a particular text has. Notice that it also has emotion for positive/negative, so in a way this can also be used as a sentiment analysis resource.

    This is just one of many resources provided [on this website.](https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm)

    Below I read in the resource and create a dictionary which can be used to analyse texts using the NRC Emotion lexicon.
    """)
    return


@app.cell
def _(requests):
    # get emotion resource and split on newlines
    emotion_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/emotion_lexicon.txt'
    raw_nrc_emotion = requests.get(emotion_url).text.split('\n')
    return (raw_nrc_emotion,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Looking at the structure of the file, we see that each word has a single row for each emotion and its rating, all separated by tab characters. So the structure for each row is `word \t emotion \t rating`
    """)
    return


@app.cell
def _(raw_nrc_emotion):
    raw_nrc_emotion[1000:1010]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We want to put this into a dictionary so it can be used to analyse text. This time, the *emotions* will be the keys, and the values will be the words associated with that emotion. Because we will be checking whether words are in these groups many times, I store the words in a `set()` rather than a list. Checking whether something is in a set is *much* faster than checking whether something is in a list.

    I loop through each row, split it on the tab characters, and if the rating is 1, I add the word to the set for that emotion. A `defaultdict(set)` means that each emotion starts as an empty set (remember `defaultdict` from the defaultdict notebook!).
    """)
    return


@app.cell
def _(raw_nrc_emotion):
    from collections import defaultdict

    nrc_emotion_dict = defaultdict(set)

    for row in raw_nrc_emotion:
      parts = row.split('\t')
      # only keep complete rows, where the word has this emotion
      if len(parts) == 3 and parts[2].strip() == '1':
        word, emotion, rating = parts
        nrc_emotion_dict[emotion].add(word)
    return (nrc_emotion_dict,)


@app.cell
def _(nrc_emotion_dict):
    # the emotions are the keys
    list(nrc_emotion_dict.keys())
    return


@app.cell
def _(nrc_emotion_dict):
    # how many words are associated with 'trust'?
    len(nrc_emotion_dict['trust'])
    return


@app.cell
def _(nrc_emotion_dict):
    # the first 25 words associated with "trust" (sorted alphabetically)
    sorted(nrc_emotion_dict['trust'])[:25]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we have a dictionary of emotions and words associated with that emotion. Using this dictionary we can profile some texts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Profiling the NRC values of a text

    How can we use this resource to develop a profile for a text? One strategy would be to tally the proportion of words which fit into each emotion, and provide that measure for a text (alongside coverage). I create such a function below.

    To calculate coverage, we need to know which words are in the lexicon *at all*. So first I make one big set of all the words in the lexicon, by looping through each emotion and using `.update()` to add all of its words to the set.
    """)
    return


@app.cell
def _(nrc_emotion_dict):
    # one set with every word that has at least one emotion
    nrc_all_words = set()

    for emotion_words in nrc_emotion_dict.values():
      nrc_all_words.update(emotion_words)

    len(nrc_all_words)
    return (nrc_all_words,)


@app.cell
def _(nltk, nrc_all_words):
    def profile_emotions(text, dictionary, show_vocab=False):
        """
        analyse emotional content of a text based on an emotion dictionary,
        and calculate the coverage of emotion-related words.

        Returns:
          output (dict): each emotion and the proportion of tokens associated with that emotion
          coverage (float): the proportion of tokens which are in the emotion dictionary
        """
        # lowercase and tokenize text, keeping only alphabetic tokens
        tokens = [token for token in nltk.word_tokenize(text.lower()) if token.isalpha()]

        # calculate the proportion of tokens in each emotion category
        output = {}
        for emotion in dictionary:
            emotion_tokens = [token for token in tokens if token in dictionary[emotion]]
            output[emotion] = round(len(emotion_tokens) / len(tokens), 2)

        # calculate coverage (how many words are actually in the dictionary)
        in_vocab = [token for token in tokens if token in nrc_all_words]
        coverage = round(len(in_vocab) / len(tokens), 2)

        if show_vocab == True:
            return output, coverage, in_vocab
        return output, coverage

    return (profile_emotions,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's try it out. We obtain results showing that 17% of the words in the following text are "negative". But we also see that coverage was very low. In fact, only one word was even counted (thirsty).
    """)
    return


@app.cell
def _(nrc_emotion_dict, profile_emotions):
    profile_emotions('these pretzels are making me thirsty', nrc_emotion_dict, show_vocab = True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's compare to a text which has higher coverage. Here we can see how words contribute to one or more categories.
    """)
    return


@app.cell
def _(nrc_emotion_dict, profile_emotions):
    profile_emotions('love hate hurt heal', nrc_emotion_dict, show_vocab = True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Valence, Arousal, Dominance (VAD)

    The VAD lexicon focuses on psychological constructs thought to represent larger categories in psychology. One such is the Valence, Arousal, and Dominance triad, which is thought to represent emotions which influence language processing (I am myself not totally sure how I feel about such claims, but it is interesting to think about). [One existing lexicon in English contains ratings of these features for over 13,000 English words.](https://link.springer.com/article/10.3758/s13428-012-0314-x)

    From the abstract:

    ```
    Valence (the pleasantness of a stimulus)
    Arousal (the intensity of emotion provoked by a stimulus)
    Dominance (the degree of control exerted by a stimulus)
    ```

    The VAD dictionary is different in that the words are provided ratings along a scale for each emotion, rather than the binary yes/no for each word. Let's load in the resource and create a dictionary.
    """)
    return


@app.cell
def _(requests):
    # VAD ratings
    vad_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/warriner_VAD.txt'
    raw_vad = requests.get(vad_url).text.split('\n')

    # the first row is the column names
    raw_vad[:3]
    return (raw_vad,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Create a dictionary which has words as keys, and another dictionary with the three ratings as the values. Convert the ratings to floats (decimals). I use `[1:]` to skip the first row, which has the column names.
    """)
    return


@app.cell
def _(raw_vad):
    vad_dict = {}

    for line in raw_vad[1:]:
      vad_parts = line.strip().split('\t') # .strip() removes any trailing spaces/newlines
      # only keep complete rows
      if len(vad_parts) == 4:
        vad_word, valence, arousal, dominance = vad_parts
        vad_dict[vad_word] = {'valence': float(valence), 'arousal': float(arousal), 'dominance': float(dominance)}
    return (vad_dict,)


@app.cell
def _(vad_dict):
    # look up some VAD values for these words
    vad_targets = ['fight', 'play', 'shout', 'clown', 'tornado']

    for vad_target in vad_targets:
      if vad_target in vad_dict:
        print(f'VAD values for {vad_target} are {vad_dict[vad_target]}')
      else:
        print(f'Sorry, {vad_target} not found')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Profiling the VAD ratings of a text

    Here I will create a function which provides average VAD ratings + coverage for an entire text. Just like in the lexical sophistication notebook, the function returns `None` for the averages if none of the words are in the lexicon, to avoid dividing by zero.
    """)
    return


@app.cell
def _(nltk):
    def vad_profile(text, dictionary):
      '''
      Calculates the average valence, arousal, and dominance scores of a text,
      plus the coverage of the dictionary.
      '''
      # lowercase and tokenize text, keeping only alphabetic tokens
      tokens = [token for token in nltk.word_tokenize(text.lower()) if token.isalpha()]

      # create empty containers to store our values
      v = []
      a = []
      d = []

      # look up each token in the dictionary
      for token in tokens:
        if token in dictionary:
          v.append(dictionary[token]['valence'])
          a.append(dictionary[token]['arousal'])
          d.append(dictionary[token]['dominance'])

      # avoid dividing by zero if no words were in the dictionary
      if len(v) == 0:
        return None, None, None, 0

      # calculate average scores, and round them
      v_average = round(sum(v) / len(v), 2)
      a_average = round(sum(a) / len(a), 2)
      d_average = round(sum(d) / len(d), 2)
      coverage = round(len(v) / len(tokens), 2)

      return v_average, a_average, d_average, coverage

    return (vad_profile,)


@app.cell
def _(vad_dict, vad_profile):
    vad_profile('love hate hurt heal', vad_dict)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Comparing texts**

    Let's try out these functions on multiple texts - comparing a *Seinfeld* episode, a Lorde song, and They're made out of meat
    """)
    return


@app.cell
def _(requests):
    mb = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/marine_biologist.txt').text
    mr = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/mood_ring.txt').text
    meat = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/refs/heads/main/resources/tmoom.txt').text

    texts = {'Marine Biologist': mb, 'Mood Ring': mr, 'tmoom' : meat}
    return mb, meat, mr, texts


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now I loop through the texts to get the VAD profile of each one, and put the results into a polars dataframe:
    """)
    return


@app.cell
def _(pl, texts, vad_dict, vad_profile):
    vad_rows = []

    for text_name in texts:
      v_text, a_text, d_text, coverage_text = vad_profile(texts[text_name], vad_dict)
      vad_rows.append({'text': text_name, 'valence': v_text, 'arousal': a_text, 'dominance': d_text, 'coverage': coverage_text})

    pl.DataFrame(vad_rows)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And the same for the NRC emotion profiles. This time I put the texts in the columns and the emotions in the rows, so that the two texts are easy to compare:
    """)
    return


@app.cell
def _(mb, meat, mr, nrc_emotion_dict, pl, profile_emotions):
    mb_emotions, mb_coverage, mb_words = profile_emotions(mb, nrc_emotion_dict, show_vocab=True)
    mr_emotions, mr_coverage, mr_words = profile_emotions(mr, nrc_emotion_dict, show_vocab=True)
    tmoom_emotions, tmoom_coverage, tmoom_words = profile_emotions(meat, nrc_emotion_dict, show_vocab=True)

    emotion_names = sorted(mb_emotions.keys())

    pl.DataFrame({
      'emotion': emotion_names + ['coverage'] + ['words'],
      'Marine Biologist': [mb_emotions[emotion] for emotion in emotion_names] + [mb_coverage] + [mb_words],
      'Mood Ring': [mr_emotions[emotion] for emotion in emotion_names] + [mr_coverage] + [mr_words],
        'Tmoom': [tmoom_emotions[emotion] for emotion in emotion_names] + [tmoom_coverage] + [tmoom_words],
    }, strict=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    - Which text has more positive emotion? More negative emotion? Does that match what you know (or can guess) about the texts?
    - Look at the words in each text which count towards a particular emotion (e.g., `fear`). Do they really express that emotion in the text?
    - Try the functions on some texts of your own, such as the Seinfeld scripts, the Brown categories, or the satirical Amazon reviews from the sentiment notebook.
    - The NRC lexicon was made by asking people whether a word is *associated* with an emotion. What is the difference between a word that is associated with an emotion, and a text that *expresses* that emotion?
    """)
    return


@app.cell
def _():
    # use this code cell to explore emotion lexicons!
    return


if __name__ == "__main__":
    app.run()
