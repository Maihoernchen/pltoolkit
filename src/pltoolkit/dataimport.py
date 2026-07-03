import pandas as pd
import numpy as np
import os

class Scaff:
    def __init__(self, filenames=None, dir=None, type=None, ntype=None, includes=None, excludes=None, skip = 1, gencols = 0):
        self.dad = {}
        self.scale = {}
        self.columns = {}
        if filenames:
            self.filenames = filenames
        elif dir:
            path = dir
            self.filenames = os.listdir()    
        else:
            raise Exception("No List of filenames or directory provided.")
        if type:
            self.filenames = [filename for filename in self.filenames if filename.endswith(type)]
        if ntype:
            self.filenames = [filename for filename in self.filenames if not filename.endswith(ntype)]
        if includes:
            self.filenames = [filename for filename in self.filenames if includes in filename]
        if excludes:
            self.filenames = [filename for filename in self.filenames if not excludes in filename]
        for filename in filenames:
            self.dad[filename] = self.load(filename, skip)
        if gencols:
            for header in self.dad[list(self.dad.keys())[0]].columns:
                self.columns[header] = self.column(header)
    def load(self, path, skip=1):
        try:
            df = pd.read_json(path, dtype=str)
        except:
            df = pd.read_csv(path, sep=';', skiprows=skip, dtype=str)
            df = df.dropna(axis=1, how='all')
            try:
                df = df.apply(lambda col: col.str.replace(",", ".")).astype(float)
                self.scale[path] = 2
            except:
                print('Warning: Data is not Float-Convertible and therefore not plottable.')
                self.scale[path] = 1
        return df
    def column(self, name = None, index = 0, start=None, end=None):
        columns = {}
        if name:
            for filename in self.dad:
                columns[filename] = self.dad[filename][name]
                if self.scale[filename] >=2:
                    columns[filename] = columns[filename].astype(float).to_numpy()
        return columns
# Scaff(['../../../data/10/5.txt'], gencols=1)