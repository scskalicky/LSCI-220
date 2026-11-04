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
    # **Text readability**

    What makes a text more or less difficult to read? Lexical profiles of sophistication and other metrics are one way to measure this. Knowing the difficulty level of a text means that teachers and educators can select texts and readings most appropriate for a particular reading population. These considerations can be made based on grade level (e.g., primary vs. high school), but also language knowledge (e.g., first language vs. second language speakers).

    For several decades now, researchers and scientists have been developing **readability formulas** for the automatic assessment of text readability. The most well-known readability formulas are probably the Flesch-Kincaid formulas. In fact, if you have ever used Microsoft Word, the software includes this formula as a way to assess the overall difficulty of a text. There are a number of other formulas, such as Dale-Chall and the Gunning Fog Index. [If you are interested, you can read all about the different formulas on *Wikipedia*.](https://en.wikipedia.org/wiki/Readability)

    These formulas have been used in many applications, and are generally accepted to be valid measures of text readability. However, these formulas have also come under criticism because they do not capture cognitive aspects of the reading process. Some of my own research has been working with teams to develop new readability formulas that might better model the reading process. [You can read about this topic in detail in one of our first articles on this topic.](https://www.tandfonline.com/doi/full/10.1080/0163853X.2017.1296264) However, some of our other research suggests that sometimes the [older readability formulas can function just as well to predict text readability.](https://onlinelibrary.wiley.com/doi/full/10.1111/1467-9817.12283)

    While work continues to develop in this area, we can take this opportunity to calculate some of these classic readability metrics in Python. We will start with Flesch-Kincaid readability formulas.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import random
    import requests
    import nltk
    from nltk.corpus import cmudict

    # download the NLTK resources for this notebook
    nltk.download(['punkt_tab', 'cmudict'])
    return cmudict, nltk, random, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Flesch-Kincaid**

    There are two [Flesch-Kincaid formulas](https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests): reading ease, and grade level. What do the formulas calculate? *Wikipedia* gives us these formulas:

    **Flesch Reading Ease**

    $$
    \text{Flesch Reading Ease} = 206.835 - (1.015 \times \frac{\text{total words}}{\text{total sentences}}) - (84.6 \times \frac{\text{total syllables}}{\text{total words}})
    $$

    **Flesch-Kincaid Grade Level**

    $$
    \text{Flesch-Kincaid Grade Level} = (0.39 \times \frac{\text{total words}}{\text{total sentences}}) + (11.8 \times \frac{\text{total syllables}}{\text{total words}}) - 15.59
    $$

    We can see that these measures are really not that complicated. The main things we need to calculate are the total number of words and sentences in a text, plus the total number of syllables. We already know that getting the words and sentences in a text is quite easy, using `nltk.word_tokenize()` and `nltk.sent_tokenize()`. The one new measure here that we need to grapple with is measuring the syllables in a word. First of all - let's make sure we understand what a syllable is. Here is the definition from Google dictionary:

    > a unit of pronunciation having one vowel sound, with or without surrounding consonants, forming the whole or a part of a word; for example, there are two syllables in water and three in inferno.

    The crucial part of this definition is that a syllable is associated with a vowel *sound*. Well, most of the analyses we have been doing do not really take into account *sounds*, but we can at least identify vowels in a language. So, can we write a function to identify syllables in an English word?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Hunting syllables**

    Is finding the syllables in a word as simple as counting the number of vowels? Let's try some examples. First let's make a function which just equates the number of vowels with the number of syllables.
    """)
    return


@app.function
def syllable_v1(word):
  vowels = 'aieouy'
  vowel_count = 0
  for char in word.lower():
    if char in vowels:
      vowel_count += 1
  return vowel_count


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's test this function out.
    """)
    return


@app.cell
def _():
    syllable_v1('cat')
    return


@app.cell
def _():
    syllable_v1('banana')
    return


@app.cell
def _():
    syllable_v1('ate')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The function seems to work fine so far, at least until we find words such as `ate`, which are one syllable but contain two vowels. Clearly, this correspondence between number of vowels and syllables doesn't work. We actually knew this from the start, because a syllable is associated with a vowel ***sound***, not a written vowel. Drat!

    If only there was an existing resource which measured the *sounds* of text input. And of course, there is, and it exists within NLTK - the CMU Pronunciation Dictionary! Let's load that resource in and learn what it does.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **CMU pronunciation dictionary**

    The CMU dictionary has been used for speech recognition, speech processing, etc, and attempts to encode the audible properties of language. CMU = Carnegie Mellon University in the USA. I suggest you take a look at the [CMU dictionary website](http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=C+M+U+Dictionary) so you understand how the dictionary works, and [the link to ARPABET](https://en.wikipedia.org/wiki/ARPABET) is also useful.

    The structure of the CMU dictionary is in the form of `(word, [sound1, sound2, ...])`. So when accessing any one item within the CMU dictionary, you need to know how to access both parts of a single entry. The [NLTK Book explains how to do this](https://www.nltk.org/book/ch02.html).
    """)
    return


@app.cell
def _(cmudict):
    # create a CMU dictionary object
    cmu = cmudict.dict()
    return (cmu,)


@app.cell
def _(cmudict):
    # inspect some entries to get an idea for them
    cmu_entries = cmudict.entries()

    for entry in cmu_entries[42371:42379]:
      print(entry)
    return (cmu_entries,)


@app.cell
def _(cmu_entries):
    # I found dog!
    for dog_entry in cmu_entries[33325:33335]:
      print(dog_entry)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, the CMU codes which have both letters and numbers indicate syllable stress - which means these are syllables! Look at the output for these words: do you see the syllables?
    """)
    return


@app.cell
def _(cmu):
    cmu['ate']
    return


@app.cell
def _(cmu):
    cmu['banana']
    return


@app.cell
def _(cmu):
    cmu['victoria']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If we look at the output, we can see that the vowel sounds all have a number in their output (the number shows the type of stress). So, we could count the number of times such sounds occur in the entry for any one word, and in turn get a good approximation for the number of syllables in a word. Because words can have more than one possible pronunciation, each word has these pronunciations stored as a list of lists. So, we will simplify this problem by always choosing the first list from any entry using indexing `[0]`.

    There are various ways to count if the sound has a number in it. The way that pops up when you search for this question is to slice the last part of each sound and check if that part is a digit using `.isdigit()`. I follow that approach in the function below.
    """)
    return


@app.cell
def _(cmu):
    def count_syllables(word):

      if word in cmu:
        # get the entry from the dictionary, and index the first set of sounds
        phones = cmu[word][0]

        # using a list comprehension, extract only the sounds that end in a digit
        vowel_sounds = [sound for sound in phones if sound[-1].isdigit()]

        # the number of syllables is equal to the number of vowel_sounds
        return len(vowel_sounds)
      else:
        print(f'sorry, {word} is not in the CMU Pronunciation Dictionary')
        return 0

    return (count_syllables,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Test this function on our words:
    """)
    return


@app.cell
def _(count_syllables):
    count_syllables('ear')
    return


@app.cell
def _(count_syllables):
    count_syllables('syllable')
    return


@app.cell
def _(count_syllables):
    count_syllables('extraordinary')
    return


@app.cell
def _(count_syllables):
    count_syllables('hairy')
    return


@app.cell
def _(count_syllables):
    # darn, this word isn't in the dictionary.
    count_syllables('associational')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The problem, of course, is what can we do with words that are not in the CMU Dictionary? It turns out that computationally counting the sounds in a word based on the *spelling* in English is a difficult task. [Look at the discussion here](https://stackoverflow.com/questions/405161/detecting-syllables-in-a-word) and you will see various attempts using regular expressions as well as the CMU dictionary.

    One common fallback is to go back to counting vowels, but to count *groups* of vowels rather than every single vowel. This means words like `heel` or `ear` only get counted once for their `ee` and `ea`. The function below uses the CMU dictionary when it can, and the vowel group rule when it can't.

    Can you understand the code in the `else` part? It keeps track of whether the previous character was a vowel, and only adds a syllable when a *new* group of vowels starts.
    """)
    return


@app.cell
def _(cmu):
    def count_syllables2(word):

      if word in cmu:
        # get the entry from the dictionary, and index the first set of sounds
        phones = cmu[word][0]

        # using a list comprehension, extract only the sounds that end in a digit
        vowel_sounds = [sound for sound in phones if sound[-1].isdigit()]

        # the number of syllables is equal to the number of vowel_sounds
        syllables = len(vowel_sounds)

      else:
        # if the word is not found in the dictionary, count the groups of vowels
        vowels = 'aeiouy'
        syllables = 0
        previous_char_is_vowel = False
        for char in word:
          if char in vowels:
            # only count this vowel if the previous character was not a vowel
            if previous_char_is_vowel == False:
              syllables += 1
            previous_char_is_vowel = True
          else:
            previous_char_is_vowel = False

      return syllables

    return (count_syllables2,)


@app.cell
def _(count_syllables2):
    # this one is in the CMU dictionary
    count_syllables2('ear')
    return


@app.cell
def _(count_syllables2):
    # seems to perform okay on unseen words.
    count_syllables2('associational')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Back to Flesch Kincaid and readability**

    Well, after sorting out the syllable issue, we can now start to calculate readability metrics for our text input.

    Let's start by building a function which will calculate the basic information we need:

    1. The total number of words in a text
    2. The total number of sentences in a text
    3. The total number of syllables in a text
    4. The total number of *complex* words in a text (words with three or more syllables). We don't need this for Flesch-Kincaid, but we will need it for another formula below.
    """)
    return


@app.cell
def _(count_syllables2, nltk):
    def text_info(text):

      # lowercase the text
      text = text.lower()

      # extract tokens, removing any that are just punctuation
      tokens = [token for token in nltk.word_tokenize(text) if token.isalpha()]

      # extract sentences
      sentences = nltk.sent_tokenize(text)

      # count syllables and complex words
      syllables = 0
      complex_words = 0

      for token in tokens:
        token_syllables = count_syllables2(token)
        syllables += token_syllables
        if token_syllables > 2:
          complex_words += 1

      return len(tokens), len(sentences), syllables, complex_words

    return (text_info,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read in some texts to test out the function. The first text is a short science fiction story made up almost entirely of dialogue (*They're Made Out of Meat*), and the second is an article about satire.
    """)
    return


@app.cell
def _(requests):
    tmoom = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/tmoom.txt').text
    conversation = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/conversation_satire.txt').text
    return conversation, tmoom


@app.cell
def _(text_info, tmoom):
    # words, sentences, syllables, and complex words
    text_info(tmoom)
    return


@app.cell
def _(conversation, text_info):
    text_info(conversation)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Flesch Reading Ease Function**

    Now that we can extract the necessary information, we can develop functions to calculate the different readability metrics. A *higher* reading ease score means that a text is *easier* to read.
    """)
    return


@app.cell
def _(text_info):
    def flesch_reading_ease(text):
      '''
      calculate Flesch Reading Ease
      206.835 - 1.015(total words / total sentences) - 84.6(total syllables / total words)
      '''
      words, sentences, syllables, complex_words = text_info(text)

      words_per_sentence = words / sentences
      syllables_per_word = syllables / words

      return 206.835 - (1.015 * words_per_sentence) - (84.6 * syllables_per_word)

    return (flesch_reading_ease,)


@app.cell
def _(flesch_reading_ease, tmoom):
    # a high score means that the text is highly readable.
    flesch_reading_ease(tmoom)
    return


@app.cell
def _(conversation, flesch_reading_ease):
    # a lower score means it is less readable.
    flesch_reading_ease(conversation)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Flesch-Kincaid Grade Level**

    It should be relatively simple to now create the other formula to calculate the Flesch-Kincaid Grade Level. [We can find at least one resource explaining the scales here.](https://readable.com/readability/flesch-reading-ease-flesch-kincaid-grade-level/) The "grades" are school grades in the USA.
    """)
    return


@app.cell
def _(text_info):
    def flesch_grade_level(text):
      '''
      calculate Flesch-Kincaid grade level
      0.39 * (total words / total sentences) + 11.8 * (total syllables / total words) - 15.59
      '''
      words, sentences, syllables, complex_words = text_info(text)

      words_per_sentence = words / sentences
      syllables_per_word = syllables / words

      return (0.39 * words_per_sentence) + (11.8 * syllables_per_word) - 15.59

    return (flesch_grade_level,)


@app.cell
def _(flesch_grade_level, tmoom):
    # a low grade means this text is appropriate for beginning readers
    flesch_grade_level(tmoom)
    return


@app.cell
def _(conversation, flesch_grade_level):
    # a higher grade means this text is for more skilled readers
    flesch_grade_level(conversation)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Gunning Fog Readability**

    Another of the many formulas is Gunning Fog. I chose this because it is relatively simple to calculate:

    $$
    \text{Gunning Fog Index} = 0.4 \times \left( \frac{\text{total words}}{\text{total sentences}} + 100 \times \frac{\text{complex words}}{\text{total words}} \right)
    $$

    In this formula, a complex word is a word that contains three or more syllables (and also does not count proper names, compound words, and some other exceptions we will ignore for now). This is why our `text_info()` function also counts the complex words.
    """)
    return


@app.cell
def _(text_info):
    def gunning_fog(text):
      '''
      calculate Gunning Fog
      0.4 * ((words / sentences) + 100 * (complex words / words))
      '''
      words, sentences, syllables, complex_words = text_info(text)

      words_per_sentence = words / sentences
      complex_per_word = complex_words / words

      return 0.4 * (words_per_sentence + (complex_per_word * 100))

    return (gunning_fog,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is the Gunning Fog score interpretation (again using grades from the USA). What do you think?

    Fog Index|Reading level by grade
    :-:|:-:
    17|	College graduate
    16|	College senior
    15|	College junior
    14|	College sophomore
    13|	College freshman
    12|	High school senior
    11|	High school junior
    10|	High school sophomore
    9|	High school freshman
    8|	Eighth grade
    7|	Seventh grade
    6|	Sixth grade
    """)
    return


@app.cell
def _(gunning_fog, tmoom):
    gunning_fog(tmoom)
    return


@app.cell
def _(conversation, gunning_fog):
    gunning_fog(conversation)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **What do readability formulas actually measure?**

    Look back at the formulas. They only use four things: the number of words, sentences, syllables, and complex words. They never look at what the words *mean*, or the *order* the words are in.

    To see what this means, let's scramble the words inside every sentence of *They're Made Out of Meat*. I use `random.shuffle()` to shuffle the words of each sentence (and `random.seed()` so that we all get the same shuffle).
    """)
    return


@app.cell
def _(nltk, random, tmoom):
    random.seed(220)

    scrambled_sentences = []

    for sentence in nltk.sent_tokenize(tmoom):
      # get the words of the sentence, and shuffle them
      sentence_words = [token for token in nltk.word_tokenize(sentence) if token.isalpha()]
      random.shuffle(sentence_words)
      # join them back together, and put a full stop at the end
      scrambled_sentences.append(' '.join(sentence_words) + '.')

    tmoom_scrambled = ' '.join(scrambled_sentences)

    # the first 300 characters of the scrambled story
    tmoom_scrambled[:300]
    return (tmoom_scrambled,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The scrambled story is nonsense (even more than the original!). But what do the formulas say?
    """)
    return


@app.cell
def _(
    flesch_grade_level,
    flesch_reading_ease,
    gunning_fog,
    tmoom,
    tmoom_scrambled,
):
    print('original:', flesch_reading_ease(tmoom), flesch_grade_level(tmoom), gunning_fog(tmoom))
    print('scrambled:', flesch_reading_ease(tmoom_scrambled), flesch_grade_level(tmoom_scrambled), gunning_fog(tmoom_scrambled))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The scores are the same! Because the scrambled story has the same words, sentences, and syllables as the original, the formulas think it is exactly as easy to read. This is one of the main criticisms of readability formulas: they measure some of the *surface* features of a text, but not how easy it is to actually *understand*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    I have shown you a number of formulas you can calculate. There are even more, [which you can see here.](https://en.wikipedia.org/wiki/Readability#Popular_readability_formulas)

    - Find some texts you think are easy, and some you think are difficult. Do the readability formulas accurately categorise these texts based on your expectations?
    - Consider extending what is already here. Can you add more readability formulas? Can you also make a single function which calculates all of these formulas for a text?
    - Can you write a text that the formulas say is very easy to read, but which is actually very hard to understand?
    """)
    return


@app.cell
def _():
    # use this code cell to explore readability!
    return


if __name__ == "__main__":
    app.run()
