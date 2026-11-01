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
    ## Regular Expressions

    Regular expressions are a method for finding patterns in text. They are not specific to Python, and can be used in a variety of programming languages as well as applications that allow for regular expressions. You might see them called `regex` for short. You may also come across tools such as `grep`, a command-line program for searching files which uses regular expressions.

    Learning regular expressions is an incredibly useful skill for programming in general and NLP specifically. Regular expressions allow you to specify extremely precise search patterns, and perform operations on the results of those patterns. There is, however, a bit of a learning curve (which is now mitigated with AI...).

    You can use regular expressions to search for certain filenames in a directory or certain morphemes in a word.

    In this notebook, we'll learn the basics of regex which will help us understand how NLTK has employed regex for linguistic analysis.

    To use regular expressions in Python, we need to `import re`
    """)
    return


@app.cell
def _():
    # import re (regular expressions module)
    import re

    return (re,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## creating regex patterns and `re.search()`

    All regex searches require defining a search pattern — you need to tell Python what it is you're looking for!

    Search patterns are entered as strings, but can include special characters to allow for variability and options that otherwise cannot be included in just a string. You can search for:

    - Actual characters/strings (e.g., searching for specific words or parts of words).
      - These characters mean you want Python to search for the literal version of what you typed (e.g., if you typed "hello!" you would want to search for that exact word, including the exclamation mark)


    - meta characters which represent something beyond their literal version. We have already seen some of these characters, such as `\n` for newlines and `\t` for tab.

    - Quantifiers, which allow you to constrain the number of times something repeats (e.g., asking for any number of characters followed by a number).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Searching through NZ Birds of the Year

    Let's start with a small-scale example. Let's pretend we want to search for various linguistic properties of the names of all [NZ Bird of the Year Winners](https://en.wikipedia.org/wiki/Bird_of_the_Year) with 2023 being bird of the *century*!

    - 2025:  Kārearea
    - 2024:  Hoiho
    - 2023: Pūteketeke
    - 2022:	Pīwauwau
    - 2021:	Pekapeka-tou-roa
    - 2020:	Kākāpō
    - 2019:	Hoiho
    - 2018:	Kererū
    - 2017:	Kea
    - 2016:	Kōkako
    - 2015:	Kuaka
    - 2014:	Tara iti
    - 2013:	Mōhua
    - 2012:	Kārearea
    - 2011:	Pūkeko
    - 2010:	Kākāriki
    - 2009:	Kiwi
    - 2008:	Kākāpō
    - 2007:	Riroriro
    - 2006:	Pīwakawaka
    - 2005:	Tūī

    Let's first get those winners into a list!
    """)
    return


@app.cell
def _():
    # define list of BoTY winners:
    birbs = ['Kārearea','Hoiho','Pūteketeke','Pīwauwau', 'Pekapeka-tou-roa', 'Kākāpō', 'Hoiho', 'Kererū', 'Kea', 'Kōkako', 'Kuaka', 'Tara iti',
             'Mōhua', 'Kārearea', 'Pūkeko' ,'Kākāriki', 'Kiwi', 'Kākāpō', 'Riroriro', 'Pīwakawaka', 'Tūī']
    return (birbs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Okay, now we can start using `re.search()` as a means to find if any of our bird names contain specific characters or patterns.

    `re.search()` is a function which results in two outcomes:

    1. If the pattern exists in the string being searched, `re.search()` will return a `match` object which contains details of the match
    2. If the pattern does not exist in the string being searched, `re.search()` will return nothing

    With this knowledge, we can use `re.search()` as a *conditional* test to return strings which do or do not have specific patterns of interest. More specifically, we can specify `if re.search():` which would only return `True` if there was a match in the string.

    The syntax of `re.search()` is:

    ```
    re.search(pattern = '', string = '')
    ```

    So we need to first supply the pattern we are looking for, and then supply the string we are searching.

    Knowing this,  let's search for capital "K" in our list of birds and print any bird that includes a capital K:

    (because I'm using `for loops` and not functions or list comprehensions, I will use the variable names `birb1`, `birb2`, etc, because marimo won't allow reassignment.)
    """)
    return


@app.cell
def _(birbs, re):
    # let's save our search pattern to a variable:
    upper_k = 'K'


    # create a for loop through our list of birds
    for birb1 in birbs:
      # if there is a resulting match object
      if re.search(upper_k , birb1):
      # print the bird
        print(f'{birb1} has a {upper_k}!')
      else:
        print(f'{birb1} does not have a {upper_k}!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One thing you should notice about those results is that the search is quite literal - birds with only lowercased "k" such as Pūkeko did not meet the condition of the test - which makes sense. We could repeat the same search as above but with a lowercased 'k':
    """)
    return


