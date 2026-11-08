# LSCI 220: Introduction to Computational Linguistics and NLP

[![Setup check](https://github.com/scskalicky/LSCI-220/actions/workflows/setup-check.yml/badge.svg)](https://github.com/scskalicky/LSCI-220/actions/workflows/setup-check.yml)
[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![marimo](https://img.shields.io/badge/notebooks-marimo-1C7ED6)
![uv](https://img.shields.io/badge/installed%20with-uv-DE5FE9)
![NLTK](https://img.shields.io/badge/NLP-NLTK-green)
![Developed with Claude](https://img.shields.io/badge/developed%20with-Claude-D97757?logo=claude&logoColor=white)

Course materials for LSCI 220 at Te Herenga Waka—Victoria University of Wellington. The course introduces computational approaches to analysing language, using the Python programming language. No programming experience is assumed.

All of the course materials are [marimo](https://marimo.io) notebooks.

## Getting started

If you are enrolled in the course, follow the install guide on Nuku. In short:

1. Download this folder (on GitHub, click **Code** → **Download ZIP**) and unzip it.
2. Install [uv](https://docs.astral.sh/uv/).
3. Open a terminal inside the folder and run:

   ```
   uv run marimo edit
   ```

4. Open `00_check_setup.py` and run it to check that everything works.

You can also open any notebook in [molab](https://molab.marimo.io) without installing anything, using a link like this:

```
https://molab.marimo.io/github/scskalicky/LSCI-220/blob/main/notebooks/01_variables_and_strings.py
```

## What's in this folder

| | |
|---|---|
| `00_check_setup.py` | Run this first to check your setup |
| `notebooks/` | The self-study notebooks, numbered in course order |
| `notebooks/text_analysis_functions.py` | Ready-made functions you can use in your own analyses |
| `resources/` | Texts, corpora and word lists used by the notebooks |
| `images/` | Figures used in the notebooks |
| `pyproject.toml`, `uv.lock` | The list of Python packages the course uses (uv reads these for you) |
| `.github/` | An automatic test of the setup - you can ignore it |

Keep the notebooks you make yourself in their own folder, so that you don't overwrite them if you download the course materials again.

## Data and resources

The notebooks use the following resources. Each remains under its own terms, and is included here for educational use.

- **Word frequency:** SUBTLEX-US (Brysbaert & New, 2009)
- **Age of acquisition:** Kuperman, Stadthagen-Gonzalez & Brysbaert (2012)
- **Concreteness:** Brysbaert, Warriner & Kuperman (2014)
- **Semantic diversity:** Hoffman, Lambon Ralph & Rogers (2013)
- **Sentiment:** AFINN (Nielsen, 2011) and VADER (Hutto & Gilbert, 2014)
- **Emotion:** NRC Emotion Lexicon (Mohammad & Turney, 2013)
- **Valence, arousal and dominance:** Warriner, Kuperman & Brysbaert (2013)
- **Satirical and non-satirical Amazon reviews:** Skalicky & Crossley (2015)
- **Word vectors:** GloVe (Pennington, Socher & Manning, 2014)
- **Corpora and WordNet:** NLTK (Bird, Klein & Loper, 2009) and WordNet (Princeton University)
- **Texts:** *Seinfeld* scripts; *They're Made Out of Meat* (Terry Bisson); "Mood Ring" (Lorde)

## Acknowledgements

Some of the course content was written with the help of *Natural Language Processing with Python* (the NLTK book) by Steven Bird, Ewan Klein and Edward Loper, available at [nltk.org/book](https://www.nltk.org/book/).

The 2026 version of these materials was developed with the help of Claude (Anthropic), which was used to convert previous Google Colab notebooks to marimo, revise explanations and code, and check the materials for errors. All content was reviewed and edited by me. I take sole responsibility for any remaining errors. 

## License

Course materials by Stephen Skalicky. This course content is offered under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0](http://creativecommons.org/licenses/by-nc-nd/4.0/) license. Content in this course can be considered under this license unless otherwise noted. The data and resources listed above remain under their original terms. The full license text is in the `LICENSE` file.
