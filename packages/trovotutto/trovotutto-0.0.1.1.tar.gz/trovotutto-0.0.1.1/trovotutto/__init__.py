#!/usr/bin/env python3

#    trovotutto
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


import itertools
import re
import operator
import pickle
from glob import glob
from os import listdir as ls
from os import getcwd
from os.path import expanduser
from pprint import pprint
from subprocess import check_output as sh

from argparse import ArgumentParser
from nltk import ngrams as ng
from xdg import BaseDirectory

from .color import Color

name = "trovotutto"

def save(variable, filename):
    """Save variable on given path using Pickle
    
    Args:
        variable: what to save
        path (str): path of the output
    """
    fileObj = open(filename, 'wb')
    pickle.dump(variable, fileObj)
    fileObj.close()

def load(filename):
    """Load variable from Pickle file
    
    Args:
        path (str): path of the file to load

    Returns:
        variable read from path
    """
    fileObj = open(filename, 'rb')
    variable = pickle.load(fileObj)
    fileObj.close()
    return variable

class Files:
    """Class that "documentifies" files in local filesystem

    It recursively takes every file in a location and interpret them as documents
    using the directories that form their path as words.

    It saves a list of the files founded in the index directory.

    Args:
        path (str): path to find files in (default: home directory);
        filetype (str): type of file to index; can be one of the following values:
                         - any
                         - images
                         - documents
                         - code
                         - audio
                         - video;
        exclude (list): extensions to exclude from indexing;
        update (bool): whether to rescan the file system;
        verobse(int): from 0 to 5, verbose flag.
    """
    def __init__(self, path=getcwd(), filetype="any", exclude=[], update=True, verbose=0):

        if verbose > 0:
            print("documentifiyng files' path in " + path)

        data_path = BaseDirectory.save_data_path(name)
 
        extensions = {"images":      ["bmp", "eps", "jpeg", "jpg", "png", "svg", "tiff", "webp","xfc"],
                     "documents":    ["doc", "docx", "txt", "rtf", "pdf", "ooxml", "docm", "odt", "xls", "ppt", "pptx", "xps"],
                     "code":         ["py", "css", "m", "c", "h", "php", "f90", "f77", "f08", "html", "tex", "php", "js","sh"],
                     "audio":        ["mp3", "wma", "ogg", "m4a", "wav", "flac", "xm"],
                     "video":        ["mp4", "avi", "mkv", "flv", "mov", "mpg", "wmv", "webm"] }
        if filetype == "any":
            selected_types = []
            for t in extensions.keys():
                selected_types = selected_types + extensions[t]
        else:
            selected_types = extensions[filetype]
        for t in exclude:
            selected_types.remove(t)
 
        self.elements = []
        db = ls(data_path)
 
        for ext in selected_types:
            if not (ext in db) or (update == True):
                files = glob(path + '/**/*.'+ext, recursive=True)
                save(files, data_path + '/' + ext)
                self.elements = self.elements + files
            else:
                self.elements = self.elements + load(data_path + "/" + ext)
        self.documents = [re.split("/|\.|-|:|;| |_", f.lower()) for f in self.elements]  

class PGPgramDb:
    """Class that 'documentifies' files in PGPgram pickle database

    It takes paths of the elements in the PGPgram database and interpret
    them as documents using the directories that form their path as words.

    Args:
        db (obj): PGPgram Db object;
        filetype (str): type of file to index; can be one of the following values:
                        - any (default)
                        - images
                        - documents
                        - code
                        - audio
                        - video
        exclude (list): extensions to exclude from indexing (default: empty)
        update (bool): whether to rescan the database (default: True)
    """
    def __init__(self, db, path="/", filetype="any", exclude=[], update=True):

        extensions = {"images":      ["bmp", "eps", "jpeg", "jpg", "png", "svg", "tiff", "webp","xfc"],
                     "documents":    ["doc", "docx", "txt", "rtf", "pdf", "ooxml", "docm", "odt", "xls", "ppt", "pptx", "xps"],
                     "code":         ["py", "css", "m", "c", "h", "php", "f90", "f77", "f08", "html", "tex", "php", "js","sh"],
                     "audio":        ["mp3", "wma", "ogg", "m4a", "wav", "flac", "xm"],
                     "video":        ["mp4", "avi", "mkv", "flv", "mov", "mpg", "wmv", "webm"] }
        if filetype == "any":
            selected_types = [""]
        else:
            selected_types = extensions[filetype]
        for t in exclude:
            selected_types.remove(t)

        self.elements = []
        for ext in selected_types:
            files = [d["path"] for d in db.files if d['path'].startswith(path) and d["path"].endswith(ext)]
            self.elements = self.elements + files

        self.documents = [re.split("/|\.|-|:|;| |_", f.lower()) for f in self.elements]