@app.cell
def _(birbs, re):
    # same as previous but w/ lowercase k
    lower_k = 'k'

    # create a for loop through our list of birds
    for birb2 in birbs:
      # if there is a resulting match object
      if re.search(lower_k , birb2):
      # print the bird
        print(f'{birb2} has a {lower_k}!')
      else:
        print(f'{birb2} does not have a {lower_k}!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We run into the converse situation here — birds with only uppercase "K" such as 'Kiwi' were not matched.

    Usually, we want to add a bit more flexibility into our searches so that we can find strings that meet a variety of criteria. In this case, how could we create a pattern which would allow for birds including both upper and lowercased 'k' to be returned?

    Clearly, one option would be to convert the strings to lowercase before doing any searches! But, keep in mind that we are dealing with proper nouns here (i.e., names of things), and in English these are signalled in writing through capitalization of the initial letter. So in this case, applying a lowercase to everything might not be appropriate.

    So, let's use this opportunity to see how to allow for options in our search patterns. We can use square brackets to tell `re.search()` that we are looking for *any* candidate within the square brackets:

    ```
    '[Kk]' = any of 'K' or 'k'
    ```

    In this way, the square brackets are effectively a shorthand for using `or`. Let's demonstrate this, while also exploring how to use the `match` object to show us which part of the pattern was actually a hit. We can do so by using the `.group()` method from a resulting regex match.
    """)
    return


@app.cell
def _(birbs, re):
    # define our search pattern
    either_k = '[Kk]'
    # create a for loop through our list of birds
    for birb3 in birbs:
      # save the match to a variable
      k_match = re.search(either_k, birb3)
      # if there is a match, print the bird and the results of the match
      if k_match:
      # print the bird
        print(f'{birb3} has a {k_match.group()}!')
      else:
        print(f'pattern {either_k} not found for {birb3}!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Looking at the output, we can see that `re.search()` stops as soon as it finds the first match. Crucially, the search begins from the start of the string, so all birds that start with `K` will be matched for uppercase K, but we still do not know if they contain a lower-cased `k`.

    To answer the relatively silly question of how many "k"s are in a bird name, we can use a different function: `re.findall()`. Instead of stopping at the first match, `re.findall()` returns a list of *every* match in the string. And because the result is a list, `len()` will count the matches for us:
    """)
    return


@app.cell
def _(re):
    # find every K or k in one bird name
    re.findall('[Kk]', 'Kākāriki')
    return


@app.cell
def _(re):
    # count them
    len(re.findall('[Kk]', 'Kākāriki'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    But let's move on and instead refine a method to search specific parts of a string. Let's stick with our birds for just a little bit longer. First, let's revise our search pattern so that it searches for a `k` *within* the bird name, but *not* the first or last letter of the name. But, in order to do so, we need to understand the use of certain meta characters which designate the start/end of a string, as well as meta characters which stand for any character.

    The full stop `.` is a meta character which stands for *almost* anything (it excludes newlines, for example). You can think of the full stop as a wild card — it can represent anything you want.

    So, a regex pattern comprised of three full stops `'...'` would represent `three of any character in a row`. Such a pattern would match the first combination of three characters in a string, regardless of whether the string is longer than three characters. However, the pattern would *not* match a string of two characters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Wildcard: the full stop `.`
    """)
    return


@app.cell
def _():
    # define our search pattern
    three_dots = '...'
    return (three_dots,)


@app.cell
def _(re, three_dots):
    # Returns a match object, matching 'dog'
    re.search(three_dots, 'dog')
    return


@app.cell
def _(re, three_dots):
    # also returns a match object matching 'dog' (the first 3 characters of the string):
    re.search(three_dots, 'dogs and cats')
    return


@app.cell
def _(re, three_dots):
    # Returns nothing because there is no sequence of three characters in this string
    re.search(three_dots,'ab')
    return


@app.cell
def _(re, three_dots):
    # Returns nothing because `.` cannot stand for newlines.
    re.search(three_dots, 'ab\n')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### String anchors: `^` and `$`

    Remember the challenges associated with defining a word to make tokens? Regex has special characters which sort of help with this, in that they represent the *start* and the *end* of a string (which, of course, is not always the same as a word!).

    These characters are also called `anchors`:

    ```
    ^ - start of a string
    $ - end of a string
    ```

    So we can use these anchors to better constrain our search patterns. If instead of finding any three-character sequence, we wanted to find any three-character *word*, we could revise our three dots pattern as such:
    """)
    return


@app.cell
def _():
    # regex search pattern which looks for any three characters between a start/stop of a string
    three_character_word = '^...$'
    return (three_character_word,)


@app.cell
def _(re, three_character_word):
    # it will find dog...
    re.search(three_character_word, 'dog')
    return


@app.cell
def _(re, three_character_word):
    # and cat...
    re.search(three_character_word, 'cat')
    return


@app.cell
def _(re, three_character_word):
    # but not bird. (because there are four characters between start/stop)
    re.search(three_character_word, 'bird')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quantifiers

    So far, regex patterns have allowed us to scope the nature of our search to words of certain lengths.

    Let's extend this knowledge to return to our birds and find if we can define a search pattern which locates lowercase 'k' in bird names, even if they start with an uppercase 'k'. We need to learn *one more thing* though, and that's how to attach quantifier flags to characters. Quantifiers allow us to specify how many times the *preceding* character can occur in the search. One of the most useful quantifiers is `*` which stands for `zero or more`, a rather liberal constraint on a character.

    So, if we wanted to search for "zero to infinite instances of any character", we could type `.*`, for example:
    """)
    return


@app.cell
def _(re):
    # .* basically says "find me anything"
    re.search('.*', 'these pretzels are making me thirsty!')
    return


@app.cell
def _(re):
    # even nonsense
    re.search('.*', 'asdfasdlfkjasdl;k#fjasd;lk@fj)))')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Finally back to the birds!

    So, using `.*` is quite dangerous unless we constrain the search a bit more. Let's apply this to our birds problem and define a search pattern which finds a `k` occurring inside the name of our birds. Here is the pattern:

    ```
    '^..*k.*.$'
    ```

    This pattern says search for:

    `^` (start of a string), `.` (followed by one wild card - the first letter of the name), `.*` (followed by zero or more wildcards), `k` followed by one "k", `.*` (followed by zero or more wildcards), `.` (followed by one wild card - the last letter of the name), `$` (followed by the end of the string).

    This pattern lets us find a lowercase k within a string of any length.
    """)
    return


