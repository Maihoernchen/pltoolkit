import numpy as np
import matplotlib.pyplot as plt 
import dataimport as di
import os

class pltcollection:
    def __init__(self, scaff):
        self.scaff = scaff
        self.plt = []
    def absolute_to_relative_path(self, absolute_path):
        absolute_path = os.path.expanduser(absolute_path)

        # Convert to an absolute path (falls ein relativer Pfad übergeben wurde)
        absolute_path = os.path.abspath(absolute_path)
        # Get the current working directory
        cwd = os.getcwd()
        
        # Get the relative path
        relative_path = os.path.relpath(absolute_path, cwd)
        
        return relative_path

    def plot2d(self, index, xname, yname, file=None, title=None, xlabel=None, ylabel=None, legend=True):
        if not file:
            fig, ax = plt.subplots()
            for filename in self.scaff.dad:
                x = self.scaff.column(name=xname)[filename]
                y = self.scaff.column(name=yname)[filename]
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
            self.plt.append(fig)
    def safeplot(self, filename=None, index=0):
        if not filename:
            path = self.absolute_to_relative_path(self.scaff.filenames[index])
            filename = path[:path.rfind('.')] + "_plot.svg"
        if self.plt:
            self.plt[index].savefig(filename)
        else:
            raise ValueError("No plot has been created yet. Please call plot2d() before saving the plot.")
    def safedatfiles(self, file=None):
        try:
            for colname, column in self.scaff.columns.items():
                data = np.column_stack([column[filename] for filename in self.scaff.dad])
                if not file:
                    for filename in self.scaff.filenames:
                        path = self.absolute_to_relative_path(filename)
                        filename = path[:path.rfind('.')] + "_" + colname + ".dat"
                np.savetxt(filename, data, delimiter='\t', header='\t'.join(self.scaff.dad.keys()), comments='')
                print(f"Data files saved successfully as {filename}.")
        except Exception as e:
            raise ValueError("An error occurred while saving the data files. Have you called the Scaff class with gencols=1?") from e
        
a = pltcollection(di.Scaff(['~/Documents/unineu/pl2/data/10/5.txt'], gencols=1))
a.plot2d(0, 't', 'y', title='Test Plot', xlabel='X-axis', ylabel='Y-axis', legend=True)
a.safeplot()
a.safedatfiles()