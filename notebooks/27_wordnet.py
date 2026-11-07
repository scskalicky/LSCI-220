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

    [NLTK Book, Chapter 2, Section 5](https://www.nltk.org/book/ch02.html#wordnet_index_term)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # **Introduction to WordNet**

    This notebook will introduce you to the English *WordNet*, which is a database of word associations. Of all the topics / resources we can work with in NLTK, I think WordNet may be the most interesting. That's because WordNet is trying to get at something we have not directly addressed up to this point — capturing the *meaning* of English words computationally. WordNet tries to capture such information by modelling (1) different senses associated with words and (2) relationships among those senses / words to other senses / words.

    As such, WordNet is a fantastic resource for understanding how words in English relate to one another. (There used to be an online version of WordNet, but sadly it was taken down in 2024 `:(`)

    The [Wikipedia page](https://en.wikipedia.org/wiki/WordNet) for WordNet also includes a good deal of background and discussion (although you may want to read it after going through this notebook).

    NLTK includes WordNet as a resource, and is just a matter of downloading and importing the necessary resources.

    > *You may also want to explore using `help(wn)` (after you have imported it)*.
    """)
    return


@app.cell
def _():
    # load in wordnet as wn
    import nltk
    nltk.download(['wordnet', 'omw-1.4'])
    from nltk.corpus import wordnet as wn

    return (wn,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Synsets

    In WordNet, words are organised into what are known as `synsets`, and these synsets represent the key objects you work with when using WordNet. You can search which synsets are associated with different words using the `synsets()` function.

    Simply pass the word as a string to the function.
    """)
    return


@app.cell
def _(wn):
    # we can see that the word "dog" is associated with eight different synsets.
    wn.synsets('dog')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each synset is a word or set of words associated with a specific meaning (which are referred to as *senses*). In the output above, we can see that the word `dog` is included in eight different synsets.

    This means that WordNet includes eight possible meanings (or senses) for which the word `dog` can be associated. The actual names of the synsets are provided in this format:

    ```
    word.x.01
    ```

    `word.` — the "main" word associated with the synset.

    `.x.` — the part of speech
      - (above we see `n` and `v` for `noun` and `verb`)

    `01` — this is how they maintain repeats of the same synset name and also indicate the most common uses.
      - this means whatever meaning or sense is associated with `dog.n.01` is thought to be more frequent than `dog.n.03`.

    So, inspecting the output above there are eight synsets. Two synsets have dog as the "main" word (`dog.n.01` and `dog.n.03`), whereas the other six synsets will include `dog` as word associated with the synset meaning.

    Let's save the first synset to a variable and explore the information contained within:

    CAREFUL!

    - Note that we use `synsets()` to find all synsets with a string word as input (synset**S**)

    - We use `synset()` to call a specific synset using the name of the synset
    """)
    return


@app.cell
def _(wn):
    # when you know the name of a synset you can call it directly
    # save the dog synset to a variable.
    dog01 = wn.synset('dog.n.01')
    return (dog01,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are a number of method functions we can use. Two that are helpful to understand synsets are these:

    - `.lemma_names()` — the other words which have the same meaning/sense (i.e., other words in the same synset)
    - `.definition()` — the full definition of the synset
    """)
    return


@app.cell
def _(dog01):
    # use lemma_names() to see all the other words in a synset
    # this helps us understand the "meaning" of the first synset for dog
    dog01.lemma_names()
    return


@app.cell
def _(dog01):
    # use .definition() to get the actual meaning
    # this meaning makes sense right?
    dog01.definition()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So `dog.n.01` is related to the domestic animal, and the words / phrases `domestic_dog` and `canis_familiaris` are thought to be approximately equivalent in meaning/sense. That makes...sense...right?

    Let's explore the other synset with `dog` in the name, `dog.n.03`. There is only one word in the lemma names, suggesting this is a very specific use of the word dog:
    """)
    return


@app.cell
def _(wn):
    # lemma names
    wn.synset('dog.n.03').lemma_names()
    return


@app.cell
def _(wn):
    # oh...this is clearly a different meaning!
    wn.synset('dog.n.03').definition()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So the other meaning of "dog" is a colloquialism with a very specific meaning. Again, there are no other words (or lemmas) included in this synset, further exhibiting the specific meaning associated with this use of dog.

    What about the other synsets? Each of them was returned because the word "dog" is a lemma in the synsets.

    For example, the `frank.n.02` synset meaning is related to hot dogs or frankfurters, and `dog` is one of the lemmas listed as a possible synonym.
    """)
    return


