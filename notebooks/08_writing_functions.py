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

    [NLTK Book, Chapter 2, Section 3.2](https://www.nltk.org/book/ch02.html#function_index_term)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Writing Functions

    We've already seen how functions are used and have written some of our own functions. This notebook will now explain these concepts in a little bit more detail.

    Lots of our code cells do things in a temporary manner - if we write a `for loop` or print out a bunch of information, that code is limited to the code cell it was written in. Writing a function allows us to store a procedure/operation in memory and reuse it. Moreover, writing several functions which work together is a key to writing structured *programs*.

    You may have noticed that the word *program* pops up here and there. And while we can argue that a single function we have made is technically a program, programs are usually a series of many different functions. You've seen how NLTK groups functions into different modules for different things, and this is pretty common among different packages. While we aren't going to be making modules or packages, we can start looking at developing a set of cooperative functions as a means to create an NLP pipeline.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Syntax of a function

    You've already seen how to write a function. We define a function using `def` and then assign a function name, much the same as we name variables. Functions are similar to `if statements` and `for loops` in that they have a header, followed by a colon, followed by an indented block which contains the body of the function.

    ```
    def function_name():
      stuff function does

    ```
    """)
    return


@app.function
# make a useless function
def printer(x):
  print(x)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that when I defined `printer()` above, I included an `x` in the parentheses of the function. And, inside the function, I have asked the function to do something with `x` (i.e., use `print()` on `x`).

    By declaring my function with the `x`, I am including a required `argument` to my function. The function will *not* work unless the user includes a value for `x`. You can basically think of `x` as a required variable that must be supplied. For example:
    """)
    return


@app.cell
def _():
    # supply a string to our printer() function.
    printer('this dream isn\'t feeling sweet')
    return


@app.cell
def _():
    # supply nothing to our printer function.
    printer()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If you run the cell above you get:

    ```
    TypeError: printer() missing 1 required positional argument: 'x'
    ```

    In other words, the function is complaining that it was not provided with the sufficient information it needs to work.

    You can also provide default values for arguments in functions. For example, we could make our default argument for `printer()` a string which tells the user that they have not entered a value:
    """)
    return


@app.function
def printer2(x = 'please enter a string'):
  print(x)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can run the new version, `printer2()`, without an argument, although it's a bit silly. In some ways it would be better to provide an error which teaches the user they need to enter a string to use the function properly.
    """)
    return


@app.cell
def _():
    # we don't get an error anymore, but still isn't overly useful :)
    printer2()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Function variable scope

    Another benefit of using functions is that it helps us avoid accidentally overwriting variables or running into other issues with variable names. This introduces us to the concept of variable scope. The main distinction in variable scope is between **global** scope and **local** scope. Essentially, global scope refers to your entire Python environment, and something which is global can be accessed anywhere and from anything. Local scope, on the other hand, restricts variables to the functions and classes they belong to.

    In marimo, a variable created in a cell (outside of any function) is global: it is available to every other cell. For example, if I declare a variable in the next code cell, that variable is available to other code cells:
    """)
    return


@app.cell
def _():
    # defining a variable here is in global scope
    ribs = "And I've never felt more alone, It feels so scary getting old"
    return (ribs,)


@app.cell
def _(ribs):
    # which I can access in this code cell
    [i.upper() for i in ribs.split()]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    However, if I define a variable in local scope, such as within a function, that variable is only available in that function.
    """)
    return


@app.function
def fragile():
  # note that I am assigning a variable just like you do anywhere else
   song = 'She reads the minds of all the people as they pass her by'
   print(song)


@app.cell
def _():
    # function works great
    fragile()
    return


@app.cell
def _(song):
    # but if I try to access `song` here?
    print(song)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I get an `is not defined` error, meaning there is no such variable named `song` available in the context I asked for it in (i.e., in the global scope).

    So, using functions allows us to avoid all kinds of problems *and* perform some good tricks when it comes to variables. Perhaps most specifically, I could run a `for loop` in function A and another `for loop` in function B using the same internal variable names, and I would not need to worry about any cross contamination of the variable names between the functions. Scope is a bit more complicated than I've presented it here, but I just want to make sure you see the difference, and also understand that one benefit of functions is to help us sanitize our global environment from rambling variables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Building a less useless function

    We can make much better functions than `printer()`, which is just a shell around the pre-existing `print()` function in Python. Almost anything we've already seen in Python can be done within a function, such as including conditional statements, looping, list comprehensions, and so on.

    We can also use arguments not just as data which is passed to the function, but also as flags and switches the user can use to control the way a function works. Let's explore this now.

    Let's write a function called `pre_process1()` which allows for a variety of text cleaning options. We'll start by asking our function to lowercase a string.
    """)
    return


@app.function
# pre_process1 returns a lowercased string
def pre_process1(x):
  x = x.lower() # create a lower cased version of x
  return x


@app.cell
def _():
    # test the function:
    pre_process1('WELLINGTON')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### the `return` statement

    `pre_process1()` includes a `return` statement, which means the function will output a particular value (or set of values). In the case of `pre_process1()`, the output is the lowercased string. We'll continue using `return` statements to make our functions be able to pass data to and from one another.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's now add another operation to our function, removing punctuation.
    """)
    return


