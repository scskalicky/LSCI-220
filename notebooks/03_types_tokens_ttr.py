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

    [NLTK Book, Chapter 1, Section 1.4](https://www.nltk.org/book/ch01.html#token_index_term)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **What is a word?**

    This might seem like a silly question, but it's a crucial one to ask when we want to think about the computational representation of text and language. We have seen how text can be stored as a single string in Python, and there are no real limits to how long this string can be. But a string is still seen as a single sequence of characters, and thus the most interesting information we can obtain from a string is how long a string is in terms of number of characters.

    What if we wanted to know how many words are in a string? What about sentences? Paragraphs?

    We need a method to *split* or *segment* the string so that we can extract the individual words. That means we need to create a set of rules or principles by which we can determine individual words in a string.

    Hence the question: what is a word? Or, perhaps phrased slightly differently, how do we distinguish words from one another when reading? The answer for written English and many other written forms of language is relatively simple - whitespace. The spaces between words represent simple yet effective boundaries to indicate where words begin and end. (Note that other languages, such as Chinese, do **not** use whitespace, which means many of the methods we use in this notebook require adaptation when applied to other languages).

    Let us proceed for the moment with the knowledge that segmenting words on whitespace could be a helpful way to split a string representing English into individual words. And, it just so happens that Python has a built-in function which allows us to do this with ease: the `string.split()` function.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Using `.split()` to create words from strings.

     `.split()` is a string method which means it is specific to string types. By default, `.split()` will search a string for any whitespace character and then split the string on those whitespaces. The whitespaces will be effectively removed from the string, and the resulting segments will be placed into a list, with each segment representing a value in the list. Consider the example below:
    """)
    return


@app.cell
def _():
    # define a string and save it to a variable
    pretzels = 'these pretzels are making me thirsty'

    # use .split() to convert the string into a list of segments split on whitespace
    pretzels.split()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pretty neat, right? What's more is that `.split()` can be used to split a string on **any** character one likes - the default is whitespace but you could choose anything, such as a certain character or letter:
    """)
    return


@app.cell
def _():
    # split at "o", note that the "o" is not included in the output (just like whitespace)
    'Melodrama'.split('o')
    return


@app.cell
def _():
    # split the same string on a repeated letter:

    'Melodrama'.split('a')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Can you figure out how to use `.split()` as a means to count the total number of words in a string? Hint: do you remember the `len()` function? Use `.split()` to count the number of words in the following sentence:
    """)
    return


@app.cell
def _():
    # can you use .split() and len() to find the total number of words in this sentence?
    # the "\" is used to 'escape' the quote so that python doesn't read it as a delimiter
    example = 'what if everything around you isn\'t quite as it seems?'
    return (example,)


@app.cell
def _(example):
    # the answer...
    len(example.split())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that we don't actually need to save the string to a variable first - we could wrap `len()` around the string, we just have to keep our brackets in the right place!

    However, saving as a variable sure is a bit more tidy.
    """)
    return


@app.cell
def _():
    len('what if everything around you isn\'t quite as it seems?'.split())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Types and Tokens

    Now that we know how to split a string into different words, we can start using Python to count the number of words in a string. Not only can we find the total number of words in a string, we can also find the total number of *unique* words. The distinction between unique words and total words has specific terminology:

    - A ***type*** is a unique word.
    - A ***token*** is an individual occurrence of a type.

    For example - pretend you had three pets at home: two dogs and a cat. If we sorted our pets into types and tokens, we would have three tokens (three pets total), but only two types: dog and cat.

    In Section 1.4 of Chapter 1, the NLTK book asks you to think about types and tokens by introducing you to the `set()` and `len()` functions. You have already used `len()`, but `set()` might be new. Using `set()` returns a data container that only allows one of any value to exist in the container. In other words, it returns an object where repeated values are not allowed.

    This means we can use `set()` to ask for unique values in our data.
    """)
    return


@app.cell
def _():
    # For example, what does set() give you here?
    set('aaabbbccc')
    return


@app.cell
def _():
    # and here?
    set(['a', 'a', 'a', 'b', 'b', 'b', 'c','c', 'c'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's think about how to use `len()`and `set()` to compute the Types and Tokens for a string.

    - First we'll define a string (save it as a variable)
    - then we will split the string into a list of "words"
    - then we will measure the length of the list
    - then we will measure the length of unique items in the list

    We'll also chain some of these functions together and save them to new variables.
    """)
    return


@app.cell
def _():
    # start with a string
    mood_raw = "i can\'t feel a thing, i keep looking at my mood ring"

    # create a split version
    mood_tokens = mood_raw.split()

    # compare the before/after
    print(mood_raw, '\n\n', mood_tokens)
    return mood_raw, mood_tokens


