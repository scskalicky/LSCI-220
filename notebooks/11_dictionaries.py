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
    #### Relevant NLTK Book Sections

    [NLTK Book, Chapter 5, Section 3.1 and 3.2](https://www.nltk.org/book/ch05.html#sec-dictionaries)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Python Dictionaries

    The `nltk.FreqDist()` returns a specialised version of a built-in Python data type known as a `dictionary`. In this notebook we will cover how to create and use dictionaries in more depth.

    We have already looked at using lists as a way to store data. A list is like a bucket which you can toss all of your stuff in. A dictionary imposes more order than a list, and can sometimes be more useful for many of the linguistic analyses we would like to perform.

    A Python dictionary works in a similar manner to book dictionaries, where you look up the meaning of words. You first think of the word you want to look up, find it, then read the entry. A Python dictionary works the same way — you query the dictionary for a specific entry, and instead of returning the entry itself, the dictionary returns information associated with that entry.

    Python dictionaries store information using `key:value` pairs. The `nltk.FreqDist()` function returns a dictionary where the `key` is the thing that was counted, and the `value` is the frequency of that thing.

    To create an empty Python dictionary, we can use `dict()`. To add entries to the dictionary, we use the square bracket notation `[]` after the name of the dictionary, then use `=` to assign the value.
    """)
    return


@app.cell
def _():
    # initial creation of a dictionary
    species = dict()
    return (species,)


@app.cell
def _(species):
    # adding a key and a value
    species['dog'] = 'canine'
    return


@app.cell
def _(species):
    # calling a key to get a value
    species['dog']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can also choose to pre-populate a dictionary using curly braces and colons (I've called this one `species2`, because marimo only lets each variable be created in one cell):
    """)
    return


@app.cell
def _():
    # You can create key : value pairs using curly braces
    species2 = {'dog': 'canine', 'cat': 'feline'}
    return (species2,)


@app.cell
def _(species2):
    species2['cat']
    return


@app.cell
def _(species2):
    species2['dog']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rules for dictionary keys

    - Dictionary keys need to be *immutable* values which include strings, integers, booleans, tuples, and so on. This mostly means that you can't use a list as a dictionary key
    - much like a real dictionary, each key can only occur one time in a dictionary
    - the value associated with a dictionary key can be almost anything, including another dictionary, which can then contain other dictionaries...
      - if you manually add a value, you might overwrite what is already there.

    > **marimo note:** in this notebook, several cells add to or change a dictionary that was created in an earlier cell. This works when you run the cells in order. But if you go back and change one of those cells, marimo won't automatically re-run the cells below it, so re-run them yourself.
    """)
    return


@app.cell
def _():
    # create an empty dictionary
    temp_dict = dict()
    return (temp_dict,)


@app.cell
def _(temp_dict):
    # add a string as a key
    temp_dict['one'] = 1
    return


@app.cell
def _(temp_dict):
    # look at the dictionary
    temp_dict
    return


@app.cell
def _(temp_dict):
    # add a number as a key
    temp_dict[1] = 'one'
    return


@app.cell
def _(temp_dict):
    # look up the key 1
    temp_dict[1]
    return


@app.cell
def _(temp_dict):
    # update our dictionary:
    temp_dict['one'] = 'ONE'
    return


@app.cell
def _(temp_dict):
    # we have overwritten the value, because there can be only one.
    temp_dict
    return


@app.cell
def _(temp_dict):
    # try adding a list as a key, you get an error.
    temp_dict[['one', 'two']] = [1,2]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Crucially, you should notice an important difference in how `[]` are used in dictionaries versus strings. While `[]` indexes specific *locations* in a string or list, the `[]` indexes specific *keys* in a dictionary. This means you do not need to worry about the ordering of a dictionary's keys, but instead the values of the keys themselves.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    Take this moment to make some dictionaries of your own. Start simple, such as a dictionary containing first and last names, or a dictionary containing names and phone numbers of people you know.

    Explore creating an empty dictionary and then adding values, as well as creating a dictionary using curly braces.
    """)
    return


