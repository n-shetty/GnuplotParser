"""
The package GnuplotParser will read a Gnuplot plot string, and return in a format compatible with matplotlib. It is basically a python wrapper script to parse gnuplot commands into matplotlib format.

It has dependency on the GnuplotDataStructure package.
"""

import numpy as np
import matplotlib.pyplot as plt
#from GnuplotDataStructure import GnuplotDataStructure as GDS
import shlex # to preserve substrings in one piece while splitting using space
from StringIO import StringIO # to pack list into raw data, so as to be easily read by np.loadtxt()
#import ast # to safely evaluate expression, ie to evaluate expressions tied to the "using" keyword
# using eval() directly with safety net, need to reassess  how safe this function is


class GnuplotParser:
    """

    Members:

        'file_handle' -- the file handle pointing to opened file

    Methods:

        '__init__' -- print activation information

    """

    filename = ''
    
    def __init__(self):
        print('GnuplotParser objects can be created')

    def parseGnuplotComamnd(self, gnuplot_cmd):



        # set up axes or parse "set" key values
        set_dict = {}
        for item in gnuplot_cmd.splitlines():
            if "set" in item.split():
                item = item.split()
                if len(item) != 3: # ignore if keyword is empty
                    continue
                if 'logscale' in item: # keyword logscale is repeated
                    if 'y' in item:
                        plt.yscale('log')
                    elif 'x' in item:
                        plt.xscale('log')
                set_dict[item[1]] = item[2] # fill dictionary

        print "\n"
        print "The axes have the following settings:"
        print set_dict
        print "\n"

        if 'title' in set_dict:
            plt.title(set_dict['title'].replace("'", ""))
        if 'xlabel' in set_dict:
            plt.xlabel(set_dict['xlabel'].replace("'", ""))
        if 'ylabel' in set_dict:
            plt.ylabel(set_dict['ylabel'].replace("'", ""))
        if 'xrange' in set_dict:
            xlimit_list = (set_dict['xrange'].replace("[", "").replace("]", "")).split(":")
            if xlimit_list[0]:
                plt.xlim(left = float(xlimit_list[0]))
            if xlimit_list[1]:
                plt.xlim(right = float(xlimit_list[1]))
        if 'yrange' in set_dict:
            ylimit_list = (set_dict['yrange'].replace("[", "").replace("]", "")).split(":")
            if ylimit_list[0]:
                plt.ylim(top = float(ylimit_list[0]))
            if ylimit_list[1]:
                plt.ylim(bottom = float(ylimit_list[1]))



        # set up plot options
        superplotstring = gnuplot_cmd.splitlines()[-1]  # the last line of the Gnuplot command
        plotstring_list = superplotstring.split(",")
        for plotstring in plotstring_list:
            self.parsePlotString(plotstring)
        plt.legend()
        plt.show()



    def parsePlotString(self, plotstring):
        global filename

        words = shlex.split(plotstring) # to preserve substrings in one piece while splitting using space
        if words[0] == 'plot' or words[0] == 'splot':
            plot_dict = dict(map(None, *[iter(words)] * 2))
            filename = plot_dict["plot"].replace("'", "")
        elif words[0] == '':
            plot_dict = dict(map(None, *[iter(words[1:])] * 2))
        else:
            filename = words[0]
            plot_dict = dict(map(None, *[iter(words[1:])] * 2))

        print "Following are the plot options:"
        print plot_dict
        print "\n"
        #

        index = int(plot_dict["ind"])

        if 'every' in plot_dict:
            block = int(plot_dict['every'].split(":")[-1])
        else:
            block = -1 # that is there is no block info


        col1, col2, col3, col4 = self.parseDatafile(filename, index, block)
        vars = {'__builtins__': None, 'col1': col1, 'col2': col2, 'col3': col3, 'col4': col4} # safety net for eval()

        # evaluate "using" string
        using = plot_dict["us"].split(":")
        if '$' in using[0]:
            using[0] = using[0].replace("$","col")
            x = eval(using[0], vars, {})
        else:
            x = eval("col%d" % int(using[0]), vars, {})

        if '$' in using[1]:
            using[1] = using[1].replace("$","col")
            y = eval(using[1], vars, {})
        else:
            y = eval("col%d" % int(using[1]), vars, {})



        # key word arguments
        kwargs = {}
        if 't' in plot_dict: #legend
            kwargs['label'] = plot_dict['t'].replace("'", "")
        if 'w' in plot_dict:
            kwargs['linestyle'] = 'steps'
        if 'lw' in plot_dict:
            kwargs['linewidth'] = plot_dict['lw']

        plt.errorbar(x=x, y=y, xerr=None, yerr=None, **kwargs)

        

    def parseDatafile(self, filename, index, block):
        file_handle = open(filename, 'r')
        raw_data = file_handle.read()
        file_handle.close()

        dataset = raw_data.split('\n\n\n')

      	if block != -1:
            datablock = dataset[index].split('\n\n')
            raw_datablock = StringIO(datablock[block])
        else:
            raw_datablock = StringIO(dataset[index])

        return np.loadtxt(raw_datablock, unpack=True)