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
    #### Relevant readings

    [NLTK Book, Chapter 2, Section 1](https://www.nltk.org/book/ch02.html)

    McEnery & Hardie (2012), *Corpus Linguistics*, Chapter 1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Corpora**

    A corpus is a large collection of language - usually a collection of texts. But a corpus is more than just a pile of texts: a corpus usually also contains **metadata** telling the user about different categories *within* the corpus. Categories can be anything - genre, author, speaker, year, task, etc.

    It is important to note that some of the examples used in Chapter 1 of NLTK were pedagogical; the authors have provided us with corpora and texts that have already been pre-processed in various ways, or otherwise simplified.

    In this notebook, we will:

    1. explore some of the corpora built into NLTK
    2. create our own corpus from a folder of text files
    3. create a corpus with categories, using information in the file names
    4. think about what a corpus can (and can't) represent

    Run the following cell to load in the libraries and resources for this notebook.
    """)
    return


@app.cell
def _():
    # all the libraries this notebook uses
    import io
    import os
    import zipfile
    from glob import glob
    import requests
    import nltk
    from nltk.corpus import PlaintextCorpusReader
    from nltk.corpus.reader.plaintext import CategorizedPlaintextCorpusReader
    from nltk.text import Text

    # download NLTK resources for this notebook (takes a bit)
    nltk.download(['gutenberg', 'punkt_tab', 'brown', 'state_union'])

    # allow NLTK to read corpora from the current folder (where our own corpora will be saved)
    nltk.data.path.append('.')
    return (
        CategorizedPlaintextCorpusReader,
        PlaintextCorpusReader,
        Text,
        glob,
        io,
        nltk,
        os,
        requests,
        zipfile,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **NLTK corpora**

    ## The Gutenberg Corpus

    A good example of a corpus with different categories is the Gutenberg corpus used by NLTK, which is a collection of different public domain books. [Project Gutenberg](https://www.gutenberg.org/) is a website containing thousands of free eBooks, and is named after [Johannes Gutenberg](https://en.wikipedia.org/wiki/Johannes_Gutenberg), associated with the development of the printing press.

    The Gutenberg corpus is part of the `nltk.corpus` module, which provides several built-in methods for working with text data. You can see a complete list of the methods here: [NLTK corpus package](https://www.nltk.org/api/nltk.corpus.html). You can also see a breakdown in Table 1.3 in Chapter 2 of the NLTK book.

    Please note that NLTK includes just a small set of books from Project Gutenberg. We access the gutenberg data using `nltk.corpus.gutenberg` followed by different NLTK functions and methods.

    To see the list of all of the files, we use the `.fileids()` method. The filenames are in the form of `author-title.txt`
    """)
    return


@app.cell
def _(nltk):
    # inspect the different files in the gutenberg corpus - have you read any of these books?
    nltk.corpus.gutenberg.fileids()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the `.fileids()` represent some metadata — the file id contains both the author and the name of the text. So, in this corpus, there are different texts grouped by different authors. As such, *authors* represent the *categories* of this corpus.

    Chapter 2 introduces you to the methods associated with the NLTK corpus class somewhat implicitly, but it is good to look through all the possibilities. Perhaps the most basic possibility is to use the `.raw()` method to obtain a view of the raw text file.

    Note that we need to input the fileid of the text we are interested in.
    """)
    return


@app.cell
def _(nltk):
    # we can select a single book using the book's name and the format we want, such as words or sentences.
    # We use `raw` to get the raw text file (as a string)
    macbeth = nltk.corpus.gutenberg.raw('shakespeare-macbeth.txt')

    # look at the entire text file.
    macbeth
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are different methods for sorting the corpus into words and sentences:
    """)
    return


@app.cell
def _(nltk):
    # the .words method returns words as tokens
    macbeth_words = nltk.corpus.gutenberg.words('shakespeare-macbeth.txt')
    macbeth_words[0:10]
    return


