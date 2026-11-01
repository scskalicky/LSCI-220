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
    #### Relevant NLTK Book sections

    [NLTK Book, Chapter 1, Section 4](https://www.nltk.org/book/ch01.html#control_index_term)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Traversal using `for` loops

    Being able to repeat the same action over a large set of data is one of the many benefits of learning how to use a programming language. One of the most fundamental ways to repeat an action is through the use of `for loops`. These are called `for loops` because they *loop* or repeat through a sequence of data, objects, values, or whatever you want to call them.

    What does the `for` mean? The use of "for" provides a hint about the way we control `for loops` — *for* specifies the units that will be looped over.

    For example, let's pretend we had a pile of documents that we wanted to shred. Our unit of measurement in this case is an individual document. So, if we wanted to shred each document one at a time, we could formalise this process using the following statement:

    >`for each document in all of my documents:`

    >> `shred the document`

    `... repeat until I run out of documents...`

    Applying this idea to Python, a `for loop` allows us to traverse an entire sequence and operate on elements of that sequence. For example, for each value in a sequence, we could:

    - print the value
    - use a built-in method
    - create a new variable based on the value
    - update a counter
    - perform a conditional test
    - etc...

    Much like the `if` statements, the `for` loop will contain a header with a colon followed by an indented body:

    >`for thing in sequence_of_things:`
    >>  `do something`

    Run the following cell to see how a `for` loop works.

    Because a string is a *sequence* of characters, the for loop will go through that sequence one-at-a-time.
    """)
    return


@app.cell
def _():
    # Print out each character of a string.
    for letter in 'word':
      print(letter)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You may have noticed that there seemed to be a variable in the `for` loop named `letter`. In Python, the `for` loop needs a temporary variable to stand for the value that is being passed to the loop. In the example above, the value of `letter` changed each time the loop was run, starting with "w", then "o", then "r", then "d". Because this is a variable, you can set the name of the iterating variable to anything you want. A common variable used in a `for` loop is the lower case `i`. But, you might find it worthwhile to name your variable something which makes it clear what is being looped over.

    For example, if I am going to loop over every word in a string, I might want to name my iterating variable `word`.
    """)
    return


@app.cell
def _():
    # loop over every value resulting from .split() on a string.
    for word in 'every day is exactly the same'.split():
      print(word)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > It is worth noting that `for` loops in Python are more simple to execute when compared to other programming languages. This is because the default range of a `for` loop in Python will be the beginning and ending of the sequence/thing that is being looped over. Other programming languages require the user to define the size of the loop, how to update the loop count, when to stop the loop, and so on. Fortunately, we don't need to worry about that here!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Consider the next example. I define a list and ask for each value of the list to be printed:
    """)
    return


@app.cell
def _():
    # define a list containing different countries
    countries = ['New Zealand', 'Australia', 'United States of America', 'Canada', 'Mexico', 'Norway']
    return (countries,)


@app.cell
def _(countries):
    # note I use "country" as the variable for my loop
    # doing so helps me understand the nature of the values/data
    for country in countries:
      print(country)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Conditional looping

    Now that we understand looping, let's add some conditional logic to make our loop perform different things, depending on the properties of each value within the loop. Extend the prior example and label each country as having a long or short name, depending on whether its name is over six characters. I'll also use an `if/else` statement and string formatting to make [fancier print statements](https://realpython.com/python-f-strings/#f-strings-a-new-and-improved-way-to-format-strings-in-python).
    """)
    return


@app.cell
def _(countries):
    # start a loop through `countries`
    for place in countries:
      # check the length, if it's over six characters, do this
      if len(place) > 6:
        print(f'{place} has a long name!')
      # if the if statement returns False, do this instead
      else:
        # the f'' string lets you combine {variables} and strings in one string.
        print(f'{place} has a short name!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's now check if our countries are in certain regions/continents. I will define two separate lists of our regions, containing some countries. Then I'll write a new `for` loop which uses `in` to find which region a country belongs to.
    """)
    return


@app.cell
def _():
    # Define our two regions
    australasia = ['New Zealand', 'Australia']
    north_america = ['Canada', 'United States of America', 'Mexico']
    return australasia, north_america


@app.cell
def _(australasia, countries, north_america):
    # check where our countries are
    for nation in countries:
      if nation in australasia:
        print(f'{nation} is in Australasia!')
      elif nation in north_america:
        print(f'{nation} is in North America!')
      else:
        print(f'dunno where {nation} is.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Looping to check properties of words

    In a previous notebook I asked two questions about words/language you might want to answer:

    - what if you wanted to find all of the uppercase letters in the string `"Victoria University of Wellington"`?

    - what if you wanted to find all the words in a book which were over five letters long?

    Now that you have an understanding of conditional expressions and for loops, we can easily answer these questions. Can you figure them out? The first question would require looping over the characters in the string and checking whether `.isupper()` returns `True`. The second question would require looping over the words in a book and checking if `len(word)` is greater than five characters.
    """)
    return


