"""
The package GnuplotParser will read a Gnuplot plot string, and return in a format compatible with matplotlib. It is basically a python wrapper script to parse gnuplot commands into matplotlib format.

It has dependency on the GnuplotDataStructure package.
"""

import numpy as np
import matplotlib.pyplot as plt
from GnuplotDataStructure import GnuplotDataStructure as GDS


class GnuplotParser:
    """

    Members:

        'file_handle' -- the file handle pointing to opened file

    Methods:

        '__init__' -- print activation information

    """
    
    def __init__(self):
        print('GnuplotParser objects can be created')

    def parsePlotString(self, plotstring):
        print(plotstring)
        #filename = plotstring.split()[1].replace("'", "") # extract second word and stip apostrophes
        #index = int(plotstring.split()[3]) # extract index and cast to integer
        #
        #span = 2
        #plot_dict = [tuple(words[i:i + span]) for i in range(0, len(words), span)]
        #
        words = plotstring.split()
        plot_dict = dict(map(None, *[iter(words)] * 2))
        print plot_dict
        #
        filename = plot_dict["plot"].replace("'", "")
        index = int(plot_dict["ind"])

        using = plot_dict["us"].split(":")
        x = int(using[0])-1
        y = int(using[1])-1

        block = 0

        print filename, index, x, y

        #GDS().plotData(filename, index, block=0, x=int(using[0])-1, y=int(using[1])-1)
        #def plotData(self, filename, index, block, x, y):
        data = GDS().parseDatafile(filename, index, block)

        # check for title
        if 't' in plot_dict:
            plt.title(plot_dict['t'].replace("'", ""))

        # key word arguments
        kwargs = {}

        if 'w' in plot_dict:
            kwargs['linestyle'] = 'steps'

        if 'lw' in plot_dict:
            kwargs['linewidth'] = plot_dict['lw']


        plt.errorbar(x=data[:, x], y=data[:, y], **kwargs)
        plt.show()

        
