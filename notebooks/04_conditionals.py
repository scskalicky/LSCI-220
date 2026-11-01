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
    # Conditional Execution

    Programs need to be able to make decisions at certain points. Conditional expressions allow you to define tests or decision points at which your program will execute a specific action.

    For example, what if you wanted to find all of the uppercase letters in the string `"Victoria University of Wellington"`? You would need to provide Python with a test that it can use to determine uppercased from lowercased characters.

    What if you wanted to find all the words in a book which were over five letters long? Again you would define a test which will be used to determine whether a word should be included or not.

    We use such tests all the time in daily life. Consider the picture below - if you walked past this store and wanted to go inside, you would immediately form a test in your mind in order to determine if the store is open.

    >>> ![](https://raw.githubusercontent.com/scskalicky/LSCI-220/main/images/hours.jpeg)

    - *If today is Monday, then I can't go in the store*
    - *If today is Tuesday and the current time is 1:00, then I can go in the store*
    - *If the lights are on, I can go in the store*

    Using conditional logic in Python is very similar. You use words like `if`, `and`, `or` to develop a set of tests (or *conditions*) which you ask Python to consider. And, depending on the results of the test, you ask Python to do one thing or the other.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Boolean Values and `==`

    - The values `True` and `False` are special values in Python (so don't use these as variable names!). They are called booleans, which means it is only possible to be one thing or the other: if something is `True`, it cannot be `False`, and vice versa.

    - the double equals sign `==` is an important relational operator. This operator tests whether two values are equal. Why the double equal sign? Because the single equal sign (i.e., `=`) is used for variable assignment. Compare below:
    """)
    return


app._unparsable_cell(
    r"""
    # an error because single equal sign is for assigning variables
    'Soda' = 'Soda'
    """,
    name="_"
)


@app.cell
def _():
    # the output is "True" because the two values are equal
    'Soda' == 'Soda'
    return


@app.cell
def _():
    # the output is "False" because the two values are NOT equal (do you see why?)
    'soda' == 'Soda'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The opposite of testing for equality is testing for *inequality*. You can do that with the `!=` operator, which stands for "does not equal"
    """)
    return


@app.cell
def _():
    # these strings are not equal, so the test returns "True"
    'Wellington' != 'Auckland'
    return


@app.cell
def _():
    # these strings are equal, so the test returns "False"
    'kiwi' != 'kiwi'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # `if` statements

    Now that you see how to test for equality, the next step is learning how to execute specific actions depending on the results of an equality test.

    We want to consider tests such as:

     - if two things are equal, perform Action 1
     - if two things are not equal, perform Action 2

     We can use `if` statements to do this in Python. This will formally introduce you to one of the interesting quirks of Python - the use of indentation in the code to establish a hierarchy among the order of execution. An `if` statement looks like this:

    >`if` condition is True:
    >> do something

    Here is what an `if` statement looks like in a code cell:

    ```python
    if time == 1300:
        print('the store is open')
    ```

    The parts of the `if` statement are:

    - `if` starts the statement
    - `time == 1300` is the condition being tested
    - the colon `:` ends the first line (it's easy to forget!)
    - `print('the store is open')` is the body: the code that only runs if the condition is `True`

    Note that the `print()` statement on line 2 is indented so that it is nested underneath the `if` statement. marimo (and most code editors) will add the indentation for you when you press Enter after the colon. If the indentation is missing, like this:

    ```python
    if time == 1300:
    print('the store is open')
    ```

    then running the cell gives you an `IndentationError`, telling you that Python expected an indented block.

    Time to write some `if` statements! First, use the number box below to choose a time. It uses the 24-hour clock, so 1300 is 1pm. The store examples in this notebook all use this time, and once you've run them they re-run automatically whenever you change it.
    """)
    return


@app.cell
def _(mo):
    # a number box to choose the time (24-hour clock)
    store_time = mo.ui.number(start=0, stop=2359, step=1, value=1300, label='time')
    store_time
    return (store_time,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now run the cell below, which tests whether the store is open at 1pm. Play around with the time in the number box as well as the value after the `==` in the `if` statement. While this is a successful test, it is also restricted to a single value, so we will explore how to make this test more interesting.
    """)
    return


@app.cell
def _(store_time):
    # is the store open at 1pm?
    if store_time.value == 1300:
      print('the store is open')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now change the time in the number box to 1400 (2pm). The output of the cell above disappears, and nothing seems to happen. What's going on? There is no error or problem here, the code did exactly what it was asked to do. The thing is, because the conditional test did not evaluate to `True`, the `print()` function was never used. So we clearly need a way to perform more than one thing, depending on if a test passes or fails any particular condition.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `else` statements

    But before moving on to more complex conditions, let's focus on adding to our current `if` statement. Right now, the code in the cells above only does one thing, and only if the conditional test results in `True`. If the result of the test is `False`, nothing happens!

    This demonstrates the logic here - the code nested under the `if` statement will only trigger when the `if` statement is true.

    But what if we also want to do something if the statement is False? This is where we want to combine `if` with `else`.
    """)
    return


@app.cell
def _(store_time):
    # the same number box as above - changing either one changes both
    store_time
    return


@app.cell
def _(store_time):
    # check if the time is NOT equal to 1300
    # when the time is 1300, nothing prints, because the test returns False
    if store_time.value != 1300:
      print('the time is not 1300')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can add an alternative command to the code using the `else` statement. You can think of `if` and `else` exactly the same as real life:

    - `if` you are hungry, get some food. `else`, watch some tv.
    - `if` you are tired, go to sleep. `else`, do some work.
    - `if` you can fly, that's crazy. `else`, that's normal.

    To add an `else` statement to an `if` statement, you add `else` after the body of the `if` statement, with the indentation matching between the `if` and the `else`. And, the body of `else` needs to be indented just the same way the body for `if` was indented. You can see how indentation is used to determine how different parts of the program will be run:

    ```python
    if time == 1300:
        print('the store is open')
    else:
        print('the store is closed')
    ```

    - `else` lines up with `if`, and also ends with a colon
    - the body of `else` is indented, just like the body of `if`

    You can run the code cell below to see what will happen.

    Try changing the time in the number box to get the code cell to print different statements.
    """)
    return