@app.cell
def _():
    vuw = "Victoria University of Wellington"

    for character in vuw:
      # note that this essentially asks `if character.isupper() == True`
      if character.isupper():
        print(f'{character} is an uppercased character!')
      else:
        # the "\" in the ain\'t escapes the apostrophe so the string doesn't end on that apostrophe
        print(f'{character} ain\'t uppercased')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'm going to read in a text from the internet in the next cell to demonstrate a longer text. It's okay if you don't get what's going on, and we'll dig into this later.

    - I'm loading in a library called `requests`, which allows us to read data from URLs
    - I'm then saving a URL of my choice as a string to the variable `url` (I already know this text is stored at this URL).
    - I'm then asking `requests.get()` to grab the data at that URL, and using `.text` to get it as a string.

    The result is the text data read in as a string. You can manually enter the URL into your browser to see what the data looks like.
    """)
    return


@app.cell
def _():
    # import the requests library
    import requests

    # save url to a variable
    url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/sample-texts/grasshopper.txt'

    # get the text at that url as a string
    grasshopper = requests.get(url).text

    # examine the results
    print(grasshopper)
    return (grasshopper,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have a longer text loaded in, let's operate on each word of the text.
    """)
    return


@app.cell
def _(grasshopper):
    # do you remember what will result from .split()?
    for token in grasshopper.split():
      if len(token) > 5:
        # \t means tab, it's what creates the space in the output
        print(f'{token} \t is over five characters long!')
      else:
        print(f'{token} \t must be five chars or less')


    # Examine the output. How accurate is this program? Are there any words that are incorrectly counted? Why is that happening?
    # (we'll come back to this problem in the tokenisation workshop)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Building something with a loop

    The two loops above show you how they work, but they only end up printing something to the console, which is not very useful. What is more useful is to create new values or objects from a loop, as well as put the loop inside of a function.

    For example, pretend that in addition to finding the words that are over five letters long, we then want to do something to those words and store the results for later use.

    One way to do so is to create an empty data container, such as a list, and then add words to the container if they pass a condition test. The cell below does the following:

    1. creates an empty list named `output`
    2. loops through the results of using `.split()` on grasshopper (which is a list of each word)
    3. checks whether a word is over five characters long
    4. If the word is over five characters long, it is added to `output` using the `.append()` list method.
    """)
    return


@app.cell
def _(grasshopper):
    # output starts out empty
    output = []

    # loop over every string in the list
    for word2 in grasshopper.split():
      if len(word2) > 5:
        # each time a word2 in grasshopper meets this condition, it is added to output
        output.append(word2)

    # show the output - a list of words over 5 characters long.
    print(output)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice that the cell above does everything in one go: it creates `output`, fills it with the loop, and then shows it. This matters because if `output` were created in one cell and filled in another, running the loop cell again would add the same words to the list a second time.

    Another way to keep things tidy is to write our own functions. This means the `output` variable and the for loop will live inside the function, making it less likely that variables get confused as your programs grow in complexity.

    Note the function below:

    1. first I define the function using `def` and name it `long_words`
    2. the function takes one argument, `text` - this is an arbitrary name like any variable name
    3. On line 2 I create an empty list named `output`
    4. Line 3 defines a `for loop` over the words from `.split()`. Note that the variable `text` will stand for whatever input we give the function
    5. Line 4 has the conditional test
    6. Line 5 adds the word to the list if it passes the test (i.e., the condition returns `True`)
    7. Line 6 is a `return` statement which only executes once the `for` loop is complete.

    The `return` statement means we can save the *results* of this function to a new variable, or watch the results be sent to the console.

    Running the cell below loads the function into memory.
    """)
    return


@app.function
# make a function to store words over five letters long
def long_words(text):
  output = []
  for word in text.split():
    if len(word) > 5:
      output.append(word)
  return output


@app.cell
def _(grasshopper):
    # now use the function on grasshopper
    # just running the function gives us the output.
    long_words(grasshopper)
    return


@app.cell
def _(grasshopper):
    # we can also save the results of the function to a new variable
    grasshopper_long_words = long_words(grasshopper)
    return (grasshopper_long_words,)


@app.cell
def _(grasshopper_long_words):
    # look at the variable
    grasshopper_long_words
    return


