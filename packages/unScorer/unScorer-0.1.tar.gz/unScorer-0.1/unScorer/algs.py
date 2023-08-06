from nltk import word_tokenize
import numpy as np
import re

units = {"zero": 0, "one": 1, "a": 1, "an": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8,
         "nine": 9, "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14, "fifteen": 15,
         "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19, "twenty": 20, "thirty": 30,
         "forty": 40, "fifty": 50, "sixty":60, "seventy": 70, "eighty": 80, "ninety": 90, "hundred": 100,
         "thousand": 1000, "million": 1000000}

numwords = list(units.keys()) + ["and", "-", "score"]

class Tokenize(object):

    """Class tokenizing object with nltk

    attributes:
        __init__
        run

    returns:
        self.arr (arr): input string tokenized by word

    """
    def __init__(self, object):
        self.string = object
        self.arr = None

    def __run__(self):
        self.arr = word_tokenize(self.string)
        return self.arr


class Calculate_Score(object):
    """
    Class turning scores in tokens into ints.

    Attributes:
        __init__
        __run__
    """

    def __init__(self, object):
        self.token = object

    def __run__(self):
        split_token = re.split(r"score", self.token)[0]
        split_token = split_token.replace("-","")
        if split_token.lower() in numwords:
            self.token = units[split_token.lower()] * 20
        return str(self.token)

class Has_Score(object):
    """Class finding tokens to apply unScore method to.
    """
    def __init__(self, object):
        self.arr = object

    def __run__(self):
        self.arr = [Calculate_Score(i).__run__() if str(i).endswith("score") else i for i in self.arr]
        return self.arr

class Join_Elements(object):

    """Class detokenizing array of words into final sentence.

    attributes:
        __init__
        __run__

    """

    def __init__(self, object):
        self.arr = object
        self.output = None

    def __run__(self):
        """Method running Join_Elements class. If no elements that could have
        been converted are found, method raises an error.

        returns:
            output (str): string of input verse with Ancient Hebrew measurements
            converted into modern measurements.
        """
        for unit in self.arr:
            self.output = "".join([" "+i if not i == "-" else i for i in self.arr]).strip()
        return self.output