@app.cell
def _(mood_tokens):
    # measure the total number of words
    total_mood_tokens = len(mood_tokens)
    total_mood_tokens
    return


@app.cell
def _(mood_raw):
    # measure the number of types
    # how else could you write this code for the same effect?
    total_mood_types = len(set(mood_raw.split()))
    total_mood_types
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    Before moving on, make sure you are comfortable with the difference between types and tokens, as well as how to use `len()` and `set()`.
    """)
    return


@app.cell
def _():
    # take this moment to practice with set() and len()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Measuring Lexical Diversity**
    We can now use this information to assess our text for lexical diversity: how varied the words in a text are. One very basic measure of lexical diversity is the type-token ratio (TTR), which tells us how many repeated words there are in a text. You can read more about it in [Chapter 1 of NLTK.](https://www.nltk.org/book/ch01.html)

    To calculate lexical diversity, we can use the following formula:

    <br>

    $$
    \text{TTR} = \frac{\text{number of types}}{\text{number of tokens}}
    $$

    <br>

    The code cell below creates a user-defined **function** named `lexical_diversity()` to calculate lexical diversity. Running the code cell below will load the function into memory, allowing you to use it just like other functions such as `print()`, `len()`, and `set()`.

    The name of the function is `lexical_diversity`, and it expects an input called `tokens`.

    The function will `return` (i.e., give back) the number of unique tokens (`len(set(tokens))`) divided by the number of tokens (`len(tokens)`).

    Creating functions will be covered in more detail later on.
    """)
    return


@app.function
# define a function to calculate lexical diversity

def lexical_diversity(tokens):
  # return the result of dividing the length
  return len(set(tokens))/len(tokens)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To use the function, we just need to type its name and provide a list of tokens as the argument. So, what is the lexical diversity or TTR of our example sentence?
    """)
    return


@app.cell
def _(mood_tokens):
    # what is the TTR of our example sentence?
    # we already made a list of tokens (mood_tokens) above, so we can use it here
    lexical_diversity(mood_tokens)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We get a result of .916, which means there are 0.916 types for every token: almost every token is a different word, indicating a very high lexical diversity.

    Let this sink in for a moment. If each token was represented by a unique type, that means every single word in a text would be unique, and the ratio of types to tokens would be 1:1, or 100%.

    There are almost no cases in which an authentic text has 100% lexical diversity, *unless* it is an extremely short text. So, such measures are strongly influenced by the length of a text - a more useful application of lexical diversity would be to compare larger texts against one another. We will get there later.

    For now, try the lexical diversity function on some examples yourself to see how repeating words influence the overall score.

    > ***Important!*** You need to feed a list of tokens to `lexical_diversity()`, otherwise you will get the diversity based on **characters** in the string, not words! What could you do to modify this?
    """)
    return


@app.cell
def _():
    # Lexical diversity of 50%
    # two types, four tokens
    # 2/4 = .5 (50%)

    lexical_diversity('hello world hello world'.split())
    return


@app.cell
def _():
    # Lexical diversity of 100%
    # two types, two tokens
    # 2/2 = 1 (100%)

    lexical_diversity('hello world'.split())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    Try out the lexical diversity function on some text. The function expects a list of tokens, so use `.split()` first.
    """)
    return


@app.cell
def _():
    # Play with lexical diversity on your own examples
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Comparing Lexical Diversity of Two Texts

    Now that we know how to calculate the lexical diversity of a single text, let's expand the function to compare the lexical diversity of two texts.

    We will also modify the function so that you can input a raw string to the function, rather than a list of tokens. Read the comments to see if you understand how the function works.

    Remember, we need to first load the function into memory before we can use it.
    """)
    return