@app.cell
def _(store_time):
    # the same number box as above - changing either one changes both
    store_time
    return


@app.cell
def _(store_time):
    # now our code will do something when the conditional is False or True
    if store_time.value == 1300:
      print('the store is open')
    else:
      print('the store is closed')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The way these `if` and `else` statements work is that the program will perform the tests in order.

    1. First, the `if` statement will be tested, and if the condition in that statement returns `False`, then the program will move down to the next test.

    2. If the first `if` statement returns `True`, then the program will *not* go on to the `else` statement.

    This order of operations becomes more complex as one adds more `if` and `else` statements, and you can also put `if` statements inside other `if` statements! But for now, this should give you the basics behind the if statement, and reading the Chapter 1, Section 4 in the NLTK Book will also help.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `elif` statements

    Another control statement is the `elif` statement, which is a combination of `if` and `else`. Both `elif` and `else` must come after an initial `if` statement. Using `elif` allows you to include more than one possible outcome if the result of the initial `if` statement returns False.

    1. An `if` and one `else` allows you to consider two possibilities
    2. An `if`, one `elif`, and one `else` allows you to account for three possibilities.
    3. And so on...

    The syntax of `elif` is the same as an `else` statement — consider the code cells below - try changing the value of `number` so that you can get each of the different print statements to work.

    Below, you will see the `<` sign, which means "less than"
    """)
    return


@app.cell
def _():
    number = 1

    if number < 5:
      print('number less than 5')
    elif number < 8:
      print('number is less than 8')
    elif number < 9:
      print('number is less than 9')
    else:
      print('number must be 9 or higher')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # More relational operators

    There are a number of different operators in addition to the `==` and `!=` operators which can compare general relations between two values:

    - x `>` y — is x greater than y?
    - x `>=` y — is x greater than or equal to y?
    - x `<` y — is x less than y?
    - x `<=` y — is x less than or equal to y

    These operators look like they might only work for numerical data, but you can actually compare strings using these methods.
    """)
    return


@app.cell
def _():
    # Is Wellington greater than Auckland?
    'Wellington' > 'Auckland'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The reason this works is because you are comparing the numbers that represent each character. Every character has a number, called its Unicode code point. This is similar to alphabetical order, but not quite the same: for example, every uppercase letter comes before every lowercase letter.
    """)
    return


@app.cell
def _():
    'a' > 'b'
    return


@app.cell
def _():
    'ab' > 'a'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can actually see the numerical representation using the `ord()` function:

    97 is less than 98, so a is less than b. Interesting, but perhaps not very useful for most of our purposes.
    """)
    return


@app.cell
def _():
    ord('a')
    return


