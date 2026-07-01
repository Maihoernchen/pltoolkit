import numpy as np
import matplotlib.pyplot as plt 

def plot2d(scaff, index, xname, yname, file=None, title=None, xlabel=None, ylabel=None, legend=True):
    if not file:
        fig, ax = plt.subplots()
        for filename in scaff.dad:
            x = scaff.column(name=xname)[filename]
            y = scaff.column(name=yname)[filename]
            ax.errorbar(x, y, label=filename)
        if title:
            ax.set_title(title)
        if xlabel:
            ax.set_xlabel(xlabel)
        if ylabel:
            ax.set_ylabel(ylabel)
        if legend:
            ax.legend()
        plt.show()