@app.function
def pre_process2(x):
  # define a set of punctuation marks
  punctuation = '.;"!\'[]{}:><-_?,'

  # lower case
  x = x.lower()

  # keep all letters in x, unless the letter is in punctuation
  x = ''.join([x for x in x if x not in punctuation])

  return x


@app.cell
def _():
    # the output is all lower case with no punctuation.
    pre_process2('We\'re never done with killing time. Can I kill it with you?')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Arguments controlling conditionals

    Now, let's provide the option for the user to choose exactly how the string will be pre-processed. We can do so by adding more arguments and some conditional logic inside the function. I add two arguments to the function, `lower` and `remove_punc`. I set the default values of both to `True`.

    Then I used a series of conditional `if` statements to determine if the string should be processed in different ways. The defaults being `True` means that they will run unless the user explicitly sets the arguments to `False`.
    """)
    return


@app.function
# define with default values of True for lower and remove_punc arguments
def pre_process3(x, lower = True, remove_punc = True):

  if lower == True:

    # x will not be lowercase unless lower == True (the default)
    x = x.lower()

  if remove_punc == True:

    # this variable won't be declared unless remove_punc == True (the default)
    punctuation = '.;"!\'[]{}:><-_?,'

    # this join and list comprehension won't trigger unless remove_punc == True
    x = ''.join([char for char in x if char not in punctuation])

  return x


@app.cell
def _():
    target_string = 'We\'re never done with killing time. Can I kill it with you?'
    return (target_string,)


@app.cell
def _(target_string):
    # use the function to only remove punc - capitals still remain
    pre_process3(target_string, lower = False)
    return


@app.cell
def _(target_string):
    # or to only lowercase - punctuation still remains
    pre_process3(target_string, remove_punc = False)
    return


@app.cell
def _(target_string):
    # default behaviour if we don't set the flags:
    pre_process3(target_string)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chaining functions

    Now that we have our cute little pre-processing function, let's use it within *another* function. For instance, we could develop a tokenizer function which pre-processes each token of a string. Let's use good old `str.split()` for now.
    """)
    return


@app.function
# a simple tokenizer on whitespace
def tokenizer(x):
  x = x.split()
  return x


@app.cell
def _():
    # let's save our target string to a variable
    target = "What if you could look right through the cracks? Would you find yourself? Find yourself afraid to see?"
    return (target,)


@app.cell
def _(target):
    # our function works! It returns a list of tokens.
    tokenizer(target)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Okay, now let's use our functions together. We've already been doing this in for loops and other repeated actions, and here is another example, where I use the `pre_process3()` function on each token returned by the `tokenizer()` function:
    """)
    return


@app.cell
def _(target):
    # first create the tokens
    for token in tokenizer(target):
      # then preprocess each token
      token = pre_process3(token)
      print(token)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We printed the results above, which isn't ideal. Let's make yet *another* function which uses our `tokenizer()` and `pre_process3()` functions to return the results (so that they could be kept/used elsewhere rather than just being printed).

    I need to do a bit more here to make the output make sense.

    In line 4, I create my list of tokens.

    Because this is a list, I need to either loop or use a list comprehension to get all of my values back (line 7).

    Then if I want everything as a string I need to use `' '.join()` on that list comprehension to get it all back, which I include within the `return` statement on line 10.

    As you can probably imagine, there are a variety of ways things can go wrong during this process!
    """)
    return


@app.function
# make my pipeline function
def pipeline(x):
  # first create a tokenized list
  tokens = tokenizer(x)

  # then use a list comprehension to apply pre_process3 to each individual token
  processed = [pre_process3(token) for token in tokens]

  # return the joined version to make it back into a single string
  return ' '.join(processed)