@app.cell
def _():
    # make some dictionaries.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Searching dictionaries

    Because dictionaries do not use indexing in the same way as strings and lists, we need to explore some alternative methods for looping and searching through dictionaries.

    Below, I will initialise a simple translation dictionary between English and te reo Māori. The `keys` are the English version, and the `values` are the te reo Māori.
    """)
    return


@app.cell
def _():
    # create a translation dictionary
    eng2mri = {'one': 'tahi','two': 'rua', 'three': 'toru', 'four': 'whā', 'five': 'rima', 'six': 'ono', 'seven': 'whitu', 'eight': 'waru', 'nine': 'iwa', 'ten': 'tekau'}
    return (eng2mri,)


@app.cell
def _(eng2mri):
    # test if it works
    eng2mri['ten']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To see the entire dictionary, we can use the `.items()` dictionary method:
    """)
    return


@app.cell
def _(eng2mri):
    # what are the key:value pairs in this dictionary?
    eng2mri.items()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Alternatively, we can inspect all of the entries in a dictionary by using the `.keys()` method...
    """)
    return


@app.cell
def _(eng2mri):
    # what are the keys (entries) of this dictionary?
    eng2mri.keys()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ...or we can inspect all of the values using the `.values()` method.
    """)
    return


@app.cell
def _(eng2mri):
    # what are the values of this dictionary?
    eng2mri.values()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we know how to access the keys of a dictionary, we can start to search through dictionaries using loops. For example, if we wanted to loop through each entry of a dictionary, we could use:

    ```
    for key in dict.keys():
      print(key)
    ```

    While getting the keys is useful to know what is inside the dictionary, we commonly also want to do something with the values associated with the key. So, we could adjust our for loop to loop over the keys, but then return the value associated with the key, rather than the key itself:

    ```
    for key in dict.keys():
      print(dict[key])
    ```

    Maybe this seems a bit confusing in the abstract, compare the for loops below. (Each loop uses a numbered variable, `key1`, `key2`, and so on, because marimo only lets each variable be created in one cell.)
    """)
    return


@app.cell
def _(eng2mri):
    # print all of the keys
    for key1 in eng2mri.keys():
      print(key1)
    return


@app.cell
def _(eng2mri):
    # now print all of the values by using the key as an index in the loop
    for key2 in eng2mri.keys():
      print(eng2mri[key2])
    return


@app.cell
def _(eng2mri):
    # could also print both the key and the value:
    for key3 in eng2mri.keys():
      print(key3, eng2mri[key3])
    return


@app.cell
def _(eng2mri):
    # the same thing but with some fancier print formatting
    for key4 in eng2mri.keys():
      print(f'{key4} = {eng2mri[key4]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And, we could actually reverse the order just by swapping the variables
    """)
    return


@app.cell
def _(eng2mri):
    # swap the order
    for key5 in eng2mri.keys():
      print(f'{eng2mri[key5]} = {key5}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Technically, you don't need to loop over the keys, as looping over the dictionary itself will give you the keys. But it is sometimes handy to know how to do it with the keys as well.
    """)
    return


@app.cell
def _(eng2mri):
    for entry in eng2mri:
      print(entry)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Adding conditions to our search

    Let's create some conditional logic to spruce up our searches. For example, we could look at each translation pair and print whichever of the two words is longer:
    """)
    return


@app.cell
def _(eng2mri):
    # start a loop
    for key6 in eng2mri.keys():
      # if value is at least as long as key:
      if len(eng2mri[key6]) >= len(key6):
        print(eng2mri[key6])

      else:
        print(key6)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's consider another dictionary of population of countries in Oceania. (These population figures are a few years old, so they won't match the latest counts.)
    """)
    return


@app.cell
def _():
    oceania = {'Tokelau': 1499, 'Norfolk Island': 1748, 'Federated States of Micronesia': 103000, 'Nauru': 10084, 'New Zealand': 4795886, 'Tonga': 100651, 'Tuvalu': 10640, 'Niue': 1611, 'Cook Islands': 18100, 'Samoa': 199052, 'Marshall Islands': 55500, 'Wallis and Futuna': 11700, 'French Polynesia': 275918, 'Australia': 25710853, 'American Samoa': 56700, 'Palau': 21000, 'Papua New Guinea': 8558800, 'New Caledonia': 278500, 'Northern Mariana Islands': 56200, 'Vanuatu': 304500, 'Kiribati': 120100, 'Fiji': 896445, 'Pitcairn Islands': 50, 'Guam': 172400, 'Solomon Islands': 667044}
    return (oceania,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's first print out each country and its population:
    """)
    return


