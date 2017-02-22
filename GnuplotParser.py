"""
The package GnuplotParser will read a Gnuplot plot string, and return in a format compatible with matplotlib. It is basically a python wrapper script to parse gnuplot commands into matplotlib format.

It has dependency on the GnuplotDataStructure package.
"""

import numpy as np
import matplotlib.pyplot as plt
#from GnuplotDataStructure import GnuplotDataStructure as GDS
import shlex # to preserve substrings in one piece while splitting using space
from StringIO import StringIO # to pack list into raw data, so as to be easily read by np.loadtxt()


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

        # set up axes
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

        print set_dict

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
        print plotstring_list

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
        print plot_dict
        #

        index = int(plot_dict["ind"])

        using = plot_dict["us"].split(":")
        x = int(using[0])-1
        y = int(using[1])-1

        if 'every' in plot_dict:
            block = int(plot_dict['every'].split(":")[-1])
        else:
            block = -1 # that is there is no block info

        print filename, index, x, y, block

        data = self.parseDatafile(filename, index, block)




        # key word arguments
        kwargs = {}

        if 't' in plot_dict: #legend
            kwargs['label'] = plot_dict['t'].replace("'", "")

        if 'w' in plot_dict:
            kwargs['linestyle'] = 'steps'

        if 'lw' in plot_dict:
            kwargs['linewidth'] = plot_dict['lw']


        plt.errorbar(x=data[:, x], y=data[:, y], **kwargs)

        





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

        return np.loadtxt(raw_datablock)