@app.cell
def _(nltk):
    # could we do this on our own?
    # why do we get different results when we manually split the text?
    # do you think .words is using .split(), or nltk.word_tokenize()?
    nltk.corpus.gutenberg.raw('shakespeare-macbeth.txt').split()[:10]
    return


@app.cell
def _(nltk):
    # use .sents to get the sentences
    macbeth_sents = nltk.corpus.gutenberg.sents('shakespeare-macbeth.txt')
    macbeth_sents[0:2]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Chapter 2 also provides a discussion about how to import Python modules into a shorthand, which saves typing. This helps provide some clarity into why many Python scripts and examples start with lines such as `from x import y as z` — this just means import something and give it a shorter name.

    For the current example, we can import gutenberg directly, and thus can avoid typing the `nltk.corpus` bit before it. And, you can do this same thing with other functions from other packages / modules.
    """)
    return


@app.cell
def _():
    # import the gutenberg package directly
    from nltk.corpus import gutenberg

    # now you can access `gutenberg` without needing to type `nltk.corpus`
    gutenberg.fileids()
    return (gutenberg,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Looping through Gutenberg

    Chapter 2 includes a demonstration of the different methods NLTK can provide for a raw text by asking you to think about how the following loop works.

    First, look at how the loop works. The loop is over the `.fileids()` in `gutenberg.fileids()`, which is just a list of the different text files names. In the body of the loop, the fileid is used to access the specific text - this is why the variable `book_id` is placed inside the brackets for `gutenberg.raw()` and all the other functions (`.words`, `.sents`).

    Examine the print statement and the output - do you understand how they have controlled the output using this `print()` statement? You might find it useful to include some comments in the code cell below, explaining what each line is doing.

    The NLTK book also claims there are some patterns related to average word length, average sentence length, and lexical diversity for different authors. Do you see these patterns? For instance - who has the longest sentences? The shortest?
    """)
    return


@app.cell
def _(gutenberg):
    # Can you add comments to this code explaining what each line is doing?
    for book_id in gutenberg.fileids():
      num_chars = len(gutenberg.raw(book_id))
      num_words = len(gutenberg.words(book_id))
      num_sents = len(gutenberg.sents(book_id))
      num_vocab = len(set(w.lower() for w in gutenberg.words(book_id)))
      print(round(num_chars/num_words), round(num_words/num_sents), round(num_words/num_vocab), book_id)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Brown Corpus

    You should read through the explanation of various corpora in Chapter 2. One of the more well-known corpora is the [Brown Corpus](https://en.wikipedia.org/wiki/Brown_Corpus), which has been used in numerous studies of language either for checking word use and collocations, or for compiling frequency statistics of words in spoken and written English. As Chapter 2 explains, the Brown Corpus is an ideal example for how one can use different categories in a corpus to test questions about differences in language use.

    We load in Brown in a similar manner to Gutenberg. The Brown corpus has a function that Gutenberg did not have: `.categories()`. This function shows different genres or classifications of texts in the Brown corpus.
    """)
    return


@app.cell
def _():
    # load in Brown and look at the categories
    from nltk.corpus import brown

    brown.categories()
    return (brown,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can select a specific subsection of the brown corpus using `categories = ` when accessing the Brown text as raw, words, sentences, etc.
    """)
    return


@app.cell
def _(brown):
    # look at a sentence from one of the texts labelled "humor" in the Brown corpus
    brown.sents(categories = 'humor')[80]
    return


@app.cell
def _(brown):
    # the first 20 words of the "news" category
    brown.words(categories = 'news')[:20]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The different genres or categories in Brown allow for a means to compare different writing styles. In the next session (frequency), we will use these categories to compare how often different words occur in different genres.

    ## **Your Turn**

    Have a play with the Brown corpus, explore the different categories and make sure you are comfortable loading them into Python.
    """)
    return


@app.cell
def _():
    # use this code cell to explore Brown!
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## State of the Union Corpus

    Another corpus which provides us some interesting data to use for various comparisons is a set of speeches given by US Presidents over the years. Each year, the sitting president gives a "state of the union" speech which explains how everything they have done is good and how everything their opponents want to do is bad. Because most US Presidents will serve four or eight consecutive years in office, this provides a neat way to compare the speech of different US Presidents over the years.

    We load in the corpus just like Gutenberg and Brown
    """)
    return