@app.cell
def _(target):
    # it works
    pipeline(target)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Adding defenses to our program

    Our program is doing okay for itself eh? But, what happens if we pass something that isn't a string?
    """)
    return


@app.cell
def _():
    pipeline(123)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We get an error because all of our functions are assuming a string is being entered. However, a user might not know this, or we might do something somewhere along the lines that doesn't play nice with strings.

    One way to address this is to add checks to our function which will ensure the input is what we want. There are a variety of ways to do this — `assert` statements are one method to do so and the one explained in Chapter 4 of NLTK. There are other methods we can use as well, such as `try` and `except` statements.

    We could also be less fancy and write a simple `if` statement with `type()` to check the `Type` and prevent the program from proceeding unless we have the desired `Type`
    """)
    return


@app.function
def pipeline2(x):

  # before doing anything else, is x a str?
  if type(x) != str:
    print('Please enter a string!')

  else:
    tokens = tokenizer(x)
    processed = [pre_process3(token) for token in tokens]
    return ' '.join(processed)


@app.cell
def _(target):
    pipeline2(target)
    return


@app.cell
def _():
    # We tell the user they need to enter a string.
    pipeline2(1337)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As I said there are a number of other ways to inform the user of what values to enter — but perhaps for this course and other applications your "user" is really just "you", so writing your functions defensively is a way to help you help yourself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Writing a `load_text` program

    Let's create a function which loads texts for us, so that we can automate typing the same lines each time we want to load a text. Why? We might find that we are constantly loading texts from the internet, like we did with `requests` in the for loops notebook. We might want to write a simple function to do this for us, so we can use it in many different places. A simple function can help us do this more programmatically and allow for some more pre-processing.

    First, import the `requests` library:
    """)
    return


@app.cell
def _():
    # import requests to load texts from the internet
    import requests

    return (requests,)


@app.cell
def _(requests):
    # create a program which loads and reads texts from a URL.
    def load_text1(url):
      """loads a text from a URL and returns it as a string"""
      text = requests.get(url).text
      return text

    return (load_text1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note in the program above I include a [`docstring`](https://peps.python.org/pep-0257/), which is the triple quoted description of the function inside the cell. You can see the docstring of any function (including the ones built into Python and NLTK) using `help()`:
    """)
    return


@app.cell
def _(load_text1):
    # the text in the triple quotes is called a docstring
    # help() shows you the docstring of any function
    help(load_text1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I'll test my program on a short text, the fable of the ants and the grasshopper:
    """)
    return


@app.cell
def _(load_text1):
    # save the url to a variable
    grasshopper_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/grasshopper.txt'

    load_text1(grasshopper_url)
    return (grasshopper_url,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Sweet, it works. We could then add a feature to `load_text` that lowercases the words, right? And in fact we could do this in one line:
    """)
    return


@app.cell
def _(requests):
    def load_text2(url):
      """loads a text from a URL and returns it as a lowercased string"""
      text = requests.get(url).text.lower() # read in and lowercase the string
      return text

    return (load_text2,)


@app.cell
def _(grasshopper_url, load_text2):
    load_text2(grasshopper_url)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As shown below, we could then *further* revise the function to make lower-casing optional by adding a toggle argument
    """)
    return


@app.cell
def _(requests):
    def load_text3(url, lower = True):
      """loads a text from a URL and returns it as a string, lowercased unless lower = False"""
      if lower == True:   # add condition for lowercasing
        text = requests.get(url).text.lower()
      else:
        text = requests.get(url).text
      return text

    return (load_text3,)


@app.cell
def _(grasshopper_url, load_text3):
    # default will return lower cased
    load_text3(grasshopper_url)
    return


@app.cell
def _(grasshopper_url, load_text3):
    # but we can turn that off if we like
    load_text3(grasshopper_url, lower = False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A helper function such as `load_text3()` becomes worthwhile to make because it saves you a lot of time retyping, but also because it brings consistency to your program and reduces error. Knowing that you can call `load_text3()` multiple times in a program and that each time it will work the same way means you don't have to worry about inconsistencies or even typos. Also, you can change `load_text3()` just one time and then it will change all instances of `load_text3()`.

    Future notebooks will continue exploring how to chain functions together (and some other stuff). However, you might find it worthwhile to take a moment here and create two small functions which work with one another. For example, you could try creating a tokenizer function and a function which calculates the TTR of a list of tokens, and then use them together, or any other combination of things.
    """)
    return


@app.cell
def _():
    # use this code cell to write two functions that work together!
    return


if __name__ == "__main__":
    app.run()
