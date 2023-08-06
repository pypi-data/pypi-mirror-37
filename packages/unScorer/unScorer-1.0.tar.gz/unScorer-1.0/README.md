# unScore
## Simple Python programming changing scores into modern numbers

This tool will take in short strings and find and convert any measurements using the old english unit "score". It then returns the string with the "score" units converted into a string of their integer representation. This tool can be used in conjunction with other Python packages like Text2int to fully convert textual representations of numbers to their integer forms.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This tool requires the following packages to be installed:
* Numpy
* Pandas
* NLTK
* Regex

All are available in the standard Conda distributions. To make sure your distribution is up to date navigate to your terminal and type:

```
conda update conda
```

If you do not have Anaconda installed on your system, you can find it [here](https://anaconda.org).

### Installing

**Optional:**
Optionally, you may want to create a new Conda envionrment in which to run the program. If you choose to do this, you will need Anaconda in addition to the packaged outlined above. To launch an environment, type:

```
conda create -n unscore python =3.5 anaconda
```
And hit enter. After this, type this to activate your environment:

```
source activate unscore
```

**Not Optional:**
This program is available to pip install from Pypi. To install, simply navigate to your terminal and run the following (assuming your current environment has all the above packages available):

```
pip install unScorer
```
That's it! The unScorer is not available for you to start using in Jupyter Notebooks, text editors, or straight in Python on your terminal.

## Using the tool

To use the tool, run python in your terminal with the following command (unless you';re running this in a notebook or text editor):

```
python
```

Then, import the package's tools with the following command:

```
from unScorer import *
```

Type the following with your passage or measurement inside the "Text" class parentheses:

```
unScore(Text("my text here")).run()
```

And the tool should return the text with any "score" measurements converted to their integer representation.

## Authors

**Brian Friederich** - *Data Scientist, Booz Allen Hamilton*

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
