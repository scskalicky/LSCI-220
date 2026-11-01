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
    # **Review: types and tokens**

    - types: unique word forms
    - tokens: individual occurrences of word forms
    - type / token ratio: measure of lexical diversity
      - higher TTR = more diverse vocabulary
      - lower TTR = more repetition
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Key functions:**

    - `len()` - how many values in a group of values
    - `set()` - what are the unique values in a group of values
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Create an example string to work with. Before running each cell below, predict what the output will be.
    """)
    return


@app.cell
def _():
    example_text = "there is no you there is only me"

    print(example_text)
    return (example_text,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Tokenise using `.split()`
    """)
    return


@app.cell
def _(example_text):
    example_text_tokens = example_text.split()

    print(example_text_tokens)
    return (example_text_tokens,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Length of the *string* versus length of the *list*
    """)
    return


@app.cell
def _(example_text, example_text_tokens):
    print('number of characters:')
    print(len(example_text))

    print('\nnumber of tokens:')
    print(len(example_text_tokens))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Combining `len()` with `set()`
    """)
    return


@app.cell
def _(example_text_tokens):
    # examine all the unique tokens
    set(example_text_tokens)
    return


@app.cell
def _(example_text_tokens):
    # count the number of unique tokens
    len(set(example_text_tokens))
    return


@app.cell
def _(example_text_tokens):
    # calculate difference between total tokens and unique tokens
    len(example_text_tokens) - len(set(example_text_tokens))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can calculate the *ratio* of types (unique words) to tokens (total words)

    $$
    \text{TTR} = \frac{\text{number of types}}{\text{number of tokens}}
    $$
    """)
    return


@app.cell
def _(example_text_tokens):
    len(set(example_text_tokens)) / len(example_text_tokens)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - If the ratio was 1, it would mean 1 unique word per token. No words would be repeated.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: live TTR**

    Type or paste any text into the box below. The cell after it splits the text with `.split()` and calculates its TTR, and lists any words that are repeated.
    """)
    return


@app.cell
def _(mo):
    # a text box to type or paste a text into
    ttr_box = mo.ui.text_area(value='there is no you there is only me', label='your text:', full_width=True)
    ttr_box
    return (ttr_box,)


@app.cell
def _(ttr_box):
    # tokens, types and TTR for the text in the box
    live_tokens = ttr_box.value.split()
    live_types = set(live_tokens)

    print(f"tokens: {len(live_tokens)}")
    print(f"types:  {len(live_types)}")
    print(f"TTR:    {round(len(live_types) / len(live_tokens), 3)}")
    print(f"repeated words: {[word for word in live_types if live_tokens.count(word) > 1]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Activity: TTR challenge**

    Using the TTR box above:

    1. Can you write the **longest** sentence (that makes sense!) with a TTR of exactly **1**?
    2. Can you write the **shortest** sentence with a TTR **under 0.5**?

    What did you have to do to win each one? What does that tell you about TTR?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - a long sentence with no repeated words is hard: function words (*the*, *a*, *of*, *and*) keep coming back
    - a short sentence with lots of repetition is usually easier: *no no no*
    - so TTR depends a lot on **length**: short texts look diverse, long texts look repetitive
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Activity: what aspects of texts might affect TTR?**
    """)
    return


@app.cell
def _():
    # from Wikipedia: https://en.wikipedia.org/wiki/Irony

    irony = """
    Irony is a juxtaposition of what, on the surface, appears to be the case with what is actually or
    expected to be the case. Originally a rhetorical device and literary technique, irony has also come
    to assume a metaphysical significance with implications for one's attitude towards life.
    The concept originated in ancient Greece, where it described a dramatic character who pretended to be
    less intelligent than he actually was in order to outwit boastful opponents. Over time, irony evolved
    from denoting a form of deception to, more liberally, describing the deliberate use of language to mean
    the opposite of what it says for a rhetorical effect intended to be recognized by the audience. Due to
    its double-sided nature, irony is a powerful tool for social bonding among those who share an understanding.
    For the same reason, it is also a source of division, sorting people into insiders and outsiders depending
    upon whether they are able to see the irony. In the nineteenth-century, philosophers began to expand the
    rhetorical concept of irony into a broader philosophical conception of the human condition itself.
    For instance, Friedrich Schlegel saw irony as an expression of always striving toward truth and meaning
    without ever being able to fully grasp them. Søren Kierkegaard maintained that ironic awareness of our
    limitations and uncertainties is necessary to create a space for authentic human existence and ethical choice.
    """
    return (irony,)


@app.cell
def _(irony):
    len(set(irony.split())) / len(irony.split())
    print(f"repeated words: {[word for word in irony.split() if irony.split().count(word) > 1]}")
    return


@app.cell
def _():
    jp = "Your scientists were so preoccupied with whether or not they could that they didn't stop to think if they should"
    return (jp,)


@app.cell
def _(jp):
    len(set(jp.split())) / len(jp.split())
    print(f"repeated words: {[word for word in jp.split() if jp.split().count(word) > 1]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Reflect:**
    - How long would it take you to count those repeated words?
    - How difficult is it for you to even notice them?
    - How accurate is our TTR/LD measure?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Activity: text length and TTR in inaugural addresses**

    NLTK has a corpus of every US presidential inaugural address. The addresses are all the same kind of text, but they vary a lot in length. Let's load them in.
    """)
    return