@app.cell
def _(oceania):
    for key7 in oceania.keys():
      print(f'the population of {key7} is {oceania[key7]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's do this alphabetically by employing the `sorted()` function around the keys:
    """)
    return


@app.cell
def _(oceania):
    for key8 in sorted(oceania.keys()):
      print(f'the pop of {key8} is {oceania[key8]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's consider sorting our population sizes into different categories, such as these:

    >*large* = more than 1,000,000 people

    > *medium* = 100,000 to 1,000,000 people

    > *small* = 10,000 to 100,000 people

    > *very small* = less than 10,000

    Using these criteria, we can adapt the previous `for` loop so that it returns statements like this:

    ```
    the pop of Australia is large! - 25710853
    ```

    We can do this with a series of elif statements.
    """)
    return


@app.cell
def _(oceania):
    # loop through the sorted keys
    for key9 in sorted(oceania.keys()):
      # consider different sizes and categories
      if oceania[key9] < 10000:
        size1 = 'very small'
      elif oceania[key9] >= 10000 and oceania[key9] < 100000:
        size1 = 'small'
      elif oceania[key9] >= 100000 and oceania[key9] < 1000000:
        size1 = 'medium'
      else:
        size1 = 'large'

      print(f'the pop of {key9} is {size1}! - {oceania[key9]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's calculate the total population of Oceania by adding up all of the values in the dictionary with `sum()`:

    We can then continue adapting the previous `for` loop to return statements like this:

    ```
    the pop of Australia is large! - it is 25710853, which is _____% of Oceania!
    ```
    """)
    return


@app.cell
def _(oceania):
    # total population of Oceania: add up all the values in the dictionary
    total_pop = sum(oceania.values())

    # loop through the sorted keys
    for key10 in sorted(oceania.keys()):
      # consider the size and assign a value
      # can you think of a different way to do this?
      if oceania[key10] < 10000:
        size2 = 'very small'
      elif oceania[key10] >= 10000 and oceania[key10] < 100000:
        size2 = 'small'
      elif oceania[key10] >= 100000 and oceania[key10] < 1000000:
        size2 = 'medium'
      else:
        size2 = 'large'

      # calculate population percentage and round to 3 decimals.
      pop_perc = round((oceania[key10] / total_pop) *100, 3)

      print(f'the pop of {key10} is {size2}! - it is {oceania[key10]}, which is {pop_perc}% of Oceania!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Building more complex dictionaries

    The dictionaries used so far have all included single `key:value` pairs. We can include more complex information in our dictionaries. For example, we could create a dictionary which stores lexical information about different texts — this is an ideal way to contain information about language because a dictionary can be continuously updated with new texts and new features.

    Let's start with two small texts.
    """)
    return


@app.cell
def _():
    whale = """The sea was angry that day, my friends - like an old man trying to send back soup in a deli.
    I got about fifty feet out and suddenly, the great beast appeared before me.
    I tell you, he was ten stories high if he was a foot.
    As if sensing my presence, he let out a great bellow."""

    the_kramer = """I sense great vulnerability. A man-child crying out for love. An innocent orphan in the post-modern world.
    I see a parasite. A sexually depraved miscreant who is seeking only to gratify his basest and most immediate urges.
    His struggle is man's struggle. He lifts my spirit.
    He is a loathsome, offensive brute. Yet I can’t look away.
    He transcends time and space.
    He sickens me.
    I love it.
    Me too.
    """
    return the_kramer, whale


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's create a dictionary in which the keys will represent each of these texts. The values of each key will be a *new* dictionary which contains information about the text. The first piece of information will be the text itself:
    """)
    return


@app.cell
def _(whale):
    # create a dictionary named sf_dict with one key(whale)
    # the value for the key is another dictionary, with one key (text) and the value is the string associated with whale (above)
    sf_dict = {'whale': {'text': whale} }
    sf_dict
    return (sf_dict,)


@app.cell
def _(sf_dict):
    # we can index the text by using [key][key]
    # this is asking first to look at the key "whale", then at the key "text"
    sf_dict['whale']['text']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we've added one text to the dictionary, let's add the second:
    """)
    return