@app.cell
def _(wn):
    wn.synset('frank.n.02').lemma_names()
    return


@app.cell
def _(wn):
    wn.synset('frank.n.02').definition()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Better understanding how synsets are accessed

    > *(I found this out by accident when playing around and thought it was fun to share)*

    You can explore the other meanings and definitions by calling synset names as they were provided above.

    Alternatively, since we know there are seven total synsets which include `dog` as a `noun`, we can iterate through those synsets by calling `dog.n.0x`, where `x` is the number 1-7.

    I demonstrate this below using a loop which ranges through the numbers 1-7 and then calls the synset using `dog.n.0x` instead of the names provided above.

    This helps us see that the number in the synset is related to the frequency of use of a word's different meanings, as well as the flexibility associated with calling synsets!

    >> *In the cell you will see that to cycle through 1-7, I need to call `range(1,8)`. This is similar to slicing, in that I am asking for everything starting at 1 and ending at 8, but this does **not** include 8. I encourage you to play around with `range()` in order to better understand how this works*
    """)
    return


@app.cell
def _(wn):
    # (how could this loop be changed to account for words that have more than 10 synsets?)
    # (how could you make a function which can print out the synsets regardless of their length?
    # (how could you always know the size of the synset?)

    for i in range(1,8):
      print('definition: ' + str(i))
      print(wn.synset('dog.n.0' + str(i)).definition())
    return


@app.cell
def _(wn):
    # we can also see what happens when we call a synset beyond the range (check out the WordNetError)
    wn.synset('dog.n.08')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This makes perfect sense, because if you recall, we started this whole search by searching for the word "dog" and saw that there were eight synsets, seven of which were associated with nouns. So if we wanted to know how many "meanings" or "senses" are associated with a word, we can query the total number of synsets returned for a word, regardless of the name of the synset.

    Just as a fun exercise, consider the function below where I use this information to make a smarter function which will tell us all the basic information that we might want to know for different words.
    """)
    return


@app.cell
def _(wn):
    # because you can use len to find how many senses a word has...
    len(wn.synsets('dog'))
    return


@app.cell
def _(wn):
    # and because you could use the `.pos()` method to find the POS uses...
    for dog_synset in wn.synsets('dog'):
      print(dog_synset.pos())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    One thing to know before we write the function: WordNet has *two* labels for adjectives. `a` is a regular adjective, and `s` is a "satellite" adjective, which is an adjective whose meaning is grouped around a central adjective (e.g., *joyful* is a satellite of *happy*). For our purposes, we can count both as adjectives. WordNet also uses `r` for adverbs.

    The function below loops through the synsets of a word, and keeps a list of definitions for each part of speech in a dictionary. Then it prints out how many senses there are for each part of speech, along with their definitions.
    """)
    return


@app.cell
def _(wn):
    #  you could write a function to automatically count and print various information about words
    def print_my_synsets_please(target):
      synsets = wn.synsets(target)

      # only do this stuff if there are any synsets for the target
      if len(synsets) == 0:
        print(f'Sorry, target word {target} makes no sense!')
        return

      # the names of each part of speech label (both 'a' and 's' are adjectives)
      pos_names = {'n': 'Nouns', 'v': 'Verbs', 'a': 'Adjectives', 's': 'Adjectives', 'r': 'Adverbs'}

      # a dictionary to store the definitions for each part of speech
      definitions = {}
      for synset in synsets:
        pos_name = pos_names[synset.pos()]
        if pos_name not in definitions:
          definitions[pos_name] = []
        definitions[pos_name].append(synset.definition())

      # print out the total number of senses, then the senses for each part of speech
      print(f'Target {target} has {len(synsets)} senses.\n')
      for pos_name in definitions:
        print(f'{pos_name}: {len(definitions[pos_name])}')
        for definition in definitions[pos_name]:
          print(' - ' + definition)
        print()

    return (print_my_synsets_please,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Since I've gone to all that trouble making this function, try it out on some words to see how it works!

    If you're brave, try it on the word `run`
    """)
    return


@app.cell
def _(print_my_synsets_please):
    print_my_synsets_please('dog')
    return


@app.cell
def _(print_my_synsets_please):
    print_my_synsets_please('Canada')
    return