@app.cell
def _():
    ord('b')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Adding logic: `and` & `or`

    In addition to the comparative operators, there are logical operators which allow us to place more specific constraints on our conditional statements:

    - x `and` y — both x and y must be `True`
    - x `or` y — either x or y must be `True`

    What are the philosophies of `and` & `or`?

    `and` (the enforcer)
     - everything must be `True` or else nothing is true!

    `or` (the optimist)
    - just needs one thing to be `True`
    """)
    return


@app.cell
def _():
    # and needs everything to be true
    5 == 5 and 1 == 1
    return


@app.cell
def _():
    # or just needs one thing to be true
    5 == 5 or 5 == 2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can now create more specific conditions to determine if we can go into a store at certain times. Let's write a conditional statement that asks whether the time is at or after 10am `and` at or before 5pm.

    Try changing the time in the number box to get the program to return different results.
    """)
    return


@app.cell
def _(store_time):
    # the same number box as above - changing either one changes both
    store_time
    return


@app.cell
def _(store_time):
    if store_time.value >= 1000 and store_time.value <= 1700:
      print('store is open!')
    else:
      print('store is closed!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Adding logic: `in` and `not`

    Let's wrap this up by looking at two more operators:

    - x `in` y — is x within y?
    - `not` x — is x not something?

    The use of `in` is very helpful if you would like to quickly check whether a single value is within a data container, such as lists. You could also search within other sequences, such as strings.
    """)
    return


@app.cell
def _():
    # is the character "a" in this word?
    'a' in 'Melodrama'
    return


@app.cell
def _():
    # it should be noted that capitalization matters!
    'A' in 'Melodrama'
    return


@app.cell
def _():
    # now consider a list
    'Melodrama' in ['Pure Heroine', 'Melodrama', 'Solar Power', 'Virgin']
    return


@app.cell
def _():
    # This returns False? why?
    # Because even though the character "a" exists in some values in the list, there is no single value of 'a' in this list.
    'a' in ['Pure Heroine', 'Melodrama', 'Solar Power', 'Virgin']
    return


@app.cell
def _():
    # adding 'a' as a member of the list now returns True
    'a' in ['Pure Heroine', 'Melodrama', 'Solar Power', 'Virgin', 'a']
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `not` operator is a bit trickier. `not` flips `True` to `False` and `False` to `True`, and it can go in front of any value or test (for example, `not 5 == 2` is `True`). This makes it seem like it can only be used for testing `True` versus `False`. However, it's a bit fuzzier than that and has to do with truthiness. Basically, any value which exists is `True` when asking if that value exists (a bit circular, I know).

    Examples help:
    """)
    return


@app.cell
def _():
    # True is True, so not True is False
    not True
    return


@app.cell
def _():
    # False is False, so not False is True
    not False
    return


@app.cell
def _():
    # define an empty string, it has no value
    # so it is not True and thus returns True if you check if it is not True
    # confused yet?

    my_empty_variable = ''

    not my_empty_variable
    return


@app.cell
def _():
    # but this variable has something in it, it exists, it is True
    my_full_variable = 'stuff'
    not my_full_variable
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The benefits of knowing about how values return `True` or `False` is that you can use this as a shorthand to check if something exists or not. This might not seem immediately useful for now, but it will come back later. A short demonstration:
    """)
    return


@app.function
# write a function to print the first character of a string:
def print_first_char(x):
  print(x[0])


@app.cell
def _():
    # run the function on the string "VUW"
    print_first_char('VUW')
    return


@app.cell
def _():
    # Run the function on an empty string - which gives an error
    print_first_char('')
    return


@app.function
# we can update our function with a safety check to make sure the string has a value
def print_first_char_v2(x):

  # this asks "if x exists" (the inverse of using `not`)
  if x:
    print(x[0])
  # if x does not exist, do this instead
  else:
    print('nothing here!')


@app.cell
def _():
    #function works as before with a string
    print_first_char_v2('VUW')
    return


@app.cell
def _():
    # function now doesn't crash when given an empty string.
    print_first_char_v2('')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Your Turn**

    This notebook has gone through quite a lot of conditionals and operators. You should take the time to ensure you can construct some `if` statements as well as some simple to complex conditional statements. But don't worry — these things will be used over and over again in the rest of the notebooks, so you should gain more and more familiarity with them over time.

    If you'd like to test yourself, see if you can write an `if` statement which checks whether a word is longer than a certain number of characters and is also lower case. You could use `len()` to check the length and the string function `.islower()` to check if all characters in a string are lower case.

    In the code cell below is an example doing the opposite: checking if a word is no longer than a certain number of characters and is also all caps.
    """)
    return


@app.cell
def _():
    word = 'VUW'
    return (word,)


@app.cell
def _(word):
    if len(word) <= 3 and word.isupper():
      print('found a short word which is all caps')
    return


@app.cell
def _():
    # use this code cell to write your own if statement!


    return


if __name__ == "__main__":
    app.run()