@app.cell
def _():
    # Load in the state_union corpus
    from nltk.corpus import state_union

    # fileids shows us the different files
    state_union.fileids()
    return (state_union,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Much like Gutenberg, we can access various properties of specific speeches by using the `.raw()`, `.words()`, or `.sents()` methods with a specific fileid in the brackets:
    """)
    return


@app.cell
def _(state_union):
    # Raw words of 1945 speech
    state_union.raw('1945-Truman.txt')
    return


@app.cell
def _(state_union):
    # tokenized version (truncated output)
    state_union.words('1945-Truman.txt')
    return


@app.cell
def _(state_union):
    # sentences (truncated output)
    state_union.sents('1945-Truman.txt')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We could ask a variety of questions about the nature of State of the Union addresses as they have occurred over time.

    - Have they changed in length?
    - What words are similar among all presidents?
    - What words are unique to different presidents?
    - Which president is the most lexically diverse?
    - and so on...

    Do you have an idea about how to do this? It probably involves some sort of looping over the fileids and then performing a function. For example, here is a loop which answers the first question, by printing the number of words in each speech. What do you notice?
    """)
    return


@app.cell
def _(state_union):
    for speech_id in state_union.fileids():
      # the \t stands for tab character, creating the space between the name and the number.
      print(f'{speech_id} \t {len(state_union.words(speech_id))} words')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Creating your own corpus**

    You can use NLTK to make your own corpus from a folder of text files, and then use all the same methods (`.raw()`, `.words()`, `.sents()`, `.fileids()`) on it.

    To do this, we use the `PlaintextCorpusReader` class from NLTK. In order to use it, we need three things:

    1. some files,
    2. the folder the files are in (the `root`), and
    3. the names of the files.

    Let's start with some data! The scripts of several episodes of the American television show *Seinfeld* are stored online as a single zip file. The function below downloads a zip file and unzips it into a folder. The folder will appear in the folder that contains this notebook (you can also see it with the **files** button in marimo's left sidebar).

    (You don't need to understand every line of this function. `io.BytesIO()` lets Python treat the downloaded data as if it were a file, so that `zipfile` can unzip it.)
    """)
    return


@app.cell
def _(io, requests, zipfile):
    def download_corpus(url, folder):
      # download the zip file
      response = requests.get(url)

      # open the downloaded data as a zip file
      zip_file = zipfile.ZipFile(io.BytesIO(response.content))

      # unzip everything into the folder
      zip_file.extractall(folder)

      # give back the name of the folder, so we can use it later
      return folder

    return (download_corpus,)


@app.cell
def _(download_corpus):
    # download and unzip the Seinfeld scripts into a folder called 'seinfeld'
    seinfeld_folder = download_corpus('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/seinfeld.zip', 'seinfeld')
    return (seinfeld_folder,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The files in the seinfeld folder are:

    ```
    THE BOYFRIEND PT 1_cleaned.txt
    THE BOYFRIEND PT 2_cleaned.txt
    THE CHINESE RESTAURANT_cleaned.txt
    THE DEALERSHIP_cleaned.txt
    THE DOODLE_cleaned.txt
    THE ENGLISH PATIENT_cleaned.txt
    THE FACE PAINTER_cleaned.txt
    THE GOOD SAMARITAN_cleaned.txt
    THE JUNIOR MINT_cleaned.txt
    THE LITTLE KICKS_cleaned.txt
    THE MARINE BIOLOGIST_cleaned.txt
    THE PARKING GARAGE_cleaned.txt
    THE PARKING SPACE_cleaned.txt
    THE PEZ DISPENSER_cleaned.txt
    ```

    Now we create a new variable from the `PlaintextCorpusReader`, which will become our corpus!

    The first argument is `root`, which tells the reader which folder the corpus lives in. In this case, the corpus is within the `seinfeld` folder, which we saved to the variable `seinfeld_folder`.

    The second argument is `fileids`, which asks for the list of files.

    **Let's try it out on a single file to start - using the marine biologist episode**
    """)
    return