@app.cell
def _(sf_dict, the_kramer):
    sf_dict['the_kramer'] = {'text': the_kramer}
    sf_dict
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have our texts stored in the same dictionary with their own sub dictionaries, let's start performing some actions. Let's start simple and include the total number of words per text using `len()` and `.split()`.

    Now, we could independently calculate these values and then add them to the dictionary manually.

    Or, we could initiate a for loop which simultaneously loops over the dictionary and creates the new values for us in one go.

    In the following cell, I do this in one line:
    """)
    return


@app.cell
def _(sf_dict):
    # add total length of text to the dictionary
    for key11 in sf_dict.keys():
      sf_dict[key11]['word_length'] = len(sf_dict[key11]['text'].split())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There's a lot going on in that one line (and yes, I recognize I am using `.split()` and not `nltk.word_tokenize`!).

    Basically, we are first selecting an entry in our top level dictionary, and because that will return a second dictionary, we then select an entry from *that* dictionary. This sketch of the structure might help:

    ```
    top-level dictionary (sf_dict)
      - entry 1 (whale)
        - whale dictionary
          - entry 1 (text)
          - entry 2 (word_length)
      - entry 2 (the_kramer)
        - the_kramer dictionary
          - entry 1 (text)
          - entry 2 (word_length)

    ```
    """)
    return


@app.cell
def _(sf_dict):
    # we can see the results of our new variable by calling it, for each text...
    sf_dict['whale']['word_length']
    return


@app.cell
def _(sf_dict):
    sf_dict['the_kramer']['word_length']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ideally you can see how running a single loop over a dictionary and performing operations on the information in that dictionary allows for a one-stop shop of a data container which can be expanded to include as many pieces of information as one might like.

    Let's extend the above example and create a dictionary of lexical information for our texts. For each text, we will report:

    - the total number of words according to `.split()`
    - the total number of tokens according to `nltk.word_tokenize()`
    - the resulting TTR using `.split()` versus `nltk.word_tokenize()`
    - the top 5 most frequent words using `nltk.FreqDist()` and `.split()`
    - the top 5 most frequent words using `nltk.FreqDist()` and `nltk.word_tokenize()`

    Sounds like a lot, right? You should know how to do each of these operations - it's just a matter of adding them to the for loop that we've already seen above.
    """)
    return


@app.cell
def _():
    # load in required nltk resources.
    import nltk
    nltk.download('punkt_tab')
    return (nltk,)


@app.cell
def _(sf_dict):
    # let's delete the word_length entry we made above
    del sf_dict['whale']['word_length']
    del sf_dict['the_kramer']['word_length']
    return


@app.cell
def _(nltk, sf_dict):
    # Expand the for loop to calculate more features:

    for key12 in sf_dict.keys():
      # number of words according to .split()
      sf_dict[key12]['num_split_tokens'] = len(sf_dict[key12]['text'].split())

      # number of words according to nltk.word_tokenize
      sf_dict[key12]['num_nltk_tokens'] = len(nltk.word_tokenize(sf_dict[key12]['text']))

      # ttr from split
      sf_dict[key12]['split_ttr'] = len(set(sf_dict[key12]['text'].split())) / len(sf_dict[key12]['text'].split())

      # ttr from nltk tokens
      sf_dict[key12]['nltk_tokens_ttr'] = len(set(nltk.word_tokenize(sf_dict[key12]['text']))) / len(nltk.word_tokenize(sf_dict[key12]['text']))

      # top 5 most frequent words using .split()
      sf_dict[key12]['split_five_most_frequent'] = nltk.FreqDist(sf_dict[key12]['text'].split()).most_common(5)

      # top 5 most frequent words using nltk tokens
      sf_dict[key12]['nltk_five_most_frequent'] = nltk.FreqDist(nltk.word_tokenize(sf_dict[key12]['text'])).most_common(5)
    return


@app.cell
def _(sf_dict):
    # now look at the information we have about the text
    sf_dict['whale']
    return


@app.cell
def _(sf_dict):
    sf_dict['the_kramer']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    Compare the output from the two texts above. Think about the difference you see between the `.split()` and `nltk.word_tokenize()` approaches.

    - Do you remember why these functions are providing different results?
    - What do you notice about the frequency results? Is there any pre-processing we might want to do, and if so, which results would be changed as a result of different pre-processing?
    """)
    return


@app.cell
def _():
    # use this code cell to compare the two texts!
    return


if __name__ == "__main__":
    app.run()