@app.cell
def _(print_my_synsets_please):
    print_my_synsets_please('happy')
    return


@app.cell
def _(print_my_synsets_please):
    print_my_synsets_please('comb')
    return


@app.cell
def _(print_my_synsets_please):
    print_my_synsets_please('blarg')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    What other helper functions might you want to make for WordNet? Or, how else could you update this function to allow for more options / customization?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Specify part of speech in WordNet searches

    We now know that we can use `.pos()` to check the POS of specific synsets, but we can also specify specific parts of speech when querying WordNet. You can do so by using the `pos = ` argument in `wn.synsets()`
    """)
    return


@app.cell
def _(wn):
    # only return synsets that are nouns
    wn.synsets('dog', pos = 'n')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So we can quickly count specific meanings for different types if we need — could this information be used to modify the function I wrote above?
    """)
    return


@app.cell
def _(wn):
    # how many meanings does 'dog' have as a noun?
    len(wn.synsets('dog', pos = 'n'))
    return


@app.cell
def _(wn):
    # how many meanings does 'dog' have as a verb?
    len(wn.synsets('dog', pos = 'v'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### **Your Turn**

    Explore some other words in WordNet to get a hang of looking through different synsets and accessing the information within. You should try the following **your turn** prompt:

    > *Your Turn: Write down all the senses of the word `dish` that you can think of. Now, explore this word with the help of WordNet, using the same operations we used above.*
    """)
    return


@app.cell
def _():
    # look through other synsets here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Hypernyms and Hyponyms

    So, the `synsets` show groups of words with approximately similar meanings — in this manner, these words are related to one another (through shared and similar senses). Another way words can relate to one another is through hierarchical categorization. For example, some words are larger categories for other words — the word `vehicle` is a larger category which can include `car`, `ambulance`, `truck`, and so on, while `car` is itself a larger category which can contain terms like `sedan`, `hatchback`, and so on.

    These sorts of categorical relationships are known as **hypernymy** and **hyponymy**. WordNet includes this information for all of the words in WordNet, allowing you to traverse higher-level and lower-level categories associated with particular words.

    The two key terms are **hypernym** and **hyponym**.

    > HYPER means *above*, and HYPO means *below*.

    Whether any one word is a hypernym or hyponym is always relative and depends on the word you are starting from. Using the example above of vehicles, we could say that `vehicle` is a hypernym of `car`, while `car` is a hypernym of `hatchback`. Conversely, `car` is a hyponym of `vehicle`. So, again, the designation of hypernym vs. hyponym comes down to which word one starts with, and which direction through the categories one wishes to traverse.

    We can access the hypernyms or hyponyms of words using the `.hypernyms()` and `.hyponyms()` methods from the `synset` objects.
    """)
    return


@app.cell
def _(dog01):
    # which categories are smaller (more specific) than "dog"?
    # inspect the results - are these all more specific types of dogs?
    dog01.hyponyms()
    return


@app.cell
def _(dog01):
    # which categories are larger (less specific) than "dog"?
    # inspect the results - are these categories larger than dog? Would they have additional members besides dog?
    dog01.hypernyms()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Again, you can think of the hypernyms and hyponyms as different levels up or down a hierarchy. And, because we can quantify the number of levels or steps between two words/senses, we can calculate an approximation of the distance and/or similarity among concepts associated with the words. For example, what are the hypernyms of `dog` and `wolf`?
    """)
    return


@app.cell
def _(wn):
    # compare hypernyms of dog and wolf
    print(f'Dog hypernyms: {wn.synset("dog.n.01").hypernyms()}\n\nWolf hypernyms: {wn.synset("wolf.n.01").hypernyms()}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Ah ha! We can see that `dog` and `wolf` both include `canine.n.02` as a hypernym. Inspecting that synset gives us the definition:
    """)
    return