@app.cell
def _(PlaintextCorpusReader, seinfeld_folder):
    # read in my text (I've passed the name in a list, so I could include more than one text if I need to later)
    marine_biologist_corpus = PlaintextCorpusReader(root = seinfeld_folder, fileids = ['THE MARINE BIOLOGIST_cleaned.txt'])
    return (marine_biologist_corpus,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that we've created a corpus (even if it is just one text), we can use the built-in NLTK corpus functions.
    """)
    return


@app.cell
def _(marine_biologist_corpus):
    # The raw version should be just the string
    marine_biologist_corpus.raw()[15041:15135]
    return


@app.cell
def _(marine_biologist_corpus):
    # we can also get sentences
    marine_biologist_corpus.sents()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    NLTK also has a function called `.concordance()`, which shows every place a word occurs along with the words around it. To use it on our own corpus, we need to wrap the tokenized words in an NLTK function called `Text()`. (We will look at concordances properly in week 3.)
    """)
    return


@app.cell
def _(Text, marine_biologist_corpus):
    # Create a special Text version of the corpus
    mb_txt = Text(marine_biologist_corpus.words())

    # now we can look for concordance lines
    mb_txt.concordance('whale')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Loading in multiple texts to make a corpus

    A corpus of a single text is not very interesting. Let's update our `PlaintextCorpusReader` to include all of the texts in our Seinfeld folder. But, it sure would be annoying having to type all of the filenames one-by-one. Fortunately, there are several ways around this.

    One is to use the [`glob` library](https://docs.python.org/3/library/glob.html) to quickly list all of the filenames in a folder.
    """)
    return


@app.cell
def _(glob, seinfeld_folder):
    # the * indicates you want everything from the folder.
    seinfeld_paths = glob(seinfeld_folder + '/*')

    seinfeld_paths
    return (seinfeld_paths,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Doing this gives us the folder name as well as the file name, which is kind of annoying. The `os.path.basename()` function gives us just the file name at the end of a path:
    """)
    return


@app.cell
def _(os, seinfeld_paths):
    # just the file name
    os.path.basename(seinfeld_paths[0])
    return


@app.cell
def _(os, seinfeld_paths):
    # let's write a list comprehension which keeps only the file name of each path
    seinfeld_filenames = [os.path.basename(path) for path in seinfeld_paths]

    # voila!
    seinfeld_filenames
    return (seinfeld_filenames,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can just pass `seinfeld_filenames` to the `PlaintextCorpusReader` function and make a larger corpus.
    """)
    return


@app.cell
def _(PlaintextCorpusReader, seinfeld_filenames, seinfeld_folder):
    # make our seinfeld corpus
    seinfeld_corpus = PlaintextCorpusReader(root = seinfeld_folder, fileids = seinfeld_filenames)
    return (seinfeld_corpus,)


@app.cell
def _(seinfeld_corpus):
    # we can use the fileids function to see the texts in here
    seinfeld_corpus.fileids()
    return


@app.cell
def _(seinfeld_corpus):
    # how many words are in the whole corpus?
    len(seinfeld_corpus.words())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Here is a sneak peek of the next session: `nltk.FreqDist()` counts how often each word occurs, and `.most_common()` shows the most frequent ones. What are the ten most common words in our corpus?
    """)
    return