class Index:
    """A simple inverted index

    It decompose given set of documents in ngrams and creates an inverted index
    having as keys the ngrams and values the documents containing it.

    Args:
        type_instance (obj): can be Files or PGPgramDb object (default: new Files instance)
        slb (int): length of the ngrams (default: 3)
        verbose(int): verbose flag from 0 to 5 (default: 2)
    """
    def __init__(self, type_instance, slb=4, verbose=0):
        self.slb = slb
        self.elements = type_instance.elements
        self.documents = type_instance.documents
        self.terms = list(set([t for e in self.documents for t in e]))
        self.d = len(self.terms)
        self.N = len(self.documents)
        self.D = {}
        if verbose >= 2:
            print ("indexing documents")
        for i,t in enumerate(self.terms):
            for j,e in enumerate(self.documents):
                occs = len([w for w in e if w == t])
                if occs != 0:
                    if not i in self.D.keys():
                        self.D[i] = {}
                    self.D[i][j] = occs
        if verbose >= 2:
            print ("creating ngrams")
        self.ngrams = {}
        for i,t in enumerate(self.terms):
            if len(t) >=  slb:
                for g in ng(t,slb):
                    if not g in self.ngrams.keys():
                        self.ngrams[g] = []
                    self.ngrams[g].append(i)

    def search(self, query, verbose=0):
        """Searches files satisfying query

        It first decompose the query in ngrams, then score each document containing
        at least one ngram with the number. The ten document having the most ngrams
        in common with the query are selected.
        
        Args:
             query (str): what to search;
             results_number (int): number of results to return (default: 10)
        """
        if verbose > 0:
            print("searching " + query)
        query = query.lower()
        qgram = ng(query, self.slb)
        qocument = set()
        for q in qgram:
            if q in self.ngrams.keys():
                for i in self.ngrams[q]:
                    qocument.add(i)
        self.qocument = qocument
        results = {}
        for i in qocument:
           for j in self.D[i].keys():
                if not j in results.keys():
                    results[j] = 0
                results[j] = results[j] + self.D[i][j]
        sorted_results = sorted(results.items(), key=operator.itemgetter(1), reverse=True)
        return [self.elements[f[0]] for f in sorted_results]

class Handler:
    """Display and let take action on search results
 
    Args:
        results (list): list of results obtained through Index.search
    """
    def __init__(self, results, results_number=10):
        color = Color()
        for i,f in enumerate(results[0:results_number]):
            g = f.split("/")
            print(color.GREEN + color.BOLD + str(i) + ". " + color.BLUE + g[-1] + color.END)
            print(color.GRAY + f + color.END + "\n")
        if results != []:
            choice = int(input("Select search result (by number): "))
            sh(['xdg-open', results[choice]])

def main():
    """Function for command line execution"""

    parser = ArgumentParser(description="search files using n-grams")
    parser.add_argument('--path', dest='path', help="where to search", nargs=1, action="store", default=getcwd())
    parser.add_argument('--update', dest='update', help="update the index", action='store_true', default=True)
    parser.add_argument('--filetype', dest='filetype', help="any, images, documents, code, audio, video", nargs=1, action="store", default=["any"])
    parser.add_argument('--verbose', dest='verbose', help="extended output", action='store_true', default=False)
    parser.add_argument('--results', dest='results', help="number of results to display", action="store", default=10)
    parser.add_argument('query', nargs='+', help="what to search", action="store")
    args = parser.parse_args()

    if args.verbose:
        verbose = 2
        pprint(args)
    else:
        verbose = 0
 
    query = args.query[0]
    for arg in args.query[1:]:
        query = query + " " + arg
    slb = min([len(w) for w in query.split(" ")])

    files = Files(path=args.path, filetype=args.filetype[0], exclude=[], update=args.update, verbose=verbose)
    index = Index(files, slb=slb, verbose=verbose)
    results = index.search(query, verbose=verbose)
    Handler(results, results_number=int(args.results))