@app.function
# create a new function which takes two texts as arguments:
def compare_lexical_diversity(text1, text2):

  # in one line, calculate LD of text1 using .split()
  text_1_ld = len(set(text1.split()))/len(text1.split())

  # repeat for the second text
  text_2_ld = len(set(text2.split()))/len(text2.split())

  # print out the results using an fstring
  print(f"{text1}\nLexical Diversity: {text_1_ld} \n\n{text2}\nLexical Diversity: {text_2_ld}")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### String Formatting

    You probably see that in the `print()` line in the function above looks a little crazy. It uses something called string formatting, where you can combine variables and text inside a single print statement.

    The `f` in front of the string is all you need to do to activate this format. Then, inside the string delimiters, you can use curly brackets `{}` to include variables and other Python functions.

    The `\n` is a character which stands for newline, which has the same effect as pressing the enter key on your keyboard to create a new line in a text.

    So, the output is going to be something like:

    ```
    contents of text one
    Lexical Diversity: type token ratio of text1

    contents of text two
    Lexical Diversity: type token ratio of text2

    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ok, let's create two texts and analyze them using this new function. You'll see that I use triple quotes as a means to make it easier to encase the entire text on multiple lines. This is mainly for aesthetic reasons.
    """)
    return


@app.cell
def _():
    # create two strings as our texts
    turtles = """teenage mutant ninja turtles
    teenage mutant ninja turtles
    teenage mutant ninja turtles
    heroes in a halfshell turtle power!"""


    baby_shark = """Baby Shark doo-doo doo-doo
    Baby Shark doo-doo doo-doo
    Baby Shark doo-doo doo-doo
    Baby Shark"""
    return baby_shark, turtles


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ok, time to run the function! But, before doing so, can you predict which text *should* be more lexically diverse? Remember, more repetitions of the same word means there will be *lower* lexical diversity. So, which song repeats more words?
    """)
    return


@app.cell
def _(baby_shark, turtles):
    # which song is more lexically diverse?
    compare_lexical_diversity(turtles, baby_shark)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Your Turn**

    Spend some time comparing the lexical diversity of different strings.
    """)
    return


@app.cell
def _():
    # try some lexical diversity calculations here!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Improving Lexical Diversity

    Lexical Diversity based on TTR is in many ways a crude measure of vocabulary diversity. The above examples have used very short texts, and the resulting TTR values are somewhat meaningful. However, TTR has been heavily criticized for being a relatively poor measure of lexical diversity. Why is that? At least for English, one reason is that the overall length of a text will directly influence TTR. Longer texts will naturally start to repeat certain words again, such as function words like `the`, `a`, and `an`.

    To account for this problem, there are a surprisingly large number of different TTR metrics that have been developed. Many of them try to include some sort of average TTR by moving over and calculating TTR for portions of the text, or using some other sort of function which helps address the effects of text length. Some other research also points out that human intuitions or perceptions of lexical diversity are not being captured in measures such as TTR.

    So, know that other measures exist, such as MSTTR (mean segmental TTR), MATTR (moving-average TTR) and MTLD (measure of textual lexical diversity). Chapter 1 of *Defining and measuring lexical diversity* (in the readings) explains several of them. To wrap this notebook up, let's try to "prove" how text length might influence TTR while also getting some practice with function writing :)

    We are going to write a function which splits a text into segments and then calculates the TTR for each segment, and then averages those TTR values to get an average TTR.

    But first, let's consider how we might split a text into sentences. You might have noticed me using the `\n` character in some of the print statements, this character represents a `newline` such as when you press the enter/return key to start a new paragraph.

    Remember that `.split()` will let you split a string on any character, this includes newlines! Consider the text below, it is all encoded as a single string, but because I copied and pasted it from a website in this format, it was retained new lines (I also use triple quotes \"\"\" to allow the string to span across these newlines). Run the cells to see how splitting on newlines can give us sentences:
    """)
    return


@app.cell
def _():
    # Let's read in a longer string

    rwib = """See the animal in his cage that you built.
    Are you sure what side you're on?
    Better not look him too closely in the eye.
    Are you sure what side of the glass you are on?
    See the safety of the life you have built.
    Everything where it belongs
    Feel the hollowness inside of your heart
    And it's all
    Right where it belongs
    What if everything around you
    Isn't quite as it seems?
    What if all the world you think you know
    Is an elaborate dream?
    And if you look at your reflection
    Is it all you want it to be?
    What if you could look right
    Through the cracks?
    Would you find yourself
    Find yourself afraid to see?"""
    return (rwib,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Splitting the string on `\n` means the resulting list will be approximately sentences, rather than single words. Cool!
    """)
    return


@app.cell
def _(rwib):
    rwib.split('\n')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we have figured out a way to split a string into sentences, we can build our average TTR function. I am going to include a `for loop` inside this function. We will cover these in more detail later on, but you might be able to understand the logic of it now. Basically, a `for loop` will repeat the same operation on each member of a specified population.

    If you want to explore the function as it works, you can uncomment the print statements.

    Of course, if you don't want to figure this out now, simply load the function and use it in the cells below.
    """)
    return


@app.function
# define a function named average_ttr
def average_ttr(text):

  # create an empty list to store the TTR values
  ttr_values = []

  # split the raw string input into sentences using the newline character
  # the result is a list with each value being a sentence
  sentences = text.split('\n')

  # loop through each value/sentence of sentences, one at a time.
  for sent in sentences:

    # calculate the TTR of the sentence
    # print(sent)
    sent_ld = len(set(sent.split()))/len(sent.split())

    # add the value to the list using .append()
    ttr_values.append(sent_ld)

  # use sum() to add the TTR values together,
  # then divide by total number of values (using len()) to get average TTR
  # print(ttr_values)
  average_ttr = sum(ttr_values)/len(ttr_values)

  print(f"Average Sentence TTR is: {average_ttr}")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now calculate the average TTR of our `rwib` text. The average TTR is .97 or 97%, meaning it is a pretty diverse text **when we average diversity across the sentences**.

    What do you think about that? Why are we getting such a high average TTR? How long is each sentence in the text?
    """)
    return


@app.cell
def _(rwib):
    average_ttr(rwib)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What happens if we calculate the lexical diversity of the entire song at once? The TTR is much lower! Do you understand why?
    """)
    return


@app.cell
def _(rwib):
    len(set(rwib.split())) / len(rwib.split())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # How does text length affect TTR?

    Let's test this directly with a longer text: the script of the *Seinfeld* episode "The Marine Biologist". The cell below loads the script from the internet and splits it into lowercased tokens.
    """)
    return


@app.cell
def _():
    import requests

    # load the script from the internet as one long string
    mb_url = 'https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/marine_biologist.txt'
    mb_raw = requests.get(mb_url).text

    # lowercase the text and split it into tokens
    mb_tokens = mb_raw.lower().split()

    # how many tokens are in the script?
    len(mb_tokens)
    return (mb_tokens,)


@app.cell
def _(mb_tokens):
    # look at the first bit of the text
    print(mb_tokens[:10])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The slider below chooses how many tokens from the start of the script to include. Drag it from left to right and watch what happens to the TTR in the cell after it.
    """)
    return


@app.cell
def _(mb_tokens, mo):
    # a slider to choose how many tokens to include
    length_slider = mo.ui.slider(start=50, stop=len(mb_tokens), step=50, label='number of tokens', show_value=True)
    length_slider
    return (length_slider,)


@app.cell
def _(length_slider, mb_tokens):
    # take the first however-many tokens chosen with the slider
    mb_sample = mb_tokens[:length_slider.value]

    # calculate the TTR of that sample
    print(f"TTR of the first {length_slider.value} tokens: {lexical_diversity(mb_sample)}")
    return (mb_sample,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Equal-sized segments

    The `average_ttr()` function above is close to a real measure called **mean segmental TTR (MSTTR)**. MSTTR also splits a text into segments, calculates the TTR of each one, and then averages them.

    The difference is that MSTTR makes every segment the **same size** (for example, 50 tokens). Our `average_ttr()` used lines of the song, which were only 3 to 9 words long. Very short segments almost always have a TTR close to 1, which is why we got such a high average.

    The function below splits a list of tokens into chunks of the same size and averages their TTRs. Any leftover tokens at the end that don't fill a whole chunk are ignored.
    """)
    return


@app.function
def segmental_ttr(tokens, chunk_size):

  # create an empty list to store the TTR values
  ttr_values = []

  # step through the tokens one chunk at a time
  # range(0, len(tokens) - chunk_size + 1, chunk_size) gives the starting index of each chunk
  for start in range(0, len(tokens) - chunk_size + 1, chunk_size):

    # slice out one chunk of tokens
    chunk = tokens[start:start + chunk_size]

    # calculate the TTR of the chunk and add it to the list
    ttr_values.append(lexical_diversity(chunk))

  # average the TTR values
  return sum(ttr_values) / len(ttr_values)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The cells below show the slider again and compare plain TTR and MSTTR (with chunks of 50 tokens) for the same sample. Move the slider. Which measure changes more as the text gets longer?
    """)
    return


@app.cell
def _(length_slider):
    # the same slider as above - here for convenience
    length_slider
    return


@app.cell
def _(length_slider, mb_sample):
    print(f"Number of tokens: {length_slider.value}")
    print(f"TTR: {lexical_diversity(mb_sample)}")
    print(f"MSTTR (chunks of 50): {segmental_ttr(mb_sample, 50)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Discussion

    Play around with the average TTR function and different texts.
    - You might want to explore splitting texts on different things besides newlines such as periods
    - How does the average TTR function compare to the whole text TTR? Compare the results between the two for the same texts.
    - Does calculating average sentence TTR create any new problems with TTR?
    - If you wanted to compare the lexical diversity of two texts of very different lengths, which measure would you use, and why?
    """)
    return


if __name__ == "__main__":
    app.run()