@app.cell
def _(nltk, seinfeld_corpus):
    nltk.FreqDist([word for word in seinfeld_corpus.words() if word.isalpha()]).most_common(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Using your own files

    To make a corpus from your own texts, put your `.txt` files in a folder inside the folder that contains this notebook (you can add files with the **files** button in marimo's left sidebar), and point `PlaintextCorpusReader` at that folder with `root`.

    For security reasons, NLTK will only read corpus files from folders it has been told it can use. The line `nltk.data.path.append('.')` at the top of this notebook allows the current folder (and any folders inside it). If your corpus is somewhere else on your computer, add that folder too, e.g. `nltk.data.path.append('/path/to/my/corpus')`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Creating your own categorised corpus**

    The next type of corpus you can make is a categorised corpus, which will allow you to compare groups of files within your corpus, just like the categories in Brown.

    In order to do so, we need some text files, and we also need a way to indicate what genre/category we would like those files to belong to. The NLTK authors do this by extracting information (i.e., metadata) from the filenames.

    As an example, let's use some data from a [paper I published in 2015.](https://europeanjournalofhumour.org/index.php/ejhr/article/view/68)

    In this paper, I analysed the linguistic properties of product reviews written for the American retail website Amazon.com. I was interested in two types of reviews: legitimate reviews and satirical/funny reviews.

    Let's download and unzip the data using our `download_corpus()` function:
    """)
    return


@app.cell
def _(download_corpus):
    # download and unzip the Amazon reviews into a folder called 'amazon reviews'
    amazon_folder = download_corpus('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/amazon%20reviews.zip', 'amazon reviews')
    return (amazon_folder,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the folder are 375 normal reviews and 375 satirical reviews.

    The name of each file looks like this:
    ```
    001-5-satire.txt
    002-2-normal.txt
    ```

    The first three numbers are the ID number, ranging from 1 - 375. The second number (between the two `-`) is the star rating of the review, from 1-5. The words `satire` or `normal` indicate whether the review was a normal review or a satirical funny review.

    We can exploit this information to make categories in our corpus. To use the filenames as categories, we will use a regular expression (regex) pattern to capture the `normal` or `satire` portions of the filenames using this pattern:

    ```
    .*(......).txt
    ```

    This pattern captures whatever is in the brackets `()`, and says give me the last six characters before `.txt` of my pattern.

    It corresponds to:

    ```
    001-5-(satire).txt
    002-2-(normal).txt
    ```

    Try it out:
    """)
    return


@app.cell
def _(CategorizedPlaintextCorpusReader, amazon_folder):
    # create a categorised corpus
    amz_corpus = CategorizedPlaintextCorpusReader(root = amazon_folder, fileids = '.*', cat_pattern = '.*(......).txt')

    # you can check the categories
    amz_corpus.categories()
    return (amz_corpus,)


@app.cell
def _(amz_corpus):
    # and we still have our fileids
    amz_corpus.fileids()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Just like Brown, we can now ask for the words of just one category:
    """)
    return


@app.cell
def _(amz_corpus):
    # how many words are in each category?
    print(f"satire: {len(amz_corpus.words(categories = 'satire'))} words")
    print(f"normal: {len(amz_corpus.words(categories = 'normal'))} words")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can also wrap the whole corpus, or one category, in `Text` so that we can look for concordances:
    """)
    return


@app.cell
def _(Text, amz_corpus):
    # we can look at concordances for just one category to compare them
    # the word "banana" is strongly associated with the satire corpus
    Text(amz_corpus.words(categories = 'satire')).concordance('banana')
    return