@app.cell
def _(wn):
    wn.synset('canine.n.02').definition()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And running `.hyponyms()` on that synset naturally includes `dog` and `wolf`
    """)
    return


@app.cell
def _(wn):
    # that fifth one is a doozy - run the `.definition()` to find out it refers specifically to female dogs
    wn.synset('canine.n.02').hyponyms()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So, we can see that `dog` and `wolf` are immediate members of the same hypernym (i.e., `canine`), which suggest these words are conceptually and semantically related. At the same time, there are seven total immediate members of the category `canine`, meaning that these seven terms/words/concepts/senses are relatively similar (because they are at an equal level under a hypernym).

    What do you think? We know that a fox, a wolf, and a dog are clearly different. But we know they are *similar*, and this categorization captures some approximation of that similarity.

    Do you think this categorization reflects the way that humans categorize objects/concepts through language?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Calculating specificity through hypernym/hyponym pathways

    Based on where a word is relative to other words in the WordNet hierarchy, that word may be associated with a very specific or very general concept. And, there may be different pathways to different higher-level concepts, depending on how similar the word is to other words. No matter what word you start with, there are higher level nodes that represent the "end" of many concepts.

    Several people have mapped this relationship, for example [this paper](https://www.semanticscholar.org/paper/Inductive-learning-of-lexical-semantics-with-typed-Kazakov-Dobnik/e46c008c3b83b9a0155d7f8a5319a1208d8922ae) provided this figure:

    ![](https://raw.githubusercontent.com/scskalicky/LSCI-220/main/images/wordnet.jpeg)

    You can see on this graphic the highest level node linking all of the lower-level nodes is `entity`. There are no hypernyms for `entity`, only hyponyms. Inspecting the definition of entity reveals a very broad and general category, making it a good fit for one of the highest-level concepts.
    """)
    return


@app.cell
def _(wn):
    wn.synset('entity.n.01').definition()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We can explore relative distances among words/concepts in WordNet using these paths.

    Specifically, the `.hypernym_paths()` method lets you explore these paths. For `dog`, because there are two *immediate* hypernyms (`domestic_animal` or `canine`), there are two possible routes or pathways to a higher-level category (both eventually end at `entity`). Depending on which of these two paths you take, different higher-level categories will be traversed. Remember that `wolf` only had one hypernym, and thus has only one immediate route to a higher level category.

    Examine the two hypernym paths below, you should see how the categories become less specific as one goes up the list. Also note that the end hypernym is the same for both paths.

    When starting at the bottom, you should be able to use the `"is a"` method for moving up the list. A dog is a canine, a canine is a carnivore, etc...

    As we will see later on, this is how WordNet counts the number of steps between two words to approximate their similarity - neat!
    """)
    return


@app.cell
def _(dog01):
    # save the hypernym paths of dog.n.01
    dog_paths = dog01.hypernym_paths()

    # how many paths are there?
    len(dog_paths)
    return (dog_paths,)


@app.cell
def _(dog_paths):
    # look at the first path (read from the bottom up)
    # a dog is a canine is a carnivore is a placental...(and so on)
    dog_paths[0]
    return


@app.cell
def _(dog_paths):
    # look at the second path (read from the bottom up)
    # a dog is a domestic animal is an animal is an organism...(and so on)
    dog_paths[1]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## **Semantic Similarity**

    In WordNet, the distance between two words and a root hypernym or hyponym is taken as a measure of similarity.

    In the example from the book, several different synsets are saved as variables, some of which logically are more related than others.

    The authors then demonstrate the similarity among these saved synsets.

    I have always found it confusing the authors used "right" as a variable name without explaining it, but it refers to a type of whale: [a right whale](https://en.wikipedia.org/wiki/Right_whale).

    I added the `.definition()` method for each version below so you can get an idea as to why the authors are using these examples for the test.
    """)
    return


@app.cell
def _(wn):
    orca = wn.synset('orca.n.01')
    orca.definition()
    return (orca,)


@app.cell
def _(wn):
    minke = wn.synset('minke_whale.n.01')
    minke.definition()
    return (minke,)


@app.cell
def _(wn):
    right = wn.synset('right_whale.n.01')
    right.definition()
    return (right,)


@app.cell
def _(wn):
    tortoise = wn.synset('tortoise.n.01')
    tortoise.definition()
    return (tortoise,)


