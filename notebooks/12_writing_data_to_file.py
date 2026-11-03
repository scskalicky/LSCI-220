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
    #### Other tutorials on this topic:

    [Geeks for Geeks Writing Text Data](https://www.geeksforgeeks.org/reading-writing-text-files-python/)

    [Real Python Writing to CSV](https://realpython.com/python-csv/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Getting your results out of a notebook

    Most of the output in these notebooks is printed directly in the notebook, usually underneath the code cells. This is usually fine for our purposes. However, it is also worthwhile to know how you could turn your results into actual files. You might want to create new text files, or save results of linguistic analysis
    for many texts to a new text file or spreadsheet. This notebook will show you a few options for how to accomplish this.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Writing to a text file

    Writing directly to a file in Python involves first opening the file and then adding information to the file.

    To open a file, you use the `open()` function. This function needs to point at the file in question. If you give just a file name, Python looks for the file in the folder that this notebook is in.

    So, if we wanted to write to a file named `text.txt`, we would write something like this:

    ```
    open('text.txt')
    ```
    However, we need to open the file and keep it open, so we save the results to a variable.

    ```
    myfile = open('text.txt')
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Run the cell below to try this out. You should receive an error telling you that no such file or directory exists. This makes sense, because we have not made this file!
    """)
    return


@app.cell
def _():
    missing_file = open('text.txt')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, how do we create a file if it does not already exist? The answer is by supplying options to the `mode` argument within the `open()` function. This argument tells Python what to do with files that do not exist, as well as files that do exist. The default `mode` is `r`, which means read only. There are other flags which control whether a file is created, whether it is available for reading and/or writing, and whether data should be added to the start or end of the file. [You can find a good answer about this here.](https://stackoverflow.com/questions/1466000/difference-between-modes-a-a-w-w-and-r-in-built-in-open-function)

    So, if we wanted to first create a file and then continue to add data to the file, the `a+` mode is a good choice. This mode opens a file for writing (and creates the file if it doesn't exist), and then adds data to the end of the file.

    Let's try it out:
    """)
    return


@app.cell
def _():
    myfile = open('text.txt', mode = 'a+')
    return (myfile,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can verify that this file has been created by looking in the folder that contains this notebook - it should be in there! You can also see it by clicking the **files** button in marimo's left sidebar. Next, we want to add some information to this file. We can do so with the `.write()` method, where we place the information we want to be added to the file in the argument.

    Let's write a single sentence to the file. After writing, let's close the file as well.
    """)
    return


@app.cell
def _(myfile):
    myfile.write('A good rule of thumb with kettlebell exercises: take rests for as long as you need, but for shorter than you want.')
    myfile.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can load the file again using `mode = 'r'` to see what is in the file. We will add `.read()` to the end to access the content of the file.

    You should see the sentence has been added to the text file.
    """)
    return


@app.cell
def _():
    open('text.txt', mode = 'r').read()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will be opening, writing and closing files a lot in this notebook. Rather than typing those three steps every time, let's put them into a **function**, which I will name `write_text`. The function takes three arguments: the name of the file, the text to write, and the mode.

    Because `myfile` is created *inside* the function, it is a local variable, so we can use the function over and over without any problems.
    """)
    return


@app.function
def write_text(filename, text, mode):
  """opens a file, writes text to it, then closes it"""
  # open the file
  myfile = open(filename, mode = mode)

  # write to the file
  myfile.write(text)

  # close the file
  myfile.close()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's use the function to add another sentence to the file, using the `a+` mode:
    """)
    return


@app.cell
def _():
    # add another sentence to the end of the file
    write_text('text.txt', 'a nod\'s as good as a wink to a blind bat!', 'a+')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Take another look, we see that the new information was added to the file, after the data which had already been added. The result is a single long string of text.
    """)
    return


@app.cell
def _():
    open('text.txt').read()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What happens if we were to open the file with `mode = 'w+'` and add some more data?
    """)
    return


@app.cell
def _():
    # overwrite the file with the w+ mode
    write_text('text.txt', 'with your powers combined, I am Captain Planet!', 'w+')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What does the file look like now? Well, opening the file with `w` has overwritten the existing content. Therefore, it is crucially important to make sure you open files with the right mode! Sometimes you may want to continuously add to an existing file, whereas other times you may want to start over with a fresh file each time.
    """)
    return


@app.cell
def _():
    open('text.txt').read()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    These files are saved in the folder that contains this notebook (you can also see them with the **files** button in marimo's left sidebar), so you can open them with any text editor, or use them in other notebooks that are in the same folder. You can also add to existing folders, but you'd need to make sure you point the function at the right file/folder structure.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Creating a bunch of text files

    What if we had a list of texts or some other container of files we wanted to create individual text files for? Perhaps you wanted to create a corpus based on some sort of analysis you have done, and your data is stored as dictionary?

    Let's make a sample dictionary:
    """)
    return


@app.cell
def _():
    sf_dict = {'JERRY': "What's the deal with these pretzels?",
               'KRAMER': "These pretzels are making me thirsty!",
               'GEORGE': 'We live in a society!'}
    return (sf_dict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We want to create a separate text file for each line in the dictionary. We therefore need to make a new filename for each text file. Using a loop, we could exploit the keys of the dictionary and use them as the names of the text files.

    Using string concatenation, we can glue the key to the file extension we want, in this case of `.txt`. Because we want a fresh file each time, we will use the `w+` mode with our `write_text()` function.
    """)
    return


@app.cell
def _(sf_dict):
    # initiate loop through the dictionary keys
    for character in sf_dict.keys():
      # write the dictionary data to a file with the dictionary key + .txt as the file name, using w+ mode
      write_text(character + '.txt', sf_dict[character], 'w+')
    return


@app.cell
def _(sf_dict):
    # we can loop through the files and open them to read them
    for speaker in sf_dict.keys():
      print(open(speaker + '.txt').read())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pretty easy, right? That's how you can quickly make a bunch of text files separated from larger texts or analyses, which can come in handy for making your own corpora.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # writing results of analyses as text files

    In addition to writing text to file, we might want to make a text file which holds the results of an analysis. For instance, we might want to collect the name of a text, the number of words in a text, etc.

    Or, we may want to output the results of a frequency distribution to a text file, so that we do not have to run the notebook over and over.

    The procedure for doing so is the exact same, but we may want to start including different whitespace characters to insert tabs and newlines as a means to organise the data.

    Let's see this with a frequency analysis of a small text.
    """)
    return


@app.cell
def _():
    # import nltk to use FreqDist
    import nltk

    # create text, with .split() at the end to tokenize
    woodchuck = """
    How much wood could a woodchuck chuck
    If a woodchuck could chuck wood?
    As much wood as a woodchuck could chuck,
    If a woodchuck could chuck wood.
    """.split()

    # create FreqDist of text
    fdist = nltk.FreqDist(woodchuck)
    return (fdist,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We will loop through the FreqDist and add the word plus its frequency to a text file. Crucially, we will separate the words and their frequency values with a tab character `'\t'`, and add a newline `'\n'` so that each word/frequency value is on its own line. We will write this to a file called `'woodchuckFreq.txt'`

    In order to use string concatenation, we will have to convert the number into a string using `str()`
    """)
    return


@app.cell
def _(fdist):
    for woodchuck_word in fdist.keys():
      # write the word, a tab, the frequency, and a newline
      write_text('woodchuckFreq.txt', woodchuck_word + '\t' + str(fdist[woodchuck_word]) + '\n', 'a+')

    # what happens if you run this cell a second time? Why?
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Inspect the file - if we split on newlines, we can see how the file  shows the data. And, if you manually download the file and open it in a text editor, you will see that each word/frequency pair is on its own line.
    """)
    return


@app.cell
def _():
    open('woodchuckFreq.txt').read().split('\n')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Annoyingly, our code inserts a newline at the final part of the loop, which means that the text file will have an empty newline at the end. How could this be resolved?

    1. You could use `if`/`else` logic to add newlines for all lines except the last line of the loop
    2. You could use `rstrip()` to strip the trailing newline
    3. calculate the text to be written in a loop, and then write only one time, after using `rstrip()`
    4. You could manually open the text file and delete the empty last line (sometimes the manual ways are the faster ways...but only sometimes).
    5. Likely many other ways...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # with open

    Now that you understand file reading and writing, time to introduce one more common thing you will encounter with Python file writing, the `with` statement.

    [You can read some good answers about `with` on Stack Overflow](https://stackoverflow.com/questions/3012488/what-is-the-python-with-statement-designed-for), but the details are not super important for our purposes. This information is included primarily because many examples of reading/writing files in Python will be accompanied with these statements.

    Basically, instead of opening and closing a file each time in a loop, we can hold the file open using `with`, perform all of the looping and writing while it is open, and then safely close it.

    To use `with`, simply use it before the `open()` statement and then type `as variable` followed by a colon. This creates a header within which you can perform looping to read/write to the file.
    """)
    return


@app.cell
def _():
    # hold this file open as the variable `withtext_file`
    with open('withtext.txt', 'w+') as withtext_file:
      # initiate a loop (what is enumerate doing? How is it used in the .write() line?)
      for index, word in enumerate('every day is exactly the same'.split()):
        # write to the same file
        withtext_file.write(word + '_' +  str(index) + '\n')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Test that it worked:
    """)
    return


@app.cell
def _():
    # do you understand what is going on in this list comprehension? what is the .rstrip() doing?
    [word for word in open('withtext.txt').read().rstrip().split('\n')]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # creating .csv files (spreadsheets)

    Writing text to file is useful, and can also be used to write out data results from analyses. But text files are only structured when they have tabs and newlines separating them. What if we wanted to write to a spreadsheet instead of a text file? We can! Specifically, we can create a comma-separated values file (`.csv`) which works like a spreadsheet and can be opened in programs like Google Sheets, Excel, or Libre Office.

    This is particularly useful for tabular data, such as if you had a series of metrics for a text: total number of words, lines, TTR, etc. So that data that looks like this can be created easily as a csv file:

    |text|words|lines|TTR|
    |:-:|:-:|:-:|:-:|
    |text1|200|10|.7|
    |text2|100|10|.9|

    Let's first create some data that could be written to a csv file like this. The next cells download the Seinfeld scripts, using the same `download_corpus()` function as the corpora notebook:
    """)
    return


@app.cell
def _():
    import io
    import zipfile
    import requests

    def download_corpus(url, folder):
      # download the zip file
      response = requests.get(url)

      # open the downloaded data as a zip file
      zip_file = zipfile.ZipFile(io.BytesIO(response.content))

      # unzip everything into the folder
      zip_file.extractall(folder)

      # give back the name of the folder, so we can use it later
      return folder

    # download and unzip the Seinfeld scripts into a folder called 'seinfeld'
    seinfeld_folder = download_corpus('https://raw.githubusercontent.com/scskalicky/LSCI-220/main/resources/seinfeld.zip', 'seinfeld')
    return (seinfeld_folder,)


@app.cell
def _(seinfeld_folder):
    # glob to grab the filenames
    from glob import glob

    filenames = glob(seinfeld_folder + '/*.txt')

    filenames
    return (filenames,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we will calculate the number of words, lines, and TTR for each text, and then write that information to a csv file. We will do this row by row, so to speak.

    First, import the csv library
    """)
    return


@app.cell
def _():
    # import the csv library
    import csv

    return (csv,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using the `csv` library is similar to `open` for writing text. We will use `with` and `open` to hold a .csv file open, and then use `csv.reader` or `csv.writer` to create csv files. The same modes also apply, so be sure whether you want to create a new file, or append to an existing file.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There is a lot going on in the cell below, so here is an explanation:

    Line 1: opening the file using `with` and `mode = 'w+'`, as the variable `csv_file`

    Line 2: convert the opened file into a csv writer object, called `csv_out`

    Line 4: write a header row to give the columns names. Notice that this is done *before* the loop, otherwise the header would be written for each iteration through the loop!

    Line 5: loop through our filenames, which are saved as strings in a list (done in a previous cell above, using glob)

    Line 7: open the filename and save it to the variable `script_text`, using `.rstrip()` to remove trailing newlines

    Line 9: write the name of the text, the number of words, number of lines, and TTR of the file to the csv. This information is entered as a list, where each item in the list will be a new column in the spreadsheet.
    """)
    return


@app.cell
def _(csv, filenames):
    with open('textAnalytics.csv', 'w+') as csv_file: # open the file with a temporary variable
      csv_out = csv.writer(csv_file) # convert that variable to a csv writer object
      # create header row
      csv_out.writerow(['text', 'number of words', 'number of lines', 'TTR'])
      for filename in filenames:
        # open the text
        script_text = open(filename).read().rstrip()
        # write different text calculations in a single line
        csv_out.writerow([filename, len(script_text.split()), len(script_text.split('\n')), len(set(script_text.split()))/len(script_text.split())])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After creating the file, we can use `csv.reader` to read the lines of the file:
    """)
    return


@app.cell
def _(csv):
    with open('textAnalytics.csv', 'r') as csv_file2:
      csv_in = csv.reader(csv_file2)
      for row in csv_in:
        print(row)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The file `textAnalytics.csv` is now in the folder that contains this notebook (you can also find it with the **files** button in marimo's left sidebar). You can open it in Excel, Google Sheets, or LibreOffice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Hopefully you now have a few new strategies to read and write data. While there are other ways to read/write csv files such as using `pandas` or `polars`, the `csv` module can serve the same purposes in many instances, and does not require loading in additional libraries.

    Once you get the data into spreadsheet format, you could include it in a written report or conduct visualisations on the data. You could also do that with Python, depending on how far you want to go within a single notebook.
    """)
    return


if __name__ == "__main__":
    app.run()