@app.cell
def _(Text, amz_corpus):
    # but only occurs once in the non-satire corpus.
    Text(amz_corpus.words(categories = 'normal')).concordance('banana')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will come back to this corpus later in the course.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A more complex method to create categories

    > You don't really need to worry about this unless you think you need a more complex corpus / category structure.

    You might not want to use part of the file names to create a categorised corpus reader in NLTK (in fact, doing so requires you to have a specific naming convention and potentially use more complicated regex syntax to parse the names). You might have a bunch of files, maybe even in different folders. Rather than trying to find a consistent way to put metadata into the filename, you can instead supply a file that provides the metadata for your corpus.

    This file should contain a list of all the paths for your texts, followed by the category you want to assign to those texts.

    For example the text file could look like this:

    ```
    folder1/file1.txt categoryA
    folder1/file2.txt categoryA
    folder2/file3.txt categoryB
    ```

    You can save this as a `.txt` file named something like `categories.txt`.

    Then, you pass the location of this file to the `cat_file` argument of the `CategorizedPlaintextCorpusReader` class.

    Here is an example. First download a sample corpus, which unzips into a folder called `corpus`:
    """)
    return


@app.cell
def _(download_corpus):
    # the zip file contains a folder called 'corpus', so we unzip it into the current folder ('.')
    download_corpus('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/corpus.zip', '.')
    sample_folder = 'corpus'
    return (sample_folder,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You will also need your file which maps the categories. The cell below downloads one and saves it as `categories.txt` inside the `corpus` folder (you'll learn how writing files works in a later notebook). NLTK will only read a categories file from inside the corpus folder, so that's where it needs to go.
    """)
    return


@app.cell
def _(os, requests, sample_folder):
    categories_text = requests.get('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/categories.txt').text

    # save the file inside the corpus folder
    categories_filename = 'categories.txt'
    categories_path = os.path.join(sample_folder, categories_filename)

    with open(categories_path, 'w') as categories_file:
      categories_file.write(categories_text)

    # Inspect the contents of the categories file
    print(categories_text)
    return (categories_filename,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can see it lists the file name of each file, followed by a space and the category for that file.

    Declare your corpus and give the corpus reader three pieces of information:

    1. The root folder for your corpus, which is `corpus` (saved as `sample_folder`)

    2. The names of the files. The regex pattern `.*/.*\.txt` means "any `.txt` file inside a folder", so it picks up the texts in `corpus_a` and `corpus_b` but not `categories.txt` itself, which sits directly in `corpus`

    3. The name of the `.txt` file containing the mapping of file names to categories, which is inside the root folder
    """)
    return


@app.cell
def _(CategorizedPlaintextCorpusReader, categories_filename, sample_folder):
    sample_corpus = CategorizedPlaintextCorpusReader(root = sample_folder, fileids = r'.*/.*\.txt', cat_file = categories_filename)
    return (sample_corpus,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can inspect the categories of the corpus:
    """)
    return


@app.cell
def _(sample_corpus):
    sample_corpus.categories()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As well as the filenames:
    """)
    return


@app.cell
def _(sample_corpus):
    sample_corpus.fileids()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can then use the `categories` argument to look at files in any one category:
    """)
    return


@app.cell
def _(sample_corpus):
    for sample_category in sample_corpus.categories():
      for sample_file in sample_corpus.fileids(categories = sample_category):
        print(sample_corpus.raw(sample_file), '\t', sample_category)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is probably the best method to use if you have a complex set of files and folders that you want to be able to place into different categories without relying on filenames.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **What can a corpus represent?**

    A corpus is often used to make claims about a whole language, a genre, or a group of people. But every corpus is a sample, and the claims it can support depend on what went into it. Think about the corpora in this notebook:

    - **Brown** is about 1 million words of written American English, all published in 1961. What could it tell you about English today? About spoken English? About New Zealand English?
    - **Gutenberg** (in NLTK) is 18 books by a handful of authors. If the Gutenberg loop found that one author writes longer sentences, what can you conclude about that author? About writers of their time?
    - **State of the Union** is speeches by US presidents. Who wrote them? Whose language is in the corpus: the president's, or their speechwriters'?
    - **The Amazon reviews** were collected by a researcher (me!) with a particular question in mind. How might that have shaped which reviews were included?
    """)
    return


if __name__ == "__main__":
    app.run()
