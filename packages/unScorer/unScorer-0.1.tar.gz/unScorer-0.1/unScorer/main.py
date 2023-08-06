from .algs import *
from .inputs import *

class unScore(Text):
    """Class taking an object and converting score measurements within
    it to integers.

    """

    def __init__(self, object):
        """Method initializing unScore class.

        Args:

        object (str)"""
        self.string = object.string
        self.arr = None

    def run(self):
        """Method running algs from algs.py

        returns:
            string with score numbers replaced with string of int.
        """
        self.arr = Tokenize(self.string).__run__()
        self.arr = Has_Score(self.arr).__run__()
        return Join_Elements(self.arr).__run__()