@app.cell
def _():
    # load in the inaugural address corpus
    import nltk
    nltk.download('inaugural')
    from nltk.corpus import inaugural

    # the file names of every address
    inaugural_ids = inaugural.fileids()
    return inaugural, inaugural_ids


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Pick an address from the dropdown:
    """)
    return


@app.cell
def _(inaugural_ids, mo):
    # a dropdown of every address
    address_choice = mo.ui.dropdown(options=inaugural_ids, value='2009-Obama.txt', label='address:')
    address_choice
    return (address_choice,)


@app.cell
def _(address_choice, inaugural):
    # tokens, types and TTR for the chosen address
    address_tokens = inaugural.raw(address_choice.value).split()

    print(f"{address_choice.value}")
    print(f"tokens: {len(address_tokens)}")
    print(f"types:  {len(set(address_tokens))}")
    print(f"TTR:    {round(len(set(address_tokens)) / len(address_tokens), 3)}")
    return (address_tokens,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now let's look at every address at once. Each dot below is one address: how long it is (across) and its TTR (up). The address you chose in the dropdown is shown in red.

    What pattern do you see? Is a speech with a low TTR really "less diverse"?
    """)
    return


@app.cell
def _(address_tokens, inaugural, inaugural_ids):
    import matplotlib.pyplot as plt

    # length and TTR of every address
    all_lengths = [len(inaugural.raw(fileid).split()) for fileid in inaugural_ids]
    all_ttrs = [len(set(inaugural.raw(fileid).split())) / len(inaugural.raw(fileid).split()) for fileid in inaugural_ids]

    # plot every address, then the chosen address in red
    fig, ax = plt.subplots()
    ax.scatter(all_lengths, all_ttrs)
    ax.scatter(len(address_tokens), len(set(address_tokens)) / len(address_tokens), color='red')
    ax.set_xlabel('length (tokens)')
    ax.set_ylabel('TTR')
    ax.set_title('US inaugural addresses')
    fig
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Discussion notes": mo.md(r'''
    - the longer the address, the lower the TTR, almost without exception
    - so a low TTR mostly tells us a speech is *long*, not that its vocabulary is poor
    - to compare texts of different lengths fairly we need measures that control for length, like MSTTR from the self-study notebook
    ''')})
    return


@app.cell(hide_code=True)
def _(mo):
    mo.callout(mo.md(r"""
    # **Critical reflection**

    1. TTR is meant to measure "lexical diversity". After the challenge and the inaugural addresses, what does TTR actually measure?
    2. Would you use TTR to compare two speeches of different lengths? What about an essay by a language learner and one by a native speaker? What could go wrong?
    3. Our TTR counts `Irony` and `irony`, or `run` and `ran`, as different types. What decisions are hiding inside "number of types"?
    4. Is a more "diverse" vocabulary always better? Who might be judged by a measure like this, and is that fair?
    """), kind='info')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.accordion({"Critical reflection notes": mo.md(r'''
    - TTR measures repetition, but it is also strongly affected by text length, so on its own it mostly tells us how long a text is
    - comparing texts of different lengths with TTR is unfair to the longer text; comparing learners and native speakers adds other differences too (topic, task, time)
    - "number of types" depends on tokenisation choices: case, punctuation, and whether different forms of a word count as one type or several
    - a varied vocabulary isn't always the goal: repetition can be a deliberate choice (in speeches, songs, or for clarity), and measures like this are used to assess learners and writers, so their limits have real consequences
    ''')})
    return


if __name__ == "__main__":
    app.run()