@app.cell
def _():
    mid_k = '^..*k.*.$'
    return (mid_k,)


@app.cell
def _(birbs, mid_k, re):
    # create a for loop through our list of birds
    for birb4 in birbs:
      # save the match to a variable
      mid_k_match = re.search(mid_k, birb4)
      # if there is a match, print the bird and the results of the match
      if mid_k_match:
      # print the bird
        print(f'{birb4} has a lower-cased k!')
      else:
        print(f'{birb4} does not have a lower case k!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Regex as a tokenizer

    Remember the question from the TTR notebook: *what is a word?* So far we have used `.split()`, which treats anything between spaces as a word. Regex gives us another option: we can define a word by a pattern.

    NLTK has a tool called `RegexpTokenizer` which does exactly this. You give it a regex pattern, and it returns every part of a string that matches the pattern as a list of tokens.

    Two new things in the pattern below:

    - `\w` matches any *word character*: a letter (in any alphabet, including letters with macrons), a digit, or an underscore
    - `+` is another quantifier, meaning *one or more* of the preceding character

    So `\w+` means "one or more word characters in a row". The `r` in front of the string tells Python to treat the backslash as a normal character, which you should always do with regex patterns that contain backslashes.
    """)
    return


@app.cell
def _():
    # import the tokenizer from nltk
    from nltk.tokenize import RegexpTokenizer

    # create a tokenizer which treats one or more word characters as a token
    word_tokenizer = RegexpTokenizer(r'\w+')

    word_tokenizer.tokenize("I can't believe the kākāpō won again!")
    return (RegexpTokenizer,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at the output. The punctuation is gone, the macrons in *kākāpō* are kept, but *can't* has been split into `can` and `t`. Is that what we want?

    We can change our definition of a word by changing the pattern. Square brackets mean "any of these characters", so `[\w']+` means "one or more word characters **or apostrophes** in a row":
    """)
    return


@app.cell
def _(RegexpTokenizer):
    # a tokenizer which also allows apostrophes inside tokens
    apostrophe_tokenizer = RegexpTokenizer(r"[\w']+")

    apostrophe_tokenizer.tokenize("I can't believe the kākāpō won again!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Neither tokenizer is "correct". Each one is a different decision about what counts as a word, and that decision will change any counts we make afterwards (such as TTR). We'll explore this more in the tokenisation workshop.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Regular expressions are challenging

    It goes without saying that learning regular expressions is challenging. It usually takes a good bit of trial and error in order to figure out the exact search pattern you need for your purposes.

    A really useful website for Regex is [Regex101](https://regex101.com/) (make sure you select Python), and there are a number of other resources out there to help you learn regex, such as [Geeks for Geeks](https://www.geeksforgeeks.org/python-re-search-vs-re-match/?ref=gcse). Our generative AI overlords are also quite helpful in guiding our regex pursuits.

    [The NLTK book has quite a bit on regex as well, if you're keen, in Chapter 3, Section 3.4 and 3.5](https://www.nltk.org/book/ch03.html#sec-regular-expressions-word-patterns)
    """)
    return


if __name__ == "__main__":
    app.run()