@app.cell
def _(wn):
    novel = wn.synset('novel.n.01')
    novel.definition()
    return (novel,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `lowest_common_hypernyms()` method will find the closest hypernym which two synsets share. Remember, hypernyms are the higher-level categories. So if two words share the next highest-level category (such as wolf and dog), they will be more similar than words which only share the most highest-level category, such as `entity.`

    If a hypernym is "lower" that means it is more specific because it is lower in the overall categorisation schema - so two words linked by a more specific hypernym are more similar than if they are linked by an abstract hypernym (such as entity). You can see the WordNet explanation [here](https://www.nltk.org/api/nltk.corpus.reader.wordnet.html?highlight=lowest_common_hypernyms#nltk.corpus.reader.wordnet.Synset.lowest_common_hypernyms).
    """)
    return


@app.cell
def _(minke, right):
    # what is the lowest common hypernym of right whales and minke whales?
    right.lowest_common_hypernyms(minke)
    return


@app.cell
def _(orca, right):
    # lowest common hypernym of right whale and orcas?
    right.lowest_common_hypernyms(orca)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So which pair is more similar? Right Whales and Minke Whales are linked by Baleen Whale. Right Whales and Orcas are linked by Whale. Since a Baleen Whale is more specific than the term Whale, Right Whales and Minke Whales are more similar than Right Whales and Orcas. At least, that is the logic of these relationships.

    Continue the exercise to compare right whales to tortoises and novels.
    """)
    return


@app.cell
def _(right, tortoise):
    # vertebrate is less specific when compared to 'whale'
    # so they are less similar than the comparisons done above.
    right.lowest_common_hypernyms(tortoise)
    return


@app.cell
def _(novel, right):
    # entity is the least specific category possible,
    # so right whales and novels have almost no semantic similarity.
    right.lowest_common_hypernyms(novel)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now that you conceptually understand the way NLTK defines these measures of similarity and difference, you can use the `.path_similarity()` method to see the numeric measure WordNet will return.

    Remember that `right` refers to a type of whale.
    """)
    return


@app.cell
def _(minke, right):
    # finds the shortest path which connects two things - higher number = more similar
    right.path_similarity(minke)
    return


@app.cell
def _(orca, right):
    # less similar..
    right.path_similarity(orca)
    return


@app.cell
def _(right, tortoise):
    # even less similar...
    right.path_similarity(tortoise)
    return


@app.cell
def _(novel, right):
    # even more less similar!...
    right.path_similarity(novel)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's look at some other examples. Try it out for yourself, what other examples do you want to look at?
    """)
    return


@app.cell
def _(wn):
    # compare dog and cat
    wn.synset('dog.n.01').path_similarity(wn.synset('cat.n.01'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Hopefully you're at the point where you think writing a function is a better way to explore new resources. I've written a helper function below to make it faster for us to compare similarities between inputs.
    """)
    return


@app.function
# why not write a short helper function?
def compare_similarity(base, comparison):
  '''compares two WordNet synsets'''
  print(f'{base} & {comparison}: {base.path_similarity(comparison)}')


@app.cell
def _(wn):
    # define a baseline for comparison
    base = wn.synset('beer.n.01')

    # you can add any number of synsets here
    comparisons = [wn.synset('wine.n.01'), wn.synset('water.n.01'), wn.synset('bread.n.01'),
                   wn.synset('alcohol.n.01'), wn.synset('whiskey.n.01'), wn.synset('juice.n.01'),
                   wn.synset('vegetable.n.01')]

    # loop through comparisons and compare all to base.
    for compare in comparisons:
      compare_similarity(base, compare)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Conclusion

    WordNet represents a really interesting way to start thinking about how we can computationally measure a word's "meaning." If you think about it, the `.definition()` function of WordNet is likely very useless as a computational measure (unless we can somehow parse the text of the definition!). By quantifying the space between words and concepts, WordNet provides an interesting and useful (if imperfect) measure of semantic distance and associations.

    Notice that every synset, definition, and hypernym in WordNet was decided by people: lexicographers who sat down and organised the words of English into a hierarchy. This makes WordNet very precise, but it also means WordNet only knows what its creators put into it, and it can't learn new words or meanings by itself. In the word vectors notebook, we will look at a very different approach, where the computer *learns* the relationships between words from how they are used in a corpus.

    There are other "nets" included in NLTK, such as VerbNet and the Multilingual WordNet. If you're keen, you can explore them in the NLTK docs:

    - [VerbNet](https://www.nltk.org/api/nltk.corpus.reader.verbnet.html?highlight=verb%20net#module-nltk.corpus.reader.verbnet)
    - [FrameNet](https://www.nltk.org/api/nltk.corpus.reader.framenet.html?highlight=frame%20net#module-nltk.corpus.reader.framenet)
    - [Multilingual WordNet](https://github.com/globalwordnet/OMW) - (you might need to search for "omw" which stands for open multilingual wordnet)
    """)
    return


if __name__ == "__main__":
    app.run()