@app.cell
def _(grasshopper_long_words):
    # Then we can perform new operations on our new variable!
    for long_word in grasshopper_long_words:
      if len(long_word) > 7:
        print(f'{long_word} \t is even longer than five!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # List Comprehensions

    So now that you've learned `for loops`, it's time to learn an alternative method which is commonly used in Python. This alternative method is an efficient shorthand for looping, which you will see used extensively in the NLTK book as well as almost anywhere else someone is using Python.

    This alternative format is known as a `list comprehension`. List comprehensions are good because they provide efficiency, but they can be a bit tricky to interpret when you first see them.

    The general syntax of a list comprehension is as follows:

    > `[statement/expression for value in sequence/generator]`

    The list comprehension above uses `[]`, just like a list, and will indeed return a list of values which meet the statement or expression indicated in the *first* part of the list comprehension.

    In the next cell you will see a simple list comprehension. You'll note in the example below  says `letter for letter`, which can be interpreted as "for each value, give me the value". This is the basic way to turn a sequence into a `list`, rather than spitting each value out one-at-a-time like a `for loop`.
    """)
    return


@app.cell
def _():
    # ask for each letter in "word"
    # note that the results are a list
    [letter for letter in 'word']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To achieve the same effect using a `for` loop, we would have to define a temporary output container and `.append()` or otherwise join our values to that container. A list comprehension avoids the need to do this.
    """)
    return


@app.cell
def _():
    # list comprehension helps us avoid the need to make empty containers and fill them
    letter_list = []

    for char in 'word':
      letter_list.append(char)

    letter_list
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Hopefully you can see how a list comprehension is useful — for instance we can save the results of a list comprehension directly to a variable, bypassing the need to create empty storage containers:
    """)
    return


@app.cell
def _():
    letters = [letter for letter in 'word']
    letters
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Performing operations in a list comprehension

    The expression on the left side of the list comprehension (before the `for`) is the place where we can perform operations on the values we are looping across. So, instead of just returning the value, we could do things like measure their length, convert to uppercase, or any other number of functions.

    The example below returns an upper cased version of each letter:
    """)
    return


@app.cell
def _():
    # this is equivalent to: for each letter in word, return letter.upper()
    upper_cased = [letter.upper() for letter in 'word']
    upper_cased
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next example measures the length of words:

    - note how I just use `w` as my looping variable, which is not as transparent, but quicker to type
    - note how I use `.split()` on a raw string - this means the loop will be over values in the list that is returned from using `.split()`
    """)
    return


@app.cell
def _():
    # this is equivalent to: for each word in pretzels.split(), tell me the length of the word

    pretzels = 'these pretzels are making me thirsty!'

    word_lengths = [len(w) for w in pretzels.split()]

    word_lengths
    return (pretzels,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can wrap the left-side expression in its own container to generate smaller sequences of values:

    - note how I include two versions of `w` inside square brackets `[]`, the first `w` returns the value itself, while `len(w)` returns the length of w. Because they are in square brackets, they form their own list inside the larger list.
    """)
    return


@app.cell
def _(pretzels):
    # this is equivalent to: for each word in pretzels.split(), give me the word and the length of a word inside a new list
    word_and_word_lengths = [[w, len(w)] for w in pretzels.split()]
    word_and_word_lengths
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Adding conditions to a list comprehension

    Just as we did with `for loops`, we can add conditional logic to a list comprehension so that only certain values or operations are applied.

    We use the right side of the list comprehension for this (the stuff after the `in`).

    The syntax looks like this:

    > `[expression for value in sequence if condition == True]`

    For example, the following list comprehension includes an `if` statement that checks for whether the character is uppercased:
    """)
    return


@app.cell
def _():
    # Let's make the acronym VUW
    # this is equivalent to: for each character in the string, give me that character if the character is upper cased.
    [letter for letter in 'Victoria University of Wellington' if letter.isupper()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The next example builds upon an earlier example of a `for` loop to find words over five characters long in our grasshopper example. As a reminder, here is what the `for` loop looked like:

    ```
    output = []
    for word2 in grasshopper.split():
      if len(word2) > 5:
        output.append(word2)
    ```

    Now see how the list comprehension does the same thing in a more compact manner:
    """)
    return


@app.cell
def _(grasshopper):
    # give me those words over five letters!
    [word for word in grasshopper.split() if len(word) > 5]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The sky is the limit. You can include as many complex conditional and expressions as you need. Sometimes list comprehensions can become *too* complex and unreadable, but some people enjoy the challenge of making such "one liners".
    """)
    return


@app.cell
def _(grasshopper):
    # can you understand what's going on in this one?
    [[w, w.upper(), len(w)] for w in grasshopper.split() if w.islower() and len(w) > 7]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Should you always use list comprehensions?

    There are a [number of benefits](https://realpython.com/list-comprehension-python/) in using list comprehensions. But there is also something beneficial about writing a `for loop`, especially when you are just starting out. A `for loop` *can* be a bit more readable at first, but you may also find the transition between the two becomes easier over time. If you want to stick with `for loops` in this course, that is okay!
    """)
    return


if __name__ == "__main__":
    app.run()
